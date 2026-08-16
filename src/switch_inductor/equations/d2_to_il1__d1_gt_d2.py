"""Analytical equations for D2-to-IL1, D1 > D2.

The expression is retained as an explicit case module so it can be audited
against the handwritten derivation as that documentation is completed.
"""

import numpy as np

# -----------------------------------------------------------------------------
# Model parameters and steady-state operating point
# Enter the circuit parameters and battery voltages used in PLECS.
# IL1 and IL2 are calculated automatically; do not enter them manually.
# -----------------------------------------------------------------------------
L1 = 64e-3   # H
L2 = 64e-3   # H
RB1 = 0.01  # ohm
RB2 = 0.01  # ohm
RB3 = 0.01  # ohm
Ro = 1   # load resistance
RS = 0.03   # ohm
RL = 2.6e-3   # ohm
D2 = 0.488  # steady-state duty ratio
D1 = 0.527 # steady-state duty ratio
V1 = 4.2 # V, battery-1 DC voltage
V2 = 3.8# V, battery-2 DC voltage
V3 = 4  # V, battery-3 DC voltage



def validate_model_parameters():
    """Stop with a clear message if any required input value is missing."""
    parameters = {
        "L1": L1,
        "L2": L2,
        "RB1": RB1,
        "RB2": RB2,
        "RB3": RB3,
        "Ro": Ro,
        "RS": RS,
        "RL": RL,
        "D1": D1,
        "D2": D2,
        "V1": V1,
        "V2": V2,
        "V3": V3,
    }
    missing = [name for name, value in parameters.items() if value is None]
    if missing:
        raise ValueError(
            "Replace None with numerical values for: " + ", ".join(missing)
        )

    if D1 <= D2:
        raise ValueError(
            "bode_D1.py uses the D1 > D2 equations, so D1 must be greater "
            "than D2."
        )


def mutual_coupling_term_d1_greater_d2():
    """Return the mutual-coupling term for the D1 > D2 operating region."""
    return RB2 * (
        RB1
        + D1 * (RB3 + Ro)
        - D2 * (RB1 + Ro)
    )


def solve_dc_operating_point():
    """Solve the two supplied steady-state equations for IL1 and IL2."""
    mutual_coupling = mutual_coupling_term_d1_greater_d2()
    coefficient_matrix = np.array(
        [
            [
                (1.0 - D1) * RB1 * (RB2 + RB3 + Ro)
                + D1 * RB2 * (RB1 + RB3 + Ro)
                + (RS + RL) * (RB1 + RB2 + RB3 + Ro),
                -mutual_coupling,
            ],
            [
                -mutual_coupling,
                (1.0 - D2) * RB2 * (RB1 + RB3 + Ro)
                + D2 * RB3 * (RB1 + RB2 + Ro)
                + (RS + RL) * (RB1 + RB2 + RB3 + Ro),
            ],
        ],
        dtype=float,
    )

    right_hand_side = np.array(
        [
            (1.0 - D1)
            * (RB1 * (V2 + V3) - (RB2 + RB3 + Ro) * V1)
            + D1
            * ((RB1 + RB3 + Ro) * V2 - RB2 * (V1 + V3)),
            (1.0 - D2)
            * (RB2 * (V1 + V3) - (RB1 + RB3 + Ro) * V2)
            + D2
            * ((RB1 + RB2 + Ro) * V3 - RB3 * (V1 + V2)),
        ],
        dtype=float,
    )

    try:
        dc_currents = np.linalg.solve(coefficient_matrix, right_hand_side)
    except np.linalg.LinAlgError as exc:
        raise ValueError(
            "The two DC operating-point equations are singular and cannot "
            "determine unique values of IL1 and IL2."
        ) from exc

    if not np.all(np.isfinite(dc_currents)):
        raise ValueError("The solved DC currents contain NaN or infinity.")

    residual = coefficient_matrix @ dc_currents - right_hand_side
    if not np.allclose(residual, 0.0, rtol=1e-10, atol=1e-12):
        raise ValueError(
            "The calculated IL1 and IL2 do not satisfy the supplied DC equations."
        )

    return float(dc_currents[0]), float(dc_currents[1])


def g_il1_d2(frequency_hz, IL1, IL2):
    """Evaluate I_L1_hat(s)/D2_hat(s) at s = j*2*pi*f."""
    s = 1j * 2.0 * np.pi * np.asarray(frequency_hz, dtype=float)
    mutual_coupling = mutual_coupling_term_d1_greater_d2()

    numerator = (
        -L2
        * (RB1 + RB2 + RB3 + Ro)
        * RB2
        * (RB1 + Ro)
        * IL2
        * s
        - (
            (1.0 - D2) * RB2 * (RB1 + RB3 + Ro)
            + D2 * RB3 * (RB1 + RB2 + Ro)
            + (RS + RL) * (RB1 + RB2 + RB3 + Ro)
        )
        * RB2
        * (RB1 + Ro)
        * IL2
        + mutual_coupling
        * (
            -RB2 * (RB1 + Ro) * IL1
            + (RB2 - RB3) * (RB1 + Ro) * IL2
            + (RB1 + Ro) * (V2 + V3)
            - (RB2 + RB3) * V1
        )
    )

    denominator = (
        L1 * L2 * (RB1 + RB2 + RB3 + Ro) ** 2 * s**2
        + (RB1 + RB2 + RB3 + Ro)
        * (
            L2
            * (
                (1.0 - D1) * RB1 * (RB2 + RB3 + Ro)
                + D1 * RB2 * (RB1 + RB3 + Ro)
                + (RS + RL) * (RB1 + RB2 + RB3 + Ro)
            )
            + L1
            * (
                (1.0 - D2) * RB2 * (RB1 + RB3 + Ro)
                + D2 * RB3 * (RB1 + RB2 + Ro)
                + (RS + RL) * (RB1 + RB2 + RB3 + Ro)
            )
        )
        * s
        + (
            (1.0 - D1) * RB1 * (RB2 + RB3 + Ro)
            + D1 * RB2 * (RB1 + RB3 + Ro)
            + (RS + RL) * (RB1 + RB2 + RB3 + Ro)
        )
        * (
            (1.0 - D2) * RB2 * (RB1 + RB3 + Ro)
            + D2 * RB3 * (RB1 + RB2 + Ro)
            + (RS + RL) * (RB1 + RB2 + RB3 + Ro)
        )
        - mutual_coupling**2
    )

    return numerator / denominator
