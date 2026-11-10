#!/usr/bin/env python3
"""Validate records of real outputs; does not produce a model quality score.

Format warnings never reject by themselves. Content/voice/language judgments
require an identified human reviewer outside this program.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
from editorial_checks import assess_output, unresolved_review_flags
ROOT=Path(__file__).resolve().parents[1]

def evaluate(rows, cases):
    expected={b['brand_id']+'/'+task:b for b in cases for task in ('instagram','linkedin','comment')}
    errors=[];reports=[];ids=[]
    if not isinstance(rows,list): return {'status':'INVALID','errors':['Results must be a list'],'records':[]}
    valid=[]
    for index,row in enumerate(rows):
        if not isinstance(row,dict) or not isinstance(row.get('case_id'),str):
            errors.append(f'Row {index+1}: object with string case_id required');continue
        ids.append(row['case_id']);valid.append(row)
    missing=sorted(set(expected)-set(ids));extra=sorted(set(ids)-set(expected))
    duplicates=sorted(i for i,n in Counter(ids).items() if n>1)
    if missing: errors.append(f'Missing {len(missing)} of {len(expected)} required cases')
    if extra: errors.append(f'Unknown case IDs: {len(extra)}')
    if duplicates: errors.append(f'Duplicate case IDs: {len(duplicates)}')
    for row in valid:
        identifier=row['case_id']
        if identifier not in expected: continue
        record=expected[identifier]
        report=assess_output(record,row.get('output'),cases,identifier.rsplit('/',1)[1])
        report['case_id']=identifier
        if row.get('human_approved') is not True:
            errors.append(identifier+': editorial approval missing')
        # Legacy human_approved is a declaration, never proof of an independent review.
        pending=unresolved_review_flags(report['review_flags'],row.get('reviewed_flags'))
        errors.extend(identifier+': '+f['code'] for f in report['safety_errors'])
        errors.extend(identifier+': review required: '+f['code'] for f in pending)
        report['unresolved_review_flags']=pending;reports.append(report)
    return {'status':'PASS_RECORD_CHECKS' if not errors else 'FAIL_OR_INCOMPLETE',
            'required':len(expected),'supplied':len(rows),'errors':errors,'records':reports,
            'limitations':['No automatic voice, language, originality or factual-truth score.',
                          'Human approvals and evidence references are supplied declarations.',
                          'Format ranges are editorial suggestions, not platform rules.']}

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('--results',type=Path,required=True);p.add_argument('--provider',required=True)
    p.add_argument('--model-version',required=True);p.add_argument('--report',type=Path)
    a=p.parse_args(argv)
    if not a.provider.strip() or not a.model_version.strip(): p.error('Nonempty provider and model version required')
    try:
        cases=json.loads((ROOT/'tests/fixtures/20-brands-3-rounds.json').read_text(encoding='utf-8'))['cases']
        rows=[json.loads(line) for line in a.results.read_text(encoding='utf-8').splitlines() if line.strip()]
    except (ValueError,OSError) as exc:
        print('INVALID RESULT FILE:',type(exc).__name__);return 2
    result=evaluate(rows,cases);result.update(provider=a.provider,model_version=a.model_version)
    print('Provider:',a.provider,'/',a.model_version)
    print('Status:',result['status'])
    for error in result['errors'][:30]: print(' -',error)
    print('Format warnings:',sum(len(r['format_warnings']) for r in result['records']))
    print('This checks records and safety signals; it does not establish better writing.')
    if a.report:
        a.report.parent.mkdir(parents=True,exist_ok=True)
        a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return 0 if not result['errors'] else 1
if __name__=='__main__': raise SystemExit(main())
