"""Analytical equations for D1-to-IL1, D2 > D1.

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
RB1 = 0.0065  # ohm
RB2 = 0.0065  # ohm
RB3 = 0.0065  # ohm
Ro = 1   # load resistance
RS = 0.03   # ohm
RL = 2.6e-3   # ohm
D1 = 0.487   # steady-state duty ratio
D2 = 0.525 # steady-state duty ratio
V1 = 4   # V, battery-1 DC voltage
V2 = 4.2   # V, battery-2 DC voltage
V3 = 3.8  # V, battery-3 DC voltage



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

    if D2 <= D1:
        raise ValueError(
            "The steady-state equations use the D2 > D1 region, so D2 must "
            "be greater than D1."
        )


def diagonal_model_coefficients():
    """Return the A11 and A22 diagonal coefficients."""
    resistance_sum = RB1 + RB2 + RB3 + Ro
    a11 = (
        (RS + RL) * resistance_sum
        + D1 * RB2 * (RB1 + RB3 + Ro)
        + (1.0 - D1) * RB1 * (RB2 + RB3 + Ro)
    )
    a22 = (
        (RS + RL) * resistance_sum
        + D2 * RB3 * (RB1 + RB2 + Ro)
        + (1.0 - D2) * RB2 * (RB1 + RB3 + Ro)
    )
    return a11, a22


def steady_state_mutual_coupling_d2_greater_d1():
    """Return the replacement mutual polynomial for the D2 > D1 DC model."""
    return (
        D1 * RB2 * RB3
        - (D2 - D1) * RB1 * RB3
        + (1.0 - D2) * RB1 * RB2
    )


def solve_dc_operating_point():
    """Solve the DC equations with the D2 > D1 mutual coefficient."""
    a11, a22 = diagonal_model_coefficients()
    mutual_coupling = steady_state_mutual_coupling_d2_greater_d1()

    # These two rows are the screenshot equations after arranging them as
    # coefficient_matrix @ [IL1, IL2] = right_hand_side.
    coefficient_matrix = np.array(
        [
            [a11, -mutual_coupling],
            [-mutual_coupling, a22],
        ],
        dtype=float,
    )

    right_hand_side = np.array(
        [
            D1
            * (
                -RB2 * V1
                + (RB1 + RB3 + Ro) * V2
                - RB2 * V3
            )
            + (1.0 - D1)
            * (
                -(RB2 + RB3 + Ro) * V1
                + RB1 * V2
                + RB1 * V3
            ),
            D2
            * (
                -RB3 * V1
                - RB3 * V2
                + (RB1 + RB2 + Ro) * V3
            )
            + (1.0 - D2)
            * (
                RB2 * V1
                - (RB1 + RB3 + Ro) * V2
                + RB2 * V3
            ),
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


def g_il1_d1(frequency_hz, IL1, IL2):
    """Evaluate the D2 > D1 form of I_L1_hat(s)/D1_hat(s)."""
    s = 1j * 2.0 * np.pi * np.asarray(frequency_hz, dtype=float)
    resistance_sum = RB1 + RB2 + RB3 + Ro
    a11, a22 = diagonal_model_coefficients()
    mutual_coupling = steady_state_mutual_coupling_d2_greater_d1()

    first_dynamic_factor = L1 * resistance_sum * s + a11
    second_dynamic_factor = L2 * resistance_sum * s + a22

    numerator = (
        (
            (RB1 - RB2) * (RB3 + Ro) * IL1
            + RB3 * (RB1 + RB2) * IL2
            + (RB3 + Ro) * (V1 + V2)
            - (RB1 + RB2) * V3
        )
        * second_dynamic_factor
        + mutual_coupling
        * RB3
        * (RB1 + RB2)
        * IL1
    )

    denominator = (
        first_dynamic_factor * second_dynamic_factor
        - mutual_coupling**2
    )

    return numerator / denominator
