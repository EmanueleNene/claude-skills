---
name: status
user-invocable: true
disable-model-invocation: false
description: "Give a brief snapshot of the immediate work: what we are doing now, what is running, blockers, and the next action. Use for /status or questions such as 'what is running?' and 'where are we right now?'. For a full-chat or branch-level recap of progress and reasoning, use report-it instead. Not for standalone Git status queries or system-health investigations."
---

# Status

Pause new task actions and report the immediate situation in chat. Focus on the current step and latest relevant result, rather than retelling the task history.

1. Read the recent conversation and available execution evidence. If a known job or subagent may still be active, use an available read-only status check scoped to that work. Do not launch agents, scan unrelated processes, wait for completion, or stop/restart jobs to prepare the update. If live state cannot be checked, label it as last known or unverified.
2. When the current task is linked to GitHub issues, check the relevant tickets using available read-only GitHub tools or CLI access. Limit the check to the immediate step's state, blockers, and latest relevant updates; cite issue numbers or links. If access is unavailable, say the ticket state is unverified. Do not modify tickets.
3. Answer in plain language using at most four short bullets, normally under 100 words:
   - **Now:** The current step and, if useful, its latest result.
   - **Running:** Confirmed active jobs or agents and what each is doing. Distinguish running, queued, completed, and failed work. Say 'No known active jobs' when appropriate; a plan is not a running job.
   - **Blocked:** What prevents the immediate step from moving forward, including any input needed from the user. Omit if none.
   - **Next:** The next concrete action or event we are waiting for.
4. Finish after the snapshot; do not automatically resume task actions or create a report file. If no active task is established, say so rather than inventing activity.
