"""Trusted native lifecycle and main-thread gateway. No reference imports."""
from copy import deepcopy
from concurrent.futures import Future
import queue
import threading
import time


def run_native_service(backend, dispatcher, service, *, is_running, wall_seconds,
                       close_native, replay_seconds=30.):
    """Release native resources after terminal transport completion, then serve cached results.

    The grace interval permits SDK finish/reconnect calls; it is never a delivery
    heuristic. A broken terminal write also releases native resources, retaining
    the durable response for authenticated retries during the same grace interval.
    """
    deadline = time.monotonic() + wall_seconds
    while is_running() and time.monotonic() < deadline and not service.terminal_response_complete.is_set():
        if not service.poll_storage(): break
        dispatcher.pump(timeout=.05)
    # A terminal native call may precede protocol finalization/publication.
    # Keep servicing its owner-thread finish calls; terminal backends reject
    # further physical actions, and the service serializes request execution.
    while backend.finished and service.request_inflight.is_set() and not service.terminal_response_pending.is_set():
        dispatcher.pump(timeout=.05)
    if service.terminal_response_pending.is_set():
        # Owner limits stop simulation work, not an already pending terminal
        # response. The socket write timeout bounds this transport-only drain.
        service.terminal_response_complete.wait()
    if not service.terminal_response_complete.is_set():
        backend.finish(reason='wall_time_limit' if time.monotonic() >= deadline else 'runtime_shutdown')
    dispatcher.close()
    close_native()
    if service.terminal_response_complete.is_set():
        threading.Event().wait(replay_seconds)


def runtime_socket_path(root, run_directory):
    """Dedicated short AF_UNIX endpoint; long evidence paths cannot break bind."""
    import hashlib
    import os
    from pathlib import Path
    identity=hashlib.sha256(str(Path(run_directory).resolve()).encode()).hexdigest()[:16]
    path=Path(root)/'.codex-local/sockets'/(identity+'.sock')
    if len(os.fsencode(path))>=104:raise ValueError('Native socket root is too long')
    return path


class MainThreadDispatcher:
    """Workers wait; only the simulator owner executes queued functions."""
    def __init__(self):
        self.owner = threading.get_ident()
        self.queue = queue.Queue()
        self.closed = False
        self.lock = threading.Lock()

    def call(self, function, *args):
        with self.lock:
            if self.closed: raise RuntimeError('Native dispatcher closed')
            if threading.get_ident() != self.owner:
                future = Future();self.queue.put((future,function,args))
            else: future = None
        return function(*args) if future is None else future.result()

    def pump(self, timeout=.05):
        if threading.get_ident()!=self.owner:raise RuntimeError('Native owner thread required')
        try: future,function,args = self.queue.get(timeout=timeout)
        except queue.Empty:return
        try: future.set_result(function(*args))
        except BaseException as exc: future.set_exception(exc)

    def close(self):
        with self.lock:
            self.closed=True
            while not self.queue.empty():
                future,_,_ = self.queue.get_nowait();future.set_exception(RuntimeError('Native dispatcher closed'))


class DispatchedBackend:
    def __init__(self, backend, dispatcher):self.backend,self.dispatcher=backend,dispatcher
    def describe(self):return self.dispatcher.call(self.backend.describe)
    def snapshot(self,camera_ids=()):return self.dispatcher.call(self.backend.snapshot,camera_ids)
    def step(self,action):return self.dispatcher.call(self.backend.step,action)
    def mechanism(self,name,arguments):return self.dispatcher.call(self.backend.mechanism,name,arguments)
    def finish(self):return self.dispatcher.call(self.backend.finish)
    def abort(self):return self.dispatcher.call(self.backend.abort)


class NativeBackend:
    """Exactly one reset before socket startup; observations never score or step."""
    def __init__(self, bridge, scorer, journal, *, cameras=None, max_steps=36000, prepared=False,
                 control_observer=None):
        self.bridge,self.scorer,self.journal = bridge,scorer,journal
        self.cameras,self.max_steps = cameras,max_steps
        self.control_observer = control_observer
        self.owner=threading.get_ident();self.control=0;self.physics=0
        self.previous_action=[];self.finished=False;self.samples=[]
        self._control_stage=None
        if type(prepared) is not bool:
            raise TypeError('prepared must be bool')
        if prepared:
            # Trusted runner only: validated and journaled initialization is
            # claimed without another reset or any body/joint state write.
            self.bridge.start_episode(scorer.initial)
        else:
            self.bridge.reset()
        self._description = bridge.describe()
        environment=getattr(bridge,'env',None)
        if environment is not None:
            self._description['action_spec'].update(physics_period_s=environment.physics_dt,
                control_period_s=environment.physics_dt*environment.cfg.decimation)
        self._description['task']['max_steps']=max_steps
        if cameras:self._description['cameras']=cameras.description()
        # Reset teleports initial joints without a new physics step. Native
        # force buffers still describe the pre-reset pose, so preserve them
        # as explicitly invalid reset evidence and score only fresh substeps.
        self.result = scorer.result()
        self.max_penetration=0.
        self.journal.write('reset',dict(observation=self.snapshot(),physical=bridge.physical(0,0),contacts_fresh=prepared))
        if self.control_observer:
            self.control_observer(deepcopy(bridge.physical(0,0)))
        bridge.install_hook(self._substep)

    def _assert_owner(self):
        if threading.get_ident()!=self.owner:raise RuntimeError('Native owner thread required')

    def describe(self):
        self._assert_owner();return deepcopy(self._description)

    def _substep(self):
        self.physics+=1
        state=self.bridge.physical(self.control,self.physics)
        self.samples.append(state)
        audit=self.scorer.audit_substep(state)
        self.max_penetration=max(self.max_penetration,float(audit.get('max_penetration_m',0.)))
        self.journal.write('substep',dict(snapshot=state,audit=audit))

    def snapshot(self,camera_ids=()):
        self._assert_owner()
        row=self.bridge.snapshot(self.control,self.previous_action)
        row.setdefault('privileged',{}).setdefault('diagnostics',{})['max_penetration_m']=self.max_penetration
        row.update(step_index=self.control,physics_step_count=self.physics,simulation_time_s=self.physics/120,
            terminated=bool(self.result['success'] or self.result['hard_failure'] or self.finished),
            truncated=self.control>=self.max_steps,cameras={})
        if camera_ids:
            if self.cameras is None:raise ValueError('Cameras unavailable')
            row['cameras']=self.cameras.capture(camera_ids,self.control)
            self.journal.write('capture',row['cameras'])
        return row

    def step(self,action):
        self._assert_owner()
        if self.finished or self.result['success'] or self.result['hard_failure'] or self.control>=self.max_steps:
            raise RuntimeError('Episode closed')
        from .profiles import number
        bounds=self._description['action_spec']
        if (not isinstance(action,list) or len(action)!=bounds['size']
                or not all(number(x) and lo<=x<=hi for x,lo,hi in zip(action,bounds['low'],bounds['high']))):
            raise ValueError('Invalid native action')
        self.control+=1;self.samples=[]
        import numpy as np
        self.previous_action=np.asarray(action,dtype=np.float32).astype(float).tolist()
        self.journal.write('action_begin',dict(control_step=self.control,physics_step=self.physics,
            requested_action=action,applied_action=self.previous_action))
        self._control_stage='apply'
        try:
            self.bridge.apply(self.previous_action)
            if len(self.samples)!=4:raise RuntimeError('Incomplete native control interval')
            self._control_stage='update'
            self.result=self.scorer.update(self.samples[-1],self.samples)
            if self.control_observer:
                self._control_stage='control_observer'
                self.control_observer(deepcopy(self.samples[-1]))
            self._control_stage='observation'
            row=self.snapshot()
        except BaseException as exc:
            self.abort(exception=exc)
            raise
        self.journal.write('control',dict(requested_action=action,applied_action=self.previous_action,
            observation=row,result=self.result))
        self._control_stage=None
        if row['terminated'] or row['truncated']:
            self.finish()
        return row

    def abort(self,*,exception=None,operation='abort',name=None):
        """Seal the known prefix once, including observation/transaction failures."""
        self._assert_owner()
        if not self.finished:
            self.scorer.hard_failure=True
            self.scorer.failure_reasons.add('native_execution_error')
            self.scorer.coverage_complete=False
            self.result=self.scorer.result()
            error=dict(operation='control' if self._control_stage else operation,stage=self._control_stage,
                control_step=self.control,physics_step=self.physics,
                exception_type=type(exception).__name__ if exception is not None else 'NativeBoundaryFailure',
                message=str(exception) if exception is not None else 'Native request failed outside control execution')
            if name is not None:error['name']=name
            self.journal.write('native_error',error)
        return self.finish()

    def mechanism(self, name, arguments):
        """Audit one constraint request without advancing or writing physical state."""
        self._assert_owner()
        if self.finished or self.result['success'] or self.result['hard_failure'] or self.control>=self.max_steps:
            raise RuntimeError('Episode closed')
        if 'mechanism' not in self._description or not callable(getattr(self.bridge,'mechanism',None)):
            raise ValueError('Native mechanism unavailable')
        from .mechanisms import validate_command,public_reply
        validate_command(name,arguments)
        before = deepcopy(self.bridge.physical(self.control,self.physics))
        self.journal.write('mechanism_begin',dict(name=name,arguments=arguments,
            control_step=self.control,physics_step=self.physics,before=before))
        try:
            result = self.bridge.mechanism(name,arguments)
            after = deepcopy(self.bridge.physical(self.control,self.physics))
            # Only the constraint description may change, not native clocks,
            # positions, velocities, forces or robot targets. Copy before the
            # call so in-place mutations cannot alter both sides of this audit.
            if ({k:v for k,v in before.items() if k!='mechanism'}
                    != {k:v for k,v in after.items() if k!='mechanism'}):
                raise RuntimeError('Mechanism command changed physical state')
            reply = public_reply(result)
            event = dict(name=name,arguments=arguments,result=result,before=before,after=after,
                         control_step=self.control,physics_step=self.physics)
            if callable(getattr(self.scorer,'mechanism_event',None)):
                self.scorer.mechanism_event(event)
                self.result = self.scorer.result()
            self.journal.write('mechanism',event)
            if self.result['hard_failure']:
                raise RuntimeError('Independent mechanism audit rejected the transaction')
            return reply
        except BaseException as exc:
            self.abort(exception=exc,operation='mechanism',name=name)
            raise

    def finish(self, reason=None):
        self._assert_owner()
        if not self.finished:
            self.finished=True
            reason=('success' if self.result['success'] else 'hard_failure' if self.result['hard_failure']
                else 'step_limit' if self.control>=self.max_steps else reason or 'agent_finish')
            self.journal.finish(dict(result=self.result,step_count=self.control,physics_steps=self.physics,termination_reason=reason))
        return dict(success=bool(self.result['success']),score=float(self.result['success']),step_count=self.control,
            terminated=True,truncated=self.control>=self.max_steps)
