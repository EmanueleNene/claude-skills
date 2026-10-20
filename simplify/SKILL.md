---
name: simplify
description: "Review and refine code for clarity, consistency, and maintainability while preserving exact functionality. Bounded to recently modified or specified lines. MANDATORY TRIGGERS: '/simplify', 'simplify', 'simplify code', 'code simplifier'. Pair with `yagni-refactor` when structural bloat or dead abstractions need cutting first."
---

# Simplify (Code Simplifier)

Review and refine code for clarity, consistency, and maintainability while strictly preserving all functionality. Focus on recently modified or targeted code lines.

## Principles

1. **Preserve Functionality Strictly**: Never alter what the code does or what it outputs. All existing tests, numerical baselines, and invariant checks must pass with zero deviation.
2. **Apply Project Standards**: Follow the conventions established in `CLAUDE.md` and `AGENTS.md` (e.g. naming rules, Fortran style, double precision, Python typing, error handling).
3. **Enhance Clarity & Flatten Logic**:
   - Reduce unnecessary nesting and cyclomatic complexity using guard clauses and early returns.
   - Eliminate redundant local variables and intermediate single-use abstractions.
   - Avoid nested ternary operators — prefer explicit `if/else` chains or switch/dispatch blocks.
   - Improve variable, routine, and argument names for self-documenting intent.
   - Consolidate tightly related logic.
4. **Clean Noise, Protect Domain Rationale**:
   - Remove trivial comments that merely restate syntax (e.g., `i = i + 1 ! increment`).
   - Strictly preserve comments that explain physical models, mathematical derivations, boundary conditions, tolerance choices, or non-obvious invariants.
5. **Maintain Balance**:
   - Explicit and readable code is always superior to dense, clever one-liners.
   - Do not combine too many concerns into single monolithic functions.
   - Do not strip useful modularity or helpful abstractions.
   - When renaming files or folders during simplification, always use `git mv`.

## Scope

- Focus strictly on changed lines (from `git diff`, `git status`, or the specified file paths).
- You may read surrounding code for context, but do not edit outside the target scope unless essential to fix a broken contract.
- If a worthwhile simplification requires editing wider unchanged code, document it as a recommendation rather than expanding the diff.

## Process

1. **Inspect the Diff / Changed Lines**: Identify the files and exact line ranges modified or targeted.
2. **Scan for Simplification Opportunities**: Check for deep nesting, redundant intermediate state, unclear names, dead branches, and code smells.
3. **Apply Targeted Edits**: Refine the code file-by-file, maintaining strict behavior preservation and adhering to project rules.
4. **Validate**: Run the relevant test suite, convergence check, or validation command to prove zero behavioral drift.
5. **Summarize**: Report what was simplified, lines cleaned, and validation results.
