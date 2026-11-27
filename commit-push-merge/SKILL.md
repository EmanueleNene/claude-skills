---
name: commit-push-merge
description: "Commit, push, and merge into the default branch so everything goes live, on any branch, no ticket to close. Use when the user says 'commit push and merge' with no issue #N, or 'ship it live'."
---

# Commit, push, merge

Invoking this skill authorizes every step below. Ask only when scope is uncertain or a step stops.

## Steps

1. **Scope and validate.** Scope as in `commit-push` step 1, including commits already ahead on the branch.
   For code changes (not docs or tests), run `/simplify` on the changed lines, then validate as in `commit-push` step 2.
   Note from the repo rules whether it merges only via pull requests, and its merge style.
   Done when the exact scope is known and its checks pass on the final content.

2. **Message.** Draft as in `commit-push` step 3, then shorten it with `caveman:caveman-commit`.
   Done when the short message keeps the repo format and attribution rules and still says what changed and why.

3. **Commit** as in `commit-push` step 4.

4. **Push the current branch.** `git fetch origin`, then `git push -u origin <branch>`.
   Rejected or diverged: stop and report. Never force-push.
   Done when `git status -sb` shows the branch in sync with its remote.

5. **Merge.** Default branch: `git symbolic-ref --short refs/remotes/origin/HEAD` (strip `origin/`); if unset, run `git remote set-head origin --auto` and retry.
   - **Already on the default branch:** skip to step 6.
   - **PR-only repo:** stop here and offer `gh pr create --base <default> --head <branch>`.
   - **Repo requires a merge style other than `--no-ff`** (squash, rebase): stop and report.
   - **Feature branch:** the merge runs where `<default>` is checked out (`git worktree list`); elsewhere use `git -C "<that-worktree>"`, else `git switch <default>` in this one. Before merging, both must hold, else stop and report:
     - that worktree is clean: `git status --porcelain` is empty;
     - local `<default>` has no unpushed commits: `git log --oneline origin/<default>..<default>` is empty.

     Then:
     ```
     git pull --ff-only origin <default>
     git merge --no-ff <branch> -m "Merge <branch>"
     git push origin <default>
     ```
   - **Merge conflict:** `git merge --abort`, then stop and report. Never resolve conflicts on your own.
   - **Push of `<default>` rejected:** stop and report that local `<default>` holds an unpushed merge commit.

   Keep the feature branch; delete it only if the user asks.
   Done when `<default>` is pushed, or the stop reason is reported.

6. **Verify and report.** Where `<default>` is checked out, `git status -sb` shows it in sync with `origin/<default>`, and `git branch -r --contains <commit>` lists `origin/<default>`. Skip the check if step 5 stopped.
   Report in plain words: commit hash and subject, branches pushed, merge result or stop reason, and what is left uncommitted locally.
