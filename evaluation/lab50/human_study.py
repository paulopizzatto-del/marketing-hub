#!/usr/bin/env python3
"""Causal-workflow assignment/validation for human-AI study. No users or results fabricated."""
from __future__ import annotations
import argparse, csv, json, random
from collections import defaultdict,Counter
from pathlib import Path
from datetime import datetime,timezone
ARMS=('H0_AI_only','H1_light_review','H2_deep_review','H3_human_leads_AI','H4_human_only')
SESSION_FIELDS=('participant_id','task_id','assigned_arm','followed_arm','duration_minutes','edits_count','claims_checked','publishable_by_blind_reviewer','blind_quality_score','confidence_1_to_5','notes')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def savecsv(path,rows,fields):
    with path.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def assign(roster,out,seed=4206):
    if out.exists():raise FileExistsError('Saída já existe; preserve alocação original')
    data=read(roster);people=data.get('participants') if isinstance(data,dict) else None
    if not isinstance(people,list) or len(people)<5:raise ValueError('Precisa de pelo menos cinco participantes consentidos, reais e pseudonimizados')
    ids=[]; strata=defaultdict(list)
    for p in people:
        if not isinstance(p,dict):raise ValueError('Participante inválido')
        pid=p.get('participant_id','')
        if not isinstance(pid,str) or not pid.startswith('P') or not pid[1:].isdigit():raise ValueError('Use IDs P001, P002... sem nomes reais')
        if p.get('consent_confirmed') is not True:raise ValueError('Falta consentimento: '+pid)
        if pid in ids:raise ValueError('Participante repetido: '+pid)
        ids.append(pid);strata[(p.get('role','unspecified'),p.get('experience','unspecified'))].append(pid)
    rng=random.Random(seed);allocated=[]
    quotas={arm:len(people)//len(ARMS) for arm in ARMS}
    leftovers=len(people)%len(ARMS)
    extras=list(ARMS);rng.shuffle(extras)
    for arm in extras[:leftovers]:quotas[arm]+=1
    for key in sorted(strata,key=lambda k:-len(strata[k])):
        group=strata[key];rng.shuffle(group)
        local=Counter()
        for pid in group:
            options=[a for a in ARMS if quotas[a]>0]
            if not options:raise RuntimeError('Erro de cotas')
            rng.shuffle(options)
            arm=min(options,key=lambda a:(local[a],-quotas[a]))
            quotas[arm]-=1;local[arm]+=1
            allocated.append({'participant_id':pid,'assigned_arm':arm,'role':key[0],'experience':key[1]})
    rng.shuffle(allocated)
    out.mkdir(parents=True)
    savecsv(out/'allocations.private.csv',allocated,('participant_id','assigned_arm','role','experience'))
    savecsv(out/'sessions.private.template.csv',[],SESSION_FIELDS)
    (out/'manifest.private.json').write_text(json.dumps({'status':'ASSIGNMENT_ONLY_NOT_STUDY_RESULTS','seed':seed,'n_participants':len(people),'planned_tasks_per_participant':4,'arms':ARMS,'n_by_arm':dict(Counter(x['assigned_arm'] for x in allocated)),'roster_sha256':__import__('hashlib').sha256(roster.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    print(f'{len(people)} participantes alocados por estratos declarados; 0 sessões executadas.')
def analyze(plan,sessions,out):
    if out.exists():raise FileExistsError('Análise existente; não sobrescrever')
    with (plan/'allocations.private.csv').open(encoding='utf-8',newline='') as f:allocation={r['participant_id']:r for r in csv.DictReader(f)}
    with sessions.open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
    if not rows:raise ValueError('Nenhuma sessão real registrada')
    if set(SESSION_FIELDS)-set(rows[0]):raise ValueError('Colunas faltantes')
    byperson=defaultdict(set);summary=defaultdict(lambda:{'sessions':0,'participants':set(),'total_duration':0.,'quality_scores':[],'declared_publishable':0,'adherence_count':0})
    for r in rows:
        pid=r['participant_id'];task=r['task_id'];assigned=allocation.get(pid)
        if not assigned or not task or task in byperson[pid]:raise ValueError('Sessão desconhecida/duplicada')
        byperson[pid].add(task)
        if r['assigned_arm'] != assigned['assigned_arm'] or r['followed_arm'] not in ARMS:raise ValueError('Alocação ou adesão inválida')
        try:minutes=float(r['duration_minutes']);score=float(r['blind_quality_score'])
        except ValueError as e:raise ValueError('Minutos e nota cega devem ser numéricos, verificados') from e
        if not 0<=minutes<=240 or not 1<=score<=5:raise ValueError('Intervalo inválido')
        if r['publishable_by_blind_reviewer'] not in ('yes','no'):raise ValueError('Revisão cega de publicabilidade ausente')
        k=summary[r['assigned_arm']];k['sessions']+=1;k['participants'].add(pid);k['total_duration']+=minutes;k['quality_scores'].append(score);k['declared_publishable']+=r['publishable_by_blind_reviewer']=='yes';k['adherence_count']+=r['followed_arm']==r['assigned_arm']
    if set(byperson)!=set(allocation) or any(len(s)!=4 for s in byperson.values()):raise ValueError('Sessões incompletas: exigidas quatro por participante alocado')
    result={'status':'DECLARED_HUMAN_STUDY_RECORDS_PRESENT_NOT_INDEPENDENTLY_AUTHENTICATED','design':'Randomized assignment (ITT); do not reclassify based on compliance','n_participants':len(allocation),'n_sessions':len(rows),'by_assigned_arm':{},'limits':['Descriptive only; participant eligibility, blinded scores and actual treatment are user-declared.','No preregistered effect model, clustered CI or attrition analysis is provided in this script.','Post-treatment duration is a mediator, not a baseline covariate for primary ITT.']}
    for arm in ARMS:
        k=summary[arm];n=k['sessions'];result['by_assigned_arm'][arm]={'participants':len(k['participants']),'sessions':n,'mean_minutes':k['total_duration']/n if n else None,'mean_blind_quality':sum(k['quality_scores'])/n if n else None,'publishability_fraction':k['declared_publishable']/n if n else None,'protocol_adherence_fraction':k['adherence_count']/n if n else None}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Resumo ITT descritivo pronto; sem alegação causal confirmatória.')
def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('assign');a.add_argument('--roster',required=True,type=Path);a.add_argument('--out',required=True,type=Path);a.add_argument('--seed',type=int,default=4206)
    b=sub.add_parser('analyze');b.add_argument('--plan',required=True,type=Path);b.add_argument('--sessions',required=True,type=Path);b.add_argument('--out',required=True,type=Path)
    z=p.parse_args()
    try:assign(z.roster,z.out,z.seed) if z.cmd=='assign' else analyze(z.plan,z.sessions,z.out)
    except (ValueError,FileNotFoundError,FileExistsError) as e:p.error(str(e))
if __name__=='__main__':main()
