#!/usr/bin/env python3
"""Distribute blinded review to multiple independent humans; never include arm key.

The original blind/R1 and blind/R2 remain the canonical complete datasets.
Shards create per-worker private review packets, preserving the two reviewer slots.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from collections import defaultdict
from pathlib import Path
import lab, lab_ui

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def make(blind:Path,out:Path,workers:int):
    if not 4<=workers<=100 or workers%2: raise ValueError('workers deve ser par, entre 4 e 100')
    if out.exists(): raise FileExistsError('Destino existe; não recrie os pacotes após distribuição')
    indata={r:lab.load_json(blind/r/'reviewer_cases.json') for r in ('R1','R2')}
    first=indata['R1']['cases']; second=indata['R2']['cases']
    if {c['pair_id'] for c in first}!={c['pair_id'] for c in second}: raise ValueError('Pares R1/R2 diferentes')
    mapping={r:{c['pair_id']:c for c in indata[r]['cases']} for r in ('R1','R2')}
    assignments={f'reviewer-{w+1:02}':[] for w in range(workers)}
    for i,c in enumerate(first):
        # Adjacent slots for the same pair MUST be evaluated by different humans.
        for slot,person in (('R1',i%workers),('R2',(i+workers//2)%workers)):
            assignments[f'reviewer-{person+1:02}'].append((slot,mapping[slot][c['pair_id']]))
    out.mkdir(parents=True)
    audit={'format':'lab50-shards-v1','n_workers':workers,'blind_slot_ids':['R1','R2'],
           'n_pairs':len(first),'assignment':{},'checksum':{}}
    for worker,records in assignments.items():
        directory=out/worker;directory.mkdir()
        cases=[dict(item,reviewer_slot=slot) for slot,item in records]
        d={'reviewer_id':worker,'cases':cases,'note':'Privado. Não há código A/B/C aqui.'}
        raw=directory/'reviewer_cases.json';lab.write_json(raw,d)
        audit['assignment'][worker]=[{'pair_id':v['pair_id'],'slot':v['reviewer_slot']} for v in cases]
        audit['checksum'][worker]=sha(raw)
        with (directory/'judgments.csv').open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=('pair_id','reviewer_id','choice','notes'));w.writeheader()
            w.writerows({'pair_id':c['pair_id'],'reviewer_id':c['reviewer_slot'],'choice':'','notes':''} for c in cases)
        ui_data=lab_ui.safe_json(d)
        body=f'''<div class="eyebrow">Revisão cega distribuída</div><h1>Compare textos de marca</h1><p class="warning">Pacote privado de {worker}. Não compartilhe. Você verá duas opções sem identificação de método ou modelo. Salve os votos no CSV para devolução ao organizador.</p><div class="card"><div class="top"><strong id="case"></strong><span class="pill" id="count"></span></div><p id="brief"></p><p id="task"></p><div id="refs"></div></div><section class="grid" style="margin:16px 0"><div class="card"><h3>Esquerda</h3><div id="left" class="example"></div></div><div class="card"><h3>Direita</h3><div id="right" class="example"></div></div></section><nav class="actions" aria-label="Avaliar"><button class="btn" data-v="left">Esquerda</button><button class="btn" data-v="right">Direita</button><button class="btn" data-v="tie">Empate</button><button class="btn" data-v="both_bad">Ambos inadequados</button></nav><div class="card"><label for="note">Observação opcional</label><textarea id="note"></textarea><div class="top"><div class="row"><button id="prev" class="btn">Anterior</button><button id="next" class="btn">Próximo</button></div><button id="download" class="btn primary">Exportar CSV</button></div></div><script id="data" type="application/json">{ui_data}</script>'''
        js=r'''<script>
'use strict';const data=JSON.parse(document.getElementById('data').textContent), rows=data.cases;
let i=0,votes={};const key='lab50-'+data.reviewer_id+'-'+rows.length+'-'+rows[0].pair_id;
try{votes=JSON.parse(localStorage.getItem(key)||'{}')}catch(_){}
const q=x=>document.getElementById(x),save=()=>{try{localStorage.setItem(key,JSON.stringify(votes))}catch(_){}};
function render(){const a=rows[i],v=votes[a.pair_id]||{};q('case').textContent='Caso '+(i+1)+' de '+rows.length;q('count').textContent=rows.filter(x=>votes[x.pair_id]&&votes[x.pair_id].choice).length+' avaliados';q('brief').textContent=a.brief;q('task').textContent=a.task_brief;q('left').textContent=a.left;q('right').textContent=a.right;q('note').value=v.notes||'';q('refs').replaceChildren();for(let x of a.references){const p=document.createElement('p');p.className='reference';p.textContent=x;q('refs').append(p)}q('prev').disabled=i===0;q('next').disabled=i===rows.length-1;document.querySelectorAll('[data-v]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.v===v.choice)))}
function choose(choice){const a=rows[i];votes[a.pair_id]={choice,notes:q('note').value};save();if(i<rows.length-1)i++;render()}
for(const b of document.querySelectorAll('[data-v]'))b.onclick=()=>choose(b.dataset.v);
q('note').onchange=()=>{const a=rows[i];votes[a.pair_id]={...(votes[a.pair_id]||{}),notes:q('note').value};save()};
q('prev').onclick=()=>{if(i>0)i--;render()};q('next').onclick=()=>{if(i<rows.length-1)i++;render()};
function esc(s){s=String(s||'');if(/^[=+@\-\t\r]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"'}
q('download').onclick=()=>{if(rows.some(x=>!votes[x.pair_id]||!votes[x.pair_id].choice)&&!confirm('Existem votos pendentes. Exportar CSV parcial?'))return;let csv='pair_id,reviewer_id,choice,notes\r\n'+rows.map(x=>[x.pair_id,x.reviewer_slot,(votes[x.pair_id]||{}).choice||'',(votes[x.pair_id]||{}).notes||''].map(esc).join(',')).join('\r\n');let u=URL.createObjectURL(new Blob(['\ufeff'+csv],{type:'text/csv;charset=utf-8'}));let a=document.createElement('a');a.href=u;a.download='judgments.csv';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000)};render();
</script>'''
        (directory/'review.html').write_text(lab_ui.frame('Marketing Hub 50 — '+worker,body,js),encoding='utf-8')
    lab.write_json(out/'SHARD_ASSIGNMENT_PRIVATE.json',audit)
    print(f'{workers} pacotes gerados: {sum(map(len,assignments.values()))} votos planejados, zero coletado.')

def merge(blind:Path,shards:Path):
    plan=lab.load_json(shards/'SHARD_ASSIGNMENT_PRIVATE.json')
    by_slot=defaultdict(dict)
    allowed={'left','right','tie','both_bad'}
    for worker, entries in plan['assignment'].items():
        directory=shards/worker
        if sha(directory/'reviewer_cases.json')!=plan['checksum'][worker]:raise ValueError('Pacote alterado: '+worker)
        with (directory/'judgments.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
        expected={(x['pair_id'],x['slot']) for x in entries}
        actual={(x.get('pair_id'),x.get('reviewer_id')) for x in rows}
        if expected!=actual or len(rows)!=len(expected):raise ValueError('Votos incompletos/IDs divergentes: '+worker)
        for r in rows:
            if r['choice'] not in allowed:raise ValueError('Voto ausente ou inválido: '+worker)
            pair,slot=r['pair_id'],r['reviewer_id']
            if pair in by_slot[slot]:raise ValueError('Par duplicado: '+pair)
            by_slot[slot][pair]={'pair_id':pair,'reviewer_id':slot,'choice':r['choice'],'notes':r['notes']}
    for slot in ('R1','R2'):
        orig=blind/slot/'judgments.csv'
        with orig.open(encoding='utf-8-sig',newline='') as f: old=list(csv.DictReader(f))
        if any(r['choice'] for r in old):raise ValueError('Existem votos anteriores em '+slot+'; não sobrescrever')
        if {r['pair_id'] for r in old} != set(by_slot[slot]):raise ValueError('Cobertura incompleta de '+slot)
    for slot in ('R1','R2'):
        orig=blind/slot/'judgments.csv'
        with orig.open(encoding='utf-8',newline='') as f: old=list(csv.DictReader(f))
        with orig.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['pair_id','reviewer_id','choice','notes']);w.writeheader();w.writerows(by_slot[slot][r['pair_id']] for r in old)
    lab.write_json(blind/'reviewer_pool.private.json',{'n_workers_declared':plan['n_workers'],'reviewer_slots':['R1','R2'],'assignment_sha256':sha(shards/'SHARD_ASSIGNMENT_PRIVATE.json'),'note':'Worker identities not authenticated; R1/R2 are voting slots, not two actual reviewers.'})
    print('Votos cegos completos importados; identidade externa dos avaliadores não é autenticada.')

def main():
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='cmd',required=True)
    a=s.add_parser('create');a.add_argument('--blind',required=True,type=Path);a.add_argument('--out',required=True,type=Path);a.add_argument('--workers',type=int,default=20)
    b=s.add_parser('merge');b.add_argument('--blind',required=True,type=Path);b.add_argument('--shards',required=True,type=Path)
    args=p.parse_args()
    try: make(args.blind,args.out,args.workers) if args.cmd=='create' else merge(args.blind,args.shards)
    except (ValueError,FileNotFoundError,FileExistsError) as e:p.error(str(e))
if __name__=='__main__':main()
