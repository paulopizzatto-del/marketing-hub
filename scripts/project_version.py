"""One source for the distribution version; profile schema has its own version."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
def read_version(root=ROOT):
    value = (root / 'VERSION').read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', value):
        raise ValueError('VERSION must contain a semantic release version')
    return value
