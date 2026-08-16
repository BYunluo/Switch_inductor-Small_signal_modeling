# Repository Structure

```text
switch-inductor-small-signal-modeling/
├── .github/workflows/          # Continuous integration
├── configs/                    # Eight-case model/data/formula mapping
├── data/
│   └── raw/plecs/              # Eight untouched PLECS CSV exports
├── docs/
│   ├── assets/                 # Original comparison figures used by README
│   ├── derivations/            # Four evolving handwritten PDF derivations
│   └── source/                 # Unchanged original Word validation report
├── models/
│   ├── plecs/                  # Eight small-signal AC-sweep models
│   └── simulink/               # Original circuit and digital-control model
├── results/
│   ├── figures/                # Eight curated Bode comparison figures
│   └── tables/                 # Eight point-by-point comparison tables
├── scripts/                    # Direct repository entry points
├── src/switch_inductor/
│   ├── equations/              # Eight explicit analytical formula modules
│   └── validation.py           # Shared evaluation and plotting pipeline
└── tests/                      # Configuration, model, and numerical checks
```

## Ownership rules

- `data/raw/`, `docs/assets/original_comparisons/`, `docs/derivations/`,
  `docs/source/`, and `models/` are source evidence. Replace them only when a
  new authoritative source is available.
- `src/`, `configs/`, and `tests/` define the reproducible implementation.
- `results/figures/`, `results/tables/`, and `results/validation_summary.csv`
  are reviewed outputs tied to the current implementation.
- `results/generated/` is disposable local output and is ignored by Git.

The descriptive filenames encode input, output, and operating region, avoiding
the opaque numbered folders and generic filenames used in the working area.
