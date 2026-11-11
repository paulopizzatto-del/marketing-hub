"""No real brand/LLM/human result is created; synthetic software checks only."""
from __future__ import annotations
import csv, json, sys, tempfile, unittest
from pathlib import Path
from argparse import Namespace
ROOT=Path(__file__).resolve().parents[1]
LAB=ROOT/'evaluation'/'lab50'
sys.path.insert(0,str(LAB))
import lab,lab_shard,human_study

class Study50Tests(unittest.TestCase):
    def synthetic_brands(self,n):
        return {'brands':[{'brand_id':f'brand-{i:03}', 'brand_brief':'Esta é uma marca totalmente fictícia. Serve exclusivamente a testes de sistema e não é evidência editorial de uma empresa.',
            'approved_samples':[f'Amostra visível fictícia {i}-{j}: texto gerado pelo desenvolvedor somente para exercitar software e estrutura de um formulário de briefing. '*2 for j in range(3)],
            'held_out_references':[f'REF_HOLDOUT_{i}_{j} Texto reservado fictício usado para testar vazamento; nunca enviado ao gerador. '*2 for j in range(3)],
            'voice_card':'Fala de modo direto, usa frases curtas e fatos claramente confirmados. Não usa slogans inventados; preserva a situação do leitor e oferece orientações precisas.',
            'human_approved_by':'SYNTHETIC_TEST_ONLY','human_approved_at':'2026-11-11','permission_to_use':True,
            'tasks':{k:('Teste sintético, sem relação com empresas reais: escreva um texto seguro sobre tema fictício do tipo '+k+' sem dados de desempenho.') for k in lab.TASKS}}
            for i in range(1,n+1)]}
    def prepare(self,t,n):
        p=t/'brands.json';lab.write_json(p,self.synthetic_brands(n));out=t/'private'
        lab.prepare(Namespace(brands=p,skill_root=ROOT/'skills/marketinghub',out=out,seed=43,brand_count=n))
        return out
    def test_empty_templates_rejected(self):
        inp=lab.load_json(LAB/'brands.50.template.json');self.assertEqual(50,len(inp['brands']))
        self.assertEqual(50,len({x['brand_id'] for x in inp['brands']}))
        self.assertTrue(lab.validate_brands(inp,expected_brands=50))
        self.assertEqual(10,len(lab.CORE_TASKS));self.assertEqual(4,len(lab.STRESS_TASKS))
    def test_50_brand_3600_prompt_generation_and_heldouts(self):
        with tempfile.TemporaryDirectory() as d:
            out=self.prepare(Path(d),50)
            m=lab.load_json(out/'manifest.private.json')
            self.assertEqual(3600,m['planned_outputs']);self.assertEqual(0,m['actual_outputs'])
            self.assertEqual('INTEGRITY_OK',lab.experiment_audit(out)['status'])
            self.assertEqual(600,len([x for x in m['trials'] if x['task'] in lab.STRESS_TASKS]))
            for arm in 'ABC':
                p=out/'prompts'/f'brand-001--landing--r1--{arm}.txt'
                text=p.read_text(encoding='utf-8');self.assertNotIn('REF_HOLDOUT',text)
                self.assertEqual(arm in 'BC','CARTÃO DE VOZ (preparado' in text)
                self.assertEqual(arm=='C','INSTRUÇÕES ADICIONAIS DA SKILL MARKETING HUB' in text)
            with self.assertRaises(ValueError):lab.build_blind(Namespace(experiment=out,out=Path(d)/'blind',seed=44))
    def test_integrity_tamper_detected(self):
        with tempfile.TemporaryDirectory() as d:
            t=Path(d);out=self.prepare(t,10)
            target=out/'prompts'/'brand-001--email--r1--B.txt';target.write_text(target.read_text()+'\nALTERADO')
            self.assertTrue(lab.experiment_audit(out)['problems'])
    def test_full_mock_blinding_and_sharding(self):
        with tempfile.TemporaryDirectory() as d:
            t=Path(d);out=self.prepare(t,10);m=lab.load_json(out/'manifest.private.json');meta={}
            for row in m['trials']:
                case=row['case_id'];p=out/'responses'/(case+'.txt')
                p.write_text('Amostra sintética apenas para testar a integridade e o cegamento. Esta não é uma resposta de modelo real. '+lab.sha256(case.encode())[:12]+'\n',encoding='utf-8')
                meta[case]={'provider':'TEST_ONLY','model':'MOCK','temperature':0.2,'generation_date':'2026-11-11T15:00:00Z','sha256':lab.sha256(p.read_bytes())}
            m.update(provider='TEST_ONLY',model_version='MOCK',temperature=0.2,actual_outputs=len(meta),status='TEST_ONLY')
            lab.write_json(out/'manifest.private.json',m);lab.write_json(out/'capture_metadata.private.json',meta)
            self.assertEqual('INTEGRITY_OK',lab.experiment_audit(out,require_complete=True)['status'])
            blind=t/'blind';lab.build_blind(Namespace(experiment=out,out=blind,seed=45))
            self.assertEqual(600,len(lab.load_json(blind/'answers_DO_NOT_SHARE_WITH_REVIEWERS.json')))
            shards=t/'shards';lab_shard.make(blind,shards,20)
            plan=lab.load_json(shards/'SHARD_ASSIGNMENT_PRIVATE.json')
            self.assertEqual(1200,sum(len(x) for x in plan['assignment'].values()))
            with self.assertRaises(ValueError):lab_shard.merge(blind,shards)
            for worker in plan['assignment']:
                p=shards/worker/'judgments.csv'
                with p.open(encoding='utf-8') as rf:rows=list(csv.DictReader(rf))
                for row in rows:row['choice']='left'
                with p.open('w',encoding='utf-8',newline='') as f:
                    w=csv.DictWriter(f,fieldnames=['pair_id','reviewer_id','choice','notes']);w.writeheader();w.writerows(rows)
            lab_shard.merge(blind,shards);res=t/'analysis.json'
            lab.analyze(Namespace(blind=blind,out=res))
            result=lab.load_json(res);self.assertEqual(1200,result['n_votes']);self.assertEqual(600,result['n_pairs'])
            self.assertEqual(20,result['n_reviewers_declared'])
            self.assertEqual(10,sum(result['contrasts']['BC']['brand_direction'].values()))
    def test_human_assignment_balanced_and_consent_gated(self):
        with tempfile.TemporaryDirectory() as d:
            t=Path(d);inp=t/'people.json'
            roster={'participants':[{'participant_id':f'P{i:03}','role':'redator' if i%2 else 'designer','experience':'senior' if i%3 else 'junior','consent_confirmed':True} for i in range(1,251)]}
            inp.write_text(json.dumps(roster),encoding='utf-8');human_study.assign(inp,t/'study',seed=100)
            manifest=lab.load_json(t/'study'/'manifest.private.json')
            self.assertEqual([50]*5,sorted(manifest['n_by_arm'].values()))
            inp.write_text(json.dumps({'participants':[{'participant_id':'P001','consent_confirmed':False}]}),encoding='utf-8')
            with self.assertRaises(ValueError):human_study.assign(inp,t/'bad',seed=100)
if __name__=='__main__':unittest.main()
