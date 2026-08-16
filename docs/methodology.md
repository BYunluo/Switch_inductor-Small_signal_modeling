# Modeling and Validation Methodology

## 1. System definition

The original model is retained at
`models/simulink/switch_inductor_system.slx`. It contains the switching power
stage and the associated digital control logic. The PLECS cases isolate the
small-signal behavior required for frequency-domain verification.

The public documentation should eventually define:

- positive current directions for `IL1` and `IL2`;
- voltage polarities and source numbering;
- the definitions of duty ratios `D1` and `D2`;
- the switching-state sequence in both duty-ratio regions;
- the operating point used for each validation case.

## 2. Piecewise averaged model

The averaged equations differ between `D1 > D2` and `D2 > D1`. This region
split is preserved explicitly throughout the repository instead of hiding it
behind one opaque formula.

For each region, the intended analytical sequence is:

1. enumerate the switching intervals;
2. write the inductor-voltage equations for each interval;
3. average the equations over one switching period;
4. solve the DC operating-point equations for `IL1` and `IL2`;
5. perturb state and duty variables around the operating point;
6. retain first-order terms to obtain the small-signal state-space model;
7. derive the requested duty-to-current transfer function.

The handwritten source documents are indexed in `derivation_status.md`.

## 3. Validation channels

The implementation evaluates four channels in both operating regions:

```text
G_IL1,D1(s) = iL1_hat(s) / d1_hat(s)
G_IL2,D1(s) = iL2_hat(s) / d1_hat(s)
G_IL1,D2(s) = iL1_hat(s) / d2_hat(s)
G_IL2,D2(s) = iL2_hat(s) / d2_hat(s)
```

These equations are notation only; the full case-dependent expressions remain
in the explicit equation modules until the handwritten derivation is complete.

## 4. Numerical comparison

For every case, the shared validation pipeline:

1. validates the hard-coded physical parameters;
2. solves the two DC operating-point equations;
3. reads the matching three-column PLECS export;
4. evaluates the analytical transfer function at the PLECS frequencies;
5. computes magnitude and unwrapped phase;
6. writes point-by-point magnitude and phase errors;
7. generates a combined Bode comparison plot;
8. records maximum and RMS errors in a summary table.

The raw CSV column order is:

```text
frequency in Hz, magnitude in dB, phase in degrees
```

PLECS export headings are not treated as stable API fields; the pipeline reads
the first three columns by position after skipping the heading row.

## 5. Interpretation

The validation range is 10–100 Hz, while the switching frequency represented
in the analytical scripts is 100 kHz. The approximately 0.18-degree phase
offset seen in several cases is consistent with a half-switching-period delay
at 100 Hz:

```text
phase delay = 360 deg × frequency × (1 / (2 × switching frequency))
            = 0.18 deg at 100 Hz and 100 kHz switching frequency
```

This interpretation should be confirmed against the final PLECS sampling and
perturbation setup when the formal derivation is completed.

