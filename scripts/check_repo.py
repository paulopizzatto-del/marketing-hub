#!/usr/bin/env python3
"""Offline sanity check for Marketing Hub before sharing the repository."""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ICON_SHA256 = 'e28a3b8b9db85c893476a6f02726a4e317eb7ed7450c757bd54b12c85efa23b5'
MUST_EXIST = (
    'README.md', 'README.en.md', 'LICENSE', 'NOTICE.md', 'BRAND-ASSETS-LICENSE.md',
    'AGENTS.md', 'CLAUDE.md', 'GEMINI.md', 'prompts/marketinghub-universal.md',
    'skills/marketinghub/SKILL.md', 'plugin.json', '.codex-plugin/plugin.json',
    '.github/workflows/ci.yml', '.github/workflows/release.yml',
    'scripts/install.py', 'scripts/build_release.py', 'docs/instalacao.md',
    'docs/compatibilidade.md', 'docs/perfil-de-marca.md', 'docs/publicacao-no-github.md',
    'assets/marketinghub-icon.png', 'assets/banner.png', 'assets/social-preview-1280x640.png', 'assets/ASSET-PROVENANCE.json', 'docs/identidade-visual.md', 'skills/marketinghub/LICENSE',
)


def check():
    errors = []
    for file in MUST_EXIST:
        if not (ROOT / file).is_file(): errors.append(f'Arquivo ausente: {file}')
    if errors: return errors
    for manifest in ('plugin.json', '.codex-plugin/plugin.json'):
        data = json.loads((ROOT/manifest).read_text(encoding='utf-8'))
        if data.get('name') != 'marketinghub' or data.get('version') != '2.2.1':
            errors.append(f'Manifesto invalido: {manifest}')
    # One canonical SKILL.md, not 17 different entrypoints.
    skill_paths = [p.relative_to(ROOT) for p in ROOT.rglob('SKILL.md') if 'dist' not in p.parts and not any(hidden in p.relative_to(ROOT).parts for hidden in ('.agents','.claude','.gemini','.copilot')) and p.relative_to(ROOT).parts[:3] != ('.github','skills','marketinghub')]
    if skill_paths != [Path('skills/marketinghub/SKILL.md')]:
        errors.append(f'Skill duplicada ou faltante: {skill_paths}')
    icon = ROOT/'assets/marketinghub-icon.png'
    if hashlib.sha256(icon.read_bytes()).hexdigest() != EXPECTED_ICON_SHA256:
        errors.append('O icone principal difere do PNG oficial fornecido')
    if icon.read_bytes() != (ROOT/'skills/marketinghub/assets/marketinghub-icon.png').read_bytes():
        errors.append('Icones do plugin e da skill divergem')
    # Ensure relative README links are valid (skip URLs and in-page anchors).
    for readme in ('README.md', 'README.en.md'):
        text = (ROOT/readme).read_text(encoding='utf-8')
        links = re.findall(r'\]\(([^)]+)\)|(?:src|href)="([^"]+)"', text)
        for link, attr in links:
            value = link or attr
            if value.startswith(('http:', 'https:', 'mailto:', '#')): continue
            target = value.split('#')[0]
            if not (ROOT/target).exists(): errors.append(f'Link quebrado em {readme}: {value}')
    # Only owner-provided original art is allowed. Manifest records must match all image assets.
    provenance = json.loads((ROOT/'assets/ASSET-PROVENANCE.json').read_text(encoding='utf-8'))
    visual_extensions = {'.png', '.jpg', '.jpeg', '.svg', '.webp'}
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.suffix.lower() in visual_extensions and 'dist' not in p.relative_to(ROOT).parts}
    listed = {item['file'] for item in provenance['assets']}
    if listed != actual:
        errors.append(f'Imagens ausentes do registro ou arquivos extras: {sorted(actual ^ listed)}')
    for item in provenance['assets']:
        f = ROOT / item['file']
        if f.exists() and hashlib.sha256(f.read_bytes()).hexdigest() != item['sha256']:
            errors.append(f'Imagem modificada ou não autorizada: {item["file"]}')
    # Detect broken local image links on GitHub Pages and forbid README placeholders.
    for html_file in (ROOT / 'docs').rglob('*.html'):
        text_html = html_file.read_text(encoding='utf-8')
        for src in re.findall(r'<img[^>]+src="([^"]+)"', text_html):
            if not src.startswith(('http:', 'https:')) and not (html_file.parent/src).is_file():
                errors.append(f'Imagem ausente no site: {html_file.name}: {src}')
    for filename in ('README.md', 'README.en.md'):
        content = (ROOT/filename).read_text(encoding='utf-8')
        if '[AJUSTAR' in content or 'URL_DO_REPOSITORIO' in content:
            errors.append(f'Placeholder não resolvido em {filename}')
    notice = (ROOT/'NOTICE.md').read_text(encoding='utf-8')
    license_txt = (ROOT/'skills/marketinghub/LICENSE').read_text(encoding='utf-8')
    if 'Charlie Hills' not in notice or 'Charlie Hills' not in license_txt:
        errors.append('Atribuicao MIT original nao preservada')
    if len((ROOT/'prompts/marketinghub-universal.md').read_text(encoding='utf-8')) < 3500:
        errors.append('Prompt portatil muito curto para ser autocontido')
    skilltest = subprocess.run([sys.executable, str(ROOT/'skills/marketinghub/scripts/selftest.py')], capture_output=True, text=True)
    if skilltest.returncode:
        errors.append('Selftest da skill falhou: ' + skilltest.stdout[-1000:])
    validator = ROOT/'skills/marketinghub/scripts/validate_brand_profile.py'
    valid = subprocess.run([sys.executable, str(validator), str(ROOT/'examples/brand-profile-ficticio.json')], capture_output=True, text=True)
    if valid.returncode: errors.append('Exemplo ficticio de marca nao validou')
    return errors

if __name__ == '__main__':
    mistakes = check()
    if mistakes:
        print('FALHA:')
        for message in mistakes: print(' -', message)
        raise SystemExit(1)
    print('OK: icones oficiais, hashes de artes, versoes, links, metodos, skill e atribuicao')
