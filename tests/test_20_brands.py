"""20 synthetic brands x 3 authored responses = 60 offline editorial smoke tests.

No live model is called: examples test the editorial contract and profile data
safety, NOT cross-provider LLM quality. A real-model gate remains separate.
"""
from __future__ import annotations
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'marketinghub'
sys.path.insert(0, str(SKILL / 'scripts'))
from validate_brand_profile import validate_profile

DATASET = ROOT / 'tests' / 'fixtures' / '20-brands-3-rounds.json'
REGULATED = {'sorriso-de-jade', 'cofre-de-cha'}
FICTITIOUS = {'sample', 'synthetic', 'fictional', 'fictício'}
BANNED_IMPLIED = (
  'somos número 1', 'número um do mercado', 'resultado garantido',
  'rendimento garantido', 'aprovação garantida', 'ganho garantido',
  'risco zero', 'crescimento garantido', 'dobre suas vendas',
)

def errors_for_output(record, candidate, brands):
    """Objective smoke criteria only, deliberately not a subjective AI quality score."""
    problems=[]
    content=candidate['content']
    casefold=content.casefold()
    if not (65 <= len(content) <= 520):
        problems.append('Tamanho fora da faixa editorial de teste 65-520 caracteres')
    if not any(term.casefold() in casefold for term in record['relevance_terms']):
        problems.append('Nenhum vocábulo do assunto definido no briefing')
    if any(term.casefold() in casefold for term in record['forbidden_terms']):
        problems.append('Termo proibido da marca')
    if any(term in casefold for term in BANNED_IMPLIED):
        problems.append('Promessa absoluta sem comprovação')
    if re.search(r'\b\d{1,3}\s*%\b', content):
        problems.append('Número de desempenho não fornecido')
    if len(re.findall(r'#[A-Za-zÀ-ÖØ-öø-ÿ_]+', content)) > 3:
        problems.append('Mais de três hashtags')
    if content.strip().startswith(('#', '- ', '* ', '1.')):
        problems.append('Formato de lista aplicado a texto corrido')
    for b in brands:
        if b['brand_id'] != record['brand_id'] and b['display_name'].casefold() in casefold:
            problems.append(f'Contaminação: inclui outra marca ({b["brand_id"]})')
    if record['brand_id'] in REGULATED and any(term in casefold for term in ('garantimos', 'sem riscos', 'invista agora', 'cura certa')):
        problems.append('Alegação inadequada para setor regulado')
    if record['default_language'] == 'en-US' and not any(s in casefold for s in ('tasks', 'team', 'workflow')):
        problems.append('Amostra em inglês sem vocabulário temático')
    if record['default_language'] == 'es-MX' and not any(s in casefold for s in ('español', 'conversación', 'hablar')):
        problems.append('Amostra em espanhol sem vocabulário temático')
    return problems

class TwentyBrandMatrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset=json.loads(DATASET.read_text(encoding='utf-8'))
        cls.cases=cls.dataset['cases']

    def test_20_distinct_synthetic_profiles(self):
        self.assertEqual(20,len(self.cases))
        self.assertEqual(20,len({c['brand_id'] for c in self.cases}))
        self.assertEqual(20,len({c['display_name'] for c in self.cases}))
        for case in self.cases:
            with self.subTest(brand=case['brand_id']):
                p=ROOT/case['profile_file']
                data, errors, warnings=validate_profile(p)
                self.assertEqual([],errors, msg=f'{case["brand_id"]}: {errors}')
                self.assertEqual('operational',data['profile_status'])
                self.assertIn('fictícia',data['description'])
                self.assertEqual(case['brand_id'],data['brand_id'])
                self.assertEqual(case['default_language'],data['default_language'])
                self.assertTrue(data['offers'])
                self.assertTrue(data['voice']['sample_rules'])
                self.assertNotIn('cliente real',str(data).lower())

    def test_60_offline_editorial_smoke_samples(self):
        tested=0
        for case in self.cases:
            samples=case['outputs']
            self.assertEqual(['instagram','linkedin','comment'],[x['task'] for x in samples])
            self.assertEqual(3,len({x['content'] for x in samples}))
            for sample in samples:
                tested+=1
                with self.subTest(brand=case['brand_id'],round=sample['task']):
                    self.assertEqual([],errors_for_output(case,sample,self.cases))
        self.assertEqual(60,tested)

    def test_60_rounds_preserve_brand_id_and_isolation(self):
        # For every round, the selected profile is stable; other profiles remain distinct.
        for i,case in enumerate(self.cases):
            first=json.loads((ROOT/case['profile_file']).read_text(encoding='utf-8'))
            for sample in case['outputs']:
                with self.subTest(brand=case['brand_id'],round=sample['task']):
                    loaded=json.loads((ROOT/case['profile_file']).read_text(encoding='utf-8'))
                    self.assertEqual(first,loaded)
                    self.assertNotIn('SKILL.md',sample['content'])
                    self.assertNotIn('sk-proj-',sample['content'])
                    self.assertTrue(all(b['brand_id']!=case['brand_id'] for b in self.cases[i+1:]))

    def test_60_model_trial_prompts_ready_for_real_execution(self):
        file=ROOT/'tests/fixtures/20-brands-model-prompts.jsonl'
        prompts=[json.loads(line) for line in file.read_text(encoding='utf-8').splitlines() if line.strip()]
        self.assertEqual(60,len(prompts))
        self.assertEqual(60,len({p['case_id'] for p in prompts}))
        allowed={b['brand_id'] for b in self.cases}
        for item in prompts:
            with self.subTest(case=item['case_id']):
                self.assertIn(item['brand_id'],allowed)
                self.assertIn(item['brand_id'],item['case_id'])
                self.assertTrue((ROOT/item['brand_profile_file']).is_file())
                self.assertIn(item['brand_id'],item['prompt'])

    def test_real_model_gate_rejects_incomplete_or_unreviewed_outputs(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'partial.jsonl'
            path.write_text(json.dumps({'case_id':self.cases[0]['brand_id']+'/instagram', 'output':'Short generic sample', 'human_approved':False}),encoding='utf-8')
            command=[sys.executable,str(ROOT/'scripts/evaluate_model_outputs.py'), '--results',str(path),'--provider','Offline fixture', '--model-version','not-real']
            completed=subprocess.run(command,text=True,capture_output=True)
            self.assertEqual(1,completed.returncode)
            self.assertIn('Missing 59',completed.stdout)
            self.assertIn('approval missing',completed.stdout)

    def test_safety_negative_mutations_get_caught(self):
        case=self.cases[0]
        sample=case['outputs'][0]
        altered=dict(sample, content=sample['content']+' '+self.cases[1]['display_name'])
        self.assertTrue(any('Contaminação' in x for x in errors_for_output(case,altered,self.cases)))
        altered=dict(sample, content=sample['content']+' '+case['forbidden_terms'][0])
        self.assertIn('Termo proibido da marca',errors_for_output(case,altered,self.cases))
        altered=dict(sample, content=sample['content']+' Somos número 1.')
        self.assertIn('Promessa absoluta sem comprovação',errors_for_output(case,altered,self.cases))
        original=json.loads((ROOT/case['profile_file']).read_text(encoding='utf-8'))
        original['voice']['approved_examples']=['sk-proj-'+'a'*25]
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'injected.json'; path.write_text(json.dumps(original),encoding='utf-8')
            _,err,_=validate_profile(path)
            self.assertTrue(any('credencial' in x for x in err))
        original['voice']['approved_examples']=[]
        original['voice']['formality']=9
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'invalid.json';path.write_text(json.dumps(original),encoding='utf-8')
            _,err,_=validate_profile(path)
            self.assertTrue(any('formality' in x for x in err))

if __name__=='__main__':
    unittest.main()
