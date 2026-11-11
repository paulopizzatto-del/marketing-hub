#!/usr/bin/env python3
"""Separate blind factuality review of captured outputs (operator/reviewer files private)."""
from __future__ import annotations
import argparse
import csv
import json
import random
from collections import defaultdict
from pathlib import Path
import lab
import lab_ui

FACT_CHOICES={'supported','no_objective_claim','unsupported','uncertain'}
PUB_CHOICES={'yes','no','unsure'}


def prepare(experiment:Path,out:Path,seed:int=9345):
    audit=lab.experiment_audit(experiment,require_complete=True)
    if audit['problems']:raise ValueError('Capture incomplete or tampered: '+'; '.join(audit['problems'][:3]))
    if out.exists():raise FileExistsError('Review already exists; do not re-randomize after first review')
    out.mkdir(parents=True)
    manifest=lab.load_json(experiment/'manifest.private.json')
    hold=lab.load_json(experiment/'heldouts.private.json')
    rng=random.Random(seed)
    cases=[];secret={}
    for t in manifest['trials']:
        real=t['case_id']
        id='item-'+lab.sha256((str(seed)+':'+real).encode())[:16]
        brand=t['brand_id']
        output=(experiment/'responses'/(real+'.txt')).read_text(encoding='utf-8')
        cases.append({'id':id,'task':t['task'],'brief':hold[brand]['brand_brief'],
                      'task_brief':hold[brand]['tasks'][t['task']], 'response':output})
        item=cases[-1]
        item_digest=lab.sha256(json.dumps(item,ensure_ascii=False,sort_keys=True).encode('utf-8'))
        secret[id]={'case_id':real,'brand_id':brand,'arm':t['arm'],'task':t['task'],
                    'response_sha256':lab.sha256((experiment/'responses'/(real+'.txt')).read_bytes()),
                    'item_sha256':item_digest}
    rng.shuffle(cases)
    lab.write_json(out/'items_FOR_REVIEWER.json',{'cases':cases})
    lab.write_json(out/'answers_DO_NOT_SHARE_WITH_REVIEWER.json',secret)
    with (out/'factuality.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['id','factuality','publishable','edit_minutes','notes'])
        w.writeheader();w.writerows([{'id':x['id'],'factuality':'','publishable':'','edit_minutes':'','notes':''} for x in cases])
    return len(cases)


def create_ui(root:Path):
    data=lab.load_json(root/'items_FOR_REVIEWER.json')
    raw=lab_ui.safe_json(data)
    body=f'''<div class="eyebrow">Auditoria factual independente · privada</div><h1>Fatos, risco e esforço de edição</h1><div class="warning">Avalie só o que o briefing permite confirmar. Não consulte a condição experimental. Esta página funciona offline; ao finalizar, exporte o CSV e preserve os arquivos privadamente.</div>
<div class="card" style="margin-top:17px"><div class="top"><strong id="index"></strong><span class="pill" id="progress"></span></div><p><b>Contexto da marca</b><span id="brief" style="display:block"></span></p><p><b>Tarefa</b><span id="taskbrief" style="display:block"></span></p></div>
<div class="card" style="margin-top:17px"><h3>Texto a avaliar</h3><div id="response" class="example" style="max-height:500px"></div></div>
<div class="card" style="margin-top:17px"><label><b>Alegações objetivas</b><select id="factuality" class="btn" style="width:100%;margin:9px 0"><option value="">Selecione</option><option value="supported">Alegações sustentadas pelo briefing</option><option value="no_objective_claim">Sem alegações objetivas</option><option value="unsupported">Uma ou mais alegações não sustentadas</option><option value="uncertain">Não é possível decidir com o briefing</option></select></label>
<label><b>Publicável com poucos ajustes?</b><select id="publishable" class="btn" style="width:100%;margin:9px 0"><option value="">Selecione</option><option value="yes">Sim</option><option value="no">Não</option><option value="unsure">Incerto</option></select></label>
<label><b>Tempo estimado de edição (minutos, opcional)</b><input id="minutes" type="number" min="0" max="600" step=".5" class="btn" style="width:100%;margin:9px 0"></label>
<label><b>Justificativa breve (opcional)</b><textarea id="notes"></textarea></label><div class="top" style="margin-top:12px"><div class="row"><button class="btn" id="prev">Anterior</button><button class="btn" id="next">Próximo</button><button class="btn" id="pending">Próximo pendente</button></div><button class="btn primary" id="export">Exportar factuality.csv</button></div></div>
<script id="cases" type="application/json">{raw}</script>'''
    script=r'''<script>
'use strict';const D=JSON.parse(document.getElementById('cases').textContent).cases;
const key='mh-factual-v1-'+D.length+'-'+D[0].id;let state={};try{state=JSON.parse(localStorage.getItem(key)||'{}')}catch(_){state={}};
let i=0;const el=x=>document.getElementById(x);function persist(){try{localStorage.setItem(key,JSON.stringify(state))}catch(_){}}
function save(){let id=D[i].id;state[id]={factuality:el('factuality').value,publishable:el('publishable').value,edit_minutes:el('minutes').value,notes:el('notes').value};persist()}
function render(){let a=D[i],v=state[a.id]||{};el('index').textContent='Item '+(i+1)+' de '+D.length+' · '+a.id;el('brief').textContent=a.brief;el('taskbrief').textContent=a.task_brief;el('response').textContent=a.response;
for(let f of ['factuality','publishable'])el(f).value=v[f]||'';el('minutes').value=v.edit_minutes||'';el('notes').value=v.notes||'';
el('progress').textContent=D.filter(x=>state[x.id]&&state[x.id].factuality&&state[x.id].publishable).length+'/'+D.length+' completos';
el('prev').disabled=i===0;el('next').disabled=i===D.length-1}
['factuality','publishable','minutes','notes'].forEach(f=>el(f).onchange=save);
el('prev').onclick=()=>{save();if(i>0)i--;render()};el('next').onclick=()=>{save();if(i<D.length-1)i++;render()};
el('pending').onclick=()=>{save();let k=D.findIndex(x=>!state[x.id]||!state[x.id].factuality||!state[x.id].publishable);if(k>=0){i=k;render()}else alert('Todos avaliados. Exporte o CSV.')};
function csv(t){t=String(t??'');if(/^[=+@\-\t\r]/.test(t))t="'"+t;return '"'+t.replaceAll('"','""')+'"'}
el('export').onclick=()=>{save();if(D.some(x=>!state[x.id]||!state[x.id].factuality||!state[x.id].publishable)&&!confirm('Exportar CSV parcial?'))return;
let records=D.map(x=>[x.id,(state[x.id]||{}).factuality||'',(state[x.id]||{}).publishable||'',(state[x.id]||{}).edit_minutes||'',(state[x.id]||{}).notes||''].map(csv).join(','));
let blob=new Blob(['\ufeffid,factuality,publishable,edit_minutes,notes\r\n'+records.join('\r\n')+'\r\n'],{type:'text/csv;charset=utf-8'});
let url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='factuality.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};
render();
</script>'''
    page=root/'factuality.html';page.write_text(lab_ui.frame('Marketing Hub — auditoria factual',body,script),encoding='utf-8')
    return page


def analyze(root:Path,out:Path):
    mapping=lab.load_json(root/'answers_DO_NOT_SHARE_WITH_REVIEWER.json')
    items=lab.load_json(root/'items_FOR_REVIEWER.json')['cases']
    if len(items)!=len(mapping) or len({x['id'] for x in items})!=len(mapping):
        raise ValueError('Dados de auditoria factual incoerentes')
    for item in items:
        if item['id'] not in mapping or lab.sha256(item['response'].encode('utf-8')) != mapping[item['id']]['response_sha256']:
            raise ValueError('Texto cego alterado depois da preparação da auditoria factual')
        if lab.sha256(json.dumps(item,ensure_ascii=False,sort_keys=True).encode('utf-8')) != mapping[item['id']].get('item_sha256'):
            raise ValueError('Briefing ou cartão factual alterado depois da preparação')
    with (root/'factuality.csv').open('r',encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=len(mapping) or {x['id'] for x in rows}!=set(mapping):
        raise ValueError('Faltam respostas ou IDs de auditoria factual')
    counts=defaultdict(lambda:{'cases':0,'supported':0,'no_objective_claim':0,'unsupported':0,'uncertain':0,'publishable_yes':0,'publishable_no':0,'publishable_unsure':0,'edit_minutes':[]})
    for row in rows:
        fc=row['factuality'].strip();pc=row['publishable'].strip()
        if fc not in FACT_CHOICES or pc not in PUB_CHOICES:
            raise ValueError('Factuality incompleta ou opção inválida')
        m=row['edit_minutes'].strip()
        if m:
            try:value=float(m)
            except ValueError as ex:raise ValueError('Minutos de edição não numéricos') from ex
            if not 0<=value<=600:raise ValueError('Tempo de edição fora de 0..600')
        else:value=None
        arm=mapping[row['id']]['arm'];d=counts[arm];d['cases']+=1;d[fc]+=1;d['publishable_'+pc]+=1
        if value is not None:d['edit_minutes'].append(value)
    result={'status':'BLINDED_FACTUAL_REVIEW_USER_DECLARED_NOT_VERIFIED','n_items':len(rows),'by_arm':{},
            'limits':['One reviewer, not independently authenticated.',
                      'Supported means supported by provided briefing, not external fact-check.',
                      'Do not treat a higher publishability rate as causal without clustered uncertainty.']}
    for arm in lab.ARMS:
        x=counts[arm];n=x['cases'];result['by_arm'][arm]={k:v for k,v in x.items() if k!='edit_minutes'}
        result['by_arm'][arm]['unsupported_fraction']=x['unsupported']/n if n else None
        result['by_arm'][arm]['publishable_fraction']=x['publishable_yes']/n if n else None
        result['by_arm'][arm]['edit_minutes_mean_when_reported']=sum(x['edit_minutes'])/len(x['edit_minutes']) if x['edit_minutes'] else None
        result['by_arm'][arm]['edit_time_observations']=len(x['edit_minutes'])
    if out.exists():raise FileExistsError('Análise factual existente; não sobrescrever')
    lab.write_json(out,result)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('prepare');a.add_argument('--experiment',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--seed',type=int,default=9345)
    a=sub.add_parser('ui');a.add_argument('--review',type=Path,required=True)
    a=sub.add_parser('analyze');a.add_argument('--review',type=Path,required=True);a.add_argument('--out',type=Path,required=True)
    x=p.parse_args()
    if x.command=='prepare':print('Prepared',prepare(x.experiment,x.out,x.seed),'blind factual-review items')
    elif x.command=='ui':print('Created',create_ui(x.review))
    else:print(json.dumps(analyze(x.review,x.out),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
