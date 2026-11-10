#!/usr/bin/env python3
"""Evaluate externally generated 20x3 outputs; FAIL CLOSED on missing samples.

Input JSONL lines: {"case_id":"brand-id/instagram", "output":"...", "human_approved": true}
Only claims baseline adherence, not 100% correctness. Requires an explicit model/provider id.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from test_20_brands import errors_for_output


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--results',type=Path,required=True)
    p.add_argument('--provider',required=True)
    p.add_argument('--model-version',required=True)
    args=p.parse_args()
    cases=json.loads((ROOT/'tests/fixtures/20-brands-3-rounds.json').read_text(encoding='utf-8'))['cases']
    expected={b['brand_id']+'/'+t:b for b in cases for t in ('instagram','linkedin','comment')}
    try:
        rows=[json.loads(s) for s in args.results.read_text(encoding='utf-8').splitlines() if s.strip()]
    except (ValueError,OSError) as e:
        print('INVALID RESULT FILE:',e);return 2
    ids=[x.get('case_id') for x in rows]
    duplicate=sorted({x for x in ids if ids.count(x)>1})
    missing=sorted(set(expected)-set(ids))
    extra=sorted(set(ids)-set(expected))
    failed=[]
    if missing: failed.append(f'Missing {len(missing)} of 60 required cases')
    if extra: failed.append(f'Unknown {len(extra)} case IDs')
    if duplicate: failed.append(f'Duplicate IDs: {len(duplicate)}')
    for row in rows:
        identifier=row.get('case_id')
        if identifier not in expected:continue
        output=row.get('output')
        if not isinstance(output,str) or not output.strip():
            failed.append(f'{identifier}: output missing');continue
        if row.get('human_approved') is not True:
            failed.append(f'{identifier}: editorial approval missing')
        b=expected[identifier]
        task=identifier.split('/')[-1]
        issues=errors_for_output(b,{'task':task,'content':output},cases)
        failed.extend(f'{identifier}: {issue}' for issue in issues)
    print(f'Provider: {args.provider} / {args.model_version}')
    print('Required trials: 60 | supplied:',len(rows))
    print('Status:', 'PASS' if not failed else 'FAIL/INCOMPLETE')
    for message in failed[:20]:print(' -',message)
    if len(failed)>20:print(f'... plus {len(failed)-20} additional issues')
    if not failed:print('All prescribed baseline checks and external human approvals are recorded for this model only.')
    return 0 if not failed else 1

if __name__=='__main__':
    raise SystemExit(main())
