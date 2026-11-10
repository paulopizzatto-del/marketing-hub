import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import install

class MarketingHubTests(unittest.TestCase):
    def test_brand_profile_example_valid(self):
        command = [sys.executable, str(ROOT / 'skills/marketinghub/scripts/validate_brand_profile.py'), str(ROOT / 'examples/brand-profile-ficticio.json')]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)

    def test_bad_profile_rejected(self):
        command = [sys.executable, str(ROOT / 'skills/marketinghub/scripts/validate_brand_profile.py'), str(ROOT / 'skills/marketinghub/tests/brand-profile.invalid.json')]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)

    def test_install_project_targets_and_existing_guard(self):
        with tempfile.TemporaryDirectory() as t:
            path = Path(t)
            for platform in install.LOCATIONS:
                target = install.install(platform, 'project', path)
                self.assertTrue((target / 'SKILL.md').is_file())
                with self.assertRaises(FileExistsError):
                    install.install(platform, 'project', path)
                replaced = install.install(platform, 'project', path, force=True)
                self.assertTrue((replaced / 'SKILL.md').is_file())

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as t:
            path = Path(t)
            result = install.install('gemini', 'project', path, dry_run=True)
            self.assertFalse(result.exists())

    def test_one_canonical_skill(self):
        skills = [p for p in ROOT.rglob('SKILL.md') if not any(hidden in p.relative_to(ROOT).parts for hidden in ('.agents','.claude','.gemini','.copilot')) and p.relative_to(ROOT).parts[:3] != ('.github','skills','marketinghub')]
        self.assertEqual([s.relative_to(ROOT).as_posix() for s in skills], ['skills/marketinghub/SKILL.md'])

    def test_release_archives_integrity(self):
        subprocess.run([sys.executable, str(ROOT / 'scripts/build_release.py')], check=True, capture_output=True)
        for filename in ('skill.zip', 'marketing-hub-plugin.zip', 'marketing-hub-repository.zip'):
            with ZipFile(ROOT/'dist'/filename) as bundle:
                self.assertIsNone(bundle.testzip())
                paths = bundle.namelist()
                self.assertTrue(any(p.endswith('SKILL.md') for p in paths))
                self.assertEqual(sum(p.endswith('SKILL.md') for p in paths), 1)

    def test_visual_assets_match_user_provided_manifest(self):
        import hashlib
        manifest = json.loads((ROOT / 'assets/ASSET-PROVENANCE.json').read_text(encoding='utf-8'))
        rows = manifest['assets']
        files = {row['file'] for row in rows}
        actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
                  if p.is_file() and p.suffix.lower() in {'.png', '.svg', '.jpg', '.jpeg', '.webp'}
                  and 'dist' not in p.relative_to(ROOT).parts}
        self.assertEqual(files, actual)
        for row in rows:
            img = ROOT / row['file']
            self.assertEqual(hashlib.sha256(img.read_bytes()).hexdigest(), row['sha256'])
        self.assertIn('assets/archive/v2.3.0/banner.png', files)
        self.assertIn('assets/archive/v2.3.0/social-preview-1280x640.png', files)

    def test_readme_visual_assets_and_no_placeholders(self):
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('src="assets/brand/marketinghub-horizontal.png"', readme)
        self.assertNotIn('src="assets/banner.png"', readme)
        self.assertNotIn('[AJUSTAR', readme)
        self.assertNotIn('URL_DO_REPOSITORIO', readme)

    def test_official_release_documentation(self):
        paths = (
            'README.md', 'README.en.md', 'CHANGELOG.md',
            
            'docs/index.html', 'docs/lancamento-publico.md',
            'docs/publicacao-no-github.md', 'docs/plano-de-testes.md',
            'docs/testes-reais-com-modelos.md', 'docs/qa-20-marcas.md',
        )
        for relpath in paths:
            with self.subTest(path=relpath):
                content = (ROOT / relpath).read_text(encoding='utf-8').lower()
                self.assertNotIn('beta', content)
                self.assertNotIn('v2.3.0-beta.1', content)
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('/releases/latest', readme)
        self.assertTrue((ROOT / 'docs/demonstracao.md').is_file())

    def test_product_description_not_automatic_publisher(self):
        text = (ROOT / 'README.md').read_text(encoding='utf-8').lower()
        self.assertTrue('n\u00e3o' in text or 'nao' in text)
        self.assertIn('prompt', text)

if __name__ == '__main__':
    unittest.main()
