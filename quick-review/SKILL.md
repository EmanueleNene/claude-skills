---
name: quick-review
description: Light review of a diff mid-work - bugs, simplify, yagni - by Agy (Gemini 4 Hydrogen) to spare Claude usage, with a preview patch; edits only on your go. No commit.
disable-model-invocation: true
---

# Quick Review

A fast look while the work is still moving. **Agy** (`gemini-4-hydrogen-high`) does the review so it spends Gemini quota, not Claude usage; the parent only relays, previews, and applies. Nothing touches the files until the user says go. For the full end-of-work gate and shipping, the user runs `/no-mistake`.

## 1. Fix the target

User-given paths or range, else uncommitted work (`git diff HEAD` plus untracked files), else the last commit.

Done when the target is a concrete file/line list. Empty target (no diff and no untracked files): stop and say so.

## 2. Review with Agy

Check `command -v agy` and take a **fingerprint** of the working tree:

```bash
{ git status --porcelain; git diff HEAD; git ls-files -o --exclude-standard -z | xargs -0 -r git hash-object; } 2>/dev/null | git hash-object --stdin
```

Run from the repo root (the timeout turns a stalled run into a failure):

```bash
agy -p "<prompt>" --model gemini-4-hydrogen-high --print-timeout 20m
```

Without `agy`, or when the run fails, a `haiku` subagent (`model: haiku`) runs the same prompt instead; name the reason in the preview.

The prompt carries:

- How to see the diff (the git command for the step 1 target), the target file list, and that untracked files are read in full.
- Read-only: edit nothing, propose only.
- Three lenses: **Correct** (wrong, unsafe, or untested; flag `BUG`), **Simplify** (a name, branch, or expression a reader decodes slower than needed), **YAGNI** (a line, option, or abstraction nothing uses; deletion beats extraction).
- Findings that trace to the target only; behavior changes only for `BUG`s.
- Output: one line per finding `file:start-end (symbol) | lens | problem with its failure path (input or state -> wrong result) | fix | check that proves it`, `BUG`s first, then one unified diff of all proposed edits.

Keep `--mode plan` and `--dangerously-skip-permissions` off the command: plan mode writes a plan file instead of answering. After it returns, retake the fingerprint; if it changed, stop and show the user `git status` and `git diff HEAD` (do not revert: the tree holds uncommitted user work).

Done when the findings and diff are back and the fingerprint is unchanged.

## 3. Preview

Two readers: the user has ADHD and scans the table; an agent applying a row later works from its detail block and hunk alone. Row numbers tie them together. Show only this:

1. **First line:** `<N> findings, <B> bugs - reply "go", "go 1,3", or "skip"`.
2. **One table**, `BUG`s first, at most 5 rows per lens (past that, `+N more <lens>`):

   | # | Where | Lens | Problem | Fix |
   |---|-------|------|---------|-----|
   | 1 | `src/auth.ts:42` | BUG | null token crashes login | guard `token` |

   `Where` is a clickable `file:line`. `Problem` and `Fix` are at most 8 words each.
3. **Detail for agents**, under a `---` rule: per row, `#<row> <lens> - <file>:<start>-<end> (<symbol>)`, then `Problem:` with the failure path (input or state -> wrong result) and `Check:` with the command or test that proves the fix. The fix itself is the row's hunk below.
4. **The preview**: one `diff` block, each hunk preceded by a `# <row>` comment line so the user can pick rows. Drop hunks outside the target. Check tracked-file hunks with `git apply --check`; read untracked-file hunks against the file. Mark any hunk that does not fit.

Name the fallback in one line under the table if Haiku ran. No preamble, no closing line.

Done when the user has the table and the preview. Stop and wait.

## 4. Apply on go

Apply only what the user accepts (all, a subset, or none), as direct edits to the current file contents. Run the smallest validation command (tests, build) if one exists, and report it.

Done when the accepted edits are in and validation is reported. Commit and push are the user's next call.
