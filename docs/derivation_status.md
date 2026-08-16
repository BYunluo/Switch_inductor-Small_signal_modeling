# Derivation Status and Traceability

The analytical expressions in `src/switch_inductor/equations/` came from the
project's handwritten modeling work. The numerical implementation and PLECS
validation cover all eight cases; the handwritten transfer-function document
currently contains only part of the final derivation set and will be expanded
as a later project update. This documentation work does not block the current
numerical validation evidence.

## Document sequence

| Stage | Source document | Current repository status |
|---|---|---|
| Large-signal model | `derivations/01_large_signal_model.pdf` | Source PDF retained; typed transcription pending |
| Averaged model | `derivations/02_averaged_model.pdf` | Source PDF retained; region-by-region typed summary pending |
| State-space equations | `derivations/03_state_space_equations.pdf` | Source PDF retained; notation table and matrix transcription pending |
| Transfer functions | `derivations/04_transfer_functions.pdf` | Partial handwritten set; remaining channels to be added |

## Case matrix

| Case | Python expression | PLECS model/data | Handwritten equation identifier |
|---|---:|---:|---|
| D1 → IL1, D1 > D2 | Complete | Validated | To be assigned |
| D1 → IL1, D2 > D1 | Complete | Validated | To be assigned |
| D1 → IL2, D1 > D2 | Complete | Validated | To be assigned |
| D1 → IL2, D2 > D1 | Complete | Validated | To be assigned |
| D2 → IL1, D1 > D2 | Complete | Validated | To be assigned |
| D2 → IL1, D2 > D1 | Complete | Validated | To be assigned |
| D2 → IL2, D1 > D2 | Complete | Validated | To be assigned |
| D2 → IL2, D2 > D1 | Complete | Validated | To be assigned |

## Recommended update procedure

1. Give every handwritten state-space and transfer-function equation a stable
   identifier such as `SS-A-01` or `TF-D2-IL1-B`.
2. Record the PDF page and equation identifier in the corresponding Python
   module docstring.
3. Add a typed notation table defining signs, current directions, duty ratios,
   and perturbation variables.
4. Re-run `python scripts/run_validation.py` after changing any equation.
5. Run the unit tests and review the changed error metrics before committing.

This matrix should be updated as the handwritten derivation is completed. It
must not mark a formula as documented solely because its Python implementation
exists.
