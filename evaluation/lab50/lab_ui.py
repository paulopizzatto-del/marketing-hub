#!/usr/bin/env python3
"""Offline interfaces for reviewer voting, operator status and exploratory results.

Never sends data over the network; all generated HTML must stay inside private/.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

import lab

STYLE = """
:root{--pink:#ff4f8b;--pink2:#b31a55;--ink:#2b1720;--muted:#71616a;--paper:#fff8fb;--line:#f0d5e1;--surface:#fff;--ok:#168a66}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 system-ui,-apple-system,Segoe UI,Arial,sans-serif}
header{background:var(--ink);color:#fff;padding:22px max(20px,calc((100vw - 1140px)/2));border-bottom:5px solid var(--pink)}
header .brand{font-size:19px;font-weight:900;letter-spacing:-.035em}header .brand b{color:#ff82ac}header .sub{color:#f1cfdc;font-size:13px;margin-top:4px}
main{max-width:1140px;margin:auto;padding:28px 20px 58px}.eyebrow{color:var(--pink2);font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:800}
h1{font-size:clamp(26px,4vw,38px);letter-spacing:-.04em;line-height:1.1;margin:8px 0 14px}
.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px;box-shadow:0 7px 25px #49233109}
.row{display:flex;gap:16px;align-items:center;flex-wrap:wrap}.top{display:flex;justify-content:space-between;gap:14px;align-items:center;flex-wrap:wrap}
.small,.hint{font-size:13px;color:var(--muted)}.warning{padding:12px 15px;border:1px solid #ecbfcc;border-radius:12px;background:#fff1f6;color:#653043}
.pill{padding:5px 11px;border-radius:20px;background:#ffe8f0;color:#86234a;font-weight:700;font-size:12px}
.btn{cursor:pointer;border:1px solid var(--line);border-radius:11px;background:#fff;color:var(--ink);padding:11px 15px;font-weight:700;min-height:43px}
.btn:hover{background:#fff1f6}.btn:focus-visible,input:focus-visible,textarea:focus-visible{outline:3px solid var(--pink);outline-offset:3px}
.btn.primary{background:var(--ink);border-color:var(--ink);color:#fff}.btn.primary:hover{background:#512b3d}
.btn:disabled{opacity:.5;cursor:not-allowed}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
article h3{font-size:15px;margin:0 0 12px}.example{white-space:pre-wrap;overflow-wrap:anywhere;font-size:15px;line-height:1.65;max-height:340px;overflow:auto}
.reference{background:#fbf4f7;border-left:3px solid var(--pink);padding:14px 16px;margin:12px 0;border-radius:0 10px 10px 0;white-space:pre-wrap;overflow-wrap:anywhere}
nav.actions{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}nav.actions .btn{flex:1 1 160px}
textarea{width:100%;min-height:80px;resize:vertical;padding:13px;border:1px solid var(--line);border-radius:12px;font:inherit}
.progress{height:10px;background:#efd9e2;border-radius:99px;overflow:hidden}.progress>div{height:100%;background:var(--pink);width:0;transition:width .18s}
.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin:20px 0}.metric{background:white;border:1px solid var(--line);padding:18px;border-radius:15px}.metric strong{font-size:27px;display:block;letter-spacing:-.04em}
@media(max-width:780px){.grid,.metrics{grid-template-columns:1fr}main{padding:20px 15px}.card{padding:17px}header{padding:17px 18px}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
"""


def safe_json(obj):
    # Prevent untrusted model output from closing a script block.
    return (json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
            .replace("<", "\\u003c").replace(">", "\\u003e")
            .replace("&", "\\u0026").replace("\\u2028", "\\\\u2028"))


def frame(title, body, extra_script=""):
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="referrer" content="no-referrer"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; form-action 'none'"><title>{html.escape(title)}</title><style>{STYLE}</style></head><body><header><div class="brand">marketing <b>hub.</b></div><div class="sub">Laboratório editorial independente · acesso local</div></header><main>{body}</main>{extra_script}</body></html>'''


def make_reviewer(blind: Path):
    written = []
    for reviewer in ("R1", "R2"):
        loc = blind / reviewer
        source = loc / "reviewer_cases.json"
        data = lab.load_json(source)
        if data.get("reviewer_id") != reviewer or not data.get("cases"):
            raise ValueError("Pasta de avaliação inválida ou incompleta")
        ids = [x["pair_id"] for x in data["cases"]]
        if len(ids) != len(set(ids)):
            raise ValueError("ID de par repetido")
        raw = safe_json(data)
        body = f'''<div class="top"><div><div class="eyebrow">Revisão às cegas · {reviewer}</div><h1>Qual texto parece mais com a marca?</h1></div><span class="pill" id="counter">0 de {len(ids)}</span></div>
<div class="warning">Este arquivo contém material privado de marcas. Não publique, não abra em serviços externos. O avaliador não recebe a chave das condições. Exporte o CSV de votos ao terminar.</div>
<section class="card" style="margin-top:18px"><div class="top"><strong id="case-title"></strong><span id="task" class="pill"></span></div><p id="brief"></p><p id="task-brief" class="small"></p><h3>Referências de voz reservadas</h3><div id="references"></div><div class="progress" aria-label="Progresso dos votos"><div id="bar"></div></div></section>
<section class="grid" style="margin-top:17px"><article class="card"><h3>Texto da esquerda</h3><div id="left" class="example"></div></article><article class="card"><h3>Texto da direita</h3><div id="right" class="example"></div></article></section>
<nav class="actions" aria-label="Escolha qual texto é melhor"><button class="btn" data-choice="left">Prefiro esquerda (1)</button><button class="btn" data-choice="right">Prefiro direita (2)</button><button class="btn" data-choice="tie">Sem diferença (3)</button><button class="btn" data-choice="both_bad">Ambos ruins (4)</button></nav>
<div class="card"><label for="notes"><b>Observações (opcional)</b></label><textarea id="notes" maxlength="2000" placeholder="Por quê? O que soou genérico ou saiu da voz da marca?"></textarea><div class="top" style="margin-top:12px"><div class="row"><button id="prev" class="btn">Anterior</button><button id="next" class="btn">Próximo</button><button id="unanswered" class="btn">Ir para pendente</button></div><button id="export" class="btn primary">Exportar judgments.csv</button></div><p class="hint">Atalhos: 1/2/3/4 para escolher; setas para navegar. Os votos são guardados localmente no navegador; o CSV é o registro que deve ser preservado. Não use o botão Exportar para compartilhar textos.</p></div>
<script id="lab-data" type="application/json">{raw}</script>'''
        script = r'''<script>
'use strict';
const D=JSON.parse(document.getElementById('lab-data').textContent);const rows=D.cases;
const key='mh-lab-v2-'+D.reviewer_id+'-'+rows.length+'-'+rows[0].pair_id;
let votes={};try{votes=JSON.parse(localStorage.getItem(key)||'{}')}catch(_){votes={}}
let i=0;const get=id=>document.getElementById(id);
function save(){try{localStorage.setItem(key,JSON.stringify(votes))}catch(_){}}
function render(){let c=rows[i],v=votes[c.pair_id]||{};
get('case-title').textContent='Comparação '+(i+1)+' / '+rows.length+' · '+c.pair_id;
get('task').textContent=c.task;get('brief').textContent=c.brief;get('task-brief').textContent=c.task_brief;
const r=get('references');r.replaceChildren();for(let j=0;j<c.references.length;j++){let e=document.createElement('div');e.className='reference';e.textContent='Referência '+(j+1)+': '+c.references[j];r.append(e)}
get('left').textContent=c.left;get('right').textContent=c.right;get('notes').value=v.notes||'';
let done=rows.filter(x=>votes[x.pair_id]&&votes[x.pair_id].choice).length;
get('counter').textContent=done+' / '+rows.length+' votados';get('bar').style.width=100*done/rows.length+'%';
document.querySelectorAll('[data-choice]').forEach(b=>{b.setAttribute('aria-pressed',String(b.dataset.choice===v.choice));b.style.borderColor=b.dataset.choice===v.choice?'#ff4f8b':'var(--line)'})
get('prev').disabled=i===0;get('next').disabled=i===rows.length-1;}
function vote(choice){let c=rows[i];votes[c.pair_id]={choice,notes:get('notes').value};save();render();if(i<rows.length-1){i++;render()}}
document.querySelectorAll('[data-choice]').forEach(b=>b.onclick=()=>vote(b.dataset.choice));
get('notes').oninput=()=>{let id=rows[i].pair_id;votes[id]={...(votes[id]||{}),notes:get('notes').value};save()};
get('prev').onclick=()=>{if(i>0)i--;render()};get('next').onclick=()=>{if(i<rows.length-1)i++;render()};
get('unanswered').onclick=()=>{let j=rows.findIndex(x=>!(votes[x.pair_id]&&votes[x.pair_id].choice));if(j>=0){i=j;render()}else alert('Todos os pares já têm uma escolha. Exporte o CSV.')};
function clean(t){t=String(t||'');if(/^[=+@\-\t\r]/.test(t))t="'"+t;return '"'+t.replaceAll('"','""')+'"'}
get('export').onclick=()=>{let all=rows.every(c=>votes[c.pair_id]&&votes[c.pair_id].choice);if(!all&&!confirm('Ainda há pares sem voto. Deseja exportar um CSV parcial?'))return;
let csv='pair_id,reviewer_id,choice,notes\r\n'+rows.map(c=>[c.pair_id,D.reviewer_id,(votes[c.pair_id]||{}).choice||'',(votes[c.pair_id]||{}).notes||''].map(clean).join(',')).join('\r\n')+'\r\n';
let blob=new Blob(['\ufeff'+csv],{type:'text/csv;charset=utf-8'});let url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='judgments-'+D.reviewer_id+'.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};
document.addEventListener('keydown',e=>{if(['TEXTAREA','INPUT'].includes(e.target.tagName))return;if(['1','2','3','4'].includes(e.key)){let choices=['left','right','tie','both_bad'];vote(choices[Number(e.key)-1])}else if(e.key==='ArrowLeft'){get('prev').click()}else if(e.key==='ArrowRight'){get('next').click()}});
render();
</script>'''
        page = frame("Marketing Hub — revisão cega " + reviewer, body, script)
        out = loc / "review.html"
        out.write_text(page, encoding="utf-8")
        written.append(out)
    return written


def build_dashboard(experiment: Path, out: Path):
    audit = lab.experiment_audit(experiment)
    mf = lab.load_json(experiment / 'manifest.private.json')
    captured = audit['captured']
    total = audit['expected']
    meta = lab.load_json(experiment / 'capture_metadata.private.json')
    by_task = {t:{'planned':0,'captured':0} for t in lab.TASKS}
    by_arm = {a:{'planned':0,'captured':0} for a in lab.ARMS}
    for t in mf['trials']:
        by_task[t['task']]['planned']+=1;by_arm[t['arm']]['planned']+=1
        if t['case_id'] in meta:
            by_task[t['task']]['captured']+=1;by_arm[t['arm']]['captured']+=1
    cards = f'''<div class="eyebrow">Painel do operador · privado</div><h1>Progresso das gerações</h1><div class="warning">Painel de execução — não é medição de desempenho. Nenhum julgamento editorial aparece antes da avaliação cega.</div><div class="metrics"><div class="metric"><span class="small">Prompts preparados</span><strong>{total}</strong></div><div class="metric"><span class="small">Saídas registradas</span><strong>{captured}</strong></div><div class="metric"><span class="small">Faltando</span><strong>{audit['missing_count']}</strong></div></div><div class="card"><b>Captura</b><div class="progress" style="margin-top:12px"><div style="width:{100*captured/total if total else 0:.1f}%"></div></div><p class="small">Modelo: {html.escape(str(audit['model_version'] or 'ainda não registrado'))}; provedor: {html.escape(str(audit['provider'] or 'ainda não registrado'))}</p><p>Integridade: <b>{html.escape(audit['status'])}</b></p></div>'''
    for heading, values in (("Por tarefa",by_task),("Por condição (somente operador)",by_arm)):
        cards += '<h2>'+html.escape(heading)+'</h2><div class="metrics">'
        for label, counts in values.items():
            cards += f'<div class="metric"><span class="small">{html.escape(label)}</span><strong>{counts["captured"]}/{counts["planned"]}</strong></div>'
        cards += '</div>'
    if audit['problems']:
        cards += '<div class="warning"><b>Falhas de integridade:</b><ul>'+''.join(f'<li>{html.escape(p)}</li>' for p in audit['problems'])+'</ul></div>'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(frame('Marketing Hub — acompanhamento', cards),encoding='utf-8')
    return out


def build_results(analysis: Path, out: Path):
    data = lab.load_json(analysis)
    if data.get('status') != 'REAL_REVIEW_RECORDS_PRESENT_NOT_INDEPENDENTLY_AUTHENTICATED' or not data.get('contrasts'):
        raise ValueError('Relatório exige análise completa de respostas e votos registrados')
    body = '''<div class="eyebrow">Resultados exploratórios · leitura restrita</div><h1>Resultados do piloto editorial</h1><div class="warning"><b>Não é comprovação de superioridade.</b> As avaliações foram fornecidas externamente; a identidade dos revisores e a origem das respostas não foram autenticadas. Não publique dados privados sem autorização.</div>'''
    body += f'''<div class="metrics"><div class="metric"><span class="small">Pares cegos</span><strong>{data['n_pairs']}</strong></div><div class="metric"><span class="small">Votos registrados</span><strong>{data['n_votes']}</strong></div><div class="metric"><span class="small">Concordância bruta</span><strong>{data['reviewer_agreement_raw']:.1%}</strong></div></div>'''
    descriptions = {"AC":"IA competente × Hub completo", "BC":"Cartão de voz × Hub completo", "AB":"IA competente × cartão de voz"}
    for comp in ('AC','BC','AB'):
        row = data['contrasts'][comp]
        val = row['favor_second_excluding_ties']
        p = row['one_sided_exact_brand_sign_p']
        body += f'<section class="card" style="margin-top:20px"><div class="eyebrow">Comparação {comp}</div><h2>{descriptions[comp]}</h2><p class="small">Preferência pela segunda condição, excluindo empates e "ambos ruins"</p>'
        if val is None:
            body += '<p>Sem comparações decisivas</p>'
        else:
            body += f'<strong style="font-size:34px">{val:.1%}</strong><div class="progress"><div style="width:{val*100:.1f}%"></div></div>'
        body += f'<p class="small">Empates + ambos ruins: {row["tie_rate"]:.1%}; marcas favoráveis à segunda: {row["brand_direction"]["better"]}, à primeira: {row["brand_direction"]["worse"]}, sem direção: {row["brand_direction"]["tie"]}. Teste exato por marcas (exploratório): {p if p is not None else "não aplicável"}.</p>'
        body += '<h3>Por tarefa</h3><div class="grid">'
        for task, d in row.get('per_task',{}).items():
            v=d['favor_second_excluding_ties']
            body += f'<div><span class="pill">{html.escape(task)}</span> <strong>{f"{v:.1%}" if v is not None else "sem decisão"}</strong><p class="small">{sum(d["counts"].values())} votos brutos</p></div>'
        body += '</div><h3>Por avaliador</h3><div class="grid">'
        for reviewer, d in row.get('per_reviewer',{}).items():
            v=d['favor_second_excluding_ties']
            body += f'<div>{html.escape(reviewer)}: <strong>{f"{v:.1%}" if v is not None else "sem decisão"}</strong></div>'
        body += '</div></section>'
    body += '<p class="hint">As saídas do mesmo modelo, marca e tarefa não são independentes. A análise não mede conversão, ROI ou ganhos comerciais. Comparações não são evidência confirmatória.</p>'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(frame('Marketing Hub — resultados exploratórios',body),encoding='utf-8')
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('review-ui',help='Create reviewer-specific offline voting pages')
    a.add_argument('--blind',type=Path,required=True)
    a=sub.add_parser('dashboard',help='Create private progress dashboard')
    a.add_argument('--experiment',type=Path,required=True);a.add_argument('--out',type=Path,required=True)
    a=sub.add_parser('results',help='Create exploratory results page after independent votes')
    a.add_argument('--analysis',type=Path,required=True);a.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    if args.cmd=='review-ui': files=make_reviewer(args.blind)
    elif args.cmd=='dashboard': files=[build_dashboard(args.experiment,args.out)]
    else: files=[build_results(args.analysis,args.out)]
    for file in files: print('GERADO',file)

if __name__=='__main__':main()
