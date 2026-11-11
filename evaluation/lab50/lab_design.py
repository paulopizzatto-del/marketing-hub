#!/usr/bin/env python3
"""Exact sign-test design sensitivity under explicit independent-brand assumptions.

This is NOT a power analysis fitted to actual Marketing Hub outputs. It is an
illustrative calculation where each brand independently favors the test arm with
probability p, no ties, one-sided alpha=0.05.
"""
import argparse
import csv
import json
from math import comb
from pathlib import Path


def one_sided_p(wins, brands):
    return sum(comb(brands,i) for i in range(wins,brands+1))/2**brands


def design_table(ns=(10,20,32,50,75,100), probabilities=(.55,.60,.65,.70), alpha=.05):
    rows=[]
    for n in ns:
        reject=min((k for k in range(n+1) if one_sided_p(k,n)<=alpha),default=None)
        for p in probabilities:
            prob=(sum(comb(n,k)*p**k*(1-p)**(n-k) for k in range(reject,n+1))
                  if reject is not None else 0)
            rows.append({'brands':n,'assumed_probability_brand_prefers_hub':p,
                         'minimum_brand_wins_for_one_sided_alpha':reject,
                         'chance_of_rejection_under_assumptions':round(prob,6),
                         'alpha':alpha})
    return rows


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--format',choices=['json','csv'],default='json')
    p.add_argument('--alpha',type=float,default=.05)
    a=p.parse_args()
    if not 0<a.alpha<1:raise SystemExit('alpha must be between 0 and 1')
    rows=design_table(alpha=a.alpha)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    if a.out.exists():raise SystemExit('Output exists; preserve previous pre-analysis plan')
    if a.format=='json':
        a.out.write_text(json.dumps({'status':'ILLUSTRATIVE_ASSUMPTIONS_NOT_EVIDENCE',
                         'assumptions':['Each brand is independent and has equal P(favoring Hub).',
                                        'No ties, only one observation per brand.',
                                        'No effect of within-brand variation or reviewers modeled.',
                                        'Not sufficient alone to choose a confirmatory sample size.'],
                         'rows':rows},indent=2)+'\n',encoding='utf-8')
    else:
        with a.out.open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print('Design sensitivity table written:',a.out)

if __name__=='__main__':main()
