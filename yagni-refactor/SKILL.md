---
name: yagni-refactor
description: "Refactor existing code with YAGNI discipline and pair with code-simplifier. MANDATORY TRIGGERS: 'refactor', 'refactoring', '/refactor', 'clean up this code', 'simplify this', 'simplify code'. Use whenever the user asks to refactor, simplify, or restructure code for maintainability without speculative abstractions."
---

# YAGNI Refactor & Code Simplifier

Refactor for the next concrete change, not an imagined future. Prefer deletion, locality, and deep modules over additional layers, and apply code simplification to ensure maximum clarity and maintainability.

## 1. Establish the contract

Read the smallest relevant slice of code, its callers, and its checks. State:

- behavior that must remain unchanged,
- the concrete maintenance pressure motivating the refactor,
- the smallest relevant validation command.

Proceed when preserved behavior and one present-day source of friction are explicit. If no concrete friction exists, recommend leaving the code alone.

## 2. Secure the baseline

Run the focused validation. If behavior lacks coverage, use the `unit-testing` skill to add the smallest check that captures the contract before restructuring.

Proceed when the baseline passes and would detect damage to the preserved behavior.

## 3. Make the smallest structural improvement (YAGNI)

Apply this order, stopping as soon as the concrete friction is removed:

1. Delete dead code, unused parameters, and obsolete options.
2. Replace custom machinery with language, standard-library, or existing-project features.
3. IMPROVE NAMES and place related behavior together. When renaming or moving files or folders, use `git mv` so Git history and traceability are preserved.
4. Extract duplicated policy only when multiple live callers must agree.
5. Introduce or reshape a seam only where behavior varies now.

Keep interfaces smaller than their implementations. Make the likely change local rather than pre-building multiple possible changes. When a real seam is involved, use the `codebase-design` skill. Whenever renaming files or directories is necessary, always execute `git mv` rather than deleting and recreating, ensuring diff tracking and history remain intact.

## 4. Apply Code Simplification (Local Clarity & Refinement)

Once structural bloat is removed, apply the `simplify` skill (Code Simplifier) to the touched code:

- **Preserve functionality strictly**: Zero behavioral or numerical drift. All existing tests and outputs must remain identical.
- **Flatten nested logic**: Reduce indentation and cyclomatic complexity with early returns, guard clauses, or clean dispatch tables. Avoid nested ternary operators.
- **Clarity over brevity**: Explicit and readable code is always superior to dense, clever one-liners.
- **Clean noise, protect rationale**: Eliminate comments that merely restate code syntax, but strictly preserve comments explaining physical rationale, mathematical formulations, domain rules, or non-obvious invariants.
- **Bounded scope**: Restrict edits to the files and line ranges touched by the refactoring; avoid touching unaffected areas.
- **Delegate when available**: If subagents are enabled, invoke `simplify` to review and refine the diff before final verification.

Proceed when the stated friction is removed with no unused flexibility added and the implementation is clean, direct, and explicit.

## 5. Prove the refactor

Run the focused validation, inspect the diff, and account for every changed line as either required restructuring, simplification, or contract protection. Report:

- what became simpler and what was deleted,
- how code-simplifier principles were applied (nesting reduced, names clarified),
- the validation performed and test outputs,
- any concrete extension that is now easier,
- remaining risk.

Give any new reliable repository-wide validation command to `continuous-integration` when automation is requested. The refactor is complete when behavior is preserved, the diff contains no speculative mechanism, and the motivating change is demonstrably more local, robust, and easy to understand.
