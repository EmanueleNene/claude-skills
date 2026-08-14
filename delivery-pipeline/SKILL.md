---
name: delivery-pipeline
description: Orchestrate technical change delivery from evidence to presentation through investigation, planning, implementation, two-axis code review, generated-artifact cleanup, plain-language explanation, and standalone HTML briefing. Use when the user wants an end-to-end bug fix, feature, refactor, migration, performance improvement, or validated technical change delivered as a traceable workflow rather than an isolated edit.
---

# Delivery Pipeline

Run a stage-gated evidence chain. Each stage writes a durable artifact that becomes the next stage's input.

## Pipeline

```text
$investigate
  -> $plan-change
  -> $implement
  -> $code-review
  -> $clean-generated-artifacts
  -> $Explain-it-easy
  -> $present-it-html
```

Announce each skill transition. Carry the original objective, project instructions, user authorization, pre-existing work, and safety boundaries through every stage.

## Bootstrap

1. Read project instructions and relevant existing documentation.
2. Capture workspace status, baseline revision when available, relevant tool availability, and pre-existing user changes.
3. Use the caller's run directory or the project's established delivery-artifact directory. Otherwise create `docs/delivery/<YYYYMMDD>-<topic-slug>/`.
4. Create `RUN.md` with the objective, baseline, permissions, protected paths, and this ledger:

```markdown
| Stage | Status | Artifact | Gate note |
|---|---|---|---|
| Investigate | pending | INVESTIGATION.md | |
| Plan | pending | PLAN.md | |
| Implement/validate | pending | VALIDATION.md | |
| Review | pending | REVIEW.md | |
| Cleanup | pending | cleanup-manifest.json | |
| Explain | pending | EXPLANATION.md | |
| Present | pending | presentation.html | |
```

Use `pending`, `running`, `passed`, `limited`, or `blocked`. Update the ledger at every transition.

Complete bootstrap when the fixed point or equivalent baseline, run directory, pre-existing work, and authorization boundaries are explicit.

## Stage 1: Investigate

Invoke `$investigate` with the original question and output path `<run>/INVESTIGATION.md`. Require evidence, competing explanations, confidence, ruled-out causes, and verifiable next steps. Keep diagnosis separate from implementation.

Gate: advance when the central question is answered with evidence or a precise blocker is documented and the user chooses how to proceed.

## Stage 2: Plan

Invoke `$plan-change` with the investigation, baseline, workspace snapshot, project instructions, and output path `<run>/PLAN.md`. Treat the plan as the review specification. Require exact targets, acceptance criteria, risk-appropriate validation, evidence paths, and cleanup preservation rules.

Gate: advance when every acceptance criterion maps to a change step and observable validation.

## Stage 3: Implement and validate

Invoke `$implement` against `<run>/PLAN.md` with these caller constraints:

- preserve unrelated user work and project-protected assets;
- run the narrowest relevant check before broader integration or system validation;
- record every command, exit status, measured result, limitation, and evidence path in `<run>/VALIDATION.md`;
- leave changes uncommitted unless the user authorized a commit;
- preserve generated evidence named by the plan.

Select validation by risk: correctness, compatibility, migration, performance, security, numerical, data-quality, or operational checks as applicable. A successful process exit is not sufficient when acceptance depends on behavior or measurement.

Gate: advance when planned work is complete and validation is `passed` or explicitly `limited` by a precise blocker.

## Stage 4: Review and repair

Invoke `$code-review` with the bootstrap baseline and `<run>/PLAN.md` as the specification.

- For committed work, review the baseline-to-HEAD diff.
- For uncommitted work, review the complete baseline-to-working-tree diff, including staged and unstaged changes, and label that mode.
- Save separate Standards and Spec reports to `<run>/REVIEW.md` without merging their rankings.

Treat correctness defects, unmet acceptance criteria, unsafe behavior, and documented-standard violations as blocking. Send blocking findings back through `$implement`, rerun affected validation, and invoke `$code-review` again. Record waived judgement calls with the user's rationale.

Gate: advance when both axes have no unresolved blocker or the user explicitly accepts the recorded limitation.

## Stage 5: Preserve evidence and clean

Retain or copy every artifact cited by the run. Invoke `$clean-generated-artifacts` with only files and directories generated or named by this workflow. Derive protection and deletion rules from project instructions and generation commands. Write `<run>/cleanup-manifest.json`.

Present the dry-run list. Apply it only after explicit approval of that exact manifest. If approval is withheld, mark cleanup `blocked`; presentation may continue but must show cleanup as pending.

Gate: advance when cleanup is applied exactly as approved or its pending state is recorded truthfully.

## Stage 6: Explain

Invoke `$Explain-it-easy` on the final problem, cause, change, validation, and limitations. Save the concise result to `<run>/EXPLANATION.md`.

Gate: advance when a reader unfamiliar with the project can state what was wrong, what changed, how confidence was established, and what remains uncertain.

## Stage 7: Present

Invoke `$present-it-html` with the whole run directory and output path `<run>/presentation.html`. Require distinct investigation, plan, implementation, validation, Standards review, Spec review, cleanup, limitation, and next-action sections. Run the bundled validator.

Gate: finish when the HTML is standalone, validator-clean, evidence-linked, and honest about every limited or pending stage.

## Final handoff

Return:

- one-sentence outcome and confidence;
- paths to `RUN.md` and all seven stage artifacts;
- components changed and review baseline;
- validation status and acceptance result;
- Standards and Spec finding counts;
- cleanup totals or pending approval;
- risks, blockers, uncommitted work, and next action.

Keep pushes, publication, deployments, external messages, issue creation, and broader deletion behind explicit authority.

## Completion check

- Every stage has an artifact and terminal status.
- Investigation evidence traces into plan decisions and acceptance criteria.
- Implementation traces into validation evidence and both review axes.
- Review blockers completed a repair-and-rereview loop.
- Cleanup preserved cited evidence and project-protected assets.
- Explanation and presentation match the recorded evidence.
- Limitations and pending actions remain visible.
