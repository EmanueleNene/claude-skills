---
name: commit-push-merge
description: "Commit with a caveman-short message, push, and merge into the default branch so everything goes live, on any branch, no ticket needed. Use when the user says 'commit push and merge', 'ship it live', or invokes /commit-push-merge."
---

# Commit, push, merge

One run takes local work all the way live. Invoking this skill authorizes every step below: commit, push the branch, merge into the default branch, push the default branch. Ask only when scope is uncertain or a step stops.

## Steps

1. **Scope and validate** as in `commit-push` steps 1-2: read repo rules, sort every change into include / leave out / uncertain, run required checks.
   For code changes (not docs or tests), run `/simplify` on the changed lines.
   Done when the exact file set is known and its checks pass.

2. **Message.** Draft the message from the final diff, then run it through `caveman:caveman-commit` to make it short.
   Keep the repo's commit format and the user's attribution rules: add no `Claude-Session:` trailer and no `Co-Authored-By`.
   Done when the short message still says what changed and why.

3. **Commit.** Stage explicit paths only, check `git diff --cached --stat` matches step 1, commit with a message file. Let hooks run; never amend.
   Done when `git status` shows nothing of the selected scope.

4. **Push the current branch** with `git push -u origin <branch>`.
   Done when `git status -sb` shows the branch in sync with its remote.

5. **Merge.** Find the default branch: `git symbolic-ref --short refs/remotes/origin/HEAD` (strip `origin/`).
   - **Already on the default branch:** nothing to merge; step 4 already put it live. Skip to step 6.
   - **Feature branch:** check `git worktree list`. If the default branch is checked out in another worktree, run the commands there with `git -C <that-worktree>`; else `git switch <default>`. Then:
     ```
     git pull --ff-only
     git merge --no-ff <branch> -m "Merge <branch>"
     git push origin <default>
     ```
   - **Conflict, rejected push, or a repo that merges only via pull requests:** stop and report. Never force-push, never resolve conflicts on your own. For PR-only repos, offer `gh pr create`.
   Keep the feature branch; delete it only if the user asks.
   Done when the default branch is pushed, or the stop reason is reported.

6. **Verify and report.** `git status -sb` shows the default branch in sync with origin, and `git branch -r --contains <commit>` lists `origin/<default>`.
   Report in plain words: commit hash and subject, branches pushed, merge result, and what is left uncommitted locally.
