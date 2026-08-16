# PLECS Validation Models

Filename convention:

```text
<duty input>_to_<current output>__<operating region>.plecs
```

Examples:

- `d1_to_il1__d1_gt_d2.plecs`: perturb `D1`, observe `IL1`, with `D1 > D2`.
- `d2_to_il2__d2_gt_d1.plecs`: perturb `D2`, observe `IL2`, with `D2 > D1`.

The saved models use PLECS 5.0 and contain an AC Sweep over 10–100 Hz with 41
points, together with a steady-state analysis. The matching exports are in
`data/raw/plecs/`.

