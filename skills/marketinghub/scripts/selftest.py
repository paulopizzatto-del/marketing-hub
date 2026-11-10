#!/usr/bin/env python3
"""Offline structural checks for Marketing Hub and optional plugin ZIP source."""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
METHODS = (
    "voice-builder", "newsletter-voice", "profile-optimizer", "post-writer", "graphic-designer",
    "post-scorer", "reels-scripting", "youtube-thumbnail", "pinned-comment", "hook-generator",
    "post-formatter", "content-matrix", "niche-research", "gemini-infographic", "gemini-carousel",
    "quote-post", "analytics-dashboard",
)
LEAK_MARKERS = ("@example.com", "sk-proj-", "API_TOKEN=")


def check():
    errors = []
    skill = ROOT / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n") or not re.search(r"\nname:\s+marketinghub\n", text):
        errors.append("Frontmatter da skill ausente ou nome divergente")
    if "description:" not in text.split("---", 2)[1]:
        errors.append("Metadata sem description")
    discovered = list(ROOT.rglob("SKILL.md"))
    if len(discovered) != 1:
        errors.append(f"Apenas uma SKILL.md e permitida no pacote, obtidas {len(discovered)}")
    if len(text.splitlines()) > 250:
        errors.append("SKILL.md excedeu 250 linhas; mover detalhes para references")

    included = [ROOT / "SKILL.md"] + list((ROOT / "references").glob("*.md"))
    content = "\n".join(p.read_text(encoding="utf-8") for p in included)
    for item in LEAK_MARKERS:
        if item.lower() in content.lower():
            errors.append(f"Nucleo contem marcadores potencialmente sensiveis: {item}")
    for match in re.findall(r"`((?:references|templates|scripts)/[^`]+?)`", content):
        if " " in match or "|" in match:
            continue
        path = ROOT / match
        if not path.exists():
            errors.append(f"Referencia sem arquivo: {match}")
    table = (ROOT / "references" / "methods-catalog.md").read_text(encoding="utf-8")
    for method in METHODS:
        if f"`{method}`" not in table:
            errors.append(f"Metodo original sem mapeamento: {method}")
    numbered = re.findall(r"^\|\s*([0-9]+)\s*\|", table, flags=re.MULTILINE)
    if numbered != [str(i) for i in range(1, 18)]:
        errors.append("Mapa de metodos nao lista exatamente 1..17")

    for name in ("brand-profile.template.json", "brand-profile.schema.json"):
        json.loads((ROOT / "templates" / name).read_text(encoding="utf-8"))
    cases = json.loads((ROOT / "tests" / "test_cases.json").read_text(encoding="utf-8"))["cases"]
    if len(cases) < 12:
        errors.append("Suite qualitativa inferior a 12 cenarios")
    validator = ROOT / "scripts" / "validate_brand_profile.py"
    positive = subprocess.run([sys.executable, str(validator), str(ROOT / "tests" / "brand-profile.valid.json")], capture_output=True, text=True)
    negative = subprocess.run([sys.executable, str(validator), str(ROOT / "tests" / "brand-profile.invalid.json")], capture_output=True, text=True)
    if positive.returncode != 0:
        errors.append(f"Perfil de teste valido rejeitado: {positive.stdout[-250:]}")
    if negative.returncode != 1:
        errors.append("Perfil de teste invalido nao rejeitado")

    print("Marketing Hub - selftest")
    print("Metodos mapeados:", len(METHODS))
    print("Cenarios qualitativos:", len(cases))
    print("Perfis de teste: positivo e negativo verificados")
    if errors:
        print("FALHOU:")
        for e in errors:
            print(" -", e)
        return 1
    print("PASSOU: estrutura, links, marca neutra, 17 metodos e validacao de perfis")
    return 0


if __name__ == "__main__":
    sys.exit(check())
