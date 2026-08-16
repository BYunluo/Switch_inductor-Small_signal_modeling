"""Run the repository validation pipeline without installing the package."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from switch_inductor.cli import main  # noqa: E402


if __name__ == "__main__":
    main()

