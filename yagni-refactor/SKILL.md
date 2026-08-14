---
name: yagni-refactor
description: "Refactor existing code with YAGNI discipline. MANDATORY TRIGGERS: 'refactor', 'refactoring', '/refactor', 'clean up this code', 'simplify this'. Use whenever the user asks to refactor, simplify, or restructure code for maintainability without speculative abstractions."
---

# YAGNI Refactor

Refactor for the next concrete change, not an imagined future. Prefer deletion, locality, and deep modules over additional layers.

## 1. Establish the contract

Read the smallest relevant slice of code, its callers, and its checks. State:

- behavior that must remain unchanged,
- the concrete maintenance pressure motivating the refactor,
- the smallest relevant validation command.

Proceed when preserved behavior and one present-day source of friction are explicit. If no concrete friction exists, recommend leaving the code alone.

## 2. Secure the baseline

Run the focused validation. If behavior lacks coverage, use the `unit-testing` skill to add the smallest check that captures the contract before restructuring.

Proceed when the baseline passes and would detect damage to the preserved behavior.

## 3. Make the smallest structural improvement

Apply this order, stopping as soon as the concrete friction is removed:

1. Delete dead code and obsolete options.
2. Replace custom machinery with language, standard-library, or existing-project features.
3. IMPROVE NAMES and place related behavior together.
4. Extract duplicated policy only when multiple live callers must agree.
5. Introduce or reshape a seam only where behavior varies now.

Keep interfaces smaller than their implementations. Make the likely change local rather than pre-building multiple possible changes. When a real seam is involved, use the `codebase-design` skill.

Proceed when the stated friction is removed with no unused flexibility added.

## 4. Prove the refactor

Run the focused validation, inspect the diff, and account for every changed line as either required restructuring or contract protection. Report:

- what became simpler,
- the validation performed,
- any concrete extension that is now easier,
- remaining risk.

Give any new reliable repository-wide validation command to `continuous-integration` when automation is requested. The refactor is complete when behavior is preserved, the diff contains no speculative mechanism, and the motivating change is demonstrably more local or easier to understand.
