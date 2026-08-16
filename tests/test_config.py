import unittest

from switch_inductor import load_cases


class ConfigurationTests(unittest.TestCase):
    def test_all_eight_cases_are_configured(self) -> None:
        cases = load_cases()
        self.assertEqual(len(cases), 8)
        self.assertEqual(
            {(case.input_name, case.output_name) for case in cases.values()},
            {
                ("D1", "IL1"),
                ("D1", "IL2"),
                ("D2", "IL1"),
                ("D2", "IL2"),
            },
        )
        self.assertEqual(
            {case.region for case in cases.values()}, {"D1 > D2", "D2 > D1"}
        )

    def test_all_configured_inputs_exist(self) -> None:
        for case in load_cases().values():
            self.assertTrue(case.plecs_csv.is_file(), case.plecs_csv)
            self.assertTrue(case.plecs_model.is_file(), case.plecs_model)

    def test_plecs_ac_sweep_matches_case_definition(self) -> None:
        perturbation_markers = {
            "D1": 'Perturbation  "D1\'"',
            "D2": 'Perturbation  base64 "RDLigJg="',
        }
        for case in load_cases().values():
            with self.subTest(case=case.case_id):
                model_text = case.plecs_model.read_text(encoding="utf-8")
                self.assertIn("Type          ACSweep", model_text)
                self.assertIn(perturbation_markers[case.input_name], model_text)
                self.assertIn(f'Response      "{case.output_name}"', model_text)


if __name__ == "__main__":
    unittest.main()
