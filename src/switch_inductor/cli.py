"""Command-line interface for reproducible validation."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_cases
from .validation import run_all_cases, run_case


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare analytical switch-inductor models with PLECS data."
    )
    parser.add_argument(
        "--case",
        choices=sorted(load_cases()),
        help="Run one case. Omit this option to run all eight cases.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Generated-output directory (default: results/generated).",
    )
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Write comparison tables only.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    cases = load_cases()
    if args.case:
        summary = run_case(
            cases[args.case],
            output_root=args.output_dir,
            create_plot=not args.no_plots,
        )
        for key, value in summary.items():
            print(f"{key}: {value}")
        return

    summary = run_all_cases(
        output_root=args.output_dir,
        create_plots=not args.no_plots,
    )
    print(
        summary[
            [
                "case_id",
                "max_magnitude_error_db",
                "max_phase_error_deg",
            ]
        ].to_string(index=False)
    )

