import hashlib
import json
from pathlib import Path
import pytest
from agentbench_platform.embedded_sources import verify_embedded_sources, embedded_manifest


def test_embedded_snapshot_detects_missing_changed_and_linked_content(tmp_path):
    source=tmp_path/'third_party/example/source.py';source.parent.mkdir(parents=True)
    source.write_bytes(b'original')
    manifest=tmp_path/'third_party/manifest.json'
    manifest.write_text(json.dumps(dict(version=1,projects=[dict(path='third_party/example')],
        files={'third_party/example/source.py':dict(sha256=hashlib.sha256(b'original').hexdigest(),bytes=8)})))
    assert verify_embedded_sources(tmp_path)['status']=='passed'
    source.write_bytes(b'changed')
    assert verify_embedded_sources(tmp_path)['issues'][0]['error']=='content_mismatch'
    source.unlink()
    assert verify_embedded_sources(tmp_path)['issues'][0]['error']=='missing_or_linked'
    source.symlink_to(manifest)
    assert verify_embedded_sources(tmp_path)['issues'][0]['error']=='missing_or_linked'


def test_embedded_manifest_rejects_path_escape(tmp_path):
    directory=tmp_path/'third_party';directory.mkdir()
    (directory/'manifest.json').write_text(json.dumps(dict(version=1,files={'third_party/../../private':{}})))
    with pytest.raises(ValueError,match='Unsafe'):embedded_manifest(tmp_path)
