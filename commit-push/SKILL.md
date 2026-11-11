---
name: commit-push
description: "Commit and push scoped changes with concise, informative commit messages and verified remote delivery. Use when the user requests commit and push, including after no-mistake or delivery-pipeline."
---

# Commit and push

Finish the intended work on the current branch. Accept the caller's objective, selected changes, review baseline, validation evidence, and destination. Invocation by the user authorizes commit and push; a handoff from another skill carries only authorization already given. Without that authorization, prepare the file selection and message before asking to publish.

## 1. Establish scope and destination

Read applicable repository and user instructions for commit format, attribution, checks, and branch rules. Inspect `git status --short --branch`, staged and unstaged diffs, untracked file contents, and recent commit subjects. Identify the current branch, remote push URL, upstream, and any commits already ahead of the destination.

Classify each changed file or hunk as include, leave out, or uncertain, using the user's request and review scope. Staging alone does not prove a change belongs. Include necessary tests, documentation, and dependency updates with their change; preserve unrelated work and existing staging. Generated evidence follows repository rules and the caller's preservation plan, rather than being included wholesale.

When ownership, required behavior, a dependency between changes, or the destination is unclear, ask a focused question naming the affected paths or hunks, the uncertainty, and the proposed selection. Do the unambiguous preparation first; wait before committing or pushing the affected work. Do not infer permission for unrelated outgoing commits from permission to push the current task.

Done when the exact commit scope and outgoing history have an understood purpose and authorized destination. Detached HEAD or an unresolved Git operation requires resolution before proceeding.

## 2. Preserve validation confidence

Reuse recent validation and review evidence only when it covers the selected final content. Run missing repository-required or risk-appropriate checks. If other local changes could mask a failure, validate the selected snapshot in isolation or report that limitation. Check the selected diff for whitespace errors, accidental credentials, local configuration, debug output, and unintended generated or binary files.

This is a finishing step: return substantive defects to implementation or review. Do not start a fresh refactoring cycle. A failed required check blocks completion; an unavailable check must be disclosed and resolved under repository rules and existing authorization.

Done when the selected content has appropriate validation and no unresolved blocker.

## 3. Write the commit message

Write from the final diff and its established purpose. Follow repository conventions; otherwise use a short imperative subject. Aim for about 50-72 characters without sacrificing meaning.

- Put the concrete change and distinguishing behavior in the subject, so `git log --oneline` is useful. Avoid vague subjects such as "update files" or "address feedback".
- Use a body only when the subject leaves out an important reason, behavior change, compatibility impact, or limitation. Lead with the most consequential missing fact; usually one short paragraph or a few bullets suffice.
- Omit file inventories, implementation narration, repeated subject text, routine check logs, and unsupported claims. Include validation details only when they materially affect interpretation of the change.
- Include issue references and required trailers when applicable. Follow user attribution rules and use only real, available session links.
- Make each commit one coherent change. Split independent work when grouping is clear; ask when splitting would require guessing intent. Preserve necessary dependencies within a commit.

Example:

```text
fix(auth): retain the return URL through session renewal

Expired sessions now return users to their requested page after login.
Previously, renewal discarded the saved destination.
```

Done when a reader can understand the change immediately, and every sentence adds supported information. Show the selected scope and proposed message before execution; an already-authorized, unambiguous commit needs no extra confirmation.

## 4. Stage and commit exactly that scope

Stage explicit paths or selected hunks. If unrelated changes are already staged, isolate the intended index without losing the user's staged state; ask if that cannot be done confidently. Never use blanket staging to bypass selection.

Inspect the complete staged diff and file list against the agreed scope. Preserve line endings and modes. Create the commit using safe quoting or a temporary message file; let hooks run. If hooks fail or change files, inspect the result and rerun affected checks before retrying. Keep user-authored commits intact; do not amend or rewrite history without authorization.

Done when the created commit contains exactly the intended content and message. If there is nothing new to commit, inspect existing outgoing commits and continue only if they are in scope.

## 5. Push and verify

Refresh the destination's remote state and inspect ahead/behind history. Use an ordinary push with an explicit remote and branch; establish the upstream if needed. If the destination diverged or the push is rejected, inspect the cause and stop for a decision when reconciliation changes history or scope. Never force-push, bypass hooks, switch branches, or automatically merge/rebase to make publication succeed.

Verify the remote branch contains the intended revision, inspect tracking status, and account for remaining staged, unstaged, and untracked work. An unexpectedly newer remote tip needs a containment check; a successful command alone is insufficient evidence.

Report commit hash and subject, destination branch, validation result, and remaining local work. If pushing fails after committing, report that distinction and the next action; preserve the local commit.

Done when the intended commit is verified on the destination and any remaining work is explicitly accounted for.
