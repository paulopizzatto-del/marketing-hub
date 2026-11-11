#!/usr/bin/env python3
"""Marketing Hub editorial pilot: offline prompt preparation, blinding, review analysis.

No model calls, no generated responses, no fabricated measurements. Python stdlib.
"""
from __future__ import annotations
import argparse
import csv
import html
import hashlib
import json
import math
import random
import re
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

CORE_TASKS = ("instagram", "linkedin", "newsletter", "landing", "cta", "email", "ad", "support", "crisis", "ux_microcopy")
STRESS_TASKS = ("ambiguous_brief", "conflicting_facts", "channel_shift", "high_risk_claim")
TASKS = CORE_TASKS + STRESS_TASKS
ARMS = ("A", "B", "C")
CONTRASTS = (("A", "C"), ("B", "C"), ("A", "B"))
BASELINE = """Você é um redator e estrategista experiente. Entregue uma peça específica, contextual e publicável. Use a voz das amostras sem copiar trechos. Preserve os fatos conhecidos, não invente números ou promessas, e atenda a intenção do leitor. Entregue somente a peça.\n"""
LENGTH = {
    "instagram": "Legendas: 100-180 palavras; respeitar instruções específicas de emojis e hashtags.",
    "linkedin": "Post: 130-220 palavras; voz e quebras apropriadas ao briefing.",
    "newsletter": "Mensagem: 220-350 palavras com linha de assunto e conteúdo útil.",
    "landing": "Landing page: seção principal, subtítulo, 3 blocos de benefícios fundamentados e CTA; cerca de 180-290 palavras.",
    "cta": "Um bloco de conversão: título, apoio, um CTA verificável; 35-75 palavras.",
    "email": "E-mail de relacionamento: assunto e corpo, 100-170 palavras.",
    "ad": "Anúncio: chamada, corpo e CTA; 35-75 palavras; sem alegações inventadas.",
    "support": "Resposta de atendimento: 45-85 palavras; privacidade e próximo passo.",
    "crisis": "Comunicado de crise: 90-160 palavras; não prometer fatos não confirmados.",
    "ux_microcopy": "Microcopy: rótulo, ajuda/erro e próximo passo; 25-90 palavras, sem criar comportamento fictício do sistema.",
    "ambiguous_brief": "Texto curto até 150 palavras; sinalizar lacuna factual sem inventar; caso de robustez.",
    "conflicting_facts": "Texto até 150 palavras; não assumir como verdade informações conflitantes; caso de robustez.",
    "channel_shift": "Adaptar ao canal descrito em até 150 palavras, mantendo fatos; caso de robustez.",
    "high_risk_claim": "Texto até 150 palavras; não atribuir resultados sem comprovação; caso de robustez."
}
SELECT_REFS = {
    "instagram": ("voice-lab.md", "copywriting.md"),
    "linkedin": ("voice-lab.md", "copywriting.md"),
    "newsletter": ("strategic-fit.md", "editorial-workflows.md"),
    "landing": ("strategic-fit.md", "editorial-workflows.md"),
    "cta": ("strategic-fit.md", "copywriting.md"),
    "email": ("human-context.md", "editorial-workflows.md"),
    "ad": ("evidence-and-claims.md", "editorial-workflows.md"),
    "support": ("human-context.md", "community-formats.md"),
    "crisis": ("human-context.md", "evidence-and-claims.md"),
    "ux_microcopy": ("ux-writing.md", "human-context.md"),
    "ambiguous_brief": ("strategic-fit.md", "evidence-and-claims.md"),
    "conflicting_facts": ("evidence-and-claims.md", "quality-assurance.md"),
    "channel_shift": ("editorial-workflows.md", "copywriting.md"),
    "high_risk_claim": ("evidence-and-claims.md", "quality-assurance.md"),
}
VALID_CHOICES = {"left", "right", "tie", "both_bad"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_id(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9][a-z0-9-]{1,32}", value or ""))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_brands(data, expected_brands=50):
    errs = []
    if not isinstance(data, dict) or not isinstance(data.get("brands"), list) or len(data["brands"]) != expected_brands:
        return [f"Esperadas {expected_brands} marcas neste estudo; ajuste --brand-count se necessário."]
    seen = set()
    for idx, b in enumerate(data["brands"], 1):
        prefix = f"marca {idx}"
        if not isinstance(b, dict):
            errs.append(f"{prefix}: objeto obrigatório")
            continue
        bid = b.get("brand_id")
        if not isinstance(bid, str) or not safe_id(bid) or bid in seen:
            errs.append(f"{prefix}: brand_id inválido/duplicado")
            continue
        seen.add(bid)
        for key, n in (("approved_samples", 3), ("held_out_references", 3)):
            items = b.get(key)
            if not isinstance(items, list) or len(items) != n or not all(isinstance(v, str) and len(v.strip()) >= 80 for v in items):
                errs.append(f"{bid}: {key} precisa de {n} textos reais de pelo menos 80 caracteres")
        a = b.get("approved_samples", [])
        h = b.get("held_out_references", [])
        if isinstance(a, list) and isinstance(h, list) and all(isinstance(v, str) for v in a+h):
            norm = [re.sub(r"\s+", " ", v.strip().casefold()) for v in a+h]
            if len(set(norm)) != len(norm):
                errs.append(f"{bid}: amostras ou referências retidas duplicadas; evite vazamento")
            card = b.get("voice_card", "")
            if isinstance(card,str) and any(x.strip() and x.strip() in card for x in h):
                errs.append(f"{bid}: cartão contém referência retida completa")
        if not isinstance(b.get("brand_brief"), str) or len(b["brand_brief"].strip()) < 40:
            errs.append(f"{bid}: briefing incompleto")
        if not isinstance(b.get("voice_card"), str) or len(b["voice_card"].strip()) < 80:
            errs.append(f"{bid}: cartão de voz obrigatório para comparar B e C; preparar apenas com as três amostras")
        tasks = b.get("tasks")
        if not isinstance(tasks, dict) or any(not isinstance(tasks.get(t), str) or len(tasks[t].strip()) < 25 for t in TASKS):
            errs.append(f"{bid}: fornecer 10 briefings principais e 4 de robustez")
        if not b.get("human_approved_by") or not b.get("human_approved_at"):
            errs.append(f"{bid}: aprovação humana/data ausentes")
        if b.get("permission_to_use") is not True:
            errs.append(f"{bid}: permission_to_use precisa ser true")
    return errs


def prompt_for(b, task, arm, skill_text, refs):
    parts = [BASELINE, f"ORÇAMENTO DE TAMANHO — {LENGTH[task]}",
             f"MARCA {b['brand_id']} — BRIEFING:\n{b['brand_brief']}",
             f"TAREFA {task}:\n{b['tasks'][task]}",
             "AMOSTRAS APROVADAS (usar como referência de voz; não copiar frases):"]
    parts.extend(f"AMOSTRA {i}:\n{s}" for i, s in enumerate(b["approved_samples"], 1))
    if arm in ("B", "C"):
        parts.append("CARTÃO DE VOZ (preparado antes do experimento, sem consultar textos retidos):\n" + b["voice_card"])
    if arm == "C":
        parts.append("INSTRUÇÕES ADICIONAIS DA SKILL MARKETING HUB v2.4.0:\n" + skill_text)
        for name in SELECT_REFS[task]:
            parts.append(f"REFERÊNCIA DA SKILL {name}:\n{refs[name]}")
    parts.append("ENTREGA: texto final apenas. Não diga qual condição foi usada.")
    return "\n\n---\n\n".join(parts).strip() + "\n"


def prepare(args):
    data = load_json(args.brands)
    errors = validate_brands(data, expected_brands=getattr(args, "brand_count", 50))
    if errors:
        raise ValueError("ENTRADAS INCOMPLETAS; nenhum prompt foi criado:\n" + "\n".join(errors))
    skill_root = args.skill_root
    skill_file = skill_root / "SKILL.md"
    skill_text = skill_file.read_text(encoding="utf-8")
    refs = {name: (skill_root / "references" / name).read_text(encoding="utf-8") for names in SELECT_REFS.values() for name in names}
    out = args.out
    if out.exists() and any(out.iterdir()):
        raise FileExistsError("Diretório de saída já contém dados. Use um novo para manter trilha imutável.")
    out.mkdir(parents=True, exist_ok=True)
    (out / "prompts").mkdir()
    (out / "responses").mkdir()
    randomizer = random.Random(args.seed)
    brands = sorted(data["brands"], key=lambda x: x["brand_id"])
    trials = []
    for b in brands:
        for task in TASKS:
            for rep in ((1, 2) if task in CORE_TASKS else (1,)):
                for arm in ARMS:
                    tid = f"{b['brand_id']}--{task}--r{rep}--{arm}"
                    p = out / "prompts" / (tid + ".txt")
                    p.write_text(prompt_for(b, task, arm, skill_text, refs), encoding="utf-8")
                    trials.append({"case_id": tid, "brand_id": b["brand_id"], "task": task,
                                   "repetition": rep, "arm": arm, "prompt_sha256": sha256(p.read_bytes()),
                                   "response_status": "not_run"})
    randomizer.shuffle(trials)
    snapshot = {"status": "NOT_RUN", "protocol_version": "50-1.0", "expected_brands": len(brands), "design": "A=baseline+brief+samples; B=A+fixed-card; C=B+Hub instructions",
                "generation_note": "Same exact model and parameters for A/B/C, fresh sessions, log real input/output tokens and costs; context input size may differ by condition.",
                "seed": args.seed, "provider": None, "model_version": None, "temperature": None, "generated_at": None,
                "skill_sha256": sha256(skill_file.read_bytes()),
                "references_sha256": {k: sha256(v.encode("utf-8")) for k, v in refs.items()},
                "brands_input_sha256": sha256(args.brands.read_bytes()),
                "planned_outputs": len(trials), "core_tasks": list(CORE_TASKS), "stress_tasks": list(STRESS_TASKS), "primary_contrast": "B vs C", "actual_outputs": 0, "trials": trials}
    write_json(out / "manifest.private.json", snapshot)
    # No raw reference texts in generation manifest; heldouts only in private review material.
    holdouts = {b["brand_id"]: {"references": b["held_out_references"], "brand_brief": b["brand_brief"],
                                "tasks": b["tasks"]} for b in brands}
    write_json(out / "heldouts.private.json", holdouts)
    snapshot["heldouts_sha256"] = sha256((out / "heldouts.private.json").read_bytes())
    write_json(out / "manifest.private.json", snapshot)
    write_json(out / "capture_metadata.private.json", {})
    print(f"GERADO: {len(trials)} prompts, 0 respostas reais. Saída privada: {out}")


def capture(args):
    exp = args.experiment
    mf = exp / "manifest.private.json"
    manifest = load_json(mf)
    cases = {x["case_id"]: x for x in manifest["trials"]}
    if args.case not in cases:
        raise ValueError("case_id desconhecido")
    text = args.text_file.read_text(encoding="utf-8").strip()
    if len(text) < 15:
        raise ValueError("Texto vazio/curto não é resposta válida; registre falha operacional à parte.")
    path = exp / "responses" / (args.case + ".txt")
    if path.exists():
        raise FileExistsError("A resposta já foi capturada; não substituir silenciosamente.")
    if not args.model or not args.provider or not args.date:
        raise ValueError("provider, model e date são necessários")
    try:
        parsed = datetime.fromisoformat(args.date.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("date deve seguir ISO8601 com timezone") from exc
    if parsed.tzinfo is None:
        raise ValueError("date deve ter timezone")
    if not (0 <= args.temperature <= 2):
        raise ValueError("temperature deve estar entre 0 e 2")
    for key, value in (("provider", args.provider), ("model_version", args.model), ("temperature", args.temperature)):
        if manifest.get(key) is not None and manifest[key] != value:
            raise ValueError(f"Condição experimental divergente: {key}. Use o mesmo modelo/parâmetros para todos os casos.")
    meta_path = exp / "capture_metadata.private.json"
    meta = load_json(meta_path)
    extra = {}
    for key in ("input_tokens", "output_tokens", "latency_ms", "cost_usd"):
        value = getattr(args, key, None)
        if value is not None:
            if not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise ValueError(f"Métrica de execução inválida: {key}")
            extra[key] = value
    path.write_text(text + "\n", encoding="utf-8")
    meta[args.case] = {"provider": args.provider, "model": args.model, "temperature": args.temperature,
                       "generation_date": args.date, "sha256": sha256(path.read_bytes()), "length_chars": len(text), **extra}
    write_json(meta_path, meta)
    manifest["provider"] = args.provider
    manifest["model_version"] = args.model
    manifest["temperature"] = args.temperature
    manifest["actual_outputs"] = len(meta)
    manifest["status"] = "PARTIAL_REAL_OUTPUTS" if len(meta) < len(cases) else "GENERATIONS_COMPLETE_REVIEW_PENDING"
    write_json(mf, manifest)
    print(f"Capturada {args.case}; total {len(meta)}/{len(cases)}")


def experiment_audit(experiment: Path, require_complete=False):
    """Check integrity of registered prompts/responses without claiming model authenticity."""
    mf = load_json(experiment / "manifest.private.json")
    meta = load_json(experiment / "capture_metadata.private.json")
    holdouts = load_json(experiment / "heldouts.private.json")
    problems = []
    if mf.get("heldouts_sha256") and sha256((experiment / "heldouts.private.json").read_bytes()) != mf["heldouts_sha256"]:
        problems.append("Referências retidas ou briefing de revisão alterados depois da preparação")
    trials = mf.get("trials", [])
    seen = set()
    if not isinstance(trials, list) or not trials:
        problems.append("Manifesto sem tarefas")
        trials = []
    expected = (len(CORE_TASKS)*2 + len(STRESS_TASKS))*len(ARMS)*mf.get("expected_brands", 50)
    if len(trials) != expected:
        problems.append(f"Tarefas: {len(trials)}; esperado {expected}")
    for t in trials:
        case = t.get("case_id", "")
        if not re.fullmatch(r"[a-z0-9-]{2,45}--[a-z_]+--r[12]--[ABC]", case):
            problems.append("case_id inválido")
            continue
        if case in seen:
            problems.append(f"case_id duplicado: {case}")
        seen.add(case)
        matches = re.fullmatch(r"(?P<brand>[a-z0-9-]+)--(?P<task>[a-z_]+)--r(?P<rep>[12])--(?P<arm>[ABC])", case)
        if (not matches or matches.group("task") not in TASKS or (matches.group("task") in STRESS_TASKS and matches.group("rep") != "1") or t.get("brand_id") != matches.group("brand") or
                t.get("task") != matches.group("task") or
                str(t.get("repetition")) != matches.group("rep") or
                t.get("arm") != matches.group("arm")):
            problems.append(f"Mapa de condição/tarefa do manifesto divergente: {case}")
        p = experiment / "prompts" / (case + ".txt")
        if not p.is_file() or sha256(p.read_bytes()) != t.get("prompt_sha256"):
            problems.append(f"Prompt ausente ou alterado: {case}")
            continue
        full = p.read_text(encoding="utf-8")
        card_marker = "CARTÃO DE VOZ (preparado antes do experimento"
        hub_marker = "INSTRUÇÕES ADICIONAIS DA SKILL MARKETING HUB"
        arm = t.get("arm")
        if (card_marker in full) != (arm in ("B","C")) or (hub_marker in full) != (arm == "C"):
            problems.append(f"Conteúdo de prompt incompatível com condição: {case}")
        for ref in holdouts.get(t.get("brand_id"), {}).get("references", []):
            if isinstance(ref, str) and ref.strip() and ref.strip() in full:
                problems.append(f"VAZAMENTO: referência retida no prompt {case}")
        if case in meta:
            response = experiment / "responses" / (case + ".txt")
            if not response.is_file() or sha256(response.read_bytes()) != meta[case].get("sha256"):
                problems.append(f"Resposta ausente ou alterada: {case}")
            if meta[case].get("model") != mf.get("model_version") or meta[case].get("provider") != mf.get("provider"):
                problems.append(f"Modelo/provedor inconsistente: {case}")
            if meta[case].get("temperature") != mf.get("temperature"):
                problems.append(f"Temperatura inconsistente: {case}")
            if response.is_file():
                raw = response.read_text(encoding="utf-8")
                if re.search(r"--r[12]--[ABC]\b|\b(?:condi[cç][aã]o|bra[cç]o)\s*[ABC]\b", raw, re.I):
                    problems.append(f"VAZAMENTO DE CEGAMENTO: identificador de braço no texto {case}")
    extra = set(meta) - seen
    if extra:
        problems.append(f"Metadados de casos desconhecidos: {len(extra)}")
    raw_files = {x.stem for x in (experiment / "responses").glob("*.txt")}
    if raw_files != set(meta):
        problems.append("Arquivos de resposta e metadados não correspondem")
    if mf.get("actual_outputs") != len(meta):
        problems.append("Contagem de respostas do manifesto não coincide")
    missing = sorted(seen - set(meta))
    if require_complete and missing:
        problems.append(f"Faltam {len(missing)} saídas reais; primeira: {missing[0]}")
    return {"status": "INTEGRITY_OK" if not problems else "FAILED", "problems": problems,
            "expected": len(trials), "captured": len(meta), "missing_count": len(missing),
            "missing_first": missing[0] if missing else None,
            "provider": mf.get("provider"), "model_version": mf.get("model_version"),
            "note": "Checks hashes/consistency only; cannot authenticate a model or human evaluator."}


def status(args):
    report = experiment_audit(args.experiment)
    if args.out:
        write_json(args.out, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["status"] != "INTEGRITY_OK":
        raise ValueError("Integridade reprovada. Revise detalhes acima.")


def capture_batch(args):
    """Import externally generated responses with a per-case declared metadata ledger.

    Prevalidate all entries before writing. Never call models or choose the best response.
    """
    data = load_json(args.ledger)
    entries = data.get('entries') if isinstance(data, dict) else None
    if not isinstance(entries, list) or not entries:
        raise ValueError('Ledger JSON precisa de entries não vazio')
    mf = load_json(args.experiment / 'manifest.private.json')
    known = {t['case_id']: t for t in mf['trials']}
    captured = load_json(args.experiment / 'capture_metadata.private.json')
    found = set()
    preflight = []
    first_provider = mf.get('provider')
    first_model = mf.get('model_version')
    first_temp = mf.get('temperature')
    root = args.ledger.parent.resolve()
    for item in entries:
        if not isinstance(item, dict):
            raise ValueError('Ledger contém item não objeto')
        case = item.get('case_id')
        if case not in known or case in found or case in captured:
            raise ValueError(f'Ledger contém caso desconhecido, duplicado ou já capturado: {case}')
        found.add(case)
        rel = item.get('response_file', '')
        if not isinstance(rel,str) or not rel.endswith('.txt'):
            raise ValueError(f'Arquivo .txt obrigatório: {case}')
        source = (root / rel).resolve()
        if not source.is_relative_to(root) or not source.is_file():
            raise ValueError(f'Arquivo fora da pasta do ledger ou ausente: {case}')
        text = source.read_text(encoding='utf-8').strip()
        if len(text) < 15:
            raise ValueError(f'Resposta vazia/curta: {case}')
        if re.search(r"--r[12]--[ABC]\b|\b(?:condi[cç][aã]o|bra[cç]o)\s*[ABC]\b", text, re.I):
            raise ValueError(f'Texto contém rótulo que quebra cegamento: {case}')
        if item.get('prompt_sha256') and item['prompt_sha256'] != known[case]['prompt_sha256']:
            raise ValueError(f'Hash do prompt não confere: {case}')
        try:
            stamp = datetime.fromisoformat(item.get('date','').replace('Z','+00:00'))
        except (ValueError, AttributeError) as ex:
            raise ValueError(f'Data inválida: {case}') from ex
        if stamp.tzinfo is None:
            raise ValueError(f'Data sem timezone: {case}')
        provider, model, temp = item.get('provider'), item.get('model'), item.get('temperature')
        if not isinstance(provider,str) or not provider.strip() or not isinstance(model,str) or not model.strip():
            raise ValueError(f'Provedor/modelo obrigatórios: {case}')
        if not isinstance(temp,(float,int)) or not 0 <= temp <= 2:
            raise ValueError(f'Temperatura inválida: {case}')
        if first_provider is not None and first_provider != provider or first_model is not None and first_model != model or first_temp is not None and first_temp != temp:
            raise ValueError(f'Modelo ou parâmetros divergentes dentro do lote: {case}')
        first_provider, first_model, first_temp = provider, model, temp
        for metric in ('input_tokens', 'output_tokens', 'latency_ms', 'cost_usd'):
            if metric in item and (not isinstance(item[metric],(int,float)) or
                                   not math.isfinite(item[metric]) or item[metric] < 0):
                raise ValueError(f'Métrica inválida em lote ({metric}): {case}')
        preflight.append((case, source, item))
    # All data validated: one immutable, recorded response per ledger entry.
    for case,source,item in preflight:
        capture(argparse.Namespace(experiment=args.experiment,case=case,text_file=source,
                provider=item['provider'],model=item['model'],date=item['date'],temperature=item['temperature'],
                input_tokens=item.get('input_tokens'),output_tokens=item.get('output_tokens'),
                latency_ms=item.get('latency_ms'),cost_usd=item.get('cost_usd')))
    audit = experiment_audit(args.experiment)
    if audit['problems']:
        raise ValueError('Lote gravado, mas auditoria detectou inconsistências: '+'; '.join(audit['problems'][:3]))
    print(f'IMPORTADO: {len(preflight)} respostas declaradas, integridade verificada. Não autentica origem de modelo.')


def build_blind(args):
    exp = args.experiment
    check = experiment_audit(exp, require_complete=True)
    if check["problems"]:
        raise ValueError("Pares cegos recusados: " + "; ".join(check["problems"][:5]))
    manifest = load_json(exp / "manifest.private.json")
    meta = load_json(exp / "capture_metadata.private.json")
    trials = manifest["trials"]
    missing = [t["case_id"] for t in trials if t["case_id"] not in meta or not (exp / "responses" / (t["case_id"] + ".txt")).is_file()]
    if missing:
        raise ValueError(f"Faltam {len(missing)} saídas reais; avaliação não criada. Primeira: {missing[0]}")
    if args.out.exists():
        raise FileExistsError("Pasta de avaliação já existe; não regenerar IDs cegos depois de receber votos")
    args.out.mkdir(parents=True)
    by_key = {(x["brand_id"], x["task"], x["repetition"], x["arm"]): x["case_id"] for x in trials}
    hold = load_json(exp / "heldouts.private.json")
    assignments = []
    rng = random.Random(args.seed)
    for brand in sorted(hold):
        for task in CORE_TASKS:
            for rep in (1, 2):
                for left_arm, right_arm in CONTRASTS:
                    pair_key = f"{brand}/{task}/r{rep}/{left_arm}{right_arm}"
                    assignments.append((pair_key, brand, task, rep, left_arm, right_arm))
    rng.shuffle(assignments)
    secret = {}
    reviewer_checksums = {}
    for rid in ("R1", "R2"):
        rd = args.out / rid
        (rd / "pairs").mkdir(parents=True)
        judgments = []
        reviewer_cases = []
        for i, (pk, brand, task, rep, arm1, arm2) in enumerate(assignments):
            # Alternate orientations across reviewers; makes positional effect identifiable.
            flipped = bool((i % 2) ^ (rid == "R2"))
            left, right = (arm2, arm1) if flipped else (arm1, arm2)
            lid = by_key[brand, task, rep, left]
            rid_case = by_key[brand, task, rep, right]
            opaque = sha256((str(args.seed) + pk).encode("utf-8"))[:12]
            pair_id = "pair-" + opaque
            secret.setdefault(pair_id, {"brand": brand, "task": task, "repetition": rep,
                                        "comparison": arm1 + arm2, "arms": {}})
            secret[pair_id]["arms"][rid] = {"left": left, "right": right, "left_case": lid, "right_case": rid_case}
            ref_lines = [f"# Caso {pair_id}", f"Tarefa: {task}", f"Briefing da marca: {hold[brand]['brand_brief']}", f"Briefing da tarefa: {hold[brand]['tasks'][task]}",
                         "## Referências de voz retidas — nunca mostradas ao gerador"]
            ref_lines.extend(f"Referência {j}:\n{v}" for j, v in enumerate(hold[brand]["references"], 1))
            ref_lines.extend(["## Opção esquerda", (exp / "responses" / (lid + ".txt")).read_text(encoding="utf-8"),
                              "## Opção direita", (exp / "responses" / (rid_case + ".txt")).read_text(encoding="utf-8")])
            pair_path = rd / "pairs" / (pair_id + ".md")
            pair_path.write_text("\n\n".join(ref_lines), encoding="utf-8")
            secret[pair_id]["arms"][rid]["pair_sha256"] = sha256(pair_path.read_bytes())
            reviewer_cases.append({"pair_id": pair_id, "task": task,
                                   "brief": hold[brand]["brand_brief"], "task_brief": hold[brand]["tasks"][task],
                                   "references": hold[brand]["references"],
                                   "left": (exp / "responses" / (lid + ".txt")).read_text(encoding="utf-8"),
                                   "right": (exp / "responses" / (rid_case + ".txt")).read_text(encoding="utf-8")})
            judgments.append({"pair_id": pair_id, "reviewer_id": rid, "choice": "", "notes": ""})
        write_json(rd / "reviewer_cases.json", {"reviewer_id": rid, "cases": reviewer_cases,
                                                  "note": "Only opaque identifiers, no arm mapping; keep private."})
        reviewer_checksums[rid] = sha256((rd / "reviewer_cases.json").read_bytes())
        with (rd / "judgments.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["pair_id", "reviewer_id", "choice", "notes"])
            w.writeheader(); w.writerows(judgments)
    # Never put the key inside reviewer folders.
    write_json(args.out / "answers_DO_NOT_SHARE_WITH_REVIEWERS.json", secret)
    write_json(args.out / "reviewer_inputs_sha256.json", reviewer_checksums)
    print(f"Pares cegos gerados: {len(assignments)} × 2 avaliadores; 0 julgamentos coletados.")


def exact_sign_p(better: int, worse: int):
    n = better + worse
    if n == 0:
        return None
    return sum(math.comb(n, i) for i in range(better, n + 1)) / (2 ** n)


def analyze(args):
    blind = args.blind
    key = load_json(blind / "answers_DO_NOT_SHARE_WITH_REVIEWERS.json")
    checkfile = blind / "reviewer_inputs_sha256.json"
    if checkfile.exists():
        for rid, expected_hash in load_json(checkfile).items():
            checkpath = blind / rid / "reviewer_cases.json"
            if not checkpath.is_file() or sha256(checkpath.read_bytes()) != expected_hash:
                raise ValueError(f"Material do revisor foi alterado: {rid}")
    for pair_id, entry in key.items():
        for rid, mapping in entry["arms"].items():
            path = blind / rid / "pairs" / (pair_id + ".md")
            if "pair_sha256" in mapping and (not path.is_file() or sha256(path.read_bytes()) != mapping["pair_sha256"]):
                raise ValueError(f"Pareamento cego alterado após a criação: {pair_id} / {rid}")
    all_votes = []
    for rid in ("R1", "R2"):
        with (blind / rid / "judgments.csv").open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        if len(rows) != len(key) or {r["pair_id"] for r in rows} != set(key):
            raise ValueError(f"{rid}: julgamento incompleto ou IDs duplicados")
        for row in rows:
            choice = row["choice"].strip()
            if choice not in VALID_CHOICES or row["reviewer_id"] != rid:
                raise ValueError(f"{rid}: voto vazio/inválido para {row['pair_id']}")
            k = key[row["pair_id"]]
            arm_map = k["arms"][rid]
            winner = arm_map[choice] if choice in {"left", "right"} else choice
            all_votes.append({"reviewer": rid, "pair_id": row["pair_id"], "brand": k["brand"],
                              "comparison": k["comparison"], "winner": winner})
    by_comparison = {}
    for contrast in CONTRASTS:
        comp = "".join(contrast)
        rows = [x for x in all_votes if x["comparison"] == comp]
        counts = {contrast[0]: 0, contrast[1]: 0, "tie": 0, "both_bad": 0}
        brand_votes = defaultdict(lambda: {contrast[0]: 0, contrast[1]: 0, "tie": 0, "both_bad": 0})
        for x in rows:
            counts[x["winner"]] += 1
            brand_votes[x["brand"]][x["winner"]] += 1
        better = contrast[1]
        worse = contrast[0]
        decisive = counts[better] + counts[worse]
        signs = {"better": 0, "worse": 0, "tie": 0}
        for b, ct in brand_votes.items():
            signs["better" if ct[better] > ct[worse] else "worse" if ct[worse] > ct[better] else "tie"] += 1
        by_task = {}
        for task in CORE_TASKS:
            subset = [x for x in rows if key[x["pair_id"]]["task"] == task]
            tc = {contrast[0]: 0, contrast[1]: 0, "tie": 0, "both_bad": 0}
            for x in subset:
                tc[x["winner"]] += 1
            dec = tc[better] + tc[worse]
            by_task[task] = {"counts": tc, "favor_second_excluding_ties": tc[better] / dec if dec else None}
        by_reviewer = {}
        for rid in ("R1", "R2"):
            rc = {contrast[0]: 0, contrast[1]: 0, "tie": 0, "both_bad": 0}
            for x in rows:
                if x["reviewer"] == rid:
                    rc[x["winner"]] += 1
            dec = rc[better] + rc[worse]
            by_reviewer[rid] = {"counts": rc, "favor_second_excluding_ties": rc[better]/dec if dec else None}
        by_comparison[comp] = {
            "counts": counts,
            "favor_second_excluding_ties": (counts[better] / decisive if decisive else None),
            "tie_rate": (counts["tie"] + counts["both_bad"]) / sum(counts.values()),
            "brand_direction": signs,
            "one_sided_exact_brand_sign_p": exact_sign_p(signs["better"], signs["worse"]),
            "per_brand": dict(brand_votes), "per_task": by_task, "per_reviewer": by_reviewer,
            "interpretation": "EXPLORATORY SUMMARY; hierarchical modeling/preregistration and independent audit needed before any superiority claim"
        }
    paired = defaultdict(dict)
    for x in all_votes:
        paired[x["pair_id"]][x["reviewer"]] = x["winner"]
    agreement = sum(1 for x in paired.values() if x["R1"] == x["R2"]) / len(paired) if paired else None
    # Cohen kappa calculated over generic comparable labels first/second/tie/both_bad, not raw A/B/C.
    agreement_by_comparison = {}
    for a1, a2 in CONTRASTS:
        comp = a1 + a2
        cases = [entry for pid, entry in key.items() if entry["comparison"] == comp]
        votes = [paired[pid] for pid, entry in key.items() if entry["comparison"] == comp]
        if not cases:
            continue
        labels = (a1, a2, "tie", "both_bad")
        observed = sum(v["R1"] == v["R2"] for v in votes)/len(votes)
        counts = {rid: {k: sum(v[rid] == k for v in votes) for k in labels} for rid in ("R1","R2")}
        expected = sum(counts["R1"][k] * counts["R2"][k] for k in labels)/(len(votes)**2)
        kappa = (observed-expected)/(1-expected) if expected < 1 else None
        agreement_by_comparison[comp] = {"raw_agreement": observed, "cohen_kappa": kappa,
                                         "note": "Agreement can be unstable with prevalent outcomes/ties."}
    pool_path = blind / 'reviewer_pool.private.json'
    pool = load_json(pool_path) if pool_path.exists() else None
    out = {"status": "REAL_REVIEW_RECORDS_PRESENT_NOT_INDEPENDENTLY_AUTHENTICATED",
           "n_reviewers_declared": pool.get('n_workers_declared',2) if pool else 2,
           "reviewer_slot_note": "R1/R2 are vote slots. When sharding is used, they are NOT individual human reviewers.", "n_pairs": len(key), "n_votes": len(all_votes),
           "reviewer_agreement_raw": agreement, "reviewer_agreement_by_contrast": agreement_by_comparison,
           "contrasts": by_comparison,
           "limits": ["The reviewer identity and sample origin are user-declared, not authenticated.",
                      "Brands, not votes, are the primary units of generalization. No claim of 50 independent randomized consumer populations.",
                      "Pilot assesses preference, not marketing ROI, conversion or guaranteed model superiority.",
                      "Do not publish any brand text without authorisation and de-identification."]}
    if args.out.exists():
        raise FileExistsError("Análise já existe; preserve a versão original dos votos")
    write_json(args.out, out)
    print(f"Analise descritiva escrita em {args.out}; não é certificação de superioridade.")


def template(args):
    if args.out.exists():
        raise FileExistsError("Modelo de entrada já existe; preserve dados do usuário")
    sectors = ["finanças/seguros", "saúde/bem-estar", "alimentos/hospitalidade",
               "varejo/e-commerce", "tecnologia B2B", "educação/serviços profissionais",
               "turismo/cultura", "organizações sociais", "serviços locais",
               "lifestyle/moda/beleza"]
    brands = []
    for i in range(args.brand_count):
        brands.append({"brand_id": f"brand-{i+1:03}", "sector": sectors[i // 5] if args.brand_count == 50 else sectors[i % len(sectors)], "market": "", "company_size": "", "risk_band": "", "locale": "", "consent_reference": "", "brand_brief": "",
                       "approved_samples": ["", "", ""], "held_out_references": ["", "", ""],
                       "voice_card": "", "human_approved_by": "", "human_approved_at": "",
                       "permission_to_use": False,
                       "tasks": {k: "" for k in TASKS}})
    write_json(args.out, {"status": "REQUIRES_HUMAN_APPROVED_INPUTS", "brands": brands})
    print(f"Modelo vazio de {args.brand_count} marcas criado: {args.out}")


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("template", help="Create blank intake for 10-brand pre-pilot or 50-brand study")
    a.add_argument("--brand-count", type=int, choices=(10,50), default=50)
    a.add_argument("--out", type=Path, required=True)
    a.set_defaults(func=template)
    a = sub.add_parser("prepare", help="Prepare 720 or 3600 prompts, never call models")
    a.add_argument("--brands", type=Path, required=True)
    a.add_argument("--skill-root", type=Path, required=True)
    a.add_argument("--out", type=Path, required=True)
    a.add_argument("--seed", type=int, default=4321)
    a.add_argument("--brand-count", type=int, choices=(10,50), default=50, help="Pré-piloto=10; estudo principal=50 marcas")
    a.set_defaults(func=prepare)
    a = sub.add_parser("capture-batch", help="Import responses from external JSON ledger after full prevalidation")
    a.add_argument("--experiment", type=Path, required=True)
    a.add_argument("--ledger", type=Path, required=True)
    a.set_defaults(func=capture_batch)
    a = sub.add_parser("status", help="Check prompt/response integrity and progress")
    a.add_argument("--experiment", type=Path, required=True)
    a.add_argument("--out", type=Path)
    a.set_defaults(func=status)
    a = sub.add_parser("capture", help="Register one actual model response")
    a.add_argument("--experiment", type=Path, required=True)
    a.add_argument("--case", required=True)
    a.add_argument("--text-file", type=Path, required=True)
    a.add_argument("--provider", required=True)
    a.add_argument("--model", required=True)
    a.add_argument("--date", required=True, help="ISO8601 model generation date")
    a.add_argument("--temperature", type=float, required=True, help="Mesma temperatura de geração para todas as condições")
    a.add_argument("--input-tokens", type=int)
    a.add_argument("--output-tokens", type=int)
    a.add_argument("--latency-ms", type=float)
    a.add_argument("--cost-usd", type=float)
    a.set_defaults(func=capture)
    a = sub.add_parser("blind", help="Prepare two independent blind reviewer sets")
    a.add_argument("--experiment", type=Path, required=True)
    a.add_argument("--out", type=Path, required=True)
    a.add_argument("--seed", type=int, default=9876)
    a.set_defaults(func=build_blind)
    a = sub.add_parser("analyze", help="Analyze complete human votes, refuse missing")
    a.add_argument("--blind", type=Path, required=True)
    a.add_argument("--out", type=Path, required=True)
    a.set_defaults(func=analyze)
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        args.func(args)
    except (ValueError, FileNotFoundError, FileExistsError, json.JSONDecodeError) as e:
        print(f"ERRO: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
