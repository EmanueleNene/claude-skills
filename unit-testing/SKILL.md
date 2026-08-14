---
name: unit-testing
description: Unit-test existing behavior at stable interfaces. Use when the user wants unit tests added or improved, a regression characterized, or a refactor protected; use when `yagni-refactor` needs a behavioral contract or `continuous-integration` needs a reliable test command.
---

# Unit Testing

Create the smallest test set that detects meaningful behavioral regressions. Test contracts through stable interfaces rather than mirroring implementation.

## 1. Find the contract

Read the relevant implementation, callers, existing tests, and repository test conventions. Identify:

- observable behavior callers rely on,
- the highest-risk branch or boundary,
- the narrowest stable interface that exposes it,
- the existing command that runs the relevant tests.

Proceed when each proposed test protects a named behavior or risk. If a test would only confirm implementation details, omit it.

## 2. Choose the smallest sufficient cases

Cover one representative success case, then add only cases justified by distinct behavior: a boundary, failure mode, or reproduced regression. Reuse the repository's current framework and helpers. Prefer real values and deterministic collaborators; use a fake only at an existing slow, external, or nondeterministic seam.

Proceed when every case can fail for a different contract violation and no case exists solely to increase coverage.

## 3. Establish the signal

For a regression, run the new test against the faulty behavior and confirm the expected failure before the fix. For characterization of correct behavior, confirm the test passes before restructuring. Keep failure messages diagnostic and remove incidental assertions.

Proceed when the test's result distinguishes the protected contract from the behavior that would violate it.

## 4. Validate and hand off

Run the focused test command, then the smallest existing broader suite affected by the change. Report both commands and results. If a stable interface must be improved for testability, hand that structural change to `yagni-refactor` and use `codebase-design` only when a real seam is involved. Give the reliable broader command to `continuous-integration` when automation is requested.

Testing is complete when all added tests protect named behavior, pass deterministically, and the relevant existing suite remains green.
