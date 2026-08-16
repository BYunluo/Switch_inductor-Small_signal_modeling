# Small-Signal Validation Report

## Scope

Eight analytical transfer-function cases were compared with PLECS AC-sweep
exports. Each case contains 41 logarithmically spaced samples from 10 Hz to
100 Hz. The current repository recomputes every table from the equation module
and raw PLECS CSV rather than trusting a plot alone.

## Results

| Case | Max magnitude error (dB) | RMS magnitude error (dB) | Max phase error (deg) | RMS phase error (deg) |
|---|---:|---:|---:|---:|
| D1 → IL1, D1 > D2 | 0.000005733 | 0.000001974 | 0.180000055 | 0.084861 |
| D1 → IL1, D2 > D1 | 0.000007392 | 0.000002545 | 0.180000017 | 0.084861 |
| D1 → IL2, D1 > D2 | 0.000004889 | 0.000001473 | 0.180193143 | 0.084951 |
| D1 → IL2, D2 > D1 | 0.000903391 | 0.000394 | 0.172197965 | 0.082330 |
| D2 → IL1, D1 > D2 | 0.000006563 | 0.000002089 | 0.179884016 | 0.084806 |
| D2 → IL1, D2 > D1 | 0.039275397 | 0.016885 | 0.081206563 | 0.058488 |
| D2 → IL2, D1 > D2 | 0.000007382 | 0.000002542 | 0.180000028 | 0.084861 |
| D2 → IL2, D2 > D1 | 0.000005781 | 0.000001991 | 0.180000065 | 0.084861 |

The authoritative numeric values are in `results/validation_summary.csv`; this
table is rounded for readability.

## Reproducibility decision

Seven stored comparison tables matched the current saved equation scripts to
numerical precision. The original table for `D2 → IL1, D2 > D1` did not:

- the saved equation script had been modified several minutes after the old
  result was generated;
- recomputing from the current script changed the maximum magnitude error from
  approximately 0.0045 dB to 0.0393 dB;
- the current result still shows close analytical/PLECS agreement;
- this repository regenerated that case's table and figure from the current
  equation source so that code, data, and published output are consistent.

This is recorded as provenance, not hidden as a plotting difference.

## Deliberate parameter-variation test

The `D2 → IL1, D1 > D2` case uses `RB1 = RB2 = RB3 = 0.01 ohm`. Most other
cases use `0.0065 ohm`. This difference is intentional: it tests whether the
derived transfer function remains valid after changing the battery-resistance
parameters. The PLECS and Python models use the same values within each case,
and their close agreement provides evidence that the analytical expression is
not limited to one nominal resistance set.

## Remaining review work

- Assign every Python formula a stable handwritten equation identifier.
- Confirm the current-direction sign convention for negative operating-point
  currents in the `D2 > D1` cases.
- Record exact PLECS version, solver settings, export steps, and model run date.
- Expand the validation frequency range if the model is intended to support
  control-loop design near crossover.
