#!/usr/bin/env python3
"""Small-cluster pilot summary. No model calls and no claim of causal proof."""
from __future__ import annotations
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

VALID = {'A', 'B', 'tie', 'both_bad'}


def exact_sign_p_value(wins, losses):
    n = wins + losses
    if n == 0:
        return None
    k = wins
    # one-sided P[X >= k] for X~Binomial(n, .5)
    return sum(math.comb(n, i) for i in range(k, n + 1)) / (2 ** n)


def summarize(rows):
    by_brand = defaultdict(lambda: {'A': 0, 'B': 0, 'tie': 0, 'both_bad': 0})
    lengths = defaultdict(list)
    errors = []
    for i, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            errors.append(f'row {i}: object required')
            continue
        brand = row.get('brand_id')
        choice = row.get('preference')
        if not isinstance(brand, str) or not brand:
            errors.append(f'row {i}: brand_id required')
            continue
        if choice not in VALID:
            errors.append(f'row {i}: preference must be one of {sorted(VALID)}')
            continue
        by_brand[brand][choice] += 1
        for cond in ('A', 'B'):
            value = row.get(f'{cond}_length')
            if isinstance(value, (int, float)) and value >= 0:
                lengths[cond].append(float(value))
    if errors:
        return {'status': 'INVALID', 'errors': errors}
    brand_direction = {'B': 0, 'A': 0, 'tie': 0}
    total = {'A': 0, 'B': 0, 'tie': 0, 'both_bad': 0}
    brand_rows = []
    for brand, counts in sorted(by_brand.items()):
        for key in total:
            total[key] += counts[key]
        if counts['B'] > counts['A']:
            direction = 'B'; brand_direction['B'] += 1
        elif counts['A'] > counts['B']:
            direction = 'A'; brand_direction['A'] += 1
        else:
            direction = 'tie'; brand_direction['tie'] += 1
        brand_rows.append({'brand_id': brand, **counts, 'direction': direction})
    decisive = total['A'] + total['B']
    b_share = total['B'] / decisive if decisive else None
    half_share = (total['B'] + .5 * (total['tie'] + total['both_bad'])) / sum(total.values()) if total and sum(total.values()) else None
    p = exact_sign_p_value(brand_direction['B'], brand_direction['A'])
    mean_len = {k: (sum(v) / len(v) if v else None) for k, v in lengths.items()}
    return {
        'status': 'DESCRIPTIVE_PILOT_SUMMARY',
        'pairs': sum(total.values()),
        'preference_counts': total,
        'B_share_excluding_ties': b_share,
        'B_share_ties_as_half': half_share,
        'brand_direction': brand_direction,
        'brand_sign_test_one_sided_p': p,
        'mean_lengths': mean_len,
        'brands': brand_rows,
        'limitations': [
            'Eight brands are few independent clusters; this summary is not a confirmatory guarantee.',
            'The exact sign test uses brand-level direction and ignores within-brand magnitude.',
            'Use a pre-registered small-cluster method for the primary inferential model.',
        ],
    }


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--judgments', type=Path, required=True, help='JSONL with brand_id, preference and optional A_length/B_length')
    p.add_argument('--out', type=Path)
    a = p.parse_args(argv)
    try:
        rows = [json.loads(line) for line in a.judgments.read_text(encoding='utf-8').splitlines() if line.strip()]
    except (OSError, ValueError) as exc:
        print('INVALID:', type(exc).__name__)
        return 2
    result = summarize(rows)
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    print(text, end='')
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(text, encoding='utf-8')
    return 0 if result['status'] != 'INVALID' else 1


if __name__ == '__main__':
    raise SystemExit(main())
