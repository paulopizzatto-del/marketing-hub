#!/usr/bin/env python3
"""Create 60 replayable prompts to test an actual model with the canonical skill."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'tests/fixtures/20-brands-3-rounds.json'
DEST=ROOT/'tests/fixtures/20-brands-model-prompts.jsonl'

def main():
    ds=json.loads(SOURCE.read_text(encoding='utf-8'))
    entries=[]
    for brand in ds['cases']:
        for task in ('instagram','linkedin','comment'):
            if task=='instagram':
                q=f"Use exclusivamente o perfil da marca {brand['display_name']} ({brand['brand_id']}). Crie uma legenda breve para Instagram relacionada ao serviço definido no perfil, para {brand['primary_audience']}. Respeite {brand['default_language']} e a identidade editorial. Não invente endereço, promoções, métricas nem depoimentos. Entregue apenas o texto da legenda."
            elif task=='linkedin':
                q=f"Use somente o perfil da marca {brand['display_name']} ({brand['brand_id']}). Escreva um post informativo para LinkedIn sobre um cuidado ou aspecto do setor {brand['sector']}, adequado a {brand['primary_audience']}. Respeite {brand['default_language']} e não afirme resultados ou certificações não documentados. Entregue um texto pronto."
            else:
                q=f"Você responde em nome da marca {brand['display_name']} ({brand['brand_id']}). Alguém comentou: 'Gostei do tema! O que devo observar primeiro?' Responda em 1-3 frases, com linguagem de {brand['default_language']} e tom da marca, sem inventar políticas, condições ou oferta nova."
            entries.append({'case_id':brand['brand_id']+'/'+task,'brand_id':brand['brand_id'],'task':task,'brand_profile_file':brand['profile_file'],'prompt':q,'expected_checks':['no other brand names','no forbidden terms','relevance to offer','no fabricated guarantees','consistent language','human editorial review']})
    if len(entries)!=60 or len(set(x['case_id'] for x in entries))!=60: raise ValueError('Unexpected number of test prompts')
    DEST.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in entries),encoding='utf-8')
    print(f'{len(entries)} prompts written to {DEST}')

if __name__=='__main__':
    main()
