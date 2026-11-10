#!/usr/bin/env python3
"""Offline runtime-only installer with guarded replacement and retained backup."""
from __future__ import annotations
import argparse
import shutil
import sys
import tempfile
import uuid
from pathlib import Path
from distribution import ROOT, SKILL as SOURCE, runtime_payload
LOCATIONS={
    'codex':('.agents/skills','.agents/skills'),
    'claude':('.claude/skills','.claude/skills'),
    'gemini':('.gemini/skills','.gemini/skills'),
    'copilot':('.github/skills','.copilot/skills'),
}

def destination(platform,scope,project):
    if platform not in LOCATIONS or scope not in ('project','user'):
        raise ValueError('Unknown platform or scope')
    base=project.expanduser().absolute() if scope=='project' else Path.home().absolute()
    return base/LOCATIONS[platform][0 if scope=='project' else 1]/'marketinghub'

def install(platform,scope,project,force=False,dry_run=False):
    target=destination(platform,scope,project)
    if target.resolve()==SOURCE.resolve(): raise RuntimeError('Target equals source')
    if target.is_symlink() or any(p.is_symlink() for p in target.parents):
        raise RuntimeError('Refusing symbolic link destination or ancestor')
    if target.exists() and not target.is_dir(): raise RuntimeError('Target is not a directory')
    if target.exists() and not force: raise FileExistsError('Existing installation; use --force to replace with a retained backup')
    payload=runtime_payload(SOURCE)
    if dry_run: return target
    target.parent.mkdir(parents=True,exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='.marketinghub-stage-',dir=target.parent))
    backup=None
    try:
        for name,content in payload.items():
            dest=stage/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(content)
        if not (stage/'SKILL.md').is_file(): raise RuntimeError('Missing SKILL.md after copy')
        if target.exists():
            backup=target.with_name('.marketinghub-backup-'+uuid.uuid4().hex)
            target.rename(backup)
        stage.rename(target)
    except Exception:
        if backup is not None and not target.exists(): backup.rename(target)
        raise
    finally:
        if stage.exists(): shutil.rmtree(stage)
    if backup is not None: print('Previous installation retained at:',backup)
    return target

def main():
    p=argparse.ArgumentParser(description='Install only the Marketing Hub runtime, offline')
    p.add_argument('--platform',choices=sorted(LOCATIONS),required=True)
    p.add_argument('--scope',choices=('project','user'),default='project')
    p.add_argument('--project',type=Path,default=Path.cwd())
    p.add_argument('--force',action='store_true');p.add_argument('--dry-run',action='store_true')
    a=p.parse_args()
    try: target=install(a.platform,a.scope,a.project,a.force,a.dry_run)
    except (OSError,RuntimeError,ValueError) as exc:
        print('ERROR:',exc,file=sys.stderr);return 1
    print('Planned destination:' if a.dry_run else 'Installed:',target)
    print('Open your compatible client and verify skill discovery. No model test was performed.')
    return 0
if __name__=='__main__': raise SystemExit(main())
