---
name: review-results
description: "Synthesize and critically analyze simulation outputs, test runs, sweep data, or iteration artifacts, highlighting anomalies, hypotheses, physical invariants, and conclusions. Use when the user asks to review, inspect, or summarize simulation results, benchmark data, or run outputs, or invokes /review-results."
---

# Review Results

Synthesize, diagnose, and critically analyze numerical simulation outputs, parametric sweeps, convergence sweeps, or benchmark data. Connect quantitative observations directly to physical mechanics and code logic.

## 5-Stage Analysis Pipeline

### 1. Evidence & Artifact Inventory
Identify and locate the exact output files and runs under review:
- Solver listings and output logs (`*.out`, `file.out`, `Two_BEAM.out`, etc.).
- Convergence and sweep records (`max_res.txt`, CSVs under `plots/`, `multiscale_bench/*.json`).
- Deck files and environmental overrides applied (e.g. `nbeam1`, `fc`, `HYG_*` flags).
- Record the exact parameters of the run (mesh density $N$, geometry $W, H, L$, angle $\theta$, load type).

### 2. Numerical Sanity & Solver Convergence Checks
Before interpreting physics, verify numerical validity:
- **Newton-Raphson convergence**: Did the solver reach true equilibrium? Check residual norms ($F_{\text{res}}$, $U_{\text{res}}$) against tolerances.
- **Divergence / Bifurcation**: Look for cutback substeps, high iteration counts, or solver warnings (`*** WARNING ***`, `*** ERROR ***`).
- **Conditioning**: Check for large pivot warnings, zero pivots, or severe stiffness matrix ill-conditioning.

### 3. Physical Invariant & Conservation Checks
Evaluate fundamental mechanics and problem invariants:
- **Equilibrium / Reaction Balance**: Do reaction forces balance external loads ($R^T f = 0$)? Do master and slave contact forces sum to zero?
- **Symmetry Error**: For symmetric cases (e.g. `Two_BEAM_sym.txt`), evaluate $\text{SymmErr} = |\max(U_z)| - |\min(U_z)| \to 0$.
- **Asymptotic Limits**: Does the response approach known analytical limits at extreme geometries (e.g., rigid beam, thin beam, $0^\circ$ or $90^\circ$ alignments)?
- **Monotonicity**: Does refinement produce monotonic convergence, or is there parity oscillation between even and odd meshes?

### 4. Anomaly Identification & Hypothesis Formation
If the data diverges from expectation, isolate the root mechanism into one of four distinct categories:
1. **Discretization Error**: Insufficient mesh density, element interpolation limits, shear-locking, or integration rule limitations.
2. **Kinematic / Geometric Modeling Limit**: 1D beam assumption breaking down in 3D zones (e.g., cross-sectional distortion, out-of-plane warping, Poisson expansion).
3. **Contact / Interface Mechanics**: Penalty stiffness artifact ($K_n$ too stiff causing ill-conditioning, or too soft causing penetration), contact projection drift, or $cp \approx \pm 1$ boundary effects.
4. **Implementation / Software Defect**: Coordinate transformation error, sign convention mismatch, unit discrepancy, or uninitialized common block variable.

### 5. Synthesis & Plain-Language Delivery
Structure the report cleanly for decision-making:
- **Executive Metric Table**: Quantitative comparison against baseline or 3D solid truth (SOLSH).
- **Visual Artifact**: ASCII curve/diagram or trend table showing convergence, error distributions, or deformed shape.
- **Intuitive Explanation**: Apply `explain-it-easy` to translate the numerical finding into clear physical intuition.
- **Actionable Verdict**: State explicitly whether the run passed, failed, or requires further data, with concrete next steps.

---

## Output Template

```text
================================================================================
SIMULATION / SWEEP REVIEW SUMMARY
================================================================================
Run / Deck:         <deck or script name>
Configuration:      W=<...>, H=<...>, Angle=<...>, Mesh N=<...>
Solver Status:      [CONVERGED / UNCONVERGED / WARNINGS]

1. QUANTITATIVE METRICS & PARITY
--------------------------------------------------------------------------------
| Metric / DOF    | Current Run | Baseline / Truth | Discrepancy (%) | Status |
| :-------------- | :---------- | :--------------- | :-------------- | :----- |
| Max Uz (mm)     | ...         | ...              | ...             | [OK]   |
| Symmetry Err    | ...         | 0.000            | ...             | [OK]   |
| Order p / GCI   | ...         | Asymptotic (2.0) | ...             | [OK]   |

2. PHYSICAL INVARIANTS & CONVERGENCE BEHAVIOR
--------------------------------------------------------------------------------
[ASCII plot, convergence diagram, or force balance summary]

3. MECHANICAL FINDINGS & ROOT CAUSE
--------------------------------------------------------------------------------
• Primary Observation: <what the numbers demonstrate>
• Underlying Mechanism: <physics or code cause>
• Anomaly / Risk: <any unexpected trend or numerical artifact>

4. VERDICT & NEXT STEPS
--------------------------------------------------------------------------------
1. <Action 1: e.g. accept baseline, refit stiffness, or adjust mesh>
2. <Action 2: sweep or validation script to execute next>
================================================================================
```

## Completion Criteria

The review is complete when:
- [ ] Output listings/data files are directly checked rather than assumed.
- [ ] Solver convergence and residual tolerances are verified.
- [ ] Key physical invariants (symmetry, equilibrium, monotonicity) are quantified.
- [ ] Any discrepancy is attributed to a testable mechanism (discretization, kinematics, contact, or code).
- [ ] A structured summary table and ASCII diagram are presented.
- [ ] Concrete, falsifiable next steps are provided.
