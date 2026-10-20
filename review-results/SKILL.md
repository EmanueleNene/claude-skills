---
name: review-results
description: "Critically review the results of the last run: simulations, sweeps, test runs, benchmarks, experiments, or any iteration output. Use when the user invokes /review-results, asks to review, inspect, check, or summarize results or run outputs, or asks whether a run worked."
---

# Review Results

Act as a **skeptical reviewer**: the results are guilty until the evidence clears them. Read the actual outputs,
connect the dots, and say what the numbers do and do not support.

## 1. Inventory

List exactly what is under review, read from the files, not assumed:

- outputs: logs, listings, CSV/JSON, plots, test reports
- inputs: script, config, parameters, flags, data version
- the baseline it is compared against: previous run, reference, analytical value, expected behaviour

Missing a baseline or key output → say so and ask before drawing conclusions.

## 2. Did the run work?

Check validity before interpreting anything:

- finished cleanly: exit status, errors, warnings, timeouts, skipped or failed cases
- converged or stable, where that applies (solver residuals, training loss, retries)
- the run used the inputs it was meant to use (right config, right data, right version)

## 3. Do the results make sense?

Test the numbers against what must hold for this domain:

- **invariants**: conservation, balance, symmetry, totals that must match
- **limits**: known values at extreme or trivial cases
- **trends**: monotonic where expected, smooth under refinement, no odd/even or run-to-run flip-flop
- **baseline**: difference vs baseline, and whether it is inside noise or tolerance

## 4. Anomalies and hypotheses

For each anomaly, name the most likely cause category and a test that would confirm or kill it:

| Category | Examples |
|---|---|
| resolution / sampling | mesh, step size, sample count, too few repeats |
| model limit | an assumption that breaks in this regime |
| setup / input | wrong parameter, units, data, environment |
| implementation defect | sign, index, unit conversion, uninitialized state |
| measurement / noise | timing jitter, randomness, flaky test |

Escalate to `investigate` when a cause stays unresolved.

## 5. Report

Use the `explain-it-easy` style. Visual first: tables, Unicode plots and drawings, bullets.

```text
RESULTS REVIEW — <run name>
Inputs:   <key parameters>
Status:   WORKED / FAILED / WARNINGS

| Metric | Current | Baseline | Diff | Status |
|--------|---------|----------|------|--------|

Trend / invariant check:  <Unicode plot or table>

Findings:
• What the numbers show
• Likely mechanism
• Anomalies / risks

Verdict:   ACCEPT / REJECT / NEED MORE DATA
Next:      1. <concrete action or run>  2. ...
```

Done when: every number cited was read from an output, validity is checked, each anomaly has a cause category and a
test, and the verdict comes with concrete next steps.
