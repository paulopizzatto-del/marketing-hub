#!/usr/bin/env python3
"""Marketing Hub: validate a portable brand profile without needing network access.

Usage: python scripts/validate_brand_profile.py profile.json [profile2.json ...]

The standard-library fallback checks essential invariants; when the optional
'jsonschema' package is installed, it performs full Draft 2020-12 validation.
No profile data is transmitted or saved by this program.
"""

import json
import re
import sys
from pathlib import Path

SCHEMA = Path(__file__).resolve().parent.parent / "templates" / "brand-profile.schema.json"
REQUIRED = ("schema_version", "brand_id", "display_name", "brand_type", "description", "primary_audience", "default_language", "profile_status", "voice")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LANG = re.compile(r"^[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")
SECRET = re.compile(r"(?:sk-(?:proj-|live-|test-)?[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16})")


def _human_errors(doc):
    """Basic validation even where jsonschema is unavailable."""
    errors = []
    if not isinstance(doc, dict):
        return ["o perfil deve ser um objeto JSON"]
    for key in REQUIRED:
        if key not in doc:
            errors.append(f"campo obrigatorio ausente: {key}")
    if doc.get("schema_version") != "2.0":
        errors.append("schema_version deve ser '2.0'")
    identifier = doc.get("brand_id", "")
    if not isinstance(identifier, str) or not SLUG.fullmatch(identifier) or not 2 <= len(identifier) <= 64:
        errors.append("brand_id deve ser slug minusculo (2-64 caracteres)")
    for key, size in (("display_name", 2), ("description", 8), ("primary_audience", 4)):
        value = doc.get(key)
        if not isinstance(value, str) or len(value.strip()) < size:
            errors.append(f"{key} precisa ter pelo menos {size} caracteres")
    if not isinstance(doc.get("brand_type"), str) or doc.get("brand_type") not in {"company", "personal", "nonprofit", "product", "other"}:
        errors.append("brand_type nao reconhecido")
    if not isinstance(doc.get("profile_status"), str) or doc.get("profile_status") not in {"draft", "calibrated", "operational"}:
        errors.append("profile_status nao reconhecido")
    lang = doc.get("default_language")
    if not isinstance(lang, str) or not LANG.fullmatch(lang):
        errors.append("default_language deve ser BCP47 simplificado, ex.: pt-BR")
    voice = doc.get("voice")
    if not isinstance(voice, dict):
        errors.append("voice precisa ser um objeto")
    else:
        for name in ("attributes", "sample_rules"):
            arr = voice.get(name)
            if not isinstance(arr, list) or not arr or any(not isinstance(s,str) or not s.strip() for s in arr):
                errors.append(f"voice.{name} precisa de ao menos uma string")
        for name in ("formality", "energy", "humor", "technicality"):
            val = voice.get(name)
            if type(val) is not int or not 0 <= val <= 5:
                errors.append(f"voice.{name} precisa ser inteiro de 0 a 5")
        if not isinstance(voice.get("pronouns"), str) or voice.get("pronouns") not in {"first_person_singular", "first_person_plural", "brand_name", "neutral", "unspecified"}:
            errors.append("voice.pronouns invalido")
        for key in ("preferred_terms", "avoid_terms"):
            if not isinstance(voice.get(key), list):
                errors.append(f"voice.{key} precisa ser uma lista")
    return errors


def validate_profile(path, require_full=False):
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return None, [f"erro lendo JSON: {error}"], []
    errors = _human_errors(document)
    warnings = []
    try:
        import jsonschema  # optional dependency
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
        for err in sorted(validator.iter_errors(document), key=lambda e: list(map(str, e.absolute_path))):
            where = ".".join(str(p) for p in err.absolute_path) or "raiz"
            message = f"{where}: schema rule {err.validator} failed"
            if message not in errors:
                errors.append(message)
    except ImportError:
        warnings.append("jsonschema nao instalado: apenas verificacao essencial executada")
        if require_full:
            errors.append("validacao completa requerida: instale jsonschema")
    if SECRET.search(json.dumps(document, ensure_ascii=False)):
        errors.append("possivel credencial detectada: remover do perfil")
    if isinstance(document, dict) and document.get("profile_status") == "operational":
        if not document.get("channels") or not document.get("goals"):
            warnings.append("perfil operacional sem canais ou objetivos definidos")
    return document, sorted(set(errors)), warnings


def main(argv):
    if not argv:
        print("Uso: python scripts/validate_brand_profile.py arquivo.json [outro.json ...]")
        return 2
    exit_code = 0
    seen = {}
    require_full = "--require-full" in argv
    filenames = [a for a in argv if a != "--require-full"]
    if not filenames:
        print("Informe ao menos um arquivo de perfil")
        return 2
    for filename in filenames:
        path = Path(filename)
        doc, errors, warnings = validate_profile(path, require_full=require_full)
        if isinstance(doc, dict):
            key = doc.get("brand_id")
            if isinstance(key, str) and key and key in seen:
                errors.append(f"brand_id repetido; ja usado em {seen[key]}")
            if isinstance(key, str) and key:
                seen[key] = path
        print(f"\n[{path}]")
        if errors:
            exit_code = 1
            print("INVALIDO")
            for error in errors:
                print("  ERRO:", error)
        else:
            print("VALIDO (schema completo)" if require_full else "VALIDO")
        for warn in warnings:
            print("  AVISO:", warn)
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
