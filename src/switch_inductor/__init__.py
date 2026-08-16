"""Switch-inductor analytical modeling and PLECS validation."""

from .config import ValidationCase, load_cases, repository_root
from .validation import evaluate_case, run_all_cases, run_case

__all__ = [
    "ValidationCase",
    "evaluate_case",
    "load_cases",
    "repository_root",
    "run_all_cases",
    "run_case",
]

