"""Shared validation pipeline for all eight small-signal cases."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .config import ValidationCase, load_cases, repository_root


COMPARISON_COLUMNS = [
    "frequency_hz",
    "plecs_magnitude_db",
    "analytical_magnitude_db",
    "magnitude_error_db",
    "plecs_phase_deg",
    "analytical_phase_deg",
    "phase_error_deg",
]


def load_plecs_csv(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Read a three-column PLECS frequency-response export."""
    try:
        frame = pd.read_csv(path, skiprows=1, header=None, usecols=[0, 1, 2])
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as exc:
        raise ValueError(f"Cannot read PLECS frequency-response data: {path}") from exc

    if frame.empty:
        raise ValueError(f"PLECS CSV contains no samples: {path}")

    try:
        frequency = pd.to_numeric(frame.iloc[:, 0], errors="raise").to_numpy(float)
        magnitude = pd.to_numeric(frame.iloc[:, 1], errors="raise").to_numpy(float)
        phase = pd.to_numeric(frame.iloc[:, 2], errors="raise").to_numpy(float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"PLECS CSV contains non-numeric samples: {path}") from exc

    if not all(np.all(np.isfinite(values)) for values in (frequency, magnitude, phase)):
        raise ValueError(f"PLECS CSV contains NaN or infinity: {path}")
    if np.any(frequency <= 0.0):
        raise ValueError(f"PLECS frequencies must be positive: {path}")

    order = np.argsort(frequency)
    return frequency[order], magnitude[order], phase[order]


def evaluate_case(case: ValidationCase) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Evaluate one analytical transfer function at the PLECS sample points."""
    module = import_module(case.equation_module)
    module.validate_model_parameters()
    il1, il2 = module.solve_dc_operating_point()
    transfer_function = getattr(module, case.transfer_function)

    frequency, plecs_magnitude, plecs_phase = load_plecs_csv(case.plecs_csv)
    response = np.asarray(transfer_function(frequency, il1, il2), dtype=complex)
    if response.shape != frequency.shape or not np.all(np.isfinite(response)):
        raise ValueError(f"Analytical response is invalid for case {case.case_id}")

    analytical_magnitude = 20.0 * np.log10(np.abs(response))
    analytical_phase = np.unwrap(np.angle(response)) * 180.0 / np.pi

    comparison = pd.DataFrame(
        {
            "frequency_hz": frequency,
            "plecs_magnitude_db": plecs_magnitude,
            "analytical_magnitude_db": analytical_magnitude,
            "magnitude_error_db": plecs_magnitude - analytical_magnitude,
            "plecs_phase_deg": plecs_phase,
            "analytical_phase_deg": analytical_phase,
            "phase_error_deg": plecs_phase - analytical_phase,
        },
        columns=COMPARISON_COLUMNS,
    )

    magnitude_error = comparison["magnitude_error_db"].to_numpy(float)
    phase_error = comparison["phase_error_deg"].to_numpy(float)
    summary: dict[str, Any] = {
        "case_id": case.case_id,
        "input": case.input_name,
        "output": case.output_name,
        "region": case.region,
        "samples": len(comparison),
        "frequency_min_hz": float(frequency.min()),
        "frequency_max_hz": float(frequency.max()),
        "il1_a": float(il1),
        "il2_a": float(il2),
        "max_magnitude_error_db": float(np.max(np.abs(magnitude_error))),
        "rms_magnitude_error_db": float(np.sqrt(np.mean(magnitude_error**2))),
        "max_phase_error_deg": float(np.max(np.abs(phase_error))),
        "rms_phase_error_deg": float(np.sqrt(np.mean(phase_error**2))),
    }
    return comparison, summary


def plot_comparison(
    case: ValidationCase,
    comparison: pd.DataFrame,
    destination: Path,
) -> None:
    """Create one portfolio-ready magnitude-and-phase comparison figure."""
    frequency = comparison["frequency_hz"].to_numpy(float)
    module = import_module(case.equation_module)
    il1, il2 = module.solve_dc_operating_point()
    transfer_function = getattr(module, case.transfer_function)

    dense_frequency = np.logspace(
        np.log10(frequency.min()), np.log10(frequency.max()), 2500
    )
    dense_response = transfer_function(dense_frequency, il1, il2)
    dense_magnitude = 20.0 * np.log10(np.abs(dense_response))
    dense_phase = np.unwrap(np.angle(dense_response)) * 180.0 / np.pi

    figure, axes = plt.subplots(2, 1, figsize=(9.0, 9.2), sharex=True)
    figure.suptitle(case.title, fontsize=15)

    axes[0].semilogx(dense_frequency, dense_magnitude, linewidth=1.8, label="Analytical model")
    axes[0].semilogx(
        frequency,
        comparison["plecs_magnitude_db"],
        linestyle="none",
        marker="o",
        markersize=4.2,
        label="PLECS data",
    )
    axes[0].set_ylabel("Magnitude (dB)")
    axes[0].grid(True, which="both", linewidth=0.6, alpha=0.55)
    axes[0].legend()

    axes[1].semilogx(dense_frequency, dense_phase, linewidth=1.8, label="Analytical model")
    axes[1].semilogx(
        frequency,
        comparison["plecs_phase_deg"],
        linestyle="none",
        marker="o",
        markersize=4.2,
        label="PLECS data",
    )
    axes[1].set_xlabel("Frequency (Hz)")
    axes[1].set_ylabel("Phase (deg)")
    axes[1].grid(True, which="both", linewidth=0.6, alpha=0.55)
    axes[1].legend()

    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.97))
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination, dpi=220, bbox_inches="tight")
    plt.close(figure)


def run_case(
    case: ValidationCase,
    output_root: Path | None = None,
    create_plot: bool = True,
) -> dict[str, Any]:
    """Run one case and write generated artifacts outside the curated results."""
    root = output_root or repository_root() / "results" / "generated"
    comparison, summary = evaluate_case(case)
    table_path = root / "tables" / f"{case.case_id}.csv"
    table_path.parent.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(table_path, index=False)
    if create_plot:
        plot_comparison(case, comparison, root / "figures" / f"{case.case_id}.png")
    return summary


def run_all_cases(
    output_root: Path | None = None,
    create_plots: bool = True,
) -> pd.DataFrame:
    """Run all configured cases and write a machine-readable summary."""
    root = output_root or repository_root() / "results" / "generated"
    summaries = [
        run_case(case, root, create_plot=create_plots)
        for case in load_cases().values()
    ]
    summary_frame = pd.DataFrame(summaries).sort_values("case_id")
    root.mkdir(parents=True, exist_ok=True)
    summary_frame.to_csv(root / "validation_summary.csv", index=False)
    return summary_frame

