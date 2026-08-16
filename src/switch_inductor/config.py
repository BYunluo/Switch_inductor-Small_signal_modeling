"""Repository paths and validation-case configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


def repository_root() -> Path:
    """Return the repository root independent of the current directory."""
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ValidationCase:
    """One analytical-model versus PLECS validation case."""

    case_id: str
    input_name: str
    output_name: str
    region: str
    equation_module: str
    transfer_function: str
    plecs_csv: Path
    plecs_model: Path

    @property
    def title(self) -> str:
        return (
            f"{self.input_name}-to-{self.output_name} small-signal response "
            f"({self.region})"
        )


def load_cases(config_path: Path | None = None) -> dict[str, ValidationCase]:
    """Load all case definitions from the repository TOML configuration."""
    root = repository_root()
    path = config_path or root / "configs" / "validation_cases.toml"
    with path.open("rb") as stream:
        raw_cases = tomllib.load(stream)["cases"]

    cases: dict[str, ValidationCase] = {}
    for case_id, values in raw_cases.items():
        cases[case_id] = ValidationCase(
            case_id=case_id,
            input_name=values["input"],
            output_name=values["output"],
            region=values["region"],
            equation_module=values["equation_module"],
            transfer_function=values["transfer_function"],
            plecs_csv=root / values["plecs_csv"],
            plecs_model=root / values["plecs_model"],
        )
    return cases

