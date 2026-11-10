#!/usr/bin/env python3
"""Summarize authored contract fixtures; never generate a performance claim."""
from pathlib import Path
import json
from editorial_checks import assess_output
ROOT=Path(__file__).resolve().parents[1]
def run():
    cases=json.loads((ROOT/'tests/fixtures/20-brands-3-rounds.json').read_text(encoding='utf-8'))['cases']
    rows=[]
    for brand in cases:
        for output in brand['outputs']:
            result=assess_output(brand,output['content'],cases,output['task'])
            rows.append({'case_id':brand['brand_id']+'/'+output['task'],**result})
    result={'kind':'authored_contract_fixtures','live_model_calls':0,'quality_claim':None,
            'records':rows,'note':'No brand-voice or model comparison has been performed.'}
    destination=ROOT/'dist/contract-report.json';destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    errors=sum(len(r['safety_errors'])+len(r['review_flags']) for r in rows)
    print('Authored fixtures checked:',len(rows),'| mechanical flags:',errors,'| live model calls: 0')
    return 0 if len(rows)==60 and not errors else 1
if __name__=='__main__':raise SystemExit(run())
