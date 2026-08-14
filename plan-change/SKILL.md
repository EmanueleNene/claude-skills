---
name: plan-change
description: Convert investigation evidence, a specification, or a concrete change request into a durable executable implementation plan. Use when software or technical project work needs scoped changes, acceptance criteria, validation commands, review inputs, artifact-preservation rules, and a reliable handoff to implementation.
---

# Plan Change

Turn evidence into an implementation contract. Plan the work without performing it.

## Inputs

Establish from the caller, workspace, and available artifacts:

- objective and observable outcome;
- investigation report, specification, ticket, or decision record;
- project instructions and current workspace state;
- constraints, non-goals, unresolved decisions, and authorization boundaries;
- caller-supplied output path, if any.

Infer discoverable inputs. Ask only when a missing decision would materially change the plan.

## Process

### 1. Lock the evidence

Read the governing request, project instructions, relevant source and configuration, tests, documentation, and focused version-control state. Separate confirmed facts, inferences, assumptions, and blockers.

Complete this step when every plan-driving claim has a source or an explicit uncertainty label.

### 2. Pin the contract

Record:

- outcome, acceptance criteria, and non-goals;
- baseline revision when version control is available;
- the plan path as the specification source for review;
- pre-existing user work and evidence that downstream cleanup must preserve;
- permissions required for commits, external writes, migrations, deployments, or deletion.

Complete this step when implementation and review can reconstruct intent from artifacts without relying on chat history.

### 3. Choose the smallest seams

Map each required behavior to the files, modules, interfaces, schemas, configuration, documentation, or operational components that own it. Identify coupled consumers, compatibility boundaries, data migrations, and rollback points as applicable.

Complete this step when every acceptance criterion maps to at least one change location and one verification.

### 4. Write executable steps

For each ordered step specify:

1. exact files, symbols, components, or resources;
2. behavior to add, remove, or preserve;
3. rationale tied to evidence;
4. focused check to run immediately;
5. observable completion criterion;
6. rollback or containment where failure has material impact.

Put tests or instrumentation before the production change when they can expose the failure first. Keep steps independently reviewable.

### 5. Build the validation ladder

Choose risk-appropriate checks, ordered from narrowest to broadest:

1. static, format, schema, or compile checks;
2. smallest focused test or reproducer;
3. integration or system validation;
4. regression, compatibility, performance, security, numerical, or operational checks as applicable;
5. final review against the baseline and this plan.

Name expected results and evidence paths. Define tolerances, units, baselines, or service-level thresholds whenever correctness depends on them.

### 6. Publish

Write to the caller's path. Otherwise use the project's established planning directory; if none exists, write `PLAN_<topic-slug>.md` at the workspace root without overwriting an unrelated plan.

Use this structure and omit empty sections:

```markdown
# Plan: <outcome>

## Contract
### Outcome
### Acceptance criteria
### Non-goals
### Baseline and review specification

## Evidence and constraints
### Confirmed findings
### Assumptions and blockers
### Protected work and artifacts

## Change map
| Component | Responsibility | Planned change | Evidence |

## Implementation steps
### 1. <step>
- Change:
- Focused check:
- Completion criterion:
- Rollback/containment:

## Validation ladder
| Order | Command or check | Expected result | Evidence path |

## Risks and rollback
## Cleanup preservation list
## Review handoff
```

## Completion check

- Every acceptance criterion has a change step and validation.
- Every step names exact targets and a checkable completion criterion.
- Risk-specific thresholds and evidence paths are explicit.
- Pre-existing work and evidence are in the preservation list.
- Baseline and plan path are ready for review.
- Unresolved decisions are visible blockers rather than hidden assumptions.

Return the plan path, baseline, first step, validation ladder, preservation list, and blockers.
