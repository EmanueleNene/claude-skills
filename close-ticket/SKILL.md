---
name: close-ticket
description: "Close a ticket in any repo: update the ticket, commit, push, merge to the default branch. Use when the user says close / update / merge / finish the ticket or issue #N, or 'commit push and merge'."
---

# Close ticket

A **ticket** is issue #N plus its branch, and the repo's local ticket notes if it keeps any.
The repo's own rules win over this skill: read them first (`docs/WORKFLOW.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`).

## Steps

1. **Rules.** From the repo docs note: branch naming, merge style, commit format, where ticket notes live
   (e.g. `tickets/N-name/ISSUE.md`). Find the default branch: `git symbolic-ref --short refs/remotes/origin/HEAD`.
   Done when you know all five, or know the repo has no rule for one (then use the defaults below).
2. **Inventory.** Switch to the ticket branch, `git status --short`, `git log --oneline <default>..HEAD`.
   Done when every uncommitted change is sorted: belongs to #N (commit it) or not (leave it, tell the user).
3. **Commit** what is left for #N. Code (not docs/tests): run `/simplify` on the changed lines first.
   Repo commit format, else Conventional Commits; body ends `Refs #N`; attribution lines per the user's CLAUDE.md.
   Keep each file's line endings. Generated output and ignored files go in only when the user asked (`git add -f`).
   Done when `git status` shows nothing of #N.
4. **Ticket notes**, if the repo keeps them: append a dated section with what changed, commands run,
   key numbers before -> after, what is left. Done when someone could redo the work from it.
5. **Issue comment** (`gh issue comment N` on GitHub): what changed (commits), commands run, metrics that moved,
   what was not run or not checked. Done when the comment has all four.
6. **Merge.** `git switch <default> && git pull`, then the repo's merge style, else
   `git merge --no-ff <branch> -m "Merge #N: <issue title>" -m "Closes #N"`; `git push`; `git branch -d <branch>`.
   Use `Refs #N` instead of `Closes #N` when the issue stays open. If the repo merges via pull requests,
   open the PR (`gh pr create`, body says `Closes #N`) and stop there unless the user said to merge it.
7. **Verify.** `git status -sb` shows the default branch in sync with origin; the issue reads `CLOSED`
   (GitHub can lag a few seconds: check again before reporting). Done when both hold.
8. **Report** in plain words: commits merged, issue link, what is left, and any risk.
