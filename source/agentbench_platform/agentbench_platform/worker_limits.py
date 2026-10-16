"""Trusted POSIX launcher: apply limits in a fresh interpreter, then exec.

This file is invoked directly with -I, without package/native imports. No Python
callback runs between fork and exec in the threaded protocol owner.
"""
import os
import resource
import sys


def attach(command, limit):
    """Bound captured streams without limiting the trusted engine's own files.

    Applying RLIMIT_FSIZE to Podman also limits writes to its shared state DB.
    The container already supplies filesystem isolation. This relay keeps each
    output bounded; the caller still owns wall timeout and process-group cleanup.
    """
    import selectors
    import subprocess
    child=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    with selectors.DefaultSelector() as selector:
        for stream,target in ((child.stdout,sys.stdout.buffer),(child.stderr,sys.stderr.buffer)):
            selector.register(stream,selectors.EVENT_READ,[target,0])
        while selector.get_map():
            for key,_ in selector.select():
                chunk=os.read(key.fd,65536)
                if not chunk:
                    selector.unregister(key.fileobj);key.fileobj.close();continue
                target,count=key.data
                remaining=limit-count
                target.write(chunk[:remaining]);target.flush()
                if len(chunk)>=remaining:return 1
                key.data[1]+=len(chunk)
    return child.wait()


def main():
    if len(sys.argv)<3:raise ValueError('Worker command required')
    limit=int(sys.argv[1])
    if not 0<limit<=512*1024:raise ValueError('Invalid worker output limit')
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    if sys.argv[2]=='--container-attach':
        if len(sys.argv)<4:raise ValueError('Container attach command required')
        return attach(sys.argv[3:],limit)
    resource.setrlimit(resource.RLIMIT_FSIZE,(limit,limit))
    os.execvpe(sys.argv[2],sys.argv[2:],os.environ)


if __name__=='__main__':raise SystemExit(main())
