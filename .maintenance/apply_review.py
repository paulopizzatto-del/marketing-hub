"""One-time integrity-guarded application of the reviewed text patch."""
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess

root = Path.cwd().resolve()
expected = 'ddb8dc6fd1b901ce02a857eb7b733a4bcde7e180887c84c63ea8b0b57fd84328'
parts = [f'{i:02d}' for i in range(1, 20)] + ['20a','20b','21a','21b']
data = b''.join((root / '.maintenance' / ('review-patch.' + p)).read_bytes() for p in parts)
if len(data) != 57916 or hashlib.sha256(data).hexdigest() != expected:
    raise SystemExit('Patch checksum mismatch; refusing all writes')
patch = json.loads(gzip.decompress(data).decode('utf-8'))
if patch['base_commit'] != 'f5f82a84ab62a06bb2eb996d4d68201832c56281':
    raise SystemExit('Unexpected base commit')
subprocess.run(['git','merge-base','--is-ancestor',patch['base_commit'],'HEAD'], check=True)

def safe(name):
    rel = PurePosixPath(name)
    if rel.is_absolute() or '..' in rel.parts or '\\' in name or not rel.parts:
        raise ValueError('Unsafe patch path')
    if rel.parts[0] in ('.git','.maintenance') or rel.parts[:2] == ('.github','workflows'):
        raise ValueError('Protected patch path')
    path = root.joinpath(*rel.parts)
    if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != root.parent):
        raise ValueError('Linked patch path')
    if not path.resolve().is_relative_to(root):
        raise ValueError('Escaping patch path')
    return path

all_names = set(patch['writes']) | set(patch['deletes']) | set(patch['moves']) | set(patch['moves'].values())
if all_names != set(patch['before_sha256']):
    raise ValueError('Incomplete precondition map')
for name in all_names:
    path = safe(name)
    before = patch['before_sha256'][name]
    if before is None:
        if path.exists():
            raise ValueError('New path already exists: ' + name)
    elif not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != before:
        raise ValueError('Source changed: ' + name)
for source, dest in patch['moves'].items():
    target = safe(dest)
    target.parent.mkdir(parents=True, exist_ok=True)
    safe(source).rename(target)
for name in patch['deletes']:
    safe(name).unlink()
for name, text in patch['writes'].items():
    path = safe(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='')
shutil.rmtree(root / '.maintenance')
print('Reviewed patch applied: 64 text writes, 2 exact-byte moves, 15 removals')
