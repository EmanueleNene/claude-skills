---
name: investigate
description: Run deep, evidence-driven root-cause investigations and produce structured diagnostics or durable reports. Use when the user says "investigate", "why did this fail", "root cause", "find why", "trace this bug", "debug this discrepancy", "what happened here", or invokes /investigate. Also use automatically when another skill encounters an unresolved cause, unexpected failure, numerical discrepancy, or conflicting evidence.
---

# Investigate

Perform a disciplined, evidence-driven investigation and deliver either a fast inline diagnostic or a durable Markdown report. Adapt the evidence-gathering method to the subject while keeping facts, inferences, hypotheses, and unknowns strictly distinct.

## Investigation Depth Dial

Select the investigation depth based on scope, impact, and user intent:

- **Lightweight Triage (Inline — No File Generated)**:
  - *When to use*: Localized bugs, straightforward errors, single-file discrepancies, or when the user asks for a quick diagnosis in chat.
  - *Output*: Deliver directly in conversation using the 5-point format:
    1. **Core Diagnosis & Root Cause**
    2. **Evidence Anchor** (exact file, line, command, or log snippet)
    3. **ASCII Causal Flow Diagram** (trigger → mechanism → symptom)
    4. **Concrete Minimal Fix & Verification Command**
    5. **Confidence & Remaining Unknowns**

- **Full Investigation (Durable Report Generated)**:
  - *When to use*: Regressions, multi-component failures, numerical/solver discrepancies, intermittent failures, architecture/design breakdowns, or whenever the user asks for an investigation report.
  - *Output*: Create a structured Markdown report following the template below.

## Composition with Other Skills

- **Primary vs Supporting**: Operate as the primary workflow when root-cause diagnosis is the main task, or as a supporting workflow when caller skills (e.g. `delivery-pipeline`) need an uncertain point resolved.
- **Strict Scope**: Diagnose without implementing a fix unless the user explicitly authorizes changes.
- **Handoffs**:
  - To plan a verified fix: hand off to `$plan-change`.
  - To clean up diagnostic artifacts/runs: hand off to `$clean-generated-artifacts`.
  - To present findings to non-technical stakeholders: hand off to `$explain-it-easy` or `$present-it-html`.

## Investigation Principles

- **Root Cause over Symptoms**: Trace backwards from the symptom to the physical or logical mechanism that created the faulty state.
- **Direct Empirical Evidence**: Prefer direct evidence (source lines, logs, test outputs, memory dumps, reproducible commands) over speculation.
- **Explicit Inferences**: Label every claim as *Fact* (directly observed), *Inference* (deduced from facts), or *Hypothesis* (plausible but unverified).
- **Legwork Gate**: Do **NOT** draft, scaffold, or write the report file until discriminating checks have run and evidence has been gathered.
- **Preserve State**: Follow repository guidelines; never delete or mutate files under investigation without authorization.

## Workflow

### 1. Frame the Investigation
Restate the question in testable terms:
- Expected behavior vs. observed behavior.
- Affected vs. unaffected scope (what still works?).
- Change boundary: timing, commit hash, environment, dependency changes.
- Determine depth: **Lightweight (Inline)** vs **Full (Report)**.

### 2. Establish Baseline & Evidence Ledger
Capture the state before altering anything. Build a lightweight evidence ledger:
- Evidence ID (e.g., `E1`, `E2`).
- Exact source: file path, line number, command, or log timestamp.
- Observation and relevance.

### 3. Gather Evidence & Run Discriminating Checks
Select diagnostic methods matched to the problem:
- **Runtime / Test Failures**: Reproduce the minimal failing case; trace call stacks and boundary conditions.
- **Numerical / Physics Discrepancies**: Check inputs, units, coordinate systems, sign conventions, boundary conditions, and formulation invariants.
- **Regressions**: Perform binary search / diff inspection across the change window.
- **Performance**: Measure CPU, memory, contention, or I/O before hypothesizing bottlenecks.

### 4. Test Competing Hypotheses (Disproof Matrix)
Form multiple plausible explanations. Actively seek tests that could **disprove** each one. Use the **Hypothesis Disproof Matrix**:

| ID | Hypothesis | Discriminating Check | Expected If True | Observed Result | Verdict | Confidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| H1 | State assumption A | Inspect variable X at t=0 | X == 0 | X == 12.4 | **RULED OUT** | High |
| H2 | Mechanism B | Run test with flag Y | Test passes | Test passes | **CONFIRMED** | High |

### 5. Build the Causal Flow Diagram
Map the confirmed failure chain using ASCII/Unicode diagrams:

```
[Trigger / Change] ──> [State Drift / Flaw] ──> [Failure Point] ──> [Observed Symptom]
```

### 6. Generate the Report (For Full Investigations)

#### Report Placement Policy
Do **not** clutter the repository root. Save the report in the first matching location:
1. User-specified path.
2. `docs/investigations/INVESTIGATION_<topic-slug>.md`
3. Existing project documentation folder (e.g., `docs/by-date/YYYY-MM-DD/`, `docs/`, `investigations/`).
4. Workspace root only if no docs folder exists and project conventions permit.

#### Report Template

```markdown
# Investigation: <Title>

## Executive Summary
<Brief statement of the core question, confirmed root cause, current confidence, and business/technical impact.>

## Causal Mechanism
```
[Trigger / Change] ──> [Intermediate State] ──> [Failure Point] ──> [Observed Symptom]
```

## Situation
- **Investigation Question**: <What specifically was investigated?>
- **Expected vs Observed**: <Clear contrast of expectation vs reality>
- **Scope & Impact**: <Affected modules, platforms, and severity>
- **Timeline & Change Window**: <Relevant commits, dates, or environmental changes>

## Hypothesis Disproof Matrix
| ID | Hypothesis | Discriminating Check | Expected If True | Observed Result | Verdict | Confidence |
|:---|:---|:---|:---|:---|:---|:---|
| H1 | ... | ... | ... | ... | Ruled Out / Confirmed | High/Med/Low |

## Analysis & Evidence
### Confirmed Root Cause
<Step-by-step physical or logical explanation supported by cited evidence.>

### Contributing Factors & Triggers
<Secondary conditions that enabled or amplified the fault.>

### Ruled-Out Explanations
<Why competing theories were eliminated, with evidence references.>

### Limitations & Remaining Unknowns
<What remains uncertain or untested, and why.>

## Next Steps
1. **Immediate Containment**: <Temporary mitigation or rollback if needed>
2. **Corrective Fix**: <Proposed fix with acceptance and verification criteria>
3. **Prevention**: <Regression tests, lint rules, or assertions to prevent recurrence>

## Evidence Index
- `E1`: `path/to/file.py:124` — Observation details.
- `E2`: Command `python tests/TestSuite.py --quick` output log snippet.
```

## Completion Checklist

Before concluding:
- [ ] Direct answer to the central question provided with high/medium/low confidence.
- [ ] Every material conclusion backed by cited evidence (file + line, command, or log).
- [ ] Competing hypotheses tested and evaluated in the disproof matrix.
- [ ] ASCII causal chain diagram included.
- [ ] Report placed cleanly without cluttering repo root (if Full mode).
- [ ] No unauthorized fixes or file mutations executed.
- [ ] Clear, verifiable next steps provided (or handoff to `$plan-change`).
