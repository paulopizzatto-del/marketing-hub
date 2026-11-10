import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from prepare_pilot import schedule,input_errors
class PilotPlanTests(unittest.TestCase):
    def test_exact_144_unique_trials_and_no_results(self):
        data=schedule();self.assertEqual(144,len(data['trials']));self.assertEqual(144,len({x['case_id'] for x in data['trials']}))
        self.assertEqual(0,data['actual_outputs']);self.assertTrue(all(x['status']=='not_run' for x in data['trials']))
        for condition in ('A','B','C'):self.assertEqual(48,sum(x['condition']==condition for x in data['trials']))
    def test_randomization_is_reproducible(self):
        self.assertEqual(schedule(1),schedule(1));self.assertNotEqual(schedule(1)['trials'],schedule(2)['trials'])
    def test_empty_human_template_cannot_pass(self):
        t=json.loads((ROOT/'evaluation/pilot-144/brands.template.json').read_text())
        self.assertTrue(input_errors(t))
