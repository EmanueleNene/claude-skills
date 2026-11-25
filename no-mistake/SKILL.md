---
name: no-mistake
description: Final gate before commit or PR - code-review, simplify + yagni-refactor, and a Codex review on one diff, merged into one verified change.
disable-model-invocation: true
---

# No Mistake

One gate, three reviewers on the same diff, one merged result.

| Agent | Skills | Question |
|-------|--------|----------|
| Correct | `code-review` | Is it wrong, unsafe, or untested? |
| Lean | `simplify` + `yagni-refactor` | Is any line speculative, deletable, or harder to read than needed? |
| Codex | Codex CLI `review` | Second model family: what did Claude miss? |

Lean's two skills can contradict (simplify extracts a helper, yagni deletes it); the agent resolves that itself, deletion first. No reviewer edits. They **propose**, the parent **edits once**.

## 1. Fix the target

Resolve the diff: user-given paths or range, else uncommitted work (`git diff`, staged changes, and untracked files), else the last commit. List files and line ranges.

Done when the target is a concrete file/line list. Empty diff: stop and say so.

## 2. Baseline

Find the smallest validation command (tests, build, convergence check). Run it before any edit.

Done when the baseline result is recorded. A red baseline is reported, not fixed here; continue review but mark it.

## 3. Review in parallel, propose-only

Spawn two agents and start the Codex review in one message. Every agent gets: the target list, the skill name(s) to follow, and this contract:

- Read-only. Edit nothing.
- Return findings as `file:line | problem | proposed fix | agent`.
- Drop findings that would change behavior, except correctness bugs, which are flagged `BUG`.

Model: `sonnet` for both (review agents, per CLAUDE.md). The Correct agent also gets the effort level the user typed, if any.

**Codex.** First check it is installed and logged in:

```bash
CODEX="$(ls -d ~/.claude/plugins/cache/openai-codex/codex/*/ 2>/dev/null | sort -V | tail -1)scripts/codex-companion.mjs"
node "$CODEX" setup --json
```

Skip Codex (here and in step 6) when the script is missing or the JSON lacks `"ready": true` and `"loggedIn": true`; list it under **Not checked** with the reason, e.g. "Codex not logged in". Otherwise run in the background with `Bash` (`run_in_background: true`):

```bash
node "$CODEX" review --wait <target flags>
```

Bash calls do not share variables: repeat the `CODEX=` line in every call that uses it.

Target flags from step 1: uncommitted work → `--scope working-tree` (covers staged, unstaged, untracked); last commit → `--base HEAD~1`; range or branch → `--base <ref>`. Codex cannot narrow to paths; drop its findings outside the target in step 4. Treat its output as findings tagged `codex`; its top-severity bugs (`[P0]`/`[P1]`, or `critical`/`high`) count as `BUG`. If the run fails, continue without it and list Codex under **Not checked**.

Done when both agents and the Codex run have reported.

## 4. Merge

In the parent, one list:

1. **Dedupe** findings on the same line.
2. **Resolve conflicts** by priority: `BUG` > Lean. A Codex finding no other reviewer raised gets verified in the code before it is accepted. Deletion beats extraction.
3. **Reject** any finding that does not trace to the diff or to behavior the diff touches (surgical changes).
4. **Escalate** to the user any `BUG` fix that changes public behavior, and any fix needing code outside the target.

Done when every finding is marked applied, rejected (with reason), or escalated.

## 5. Apply once, then prove

Apply the accepted list in one pass, smallest edits first. Rerun the step 2 command.

Done when the validation matches or beats the baseline. If it regressed, revert the edit that caused it and mark that finding rejected.

## 6. Codex recheck, once

Skip if step 5 applied nothing or Codex did not run. Otherwise rerun Codex in the foreground with `--scope working-tree`, whatever the step 3 flags were: the step 5 fixes are uncommitted, and `--base` reviews only committed history. Merge its new findings with the step 4 rules, apply, and rerun the step 2 command.

One round only. Findings from the recheck that you do not apply go to the report as **Open**; no third Codex run.

Done when the recheck findings are applied, rejected, or listed as open, and validation still matches or beats the baseline.

## 7. Report

Plain language, short:

- **Bugs**: found, fixed, escalated.
- **Simplified / deleted**: counts and the notable ones.
- **Rejected** findings with reason.
- **Codex recheck**: new findings, fixed, open.
- **Validation**: baseline vs final.
- **Not checked**: what no lens could cover (no tests, no runtime access).

When commit and push are already authorized, hand off to `commit-push` with the objective, exact reviewed scope, final validation evidence, and unresolved limitations. Otherwise finish with the report and name `commit-push` as the available next step. Running `no-mistake` alone does not authorize publication.
