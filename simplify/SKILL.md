---
name: simplify
description: "Improve local code readability while preserving behavior and project conventions. Use for /simplify, requests to simplify code, clarify names, flatten control flow, or make code easier to read, and for a clarity pass during authorized coding work. Explicit refactoring or structural cleanup belongs to yagni-refactor."
disable-model-invocation: false
---

# Simplify (Code Simplifier)

Reduce the cognitive workload needed to read code: fewer facts to keep in mind, fewer jumps to understand a flow, and clearer domain intent. Preserve or improve understanding while strictly preserving functionality and project conventions. Fewer lines, tokens, variables, or functions are not success criteria. Focus on recently modified or targeted code lines.

## Routing

- `/simplify`, "simplify this code", "make this easier to read", and an otherwise unspecified "clean up this code" select this skill.
- Work on names, expressions, comments, and local control flow within the existing structure.
- Requests to refactor or restructure code, remove dead code or speculative abstractions, or reshape module boundaries select `yagni-refactor`.
- For mixed wording, the concrete requested change determines the route: "simplify by removing this unused abstraction" selects `yagni-refactor`; "refactor these names for readability" selects `simplify`.
- Other skills may call this skill for a bounded clarity pass. If readability work reveals structural work outside the requested scope, report that opportunity separately.

## Principles

1. **Preserve Functionality Strictly**: Never alter what the code does or what it outputs. All existing tests, numerical baselines, and invariant checks must pass with zero deviation.
2. **Apply Project Standards**: Read applicable `CLAUDE.md`, `AGENTS.md`, style guides, and naming/domain glossaries before editing. Use neighboring code to establish conventions where written rules are silent. Preserve naming patterns, domain terminology, formatting, types, precision, interfaces, and error-handling conventions. Choose clearer names within those conventions; retain meaningful units, qualifiers, and distinctions. Avoid abbreviations or generic names that make readers reconstruct meaning.
3. **Enhance Clarity & Flatten Logic**:
   - Reduce nesting with guard clauses and early returns when they make the execution path easier to follow and preserve cleanup and side-effect ordering.
   - Keep named intermediate values that explain a calculation, condition, unit, or domain concept, even when used only once. Inline a value only when the resulting expression is easier to understand without repeated interpretation.
   - Avoid nested ternary operators — prefer explicit `if/else` chains or switch/dispatch blocks.
   - Improve variable, routine, and argument names for self-documenting intent.
   - Keep related logic together and make state changes and dependencies visible. Extract or retain helpers when their names express a coherent concept and reduce what the caller must understand; inline them only when doing so reduces navigation without obscuring intent.
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
2. **Identify Reading Burdens**: Establish the applicable conventions, then identify concrete burdens in the target code: deeply nested paths, scattered related logic, unclear domain meaning, hidden dependencies, or unnecessary state. For each proposed change, identify what the reader will no longer need to track or infer.
3. **Apply Targeted Edits**: Refine the code file-by-file, maintaining strict behavior preservation and adhering to project rules.
4. **Review Understanding and Validate**: Compare each edited block with its original. Can a reader still identify its purpose, conditions, data flow, side effects, and domain rationale at least as easily? Check names and other conventions against the sources read above. Rework or discard edits that trade understanding for brevity; leave already-clear code unchanged. Run relevant tests, convergence checks, or validation commands for behavioral preservation, and applicable lint/style checks. Report any unavailable checks; passing tests alone does not establish readability.
5. **Summarize**: Report which reading burdens were reduced, how conventions were preserved, and validation results. Do not use lines removed as evidence of clarity.
