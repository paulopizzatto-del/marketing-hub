#!/usr/bin/env python3
"""Create a 144-trial schedule, never fake outputs or human approvals."""
from pathlib import Path
import argparse
import hashlib
import json
import random
ROOT=Path(__file__).resolve().parents[1]
CONDITIONS={'A':'competent_assistant_brief_3_samples','B':'hub_brief_3_samples','C':'hub_brief_no_samples'}

def schedule(seed=4318):
    rows=[{'case_id':f'pilot-{b:02}/{t}/{c}/{r}','brand_id':f'pilot-{b:02}',
           'task':t,'condition':c,'repetition':r,'status':'not_run'}
          for b in range(1,9) for t in ('instagram','linkedin','comment')
          for c in CONDITIONS for r in (1,2)]
    random.Random(seed).shuffle(rows)
    return {'protocol':'claude-144-ptBR-v1','status':'not_run','seed':seed,
            'conditions':CONDITIONS,'planned_outputs':144,'actual_outputs':0,
            'skill_sha256':hashlib.sha256((ROOT/'skills/marketinghub/SKILL.md').read_bytes()).hexdigest(),
            'trials':rows}

def input_errors(data):
    brands=data.get('brands') if isinstance(data,dict) else None
    if not isinstance(brands,list) or len(brands)!=8:return ['Eight brands required']
    errors=[];seen=set()
    for b in brands:
        if not isinstance(b,dict):errors.append('Brand must be object');continue
        bid=b.get('brand_id')
        if not isinstance(bid,str) or bid in seen: errors.append('Invalid/duplicate brand_id')
        else:seen.add(bid)
        for key,n in (('approved_samples',3),('held_out_references',2)):
            values=b.get(key)
            if not isinstance(values,list) or len(values)!=n or not all(isinstance(t,str) and len(t.strip())>=30 for t in values):
                errors.append(str(bid)+': '+key+' incomplete')
        if not b.get('approved_by') or not b.get('approved_at'):errors.append(str(bid)+': reviewer/date absent')
        if not isinstance(b.get('brand_brief'),str) or not b['brand_brief'].strip():errors.append(str(bid)+': brief absent')
        tasks=b.get('tasks',{})
        if not isinstance(tasks,dict) or any(not isinstance(tasks.get(t),str) or not tasks[t].strip() for t in ('instagram','linkedin','comment')):
            errors.append(str(bid)+': tasks absent')
    return errors

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path);p.add_argument('--seed',type=int,default=4318);p.add_argument('--check-inputs',type=Path)
    a=p.parse_args()
    if a.check_inputs:
        try: errors=input_errors(json.loads(a.check_inputs.read_text(encoding='utf-8')))
        except (OSError,ValueError):errors=['Invalid input file']
        for e in errors:print(e)
        print('DECLARED INPUTS COMPLETE' if not errors else 'INPUTS INCOMPLETE; NO MODEL CALLS MADE')
        return 1 if errors else 0
    if not a.out:p.error('Use --out or --check-inputs')
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(schedule(a.seed),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('144 trials planned; actual outputs: 0. No provider was called.');return 0
if __name__=='__main__':raise SystemExit(main())
