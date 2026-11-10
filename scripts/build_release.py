#!/usr/bin/env python3
"""Reproducible packages. Runtime has no promotional graphics or internal tests."""
from __future__ import annotations
import hashlib
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from distribution import ROOT, runtime_payload
DIST=ROOT/'dist'
DIRS={'assets','docs','examples','scripts','skills','tests','evaluation','prompts',
      '.github','.codex-plugin','.cursor'}
FILES={'README.md','README.en.md','VERSION','LICENSE','NOTICE.md','BRAND-ASSETS-LICENSE.md',
       'CHANGELOG.md','CONTRIBUTING.md','SECURITY.md','SUPPORT.md','CODE_OF_CONDUCT.md',
       'AGENTS.md','CLAUDE.md','GEMINI.md','plugin.json','.gitignore','.gitattributes',
       '.editorconfig','requirements-dev.txt'}
SKIP={'.git','dist','__pycache__','.venv','venv','.pytest_cache','.mypy_cache',
      'private','results-private','.agents','.claude','.gemini','.copilot'}

def repository_files(root=ROOT):
    out=[]
    for p in root.rglob('*'):
        rel=p.relative_to(root)
        if rel.parts[0] not in DIRS and rel.as_posix() not in FILES: continue
        if any(part in SKIP for part in rel.parts): continue
        if rel.parts[:3]==('.github','skills','marketinghub'): continue
        if p.is_symlink(): raise ValueError('Refusing linked source: '+str(rel))
        if not p.is_file(): continue
        if p.name.startswith('.env') or '.secret.' in p.name or p.suffix in {'.pyc','.log','.pem','.key','.ttf','.otf','.woff','.woff2'}: continue
        out.append(p)
    return sorted(out,key=lambda p:p.relative_to(root).as_posix())

def write_zip(path,entries):
    with ZipFile(path,'w',compression=ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(entries.items()):
            i=ZipInfo(name,date_time=(2026,1,1,0,0,0));i.compress_type=ZIP_DEFLATED
            i.create_system=3;i.external_attr=0o100644<<16
            z.writestr(i,data,compress_type=ZIP_DEFLATED,compresslevel=9)
    with ZipFile(path) as z:
        if z.testzip(): raise RuntimeError('Invalid ZIP: '+path.name)

def build():
    DIST.mkdir(exist_ok=True)
    payload=runtime_payload()
    write_zip(DIST/'skill.zip',{'marketinghub/'+n:b for n,b in payload.items()})
    plugin={n:(ROOT/n).read_bytes() for n in ('plugin.json','.codex-plugin/plugin.json',
        'assets/marketinghub-icon.png','LICENSE','NOTICE.md','BRAND-ASSETS-LICENSE.md','VERSION')}
    plugin.update({'skills/marketinghub/'+n:b for n,b in payload.items()})
    write_zip(DIST/'marketing-hub-plugin.zip',plugin)
    write_zip(DIST/'marketing-hub-repository.zip',{'marketing-hub/'+p.relative_to(ROOT).as_posix():p.read_bytes() for p in repository_files()})
    outputs=[DIST/n for n in ('skill.zip','marketing-hub-plugin.zip','marketing-hub-repository.zip')]
    (DIST/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in outputs),encoding='utf-8')
    for p in outputs: print(p.name,p.stat().st_size,'bytes')
    return outputs
if __name__=='__main__': build()
