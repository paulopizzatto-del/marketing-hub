"""20 synthetic brands x 3 authored responses = 60 authored contract fixtures.

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
sys.path.insert(0,str(ROOT/'scripts'))
from editorial_checks import assess_output

def errors_for_output(record, candidate, brands):
    """Compatibility wrapper for authored fixture contracts, not model quality."""
    result=assess_output(record,candidate['content'],brands,candidate['task'])
    names={'brand_leakage':'Contamina\u00e7\u00e3o: marca diferente',
           'forbidden_term':'Termo proibido da marca',
           'absolute_claim':'Promessa absoluta sem comprova\u00e7\u00e3o'}
    return [names.get(x['code'],x['detail']) for x in result['safety_errors']+[f for f in result['review_flags'] if f['code'] in {'absolute_claim'}]]

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

    def test_60_authored_contract_fixtures(self):
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
            command=[sys.executable,str(ROOT/'scripts/evaluate_model_outputs.py'), '--results',str(path),'--cases',str(ROOT/'tests/fixtures/20-brands-3-rounds.json'),'--provider','Offline fixture', '--model-version','not-real']
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
