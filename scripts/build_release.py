#!/usr/bin/env python3
"""Build reproducible ZIPs from the one canonical skill; no external tools."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
SKILL = ROOT / 'skills' / 'marketinghub'
SKIP_DIRS = {'.git', 'dist', '__pycache__', '.venv', '.pytest_cache', '.mypy_cache', '.agents', '.claude', '.gemini', '.copilot'}
SKIP_NAMES = {'.DS_Store'}


def add(zf, path, arcname):
    data = path.read_bytes()
    info = ZipInfo(str(arcname).replace('\\', '/'), date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, data)


def skill_files():
    return sorted((p for p in SKILL.rglob('*') if p.is_file() and not any(t in SKIP_DIRS for t in p.parts) and p.name not in SKIP_NAMES), key=str)


def repository_files():
    return sorted((p for p in ROOT.rglob('*') if p.is_file() and not any(t in SKIP_DIRS for t in p.relative_to(ROOT).parts) and p.name not in SKIP_NAMES and p.relative_to(ROOT).parts[:3] != ('.github', 'skills', 'marketinghub')), key=str)


def build():
    DIST.mkdir(exist_ok=True)
    skill_zip = DIST / 'skill.zip'
    with ZipFile(skill_zip, 'w') as zf:
        for p in skill_files():
            add(zf, p, Path('marketinghub') / p.relative_to(SKILL))

    plugin_zip = DIST / 'marketing-hub-plugin.zip'
    with ZipFile(plugin_zip, 'w') as zf:
        for p in (ROOT / 'plugin.json', ROOT / '.codex-plugin' / 'plugin.json'):
            add(zf, p, p.relative_to(ROOT))
        for p in sorted((ROOT / 'assets').rglob('*')):
            if p.is_file(): add(zf, p, p.relative_to(ROOT))
        for p in skill_files():
            add(zf, p, Path('skills/marketinghub') / p.relative_to(SKILL))

    repo_zip = DIST / 'marketing-hub-repository.zip'
    with ZipFile(repo_zip, 'w') as zf:
        for p in repository_files():
            add(zf, p, Path('marketing-hub') / p.relative_to(ROOT))

    outputs = (skill_zip, plugin_zip, repo_zip)
    (DIST / 'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in outputs), encoding='utf-8')
    for p in outputs:
        with ZipFile(p) as zf:
            corrupt = zf.testzip()
            if corrupt: raise RuntimeError(f'Corrupt archive: {p.name}: {corrupt}')
    print('Arquivos prontos (SHA256SUMS.txt):')
    for p in outputs: print(f' - {p.name}: {p.stat().st_size} bytes')

if __name__ == '__main__':
    build()
