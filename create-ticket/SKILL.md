---
name: create-ticket
description: Turn a discussed problem or a supplied description into a GitHub issue and a matching local Markdown ticket. Use when the user asks to ticket the discussion, create an issue with local notes, or invokes /create-ticket. Captures work without implementing it or closing existing tickets.
argument-hint: "[problem description, discussion topic, or existing issue URL]"
---

# Create Ticket

Capture one actionable issue in GitHub and in the current project's local ticket notes. The ticket must stand on its own for a fresh session that has never read this conversation.

## 1. Recover intent and repository conventions

Use `$ARGUMENTS` as the user's supplied description or pointer. Combine it with relevant conversation context; a later correction takes precedence over an earlier proposal. If no arguments are supplied, use the problem just discussed. If neither identifies a problem, ask for the problem description before drafting.

Read applicable project instructions (`CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/WORKFLOW.md`), issue templates, and representative local tickets. Determine the intended GitHub repository, ticket directory, and naming convention. Use the current project's repository, not the directory where this skill is installed. Resolve the repository through its remotes and `gh repo view`; use explicit `--repo OWNER/REPO` on issue operations. If multiple repositories remain plausible, ask which one.

Inspect only the relevant source, tests, documentation, and evidence needed to make the ticket accurate. Capture decisions already made, constraints, and unresolved questions. Distinguish observed behavior from suspected causes. Describe a proposed implementation as a proposal unless it was agreed or verified.

Complete when the problem, intended outcome, repository, and local ticket convention are known, or the remaining material ambiguity has been put to the user.

## 2. Draft a self-contained ticket

Follow the repository's issue template. Otherwise use the structure below, omitting sections that do not apply:

```markdown
# <concise, outcome-oriented title>

## Problem
<Current behavior, affected users or workflow, and why it matters.>

## Evidence and reproduction
<Relevant file paths, symbols, commands, observed output, or source links.>

## Desired outcome
<Observable behavior after the work is complete.>

## Scope and constraints
<Included work, explicit non-goals, compatibility requirements, agreed decisions.>

## Acceptance criteria
- [ ] <Observable result that can be checked.>

## Suggested approach
<Agreed direction or clearly labeled proposal; relevant code entry points.>

## Validation
<Relevant checks and expected outcomes; identify checks still to be determined.>

## Open questions and dependencies
<Unresolved decisions, unknowns, and linked prerequisite issues.>
```

Use concrete acceptance criteria, not a checklist of vague activities. Preserve enough evidence and rationale to avoid repeating the conversation. Include only task-relevant material suitable for the repository's audience; redact secrets and personal information. Do not invent reproduction steps, test results, root causes, or links.

Default to one issue. If the requested outcome needs multiple independently deliverable tickets, explain the proposed split and resolve scope before publishing several. When splitting is requested, prefer small end-to-end outcomes and record dependencies explicitly.

Complete when a new session can understand the problem, scope, completion conditions, and unknowns without chat history.

## 3. Preserve locally and publish

Invoking this skill to create a ticket authorizes the GitHub issue and local file. Proceed without another approval unless project instructions require one or the user asked for a draft/review first. A draft-only request produces a local draft and no GitHub mutation.

Search relevant existing local tickets and GitHub issues before creating anything. If an existing issue clearly captures the same work, link it and create or reconcile its local counterpart. Preserve existing notes; update a remote issue only when the user authorized that update. Ask when a possible duplicate has materially different scope.

Save the complete draft locally before the remote write. Follow the project's convention; absent one, use `tickets/draft-<slug>/ISSUE.md`. Keep the GitHub title separate from the body so the published body does not repeat the title. With `gh`, write the body to a temporary UTF-8 file and pass it using `--body-file`; pass the title as an argument. Do not interpolate the body into shell code.

Create the issue using the verified repository. Apply labels, assignees, milestones, or projects only when requested or required by repository conventions; verify their actual values first.

On success, record the returned issue number and URL in the local file. If no project convention exists, place the completed file at `tickets/<number>-<slug>/ISSUE.md`. Include repository, issue number, URL, and status above the ticket body. Preserve an existing destination instead of overwriting it. Keep the substantive body consistent with the published issue; put later local-only work notes in a separate section.

If authentication, network access, or permissions prevent publication, retain the local draft with `GitHub: pending` and report the exact blocker. If creation times out or returns an ambiguous error, search for the attempted issue before retrying to avoid duplicates. If GitHub creation succeeds but local finalization fails, report the URL and retained draft path; repair the local counterpart without creating another issue.

Ticket creation does not include implementation, branch creation, commits, pushes, or merges.

## 4. Verify and hand off

Read the saved local file and, when published, fetch the GitHub issue to verify repository, title, body, number, and URL. Confirm that both artifacts describe the same scope and acceptance criteria.

Return the GitHub issue link, local ticket path, and any unresolved questions or publication blocker. For draft-only work, clearly report that publication is pending.
