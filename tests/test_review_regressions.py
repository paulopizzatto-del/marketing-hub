"""Regression tests for the independent review. No LLM output is generated here."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from editorial_checks import assess_output, format_warnings, unresolved_review_flags
from evaluate_model_outputs import evaluate
from distribution import runtime_payload
from project_version import read_version
import install
import build_release

class EditorialRegression(unittest.TestCase):
    def setUp(self):
        self.brand={'brand_id':'review-example','display_name':'Marca de teste','forbidden_terms':['termo proibido']}
    def test_linkedin_1200_characters_is_not_rejected(self):
        text=('A equipe registra o contexto e a proxima acao. '*40)[:1200]
        self.assertEqual(1200,len(text))
        r=assess_output(self.brand,text,[],task='linkedin')
        self.assertEqual([],r['safety_errors']+r['review_flags']+r['format_warnings'])
    def test_english_without_fixture_keywords_is_not_rejected(self):
        text='Make room for the work that matters. Keep your next step visible, capture the details once, and give every decision enough context for the person who picks it up later.'
        self.assertFalse(any(w in text.casefold() for w in ('tasks','team','workflow')))
        r=assess_output(dict(self.brand,default_language='en-US'),text,[],task='instagram')
        self.assertEqual([],r['safety_errors']+r['review_flags']+r['format_warnings'])
    def test_unprovided_percentage_before_space_is_flagged(self):
        r=assess_output(self.brand,'A produtividade aumentou 99% com o produto.')
        self.assertIn('unverified_percentage',[f['code'] for f in r['review_flags']])
    def test_percent_at_end_and_decimal_are_flagged(self):
        for text in ('Ganhe 99%','Taxa de 2,6%.','Share: 2.6%'):
            self.assertTrue(assess_output(self.brand,text)['review_flags'])
    def test_exact_confirmed_statement_is_allowed_with_source(self):
        claim='A taxa registrada foi 2,6%.'
        record=dict(self.brand,confirmed_claims=[{'text':claim,'source':'approved-test-brief'}])
        self.assertEqual([],assess_output(record,claim)['review_flags'])
        self.assertTrue(assess_output(record,'A taxa registrada foi 99%.')['review_flags'])
    def test_absolute_claim_needs_context_review(self):
        r=assess_output(self.brand,'Nosso produto tem resultado garantido.')
        self.assertIn('absolute_claim',[f['code'] for f in r['review_flags']])
    def test_credential_signal_is_hard_error(self):
        r=assess_output(self.brand,'sk-proj-'+'a'*30)
        self.assertIn('possible_secret',[f['code'] for f in r['safety_errors']])
        self.assertNotIn('a'*30,str(r))
    def test_brand_leakage_and_explicit_allowlist(self):
        other={'brand_id':'another-brand','display_name':'Outra Marca'}
        self.assertTrue(assess_output(self.brand,'Falamos de Outra Marca.',[other])['safety_errors'])
        self.assertFalse(assess_output(dict(self.brand,allowed_brand_mentions=['another-brand']),'Falamos de Outra Marca.',[other])['safety_errors'])
    def test_explicit_forbidden_term_is_hard_error(self):
        self.assertTrue(assess_output(self.brand,'Aqui existe um termo proibido.')['safety_errors'])
    def test_lengths_warn_without_hard_failure(self):
        r=assess_output(self.brand,'Texto longo. '*400,task='linkedin')
        self.assertFalse(r['safety_errors']);self.assertTrue(r['format_warnings'])
    def test_no_universal_hashtag_limit(self):
        text='Uma explicacao concreta para o publico. #um #dois #tres #quatro'
        self.assertFalse(format_warnings('instagram',text))
        self.assertTrue(format_warnings('instagram',text,{'max_hashtags':3}))
    def test_flags_require_exact_id_and_evidence(self):
        flags=assess_output(self.brand,'99%')['review_flags']
        self.assertEqual(flags,unresolved_review_flags(flags,[]))
        decision={'id':flags[0]['id'],'decision':'accepted','reason':'Dado fornecido no briefing','evidence':'fixture de teste'}
        self.assertFalse(unresolved_review_flags(flags,[decision]))
        other=assess_output(self.brand,'98%')['review_flags']
        self.assertEqual(other,unresolved_review_flags(other,[decision]))
    def test_real_evaluator_does_not_import_tests(self):
        text=(ROOT/'scripts/evaluate_model_outputs.py').read_text()
        self.assertNotIn('from test_',text);self.assertNotIn("ROOT/'tests'",text)
    def test_malformed_results_fail_cleanly(self):
        cases=[self.brand]
        for rows in ([None], [{'case_id':[]}], 'not a list'):
            self.assertNotEqual('PASS_RECORD_CHECKS',evaluate(rows,cases)['status'])
    def test_format_warning_alone_does_not_fail_reviewed_records(self):
        rows=[{'case_id':'review-example/'+task,'output':'Texto sem numeros. '*400,'human_approved':True} for task in ('instagram','linkedin','comment')]
        r=evaluate(rows,[self.brand]);self.assertEqual('PASS_RECORD_CHECKS',r['status'])
        self.assertTrue(any(x['format_warnings'] for x in r['records']))
    def test_missing_unreviewed_duplicate_and_claim_records_fail(self):
        rows=[{'case_id':'review-example/'+t,'output':'Texto de exemplo para a marca.','human_approved':True} for t in ('instagram','linkedin','comment')]
        self.assertEqual('PASS_RECORD_CHECKS',evaluate(rows,[self.brand])['status'])
        self.assertTrue(evaluate(rows[:1],[self.brand])['errors'])
        self.assertTrue(evaluate(rows+rows[:1],[self.brand])['errors'])
        rows[0]['output']='Aumente sua produtividade em 99%.'
        self.assertTrue(evaluate(rows,[self.brand])['errors'])
        rows[0]['human_approved']=False
        self.assertIn('approval missing',str(evaluate(rows,[self.brand])['errors']))

class DistributionRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls): build_release.build()
    def test_lean_runtime_under_limit(self):
        path=ROOT/'dist/skill.zip'
        self.assertLess(path.stat().st_size,120000)
        with ZipFile(path) as z:
            names=z.namelist()
            self.assertFalse(any(n.endswith(('.png','.svg','.jpg','.woff','.ttf')) for n in names))
            self.assertFalse(any('/tests/' in n or n.endswith(('AUDIT.md','CHANGELOG.md','README.md','selftest.py')) for n in names))
            self.assertIn('marketinghub/agents/openai.yaml',names)
            self.assertEqual(read_version(),z.read('marketinghub/VERSION').decode().strip())
    def test_install_matches_archive_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            t=install.install('claude','project',Path(tmp))
            actual={p.relative_to(t).as_posix():p.read_bytes() for p in t.rglob('*') if p.is_file()}
            self.assertEqual(runtime_payload(),actual)
    def test_force_preserves_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            t=install.install('claude','project',Path(tmp));(t/'personal-note.txt').write_text('keep me')
            install.install('claude','project',Path(tmp),force=True)
            backups=list(t.parent.glob('.marketinghub-backup-*'))
            self.assertEqual(1,len(backups));self.assertEqual('keep me',(backups[0]/'personal-note.txt').read_text())
            self.assertFalse((t/'personal-note.txt').exists())
    def test_failed_staging_keeps_previous_installation(self):
        with tempfile.TemporaryDirectory() as tmp:
            t=install.install('claude','project',Path(tmp)); original=(t/'SKILL.md').read_bytes()
            with mock.patch('pathlib.Path.write_bytes',side_effect=OSError('test failure')):
                with self.assertRaises(OSError):install.install('claude','project',Path(tmp),force=True)
            self.assertEqual(original,(t/'SKILL.md').read_bytes())
    def test_symlink_target_and_ancestor_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
            base=Path(tmp); (base/'.claude').symlink_to(outside,target_is_directory=True)
            with self.assertRaises(RuntimeError):install.install('claude','project',base,force=True)
    def test_zip_is_deterministic(self):
        names=['skill.zip','marketing-hub-plugin.zip','marketing-hub-repository.zip']
        before={n:hashlib.sha256((ROOT/'dist'/n).read_bytes()).hexdigest() for n in names}
        build_release.build()
        self.assertEqual(before,{n:hashlib.sha256((ROOT/'dist'/n).read_bytes()).hexdigest() for n in names})
    def test_build_excludes_private_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'scripts').mkdir();(root/'private').mkdir()
            (root/'private/card.json').write_text('private');(root/'scripts/user.secret.json').write_text('private')
            (root/'.env').write_text('test');(root/'scripts/legitimate.py').write_text('pass')
            self.assertEqual(['scripts/legitimate.py'],[p.relative_to(root).as_posix() for p in build_release.repository_files(root)])
    def test_plugin_has_asset_license_without_retired_graphics(self):
        with ZipFile(ROOT/'dist/marketing-hub-plugin.zip') as z:
            self.assertIn('BRAND-ASSETS-LICENSE.md',z.namelist())
            self.assertEqual(['assets/marketinghub-icon.png'],[n for n in z.namelist() if n.endswith(('.png','.svg'))])
    def test_version_is_not_hardcoded_in_checker(self):
        text=(ROOT/'scripts/check_repo.py').read_text()
        self.assertIn('read_version',text);self.assertNotIn("'2.3.0'",text);self.assertNotIn("'2.3.1'",text)
    def test_front_page_not_promotional_contract_score(self):
        text=(ROOT/'README.md').read_text().split('## Contribuir e verificar')[0]
        self.assertNotIn('60',text);self.assertNotIn('20 perfis',text);self.assertNotIn('17 m',text)
    def test_language_and_injection_rules_are_present(self):
        text=(ROOT/'skills/marketinghub/SKILL.md').read_text()
        self.assertIn('idioma de sua \u00faltima mensagem',text)
        self.assertIn('como dados',text)
        self.assertNotIn('usar portugu\u00eas brasileiro',text.lower())
    def test_full_schema_rejects_invalid_optional_field(self):
        sys.path.insert(0,str(ROOT/'skills/marketinghub/scripts'))
        from validate_brand_profile import validate_profile
        if importlib.util.find_spec('jsonschema') is None: self.skipTest('Full schema dependency absent')
        obj=json.loads((ROOT/'examples/brand-profile-ficticio.json').read_text());obj['channels']=[123]
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'bad.json';p.write_text(json.dumps(obj))
            _,errors,_=validate_profile(p,require_full=True);self.assertTrue(errors)
    def test_required_full_mode_cannot_silently_fallback(self):
        cmd=[sys.executable,'-S',str(ROOT/'skills/marketinghub/scripts/validate_brand_profile.py'),
             '--require-full',str(ROOT/'examples/brand-profile-ficticio.json')]
        r=subprocess.run(cmd,capture_output=True,text=True)
        self.assertEqual(1,r.returncode);self.assertIn('completa requerida',r.stdout)
if __name__=='__main__':unittest.main()
