---
name: no-mistake
description: End-of-work gate - correctness, simplify + yagni, Codex, and adversarial reviews on one diff, run on Agy Hydrogen and Codex; when green, commits, pushes, and closes the ticket.
disable-model-invocation: true
---

# No Mistake

One gate, four reviewers on the same diff, one merged result. The reviewers run on Agy (`gemini-4-hydrogen-high`) and Codex so the review spends their quota; Claude orchestrates, merges, and edits.

| Reviewer | Engine | Lens | Question |
|----------|--------|------|----------|
| Correct | Agy; fallback `sonnet` subagent | `code-review` | Is it wrong, unsafe, or untested? |
| Lean | Agy; fallback `sonnet` subagent | `simplify` + `yagni-refactor` | Is any line speculative, deletable, or harder to read than needed? |
| Codex | Codex CLI `review` on Astra (medium/high); fallback Agy, then `haiku` subagent | built-in | Second model family: what did the others miss? |
| Adversary | Agy; fallback Codex `adversarial-review`, then `haiku` subagent | adversarial | Why should this not ship? |

Lean's two skills can contradict (simplify extracts a helper, yagni deletes it); the reviewer resolves that itself, deletion first. No reviewer edits. They **propose**, the parent **edits once**.

## 1. Fix the target

Resolve the diff: user-given paths or range, else uncommitted work (`git diff`, staged changes, and untracked files), else the last commit. List files and line ranges.

Done when the target is a concrete file/line list. Empty diff: stop and say so.

## 2. Baseline

Find the smallest validation command (tests, build, convergence check). Run it before any edit.

Done when the baseline result is recorded. A red baseline is reported, not fixed here; continue review but mark it.

## 3. Review in parallel, propose-only

First run the availability checks below (`command -v agy`, Codex `setup --json`, the Astra slug) and take a **fingerprint** of the working tree:

```bash
{ git status --porcelain; git diff HEAD; git ls-files -o --exclude-standard -z | xargs -0 -r git hash-object; } 2>/dev/null | git hash-object --stdin
```

Then start all four reviewers (or their stand-ins) in one message, each in the background. Every reviewer gets the target list, how to see the diff (the git command matching the step 1 target, e.g. `git diff HEAD` plus the untracked file list, or `git show HEAD`, and to read untracked target files in full), its lens, and this contract:

- Read-only. Edit nothing.
- Return each finding as `file:start-end (symbol) | problem with its failure path (input or state -> wrong result) | exact fix (old -> new, or a short diff) | check that proves it | reviewer`.
- Drop findings that would change behavior, except correctness bugs, which are flagged `BUG`.

**Agy runs.** Each Agy reviewer is one `Bash` call (`run_in_background: true`) from the repo root; the timeout turns a stalled run into a failure, which triggers the fallback:

```bash
agy -p "<prompt>" --model gemini-4-hydrogen-high --print-timeout 20m
```

Agy cannot load Claude skills by name: for a skill lens, the prompt tells the reviewer (Agy, or its `sonnet` fallback) to read `~/.claude/skills/<skill>/SKILL.md` and use only its review criteria on the step 1 diff (for `Correct`, also check correctness bugs, safety/security flaws, and missing tests as `BUG`s). It skips the skill's process: no fixed-point or spec questions, no subagents, no other skills, no questions to the user. Keep `--mode plan` (it writes a plan file instead of answering) and `--dangerously-skip-permissions` off the command. Retake the fingerprint before launching any fallback for a failed run, and again when all runs finish; if it changed, a reviewer edited something: stop and show the user `git status` and `git diff HEAD` (do not revert: the target may hold uncommitted user work).

**Correct and Lean.** Agy runs with the lens skills from the table. If the user typed an effort level, Correct runs on the matching variant (`gemini-4-hydrogen-low`/`-medium`/`-high`/`-xhigh`). Without `agy`, or when a run fails, spawn that reviewer as a `sonnet` subagent with the same lens and contract.

**Codex.** Check it is installed and logged in:

```bash
CODEX="$(ls -d ~/.claude/plugins/cache/openai-codex/codex/*/ 2>/dev/null | sort -V | tail -1)scripts/codex-companion.mjs"
node "$CODEX" setup --json
```

If ready (`"ready": true` and `"loggedIn": true`), pick the Astra model from the local catalog:

```bash
grep -io '"slug": *"[^"]*astra[^"]*"' ~/.codex/models_cache.json | head -1 | cut -d'"' -f4
```

Run with `--model <slug>` on both `review` and `adversarial-review`; with no Astra slug, drop `--model` and Codex uses its configured default. These commands take no effort flag: effort comes from `model_reasoning_effort` in `~/.codex/config.toml`, which should be `medium` or `high`. Read it, report it in step 7's `Reviewers:` line, and leave the user's config as is.

```bash
node "$CODEX" review --wait [--model <slug>] <target flags>
```

Bash calls do not share variables: repeat the `CODEX=` line in every call that uses it.

Target flags from step 1: uncommitted work → `--scope working-tree` (covers staged, unstaged, untracked); last commit → `--base HEAD~1`; range or branch → `--base <ref>`. Codex cannot narrow to paths; drop its findings outside the target in step 4. Its top-severity bugs (`[P0]`/`[P1]`, or `critical`/`high`) count as `BUG`. When Codex is not ready or the run fails, a stand-in takes its place here and in step 6 (the step 6 stand-in reviews the working-tree diff of the target paths (reading untracked target files in full)): an Agy run asked for a general bug review, else a `haiku` subagent. Tag findings `codex` either way and name the stand-in in the report.

**Adversary.** An Agy run whose prompt is adversarial: break confidence in the change and find the strongest reasons it should not ship. Point it at trust boundaries, data loss or corruption, partial failure and retries, races and stale state, empty/null/timeout and degraded dependencies, and compatibility regressions. Material findings only, each with a concrete failure path; no style; a closing verdict `approve` or `needs-attention`. Findings it marks `BUG` count as `BUG`. Without `agy`, or when the run fails, fall back in order: Codex when ready (`node "$CODEX" adversarial-review --wait [--model <slug>] <target flags> "<path1>" "<path2>"`, one quoted argument per path; its `critical`/`high` count as `BUG`), else a `haiku` subagent with the same prompt. Tag findings `adversary` either way.

Done when all four reviewers (or their stand-ins) have reported.

## 4. Merge

In the parent, one list:

1. **Dedupe** findings on the same line.
2. **Resolve conflicts** by priority: `BUG` > Lean. A finding only one reviewer raised, and every adversary finding, gets verified in the code before it is accepted: the adversary is told to be aggressive, so it must show a concrete failure path. Deletion beats extraction.
3. **Reject** any finding that does not trace to the diff or to behavior the diff touches (surgical changes).
4. **Escalate** to the user any `BUG` fix that changes public behavior, and any fix needing code outside the target.

Done when every finding is marked applied, rejected (with reason), or escalated.

## 5. Apply once, then prove

Apply the accepted list in one pass, smallest edits first. Rerun the step 2 command.

Done when the validation matches or beats the baseline. If it regressed, revert the edit that caused it and mark that finding **reverted**.

## 6. Codex recheck, once

Skip if step 5 applied nothing. Otherwise rerun Codex in the foreground with `--scope working-tree` (falling back to the step 3 stand-in on the working-tree diff of the target paths (reading untracked target files in full) if Codex did not run or fails here), whatever the step 3 flags were: the step 5 fixes are uncommitted, and `--base` reviews only committed history. Drop findings outside both the target and the step 5 edits. Merge the rest with the step 4 rules, apply, and rerun the step 2 command; revert any edit that regresses validation and mark that finding **reverted**. A stand-in gets the step 3 contract, and an Agy stand-in is bracketed by a fresh fingerprint check.

One round only. Accepted recheck findings you do not apply go to the report as **Open**; ones the step 4 rules reject go under **Rejected** with the reason. No third Codex run.

Done when the recheck findings are applied, rejected, or listed as open, and validation still matches or beats the baseline.

## 7. Report

Two readers, one report. The user has ADHD and scans the top layer; another agent must be able to act on any row from the bottom layer alone, without re-reviewing. Row numbers tie the two layers together. Shape it like this and nothing else:

1. **First line: verdict and next action.** `GREEN - shipping`, `GREEN - stopped (no publish)`, or `BLOCKED - <the one thing to decide>`.
2. **One table**, the items that need the user's eyes first (escalated, open, reverted), then bugs fixed, then simplified:

   | # | Where | Problem | Fix | Status |
   |---|-------|---------|-----|--------|
   | 1 | `src/auth.ts:42` | null token crashes login | guard `token` | fixed |

   `Where` is a clickable `file:line`. `Problem` and `Fix` are at most 8 words each. `Status` is one word: `fixed`, `escalated`, `open`, `reverted`. Number every finding once, `1..N`, in table order; the table keeps those numbers. At most 5 rows per status; past that, one row `+N more <status> (#a-#b)` naming the hidden numbers, which still get detail blocks.
3. **Three short lines** under the table:
   - `Reviewers:` engine per reviewer, stand-ins named, Codex effort from `config.toml`, adversary verdict. Example: `Correct agy, Lean agy, Codex astra/high (or agy stand-in), Adversary agy (needs-attention)`.
   - `Validation:` baseline -> final, or `none in repo`.
   - `Not checked:` what no reviewer could cover, in a few words.
4. **Rejected** findings: one line, count plus a short reason each, e.g. `Rejected 3: style only (2), outside target (1)`.
5. **Detail for agents**, under a `---` rule: one block per row, every row including the `+N more` ones. Rows still to act on (`escalated`, `open`, `reverted`) get the full block; `fixed` rows get the header line plus `Changed:` in one sentence.

   ```text
   #3 escalated - src/auth.ts:42-58 (verifyToken)
   Problem: an expired token with a valid signature passes; verifyToken never reads `exp`, so a logged-out user keeps access.
   Fix: after the signature check, reject when `payload.exp * 1000 < Date.now()`; return 401 like the bad-signature branch.
   Check: npm test -- auth.spec.ts (add a case with an expired token)
   From: correct, adversary
   ```

   `Problem` names the failure path (input or state -> wrong result). `Fix` is exact enough to apply without searching: the symbol, the old and new behavior, or a short diff. `Check` is the command or test that proves it.

No preamble, no recap prose, no closing pleasantries. The step 8 lines (commit, push, ticket) go after the detail; the last line is always the one next action, or `Done`.

Done when the first and last lines alone tell the user what happened and what to do next. The report doubles as the ship decision below.

## 8. Ship when green

Invoking `/no-mistake` authorizes commit, push, and ticket close when the gate is **green**; the user wants no intervention on a clean run. If the user said not to publish, stop after the report. For a review without shipping they run `/quick-review`.

**Green** means all of these hold:

- Baseline was not red, and final validation matches or beats it (no validation command at all is allowed; say so in the report).
- Nothing was escalated in step 4 or step 6.
- Every verified `BUG` is fixed: none left **Open** or **reverted**.
- The adversary's verdict is `approve`, or each of its findings was fixed or rejected with a reason.
- All four reviewers reported (stand-ins count).

Not green: stop after the report, list each blocker, and name the next command (`/commit-push`, `/close-ticket #N`) the user can run once they decide.

Green, in order:

1. **Find the ticket**, before anything is pushed: user-given `#N`, else a branch name of exactly `N-slug`, `issue-N`, or `<prefix>/N-slug`, else a `Refs #N` / `Closes #N` in the commits ahead of the default branch. Confirm with `gh issue view N --json state,title` that it is `OPEN` and its title fits the work. None found, more than one candidate, or any doubt: carry on with no ticket.
2. **Commit and push**: invoke `commit-push` with the objective, `#N` for a `Refs #N` trailer when found, the exact reviewed scope (step 1 files plus step 5-6 fixes), final validation evidence, and the **Not checked** list. Authorization comes from this invocation. On the default branch of a repo that merges by pull request, stop instead: a direct push would bypass review. No ticket: stop after the push and say the ticket was not identified.
3. **Close the ticket**: invoke `close-ticket` for `#N`. Tell it the code already passed `no-mistake` (skip its `/simplify`), what was committed, the validation evidence, and the **Not checked** list for the issue comment. Its own rules decide the merge; a repo that merges by pull request stops at the opened PR. Already on the default branch, there is nothing to merge: tell it to commit and push its ticket-notes update, post the issue comment, then `gh issue close N`.

Done when the commit is on the remote and the ticket reads `CLOSED` (or the PR is open), or the run stopped at a named blocker. Append one short line per stage that ran (`Commit: <hash> <subject>`, `Pushed: <branch>`, `Ticket: #N closed` or the PR link), then the blocker if any, under the step 7 report.
