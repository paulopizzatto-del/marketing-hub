#!/usr/bin/env python3
"""Structural checks. No claim of editorial superiority or AI-free artwork."""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from project_version import ROOT, read_version
from distribution import runtime_payload
REQUIRED=('VERSION','README.md','README.en.md','LICENSE','NOTICE.md','BRAND-ASSETS-LICENSE.md',
 'skills/marketinghub/SKILL.md','skills/marketinghub/agents/openai.yaml',
 'prompts/marketinghub-universal.md','scripts/editorial_checks.py',
 'scripts/install.py','scripts/build_release.py','scripts/evaluate_model_outputs.py',
 '.github/workflows/ci.yml','.github/workflows/release.yml',
 'docs/instalacao.md','docs/compatibilidade.md','docs/revisao-2.3.1.md',
 'assets/ASSET-PROVENANCE.json','evaluation/pilot-144/PLAN.md')

def check():
    errors=[]
    for name in REQUIRED:
        if not (ROOT/name).is_file(): errors.append('Missing: '+name)
    if errors: return errors
    version=read_version()
    for name in ('plugin.json','.codex-plugin/plugin.json'):
        data=json.loads((ROOT/name).read_text(encoding='utf-8'))
        if data.get('name')!='marketinghub' or data.get('version')!=version:
            errors.append('Manifest mismatch: '+name)
    skillpaths=[p.relative_to(ROOT).as_posix() for p in ROOT.rglob('SKILL.md')
        if not any(x in {'dist','.git','.agents','.claude','.gemini','.copilot','.maintenance'} for x in p.relative_to(ROOT).parts)
        and p.relative_to(ROOT).parts[:3]!=('.github','skills','marketinghub')]
    if skillpaths!=['skills/marketinghub/SKILL.md']: errors.append('Canonical skill paths: '+str(skillpaths))
    manifest=json.loads((ROOT/'assets/ASSET-PROVENANCE.json').read_text(encoding='utf-8'))
    listed={a['file'] for a in manifest['assets']}
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
        and p.suffix.lower() in {'.png','.svg','.jpg','.jpeg','.webp','.gif'}
        and not any(x in {'dist','.git','.agents','.claude','.gemini','.copilot'} for x in p.relative_to(ROOT).parts)}
    if listed!=actual: errors.append('Asset inventory mismatch: '+str(sorted(listed ^ actual)))
    for a in manifest['assets']:
        p=ROOT/a['file']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=a['sha256']:
            errors.append('Asset integrity mismatch: '+a['file'])
    for rel in ('README.md','README.en.md','docs/index.html'):
        p=ROOT/rel;text=p.read_text(encoding='utf-8')
        for link,attr in re.findall(r'\]\(([^)]+)\)|(?:src|href)="([^"]+)"',text):
            value=link or attr
            if value.startswith(('http:','https:','mailto:','#')): continue
            target=value.split('#')[0]
            if not (p.parent/target).exists(): errors.append('Broken local link: '+rel+': '+value)
        for source in re.findall(r'<img[^>]+src="([^"]+)"',text):
            if 'banner.png' in source or 'social-preview' in source or '/archive/' in source:
                errors.append('Retired promotional graphic displayed: '+rel)
        if '[AJUSTAR' in text: errors.append('Placeholder: '+rel)
    if len((ROOT/'prompts/marketinghub-universal.md').read_text(encoding='utf-8'))<3500:
        errors.append('Portable prompt is incomplete')
    payload=runtime_payload()
    if any(n.endswith(('.png','.svg','.jpg','.webp')) or n.startswith('tests/') for n in payload):
        errors.append('Runtime contains imagery or tests')
    if payload['VERSION'].decode().strip()!=version: errors.append('Runtime version mismatch')
    if 'Charlie Hills' not in (ROOT/'skills/marketinghub/LICENSE').read_text(): errors.append('Upstream attribution missing')
    for path in (ROOT/'.github/workflows').glob('*.yml'):
        if path.name not in {'ci.yml','release.yml'}: continue
        for use in re.findall(r'uses:\s*([^\s]+)',path.read_text()):
            if use.startswith('actions/') and not re.fullmatch(r'actions/[\w-]+@[0-9a-f]{40}',use):
                errors.append('Action not pinned: '+path.name)
    command=[sys.executable,str(ROOT/'skills/marketinghub/scripts/selftest.py')]
    result=subprocess.run(command,capture_output=True,text=True)
    if result.returncode: errors.append('Skill structural selftest failed: '+result.stdout[-500:])
    return errors
if __name__=='__main__':
    errors=check()
    for e in errors: print('ERROR:',e)
    if errors: raise SystemExit(1)
    print('PASS: structural checks, versions, runtime allowlist and supplied asset byte integrity')
