---
name: investigate
description: Run deep, evidence-driven investigations and produce durable reports covering the situation, analysis, conclusions, uncertainty, and next steps. Use automatically as a primary or supporting workflow alongside other skills when they encounter an unresolved cause, unexpected behavior, repeated failure, conflicting evidence, numerical discrepancy, material uncertainty, or a question that needs root-cause analysis. Also use when the user asks to investigate, examine deeply, determine what happened or why, collect evidence, compare explanations, or create an investigation report.
---

# Investigate

Perform a disciplined investigation and create a durable Markdown report. Adapt the evidence-gathering method to the subject while keeping facts, inferences, hypotheses, and unknowns distinct.

## Composition with other skills

- Operate as the primary workflow when investigation is the main task and as a supporting workflow when another active skill needs an uncertain point resolved.
- Treat another skill that invokes `$investigate` as the caller. Preserve its objective, constraints, safety boundaries, and output contract.
- Investigate only the delegated question or unresolved portion. Reuse trustworthy context and evidence already gathered instead of restarting the caller's workflow.
- Infer the handoff from the conversation and available artifacts. Establish the investigation question, supplied evidence, constraints, and desired report path; ask for missing information only when it blocks meaningful progress.
- Return a concise handoff containing the report path, principal findings, confidence, unresolved blockers, prioritized next steps, and evidence references.
- Keep the report understandable on its own while avoiding duplicate artifacts and redundant analysis.
- Leave implementation, design, review, or other downstream work to the calling skill unless the user explicitly includes it in the investigation scope.
- Avoid recursively re-invoking the calling skill. Complete the investigation and hand control back to the broader workflow.

## Investigation principles

- Start from the user's actual question and desired decision, not from an assumed cause.
- Prefer direct evidence: source files, logs, test output, measurements, primary documentation, and reproducible observations.
- Cite each material claim with a file and line, command result, test, artifact, dataset location, or source URL when available.
- Label interpretations as inferences and state the evidence supporting them.
- Track competing hypotheses. Actively seek evidence that could disprove the leading explanation.
- Record negative results and ruled-out causes when they narrow the search.
- State confidence and remaining uncertainty. Do not present plausibility as proof.
- Preserve the investigated state. Follow repository instructions and avoid destructive or expansive actions.
- Diagnose without implementing a fix unless the user also asks for changes.
- Ask for input only when missing access, authority, or context prevents meaningful progress. Otherwise, proceed with explicit assumptions.

## Workflow

### 1. Frame the investigation

Restate the investigation question in testable terms. Establish:

- the reported situation and its impact;
- expected behavior versus observed behavior, when applicable;
- the affected and unaffected scope;
- timing, frequency, environment, and relevant changes;
- constraints, safety boundaries, and the decision the report should support.

Inspect local instructions and existing documentation before choosing methods. Reuse prior reports or artifacts as evidence, but verify claims that may be stale.

### 2. Establish a baseline

Capture the current state before deep analysis. For a codebase, inspect relevant status, configuration, entry points, dependencies, tests, and recent changes without disturbing unrelated user work. For other subjects, identify authoritative sources, known facts, assumptions, and gaps.

Create a lightweight evidence ledger while working. For each important item, retain:

- evidence identifier;
- observation or result;
- source and retrieval method;
- relevance;
- limitations or possible alternative interpretations.

### 3. Gather evidence

Select methods according to the problem:

- For software or runtime failures, reproduce the smallest safe case, inspect errors and logs, trace the execution path, compare working and failing states, and run focused diagnostics.
- For data or numerical discrepancies, verify inputs, units, assumptions, transformations, boundary conditions, invariants, and sensitivity to controlled changes.
- For regressions, identify the change window and compare behavior, configuration, dependencies, and environment across the boundary.
- For performance problems, measure before explaining; separate latency, throughput, resource use, scale, and contention.
- For general or external questions, prioritize primary and current sources, compare independent evidence, record publication and event dates, and cite URLs.
- For process or design problems, map actors, states, constraints, handoffs, failure modes, and the evidence for claimed outcomes.

Use the least invasive diagnostic that can distinguish between hypotheses. Record commands and focused outputs that make findings reproducible; exclude secrets and irrelevant bulk output.

### 4. Analyze competing explanations

Form multiple plausible hypotheses when the cause is not already proven. For each hypothesis, document:

- supporting evidence;
- contradicting evidence;
- a discriminating check or expected observation;
- current status: confirmed, likely, possible, unlikely, or ruled out;
- confidence: high, medium, or low.

Run safe discriminating checks where possible. Continue until the central question is answered with evidence or the remaining blocker is precisely identified. Distinguish:

- root cause from trigger;
- cause from correlation;
- primary fault from contributing conditions;
- observed impact from potential impact;
- confirmed facts from unresolved unknowns.

### 5. Synthesize findings

Build the explanation as a traceable chain from evidence to conclusion. If no root cause can be confirmed, present the leading explanations, why certainty is limited, and the exact evidence needed next. Do not manufacture closure.

Prioritize next steps by information gain and impact. Separate immediate containment, further verification, corrective work, and prevention when those categories apply. Include a validation condition for any proposed fix or action.

### 6. Create the report

Write a Markdown report to a path supplied by the user. Otherwise, use an established project investigation or documentation directory when one clearly exists; if none exists, create `INVESTIGATION_<topic-slug>.md` in the workspace root. Do not overwrite an unrelated existing report; use a descriptive suffix when needed.

Use the following structure, adapting subsections to the investigation:

```markdown
# Investigation: <title>

## Executive summary
<Answer the central question, current confidence, and impact in a few paragraphs.>

## Situation
### Investigation question
### Observed and expected state
### Scope and impact
### Environment, timeline, and constraints

## Analysis
### Method
### Evidence
### Hypotheses and tests
### Findings
### Root cause or leading explanation
### Contributing factors
### Ruled-out explanations
### Limitations and unknowns

## Next steps
### Immediate actions
### Further verification
### Corrective actions
### Prevention and follow-up

## Evidence index
<Files and lines, commands, tests, logs, artifacts, datasets, and URLs used.>
```

Omit empty subsections rather than filling them with boilerplate. For every next step, specify the action, rationale, priority, expected result, and verification criterion. Clearly mark actions that require user approval, external access, or material changes.

## Completion check

Before delivering, verify that:

- the report directly answers the investigation question or states the precise blocker;
- important conclusions are linked to evidence;
- contrary evidence and credible alternatives are addressed;
- confidence, assumptions, limitations, and unknowns are explicit;
- next steps are ordered, concrete, and verifiable;
- no fix or external mutation was performed without authorization;
- the report path is included in the response.
