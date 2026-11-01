---
name: no-mistake
description: Final gate before commit or PR - code-review plus simplify and yagni-refactor on one diff, merged into one verified change.
disable-model-invocation: true
---

# No Mistake

One gate, two agents on the same diff, one merged result.

| Agent | Skills | Question |
|-------|--------|----------|
| Correct | `code-review` | Is it wrong, unsafe, or untested? |
| Lean | `simplify` + `yagni-refactor` | Is any line speculative, deletable, or harder to read than needed? |

Lean's two skills can contradict (simplify extracts a helper, yagni deletes it); the agent resolves that itself, deletion first. The agents never edit. They **propose**, the parent **edits once**.

## 1. Fix the target

Resolve the diff: user-given paths or range, else `git diff` plus staged changes, else the last commit. List files and line ranges.

Done when the target is a concrete file/line list. Empty diff: stop and say so.

## 2. Baseline

Find the smallest validation command (tests, build, convergence check). Run it before any edit.

Done when the baseline result is recorded. A red baseline is reported, not fixed here; continue review but mark it.

## 3. Review in parallel, propose-only

Spawn two agents in one message. Every agent gets: the target list, the skill name(s) to follow, and this contract:

- Read-only. Edit nothing.
- Return findings as `file:line | problem | proposed fix | agent`.
- Drop findings that would change behavior, except correctness bugs, which are flagged `BUG`.

Model: `sonnet` for both (review agents, per CLAUDE.md). The Correct agent also gets the effort level the user typed, if any.

Done when both agents have reported.

## 4. Merge

In the parent, one list:

1. **Dedupe** findings on the same line.
2. **Resolve conflicts** by priority: `BUG` > Lean. Deletion beats extraction.
3. **Reject** any finding that does not trace to the diff or to behavior the diff touches (surgical changes).
4. **Escalate** to the user any `BUG` fix that changes public behavior, and any fix needing code outside the target.

Done when every finding is marked applied, rejected (with reason), or escalated.

## 5. Apply once, then prove

Apply the accepted list in one pass, smallest edits first. Rerun the step 2 command.

Done when the validation matches or beats the baseline. If it regressed, revert the edit that caused it and mark that finding rejected.

## 6. Report

Plain language, short:

- **Bugs**: found, fixed, escalated.
- **Simplified / deleted**: counts and the notable ones.
- **Rejected** findings with reason.
- **Validation**: baseline vs final.
- **Not checked**: what no lens could cover (no tests, no runtime access).

Do not commit. Committing belongs to the user or `close-ticket`.
