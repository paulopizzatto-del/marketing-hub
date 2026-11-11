#!/usr/bin/env python3
"""Operator-only mechanical diagnostics. No model calls and no quality verdicts."""
from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path

import lab


def words(text):
    return re.findall(r"\b[\wÀ-ÿ]+\b", text.casefold(), re.UNICODE)


def overlap_tokens(a, b, min_tokens=8):
    """Return true when a long contiguous chunk is copied; not a style metric."""
    aa, bb = words(a), words(b)
    if len(aa) < min_tokens or len(bb) < min_tokens:
        return False
    needles = {tuple(bb[i:i + min_tokens]) for i in range(len(bb)-min_tokens+1)}
    return any(tuple(aa[i:i+min_tokens]) in needles for i in range(len(aa)-min_tokens+1))


def audit_quality(experiment: Path, out: Path):
    integrity = lab.experiment_audit(experiment)
    if integrity['problems']:
        raise ValueError('Integridade reprovada; métricas recusadas: ' + '; '.join(integrity['problems'][:3]))
    mf = lab.load_json(experiment/'manifest.private.json')
    meta = lab.load_json(experiment/'capture_metadata.private.json')
    data = []
    by_cell = {}
    length_by_group = defaultdict(list)
    runtime_metrics = defaultdict(lambda: defaultdict(list))
    warnings = []
    for t in mf['trials']:
        case = t['case_id']
        if case not in meta:
            continue
        text = (experiment/'responses'/(case+'.txt')).read_text(encoding='utf-8')
        count = len(words(text))
        entry = {'case_id': case, 'brand_id': t['brand_id'], 'arm': t['arm'], 'task': t['task'],
                 'repetition': t['repetition'], 'word_count': count, 'character_count': len(text)}
        data.append(entry)
        by_cell[(t['brand_id'],t['task'],t['repetition'],t['arm'])]=(text,entry)
        length_by_group[(t['task'],t['arm'])].append(count)
        for metric in ('input_tokens','output_tokens','latency_ms','cost_usd'):
            value=meta[case].get(metric)
            if isinstance(value,(int,float)):
                runtime_metrics[(t['task'],t['arm'])][metric].append(value)
    groups = {'/'.join(key): {'count': len(ns), 'mean_words': statistics.mean(ns),
                              'min_words': min(ns), 'max_words': max(ns)}
              for key, ns in sorted(length_by_group.items())}
    # Only compare when all 3 arms exist; this is about confounding not quality.
    for brand in sorted({x['brand_id'] for x in mf['trials']}):
        for task in lab.CORE_TASKS:
            for rep in (1,2):
                found = {arm: by_cell.get((brand,task,rep,arm)) for arm in lab.ARMS}
                if not all(found.values()):
                    continue
                for i, left in enumerate(lab.ARMS):
                    for right in lab.ARMS[i+1:]:
                        la, lb = found[left][1]['word_count'], found[right][1]['word_count']
                        if min(la,lb) and abs(la-lb)/min(la,lb) > .30:
                            warnings.append({'type':'LENGTH_IMBALANCE', 'case': f'{brand}/{task}/r{rep}',
                                             'comparison': left+right, 'left_words':la,'right_words':lb,
                                             'note':'Potential preference confound; do not selectively regenerate.'})
                        if lab.sha256(found[left][0].encode('utf-8')) == lab.sha256(found[right][0].encode('utf-8')):
                            warnings.append({'type':'IDENTICAL_OUTPUTS','case':f'{brand}/{task}/r{rep}',
                                             'comparison':left+right,
                                             'note':'Verify capture files; equality is not proof of error.'})
    # Long verbatim reproduction from the three exposed training examples is a proxy for copying, not voice fidelity.
    # Read only the training blocks from the prompt; heldouts are never consulted here.
    for item in data:
        case=item['case_id']
        prompt=(experiment/'prompts'/(case+'.txt')).read_text(encoding='utf-8')
        text=(experiment/'responses'/(case+'.txt')).read_text(encoding='utf-8')
        chunks=re.findall(r'AMOSTRA [123]:\n(.*?)(?=\n\n---|\Z)',prompt,flags=re.S)
        if any(overlap_tokens(text, ex) for ex in chunks):
            warnings.append({'type':'LONG_VERBATIM_OVERLAP','case':case,
                             'note':'8+ token sequence from a visible sample; review manually.'})
    measured = {'/'.join(key): {metric: {'n': len(vals), 'mean': statistics.mean(vals)}
                                  for metric, vals in ms.items()}
                for key, ms in sorted(runtime_metrics.items())}
    result={'status':'MECHANICAL_DIAGNOSTICS_NOT_EDITORIAL_RESULTS',
            'captured':len(data),'expected':len(mf['trials']),'length_groups':groups, 'reported_execution_metrics':measured,
            'warnings':warnings, 'warning_count':len(warnings),
            'cautions':['Length/overlap measures are not quality or authorship tests.',
                        'Warnings require review; do not remove weak outcomes selectively.',
                        'No held-out references are exposed or scored in this report.',
                        'Token, latency and cost numbers are provider/operator-declared, not verified.',
                        'Keep the output private until review and consent.']}
    if out.exists():
        raise FileExistsError('Arquivo de diagnóstico já existe; não sobrescrever')
    lab.write_json(out,result)
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--experiment',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    result=audit_quality(args.experiment,args.out)
    print(json.dumps({'status':result['status'],'captured':result['captured'],
                      'warning_count':result['warning_count']},ensure_ascii=False))

if __name__=='__main__':main()
