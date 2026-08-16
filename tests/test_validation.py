import unittest

import numpy as np
import pandas as pd

from switch_inductor import evaluate_case, load_cases, repository_root


class ValidationTests(unittest.TestCase):
    def test_recomputed_tables_match_curated_results(self) -> None:
        root = repository_root()
        for case in load_cases().values():
            with self.subTest(case=case.case_id):
                recomputed, summary = evaluate_case(case)
                curated = pd.read_csv(
                    root / "results" / "tables" / f"{case.case_id}.csv"
                )
                self.assertEqual(list(recomputed.columns), list(curated.columns))
                self.assertTrue(
                    np.allclose(
                        recomputed.to_numpy(),
                        curated.to_numpy(),
                        rtol=1e-9,
                        atol=1e-9,
                    )
                )
                self.assertEqual(summary["samples"], 41)

    def test_all_validation_errors_are_small(self) -> None:
        for case in load_cases().values():
            with self.subTest(case=case.case_id):
                _, summary = evaluate_case(case)
                self.assertLess(summary["max_magnitude_error_db"], 0.04)
                self.assertLess(summary["max_phase_error_deg"], 0.22)

    def test_curated_figures_exist(self) -> None:
        figure_dir = repository_root() / "results" / "figures"
        for case_id in load_cases():
            with self.subTest(case=case_id):
                figure = figure_dir / f"{case_id}.png"
                self.assertTrue(figure.is_file())
                self.assertGreater(figure.stat().st_size, 10_000)


if __name__ == "__main__":
    unittest.main()
