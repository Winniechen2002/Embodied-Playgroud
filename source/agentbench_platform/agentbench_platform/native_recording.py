"""Private lossless evidence. No journal path is exposed through the protocol."""
import gzip
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform


class EvidenceJournal:
    def __init__(self, directory, *, source_paths, config):
        self.directory = Path(directory)
        self.directory.mkdir(mode=0o700, parents=True, exist_ok=False)
        os.chmod(self.directory, 0o700)
        self._stream = gzip.open(self.directory/'trace.jsonl.gz', 'xt', encoding='utf-8')
        self.closed = False
        sources = {str(p): dict(sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest(),
                                bytes=Path(p).stat().st_size) for p in source_paths}
        versions = {'python':platform.python_version()}
        for name in ('isaacsim','isaaclab','torch','numpy','scipy'):
            try: versions[name] = importlib.metadata.version(name)
            except importlib.metadata.PackageNotFoundError: pass
        config_json = json.dumps(config, sort_keys=True, allow_nan=False)
        self.write('manifest', dict(sources=sources, versions=versions, config=config,
            config_sha256=hashlib.sha256(config_json.encode()).hexdigest(), evidence_version=1))

    def write(self, kind, data):
        if self.closed: raise RuntimeError('Evidence journal closed')
        self._stream.write(json.dumps(dict(kind=kind,data=data), allow_nan=False,separators=(',',':'))+'\n')
        self._stream.flush()

    def finish(self, result):
        if self.closed: return
        self.write('final',result)
        self._stream.close()
        self.closed = True
        (self.directory/'result.json').write_text(json.dumps(result,allow_nan=False,indent=2)+'\n')
