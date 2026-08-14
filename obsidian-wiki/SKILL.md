---
name: obsidian-wiki
description: "Lint and update the Obsidian project wiki (Karpathy LLM-Wiki pattern: raw/ immutable sources + wiki/ Claude-maintained pages with index.md + log.md). Lint = audit broken [[links]], orphans, format compliance, stale claims, contradictions, missing citations, undocumented concepts. Update = ingest new raw/ sources into pages, refresh index, append log. Use when the user asks to lint / audit / clean / update / ingest into the Obsidian wiki."
trigger: /obsidian-wiki
---

# /obsidian-wiki

Maintain the Obsidian knowledge wiki for the **current project**. The wiki follows the
LLM-Wiki pattern defined in the user's global `~/.claude/CLAUDE.md`:

```
<Obsidian Vault>/<PROJECT>/
  raw/      -- immutable source files (.F, specs, papers) — NEVER modify
  wiki/     -- Claude-maintained knowledge pages
    index.md  -- table of contents (Quick Reference table of [[links]])
    log.md    -- append-only operation log (one entry per operation)
    *.md      -- one page per concept / function / source
```

Two halves: **lint** (audit page health and fix drift) and **update** (ingest new `raw/`
sources into pages, refresh `index.md`, append `log.md`).

## Usage

```
/obsidian-wiki                 # lint + report, then apply SAFE fixes (links, format, dates, index)
/obsidian-wiki lint            # report only — no writes
/obsidian-wiki update          # lint + safe fixes + ingest any un-ingested raw/ sources
/obsidian-wiki ingest <file>   # ingest one specific raw/ source into the wiki
/obsidian-wiki <path>          # operate on a specific vault/wiki path (default: auto-discover)
```

Default (no arg) = lint + safe fixes. `lint` = read-only. `update` = full incl. ingest.

## Honesty rules (do not violate)

- **NEVER modify, move, or delete anything under `raw/`.** Sources are immutable. Read only.
- **ALWAYS update `index.md` and append `log.md`** after any wiki change. No silent edits.
- **Verify every code/`file:line`/symbol citation against current source** (Grep/Read)
  before calling it stale. A citation that still resolves is NOT stale.
- **Never delete a page** without confirming it is wrong, superseded, or a true duplicate.
  When in doubt, flag — superseded pages stay as `❌ SUPERSEDED` stubs with inbound links.
- **Citations:** every factual claim ends with `(source: filename.F)`. Two sources
  disagree → note the contradiction explicitly. No source → mark `[needs verification]`.
- **Page naming:** prefer the wiki's existing convention (`NN_TOPIC.md` for numbered
  pages, `File.F.md` for source stubs, `lowercase-hyphen.md` for concepts). Do NOT
  bulk-rename to enforce a scheme — it breaks `[[links]]`. Flag inconsistency as NOTE only.
- **Style:** keep the style simple and clear. 

## Step 1 — Locate the wiki dir

```powershell
$arg = "<path-or-empty>"
if ($arg -and (Test-Path (Join-Path $arg "index.md"))) {
    $wiki = (Resolve-Path $arg).Path
} else {
    $hits = Get-ChildItem -Path . -Recurse -Filter index.md -ErrorAction SilentlyContinue |
            Where-Object { $_.DirectoryName -match '[\\/]wiki$' }
    if ($hits.Count -eq 1) { $wiki = $hits[0].DirectoryName }
    elseif ($hits.Count -gt 1) { $hits | ForEach-Object { Write-Host "CANDIDATE: $($_.DirectoryName)" } }
}
Write-Host "WIKI: $wiki"
$raw = if ($wiki) { Join-Path (Split-Path $wiki -Parent) "raw" }
Write-Host "RAW : $raw  (EXISTS: $(Test-Path $raw))"
```

If no `wiki/index.md` is found, stop: "No Obsidian wiki found for this project." Do not
create one unless the user explicitly asks to scaffold a new vault. If multiple candidates
print, ask the user which to operate on.

## Step 2 — Gather

Read `index.md`, `log.md`, and every `*.md` in `wiki/`. For each page record: filename,
title, the three header fields (`**Summary**`, `**Sources**`, `**Last updated**`), YAML
`tags` block, body, all outbound `[[links]]`, and any `file:line` / symbol / date / status
references. Build the set of page slugs (filename without `.md`) for link resolution.
List the contents of `raw/` so the ingest step can detect un-ingested sources.

## Step 3 — Lint checks

Run every check. Number findings; group by severity (BLOCKER → WARN → NOTE).

1. **Broken `[[links]]`** — every `[[slug]]` (and `[[slug#heading]]`) resolves to an
   existing page slug. Strip a trailing `.md` inside links (`[[BnDHygStrn.md]]` →
   `[[BnDHygStrn]]`). Flag links to `project_*` Claude-memory files (these live outside the
   vault and break in Obsidian — convert to plain text). Flag links to non-existent plans.
2. **Index consistency** — every wiki page (except `index.md`, `log.md`) appears in the
   `index.md` Quick Reference table; every `[[link]]` in the index resolves to a page. Flag
   missing rows and dangling rows.
3. **Orphan pages** — a page with no inbound `[[link]]` from any other page or the index.
   Flag; usual fix is a backlink from the most-related page's `## Related pages`.
4. **Page format** — each content page has: YAML `tags` block, `**Summary**:`,
   `**Sources**:`, `**Last updated**:`, a `---` separator, and a `## Related pages`
   section. Flag missing fields. (Note: `index.md` and `log.md` use their own formats.)
5. **Stale claims** — for each `file:line` / symbol / `H_key`-style citation in a body,
   verify with Grep/Read against current source. Flag only if the file is gone or the
   symbol/line no longer matches. Quote what you found. Also flag stale branch names,
   "Expected results" that are now observed, and status tags contradicted by newer log
   entries.
6. **Relative dates** — find `today|yesterday|last week|N days ago|recently`. Flag for
   conversion to absolute (use current date from context).
7. **Contradictions** — two pages asserting opposite facts about the same thing (e.g.
   conflicting `H_key(1)` semantics, conflicting fix status). Flag both; surface to the
   user — do not auto-pick a winner.
8. **Missing citations** — factual/technical claims lacking a `(source: …)` tag, where a
   source is known. Flag for citation, not deletion.
9. **Undocumented concepts** — a function/entity/term referenced across pages or present in
   `raw/` but having no page of its own. Flag as a candidate new page (NOTE).
10. **raw/ integrity** — confirm nothing under `raw/` was modified. If a diff or mtime
    suggests a `raw/` edit, flag as BLOCKER (these are immutable).

## Step 4 — Report

Print the numbered findings grouped by severity. For a read-only `lint` run, **stop here** —
propose fixes but write nothing.

## Step 5 — Apply fixes (default / `update`, never on `lint`)

Apply **safe fixes** automatically:
- Repair `[[links]]`: strip `.md`, fix known renames, convert `project_*` memory links to
  plain text with a "(Claude project memory, not an Obsidian page)" note.
- Repair `index.md`: add missing Quick Reference rows, remove dangling ones, keep the
  existing table grouping/ordering. Bump the index `Last updated` date.
- Repair page format: add missing YAML `tags`, `**Summary**/**Sources**/**Last updated**`
  fields, `---` separator, and a `## Related pages` section.
- Add backlinks to fix orphans (check 3): a `[[orphan]]` link in the most-related page's
  `## Related pages`.
- Convert flagged relative dates to absolute.

Apply **judgement fixes** only on `update` (and confirm anything destructive first):
- **Stale claim confirmed against source** — update the citation/line/status to match
  current code; if a whole section is now false, append a dated `**Correction:**` note
  rather than deleting history.
- **Contradictions** — present both pages and ask which is current; apply the user's choice.
- **Undocumented concept** — create the page only if the user wants it, or as part of an
  `ingest` (Step 6).
- **Supersession** — never delete; mark `❌ SUPERSEDED`, retain historical content, keep
  inbound links, and add a forward pointer to the replacement page.

## Step 6 — Ingest (only on `update` / `ingest <file>`)

For each new or un-ingested file in `raw/` (the `ingest` arg targets one specific file):

1. **Read the full source** from `raw/`. Do not modify it.
2. **Discuss key takeaways** with the user before writing (per global CLAUDE.md workflow),
   unless the user said to proceed.
3. **Create/update a summary page** in `wiki/` named after the source, following the page
   format (Step 4 fields + `## Related pages`).
4. **Create/update concept pages** for each major function/entity in the source.
5. **Add `[[wiki-links]]`** connecting the new page to related pages, with `(source: …)`
   citations on factual claims.
6. **Update `index.md`** — add the new page(s) to the Quick Reference table with a
   one-line description.

## Step 7 — Log + summarize

- **Append to `log.md`** a dated entry (`## YYYY-MM-DD — <what changed>`) listing every
  page created/edited, links fixed, dates converted, and ingests done. `log.md` is
  append-only — never edit or delete prior entries. Use UTF-8 (bodies contain ε, ×, →, ±).
- **Report to the user**: lint counts per check, what was fixed automatically, what was
  ingested, and what needs a decision (contradictions, risky updates, proposed new pages).
- **After ingest:** suggest `/obsidian <question about ingested content>` so the user can
  immediately query the new pages with full wiki context.

## Skill connections

| Need | Use |
|------|-----|
| Full lint + audit of wiki health | `/obsidian-wiki` ← **this skill** |
| Ingest a new `raw/` source | `/obsidian-wiki ingest <file>` ← **this skill** |
| Scaffold a new vault from scratch | `/obsidian-wiki` ← **this skill** (owns creation) |
| Q&A / task execution with wiki context | `/obsidian <task>` |
| Targeted single-page update after a finding | `/obsidian update …` |

**Write protocol:** `/obsidian-wiki` is the **single source of truth** for all wiki write
rules (page format, citation style, log format, raw/ immutability). `/obsidian` defers to
these rules when it writes — it does not maintain its own copy.

**Calling `/obsidian` from here:** after lint or ingest, if the user has a follow-up
question about the content, suggest invoking `/obsidian <question>`. Do not re-implement
Q&A logic here — delegate via the Skill tool (`skill: "obsidian"`).

**Being called by `/obsidian`:** when `/obsidian` needs a full lint or an ingest, it
invokes this skill. Accept that call and execute normally from Step 1.
