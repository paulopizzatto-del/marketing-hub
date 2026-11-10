#!/usr/bin/env python3
"""Copy the single Marketing Hub Agent Skill into a supported local client.

Offline, standard library only; does not access accounts or the network.
"""
from __future__ import annotations
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills' / 'marketinghub'
LOCATIONS = {
    'codex': ('.agents/skills', '.agents/skills'),
    'claude': ('.claude/skills', '.claude/skills'),
    'gemini': ('.gemini/skills', '.gemini/skills'),
    'copilot': ('.github/skills', '.copilot/skills'),
}

def destination(platform: str, scope: str, project: Path) -> Path:
    project_suffix, user_suffix = LOCATIONS[platform]
    home_or_project = project.expanduser().resolve() if scope == 'project' else Path.home().resolve()
    return home_or_project / (project_suffix if scope == 'project' else user_suffix) / 'marketinghub'

def install(platform: str, scope: str, project: Path, force: bool = False, dry_run: bool = False) -> Path:
    if not (SOURCE / 'SKILL.md').is_file():
        raise RuntimeError('Fonte da skill nao encontrada: skills/marketinghub/SKILL.md')
    target = destination(platform, scope, project)
    if target.resolve() == SOURCE.resolve():
        raise RuntimeError('O destino nao pode ser a propria origem')
    if target.exists() and not force:
        raise FileExistsError(f'Ja existe uma skill nesse destino: {target}. Use --force apenas se quiser substituir.')
    if dry_run:
        return target
    if target.is_symlink():
        raise RuntimeError('Recusado: destino e link simbolico')
    if target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    if not (target / 'SKILL.md').exists():
        raise RuntimeError('A copia terminou sem SKILL.md')
    return target

def main() -> int:
    parser = argparse.ArgumentParser(description='Instalador offline do Marketing Hub Agent Skill')
    parser.add_argument('--platform', choices=sorted(LOCATIONS), required=True)
    parser.add_argument('--scope', choices=('project', 'user'), default='project')
    parser.add_argument('--project', type=Path, default=Path.cwd(), help='Diretorio do projeto para --scope project')
    parser.add_argument('--force', action='store_true', help='Substitui a instalacao existente')
    parser.add_argument('--dry-run', action='store_true', help='Mostra o destino sem copiar')
    args = parser.parse_args()
    try:
        target = install(args.platform, args.scope, args.project, args.force, args.dry_run)
    except (OSError, RuntimeError) as error:
        print('ERRO:', error, file=sys.stderr)
        return 1
    print(('Destino previsto:' if args.dry_run else 'Skill copiada para:'), target)
    print('Abra/recarregue o cliente de IA e confirme a descoberta da skill.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
