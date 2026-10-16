"""Container cleanup capability shared by offline tool builders."""
from .container_engine import ContainerEngine


class OwnedContainer:
    """Bounded cleanup capability: inspect ID and task name before every mutation."""
    def __init__(self, cid, name, *, record, inspection_path=None, engine=None):
        import re
        if not re.fullmatch('[0-9a-f]{64}', cid): raise ValueError('Invalid owned container ID')
        self.cid, self.name, self.record, self.inspection_path = cid, name, record, inspection_path
        self.engine = engine or ContainerEngine()

    def _run(self, arguments, component):
        import subprocess
        try:
            result = subprocess.run(self.engine.command(*arguments), capture_output=True, text=True, timeout=15, check=False)
        except Exception as exc:
            self.record(component, 'command_exception', type=type(exc).__name__)
            return None
        return result

    def _inspect(self):
        import json
        import re
        result = self._run(['inspect', self.cid], 'container_inspect')
        if result is None: return 'ambiguous'
        if result.returncode != 0:
            # A failed inspect alone does not prove absence (daemon/permission errors).
            listing = self._run(['container', 'ls', '--all', '--no-trunc', '--quiet', '--filter', 'id='+self.cid], 'container_absence')
            if listing is not None and listing.returncode == 0:
                ids = listing.stdout.split()
                if all(re.fullmatch('[0-9a-f]{64}', cid) for cid in ids) and not ids:
                    return 'absent'
            self.record('container_inspect', 'nonzero_exit', returncode=result.returncode)
            return 'ambiguous'
        try:
            rows = json.loads(result.stdout)
            valid = (isinstance(rows, list) and len(rows) == 1 and isinstance(rows[0], dict)
                     and rows[0].get('Id') == self.cid and self.engine.owns_name(rows[0].get('Name'), self.name)
                     and isinstance(rows[0].get('State'), dict) and type(rows[0]['State'].get('Running')) is bool)
        except (ValueError, TypeError): valid = False
        if not valid:
            self.record('container_identity', 'ownership_unverified')
            return 'ambiguous'
        if self.inspection_path:
            try: self.inspection_path.write_text(result.stdout)
            except OSError as exc: self.record('container_inspect_evidence', 'write_failure', type=type(exc).__name__)
        return 'owned'

    def stop(self):
        state = self._inspect()
        if state != 'owned': return state
        result = self._run(['stop', '--time', '2', self.cid], 'container_stop')
        if result is not None and result.returncode != 0:
            self.record('container_stop', 'nonzero_exit', returncode=result.returncode)
        return 'owned' if result is not None and result.returncode == 0 else 'unresolved'

    def remove(self):
        state = self._inspect()
        if state == 'absent': return 'absent'
        if state != 'owned':
            self.record('container_remove', 'cleanup_unresolved', container_id=self.cid,
                        action='Restore container engine access and verify task ownership before cleanup.')
            return 'unresolved'
        result = self._run(['rm', self.cid], 'container_remove')
        if result is None or result.returncode != 0:
            if result is not None: self.record('container_remove', 'nonzero_exit', returncode=result.returncode)
            # Recheck ownership before bounded force removal; never use a name or ambient query.
            state = self._inspect()
            if state == 'absent': return 'removed'
            if state == 'owned':
                forced = self._run(['rm', '--force', self.cid], 'container_force_remove')
                if forced is not None and forced.returncode != 0:
                    self.record('container_force_remove', 'nonzero_exit', returncode=forced.returncode)
        if self._inspect() == 'absent': return 'removed'
        self.record('container_remove', 'cleanup_unresolved', container_id=self.cid,
                    action='Verify task-owned ID and remove it after restoring container engine access.')
        return 'unresolved'
