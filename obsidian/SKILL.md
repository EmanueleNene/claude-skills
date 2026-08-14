---
name: obsidian
description: "Task execution augmented with Obsidian wiki context. Use when user prefixes or suffixes any request with /obsidian — means: check the wiki first, answer/act using wiki knowledge, then offer to update the wiki if new information was produced."
trigger: /obsidian
---

# /obsidian

Execute a task **anchored to the project's Obsidian wiki**. The user places `/obsidian`
before or after their request to signal: "consult the wiki, then do the thing."

## Usage

```
/obsidian <task>                  # check wiki → do task → offer wiki update
<task> /obsidian                  # same — order doesn't matter
/obsidian                         # no task → open wiki index, summarise state
```

Examples:
```
/obsidian what does H_key(1) do?
explain the smearing pipeline /obsidian
/obsidian why does the even mesh diverge?
/obsidian update the smearing page with today's finding
```

## Step 1 — Locate the wiki

```powershell
$hits = Get-ChildItem -Path . -Recurse -Filter index.md -ErrorAction SilentlyContinue |
        Where-Object { $_.DirectoryName -match '[\\/]wiki$' }
```

- 1 hit → use it. Print `WIKI: <path>`.
- 0 hits → stop: "No Obsidian wiki found. Run `/obsidian-wiki` to scaffold one."
- >1 hits → list candidates; ask user which.

## Step 2 — Read the wiki index

Read `wiki/index.md` in full. Identify which pages are relevant to the user's task by
matching keywords and concepts in the task text against page titles and one-line
descriptions in the Quick Reference table.

## Step 3 — Read relevant pages

Read every page identified in Step 2. For broad tasks ("explain the pipeline", "why
does X happen") read all pages. For narrow tasks ("what is H_key(1)?") read only
the 1–3 most relevant pages. Always read `log.md` for recent changes that may
affect the answer.

## Step 4 — Execute the task

Answer the question or perform the action using wiki knowledge as primary source.
Cite which wiki pages each claim comes from (e.g. `([[smearing-kernel]])`).

If the wiki is incomplete or contradicts the current code:
- Flag the gap explicitly ("Wiki says X but current source says Y").
- Use the live code (Grep/Read) to fill the gap.
- Note what needs a wiki update (Step 5).

## Step 5 — Offer wiki update

After answering, if the task produced new findings not yet in the wiki, offer:

> "This finding isn't in the wiki yet. Want me to update `[[relevant-page]]`?"

If the user says yes (or invoked as `/obsidian update`), apply a **targeted update**
using the write protocol owned by `/obsidian-wiki` (do not duplicate it — defer to
those rules as the single source of truth):
- Page format: YAML `tags`, `**Summary**`, `**Sources**`, `**Last updated**`, `---`, `## Related pages`.
- Citations: `(source: filename.F)` on every factual claim.
- History: append `**Correction:**` note, never overwrite prior content.
- Always update `index.md` and append `log.md` after any write.

For a **full structural audit** (broken links, orphans, format sweep, raw/ integrity),
**delegate to `/obsidian-wiki`** — do not replicate that logic here.

## Skill connections

| Need | Use |
|------|-----|
| Q&A / task with wiki context | `/obsidian <task>` ← **this skill** |
| Full lint + audit of wiki health | `/obsidian-wiki` |
| Ingest a new `raw/` source | `/obsidian-wiki ingest <file>` |
| Scaffold a new vault from scratch | `/obsidian-wiki` (it owns creation) |
| Targeted single-page update after a finding | `/obsidian update …` ← **this skill** |

**Calling `/obsidian-wiki` from here:** when the user asks for a lint, audit, or ingest
inside an `/obsidian` session, invoke the Skill tool with `skill: "obsidian-wiki"` and
pass the relevant args. Do not re-implement those steps.

**Being called by `/obsidian-wiki`:** after a lint or ingest, `/obsidian-wiki` may
suggest `/obsidian <question>` to verify new content. If that happens, this skill picks
up normally from Step 1.

## Rules

- **NEVER modify `raw/`**. Read only.
- **Always cite wiki pages** in the answer.
- **Trust code over wiki** when they conflict — the code is ground truth.
- **Don't update the wiki silently** — always confirm with the user first unless
  the user explicitly said "update" in the invocation.
- **Don't run a full lint** — delegate to `/obsidian-wiki`. This skill reads + answers +
  applies targeted updates only.
- **Write protocol is owned by `/obsidian-wiki`** — when writing, follow its rules exactly,
  not a local copy.
