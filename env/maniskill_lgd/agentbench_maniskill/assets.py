"""Install the bundled dependency closure and verify every file against its hash."""
import hashlib,json,tarfile
from pathlib import Path
from .common.paths import PACKAGE_ROOT,ASSET_ROOT

def manifest():return json.loads((PACKAGE_ROOT/'resources/asset_manifest.json').read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def verify(root=ASSET_ROOT):
    root=Path(root);bad=[]
    for row in manifest()['files']:
        f=root/row['path']
        if not f.is_file() or f.stat().st_size!=row['bytes'] or sha(f)!=row['sha256']:bad.append(row['path'])
    return bad

def install(root=ASSET_ROOT):
    root=Path(root).resolve();m=manifest();bundle=PACKAGE_ROOT/'resources'/m['bundle']
    if sha(bundle)!=m['bundle_sha256']:raise ValueError('Asset archive checksum mismatch')
    root.mkdir(parents=True,exist_ok=True)
    with tarfile.open(bundle,'r:gz') as archive:
        for item in archive.getmembers():
            dest=(root/item.name).resolve()
            if not dest.is_relative_to(root) or not item.isfile():raise ValueError('Unsafe asset archive member '+item.name)
        archive.extractall(root)
    bad=verify(root)
    if bad:raise ValueError('Asset verification failed: '+', '.join(bad))
    return root
