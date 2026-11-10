"""Shared allowlist for installation and reproducible runtime packaging."""
from pathlib import Path
from project_version import read_version
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'marketinghub'
RUNTIME_FILES = ('SKILL.md','LICENSE','NOTICE.md','agents/openai.yaml',
                 'scripts/validate_brand_profile.py')
RUNTIME_DIRS = ('references','templates')
IMAGE_SUFFIXES = {'.png','.jpg','.jpeg','.svg','.webp','.gif','.woff','.woff2','.ttf','.otf'}

def runtime_files(source=SKILL):
    paths=[source/name for name in RUNTIME_FILES]
    for directory in RUNTIME_DIRS:
        paths += [p for p in (source/directory).rglob('*') if p.is_file()]
    for p in paths:
        if not p.is_file() or p.is_symlink():
            raise ValueError('Missing or linked runtime source: '+str(p.relative_to(source)))
        if any(a.is_symlink() for a in p.parents if a != source.parent):
            raise ValueError('Linked runtime ancestor')
        if p.suffix.lower() in IMAGE_SUFFIXES:
            raise ValueError('Images/fonts do not belong in the runtime')
    return sorted(set(paths),key=lambda p:p.relative_to(source).as_posix())

def runtime_payload(source=SKILL,root=ROOT):
    result={p.relative_to(source).as_posix():p.read_bytes() for p in runtime_files(source)}
    result['VERSION']=(read_version(root)+'\n').encode('utf-8')
    return result
