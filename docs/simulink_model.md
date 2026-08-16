# Original Simulink System Model

`models/simulink/switch_inductor_system.slx` is the original system-level model
from which the analytical study was motivated. It contains the switching power
stage, battery-related blocks, sensing, PWM generation, PID/control elements,
and digital logic.

## Intended role in this repository

The Simulink model is supporting engineering evidence, not the primary entry
point for reproducing the eight PLECS comparisons. It helps a reviewer see the
physical system and control implementation behind the reduced analytical
models.

## Format and dependencies

- Last saved with MATLAB/Simulink R2025b on Windows (`win64`).
- References Simscape and Simscape Electrical library blocks.
- Also references PID, frequency-response-estimation, moving-average, and
  battery library blocks.
- The original package metadata contains the local author identifier `wjy22`,
  which the repository owner confirmed belongs to 王静远 and should be retained.

Before formal release, open the model in the intended MATLAB installation,
run the dependency analyzer, update the model diagram, and capture one clean
annotated system-level screenshot for the README.

The Simulink cache files (`*.slxc`) are deliberately excluded because they are
generated artifacts and are not required to understand the model source.
