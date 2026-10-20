---
name: obsidian
description: "Use the project Obsidian wiki as the starting context for an answer or task. Trigger on /obsidian or an explicit request to consult or use the wiki as a knowledge base. Read relevant pages, cite them, and verify against current sources when needed. Wiki edits belong to obsidian-wiki."
trigger: /obsidian
---

# /obsidian — Use the wiki

Use wiki knowledge as the starting context for the requested task. This skill reads the wiki; it does not maintain it.

## Usage

```text
/obsidian <question or task>
<question or task> /obsidian
/obsidian                         # summarize the index and recent activity
```

## Workflow

1. **Locate the project wiki.** Prefer a user-supplied path or a project/vault path documented in applicable instructions. Otherwise search the current project for `wiki/index.md`. If several candidates exist, ask which to use. If none exists, ask for its location; suggest `/obsidian-wiki scaffold <path>` only if the user wants a new wiki.
2. **Read the index and relevant context.** Read `index.md`, then the pages relevant to the task and recent relevant entries in `log.md`. Follow related links only as needed. For a broad question, expand coverage by topic rather than reading the entire vault automatically. If no task was supplied, summarize the index and recent activity and stop.
3. **Answer or execute the task.** Cite the wiki pages supporting claims using `[[page-name]]` and include their file paths when useful. Distinguish sourced facts from inference. The invocation authorizes wiki consultation, not unrelated changes or simulations.
4. **Check gaps and conflicts.** Verify implementation-sensitive claims against current code or other authoritative sources. If those disagree with the wiki, state the discrepancy and cite both; do not treat wiki text as ground truth. Mark missing evidence explicitly.
5. **Finish with any update need.** If new findings make a page incomplete or stale, briefly identify the affected page and offer `/obsidian-wiki update <topic>`. Do not write to the wiki without an explicit update request.

## Ownership boundary

- Keep `raw/`, wiki pages, `index.md`, and `log.md` unchanged during consultation.
- Route explicit wiki update, ingest, lint, or scaffold requests to `obsidian-wiki`: read that skill and follow its workflow using available tools. No specific Skill tool is required.
- Ordinary tasks without a request to use the wiki do not automatically invoke this skill.
