---
name: report-it
user-invocable: true
disable-model-invocation: false
description: "Summarize the bigger picture across the current chat or branch: problem, overall progress, approach, reasoning, blockers, and remaining work. Use for /report-it or requests for a full recap or overall progress report. For the immediate step or what is running right now, use status instead. Not for new investigations, simulation-results analysis, or standalone report documents."
---

# /report-it

Pause new task actions and summarize the broader work in chat using the conversation and evidence already gathered. Cover the full chat or branch, as requested, rather than just the latest step. State the scope and any gaps in available history; do not imply that unseen branch work was reviewed. Leave running jobs alone unless the user asks to stop them. This is a big-picture recap, not a new investigation or a file-generation workflow.

When the work is tracked in GitHub issues, check the tickets relevant to the chat or branch using available read-only GitHub tools or CLI access. Summarize their current state, key decisions, blockers, and remaining scope, citing issue numbers or links. Keep the check scoped to this work rather than auditing the repository backlog. Distinguish ticket claims from verified implementation or test evidence. If access is unavailable, say the ticket state is unverified. Do not modify tickets.

Use short bullets in plain language:
- **Problem:** What we are trying to resolve.
- **Progress:** What is completed, what is in progress, and what checks actually ran.
- **Approach:** The proposed or pursued solution; distinguish a proposal from an implemented change.
- **Why:** The evidence or reasoning behind that approach.
- **Blockers:** Any unresolved issue or missing evidence; omit if none.
- **Next:** The remaining milestones or decisions needed to complete the work.

Mark unknowns explicitly. If no active task is established, say so and ask which task to report on. Finish when every applicable bullet is covered; do not automatically resume work or create a report file.
