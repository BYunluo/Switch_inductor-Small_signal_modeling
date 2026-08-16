# Equation Modules

Each module exposes one explicit analytical transfer function so that the
engineering expressions remain auditable rather than hidden behind a generic
fitting routine.

| Module | Input | Output | Operating region |
|---|---|---|---|
| `d1_to_il1__d1_gt_d2.py` | D1 | IL1 | D1 > D2 |
| `d1_to_il1__d2_gt_d1.py` | D1 | IL1 | D2 > D1 |
| `d1_to_il2__d1_gt_d2.py` | D1 | IL2 | D1 > D2 |
| `d1_to_il2__d2_gt_d1.py` | D1 | IL2 | D2 > D1 |
| `d2_to_il1__d1_gt_d2.py` | D2 | IL1 | D1 > D2 |
| `d2_to_il1__d2_gt_d1.py` | D2 | IL1 | D2 > D1 |
| `d2_to_il2__d1_gt_d2.py` | D2 | IL2 | D1 > D2 |
| `d2_to_il2__d2_gt_d1.py` | D2 | IL2 | D2 > D1 |

The configuration file at
[`../../../configs/validation_cases.toml`](../../../configs/validation_cases.toml)
connects these modules to their PLECS models and raw CSV exports. Stable
handwritten equation identifiers will be added as the derivation PDFs grow.
