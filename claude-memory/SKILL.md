---
name: claude-memory
description: "Lint and update Claude's file-based project memory (MEMORY.md index + per-fact .md files). Checks index consistency, frontmatter validity, broken [[links]], duplicates, contradictions, stale code references, and relative dates. Use when the user asks to lint / audit / clean / update / fix Claude's memory."
trigger: /claude-memory
---

# /claude-memory

Lint and repair the file-based memory for the **current project**. Memory lives at
`~/.claude/projects/<encoded-cwd>/memory/`: a `MEMORY.md` index (one pointer line per
memory) plus one `.md` file per fact, each with frontmatter (`name`, `description`,
`metadata.type` ∈ `user|feedback|project|reference`).

## Usage

```
/claude-memory            # lint, report, then apply SAFE fixes (index, frontmatter, dates)
/claude-memory lint       # report only — no writes
/claude-memory update     # apply all fixes including merges (asks before deletes)
```

Default (no arg) = lint + safe fixes. `lint` = read-only. `update` = full.

## Honesty rules (do not violate)

- **Never delete a memory** without first verifying it is wrong, superseded, or a true
  duplicate. When in doubt, flag — do not remove.
- **Verify every code reference against current code** (Grep/Read) before calling it
  stale. A memory naming a `file:line` or symbol that still exists is NOT stale.
- **Preserve `user` and `feedback` memories.** Only touch them to fix format or merge an
  exact duplicate.
- Keep `MEMORY.md` to one line per memory. Never put memory *content* in the index.

## Step 1 — Locate the memory dir

```powershell
$enc = ((Resolve-Path .).Path) -replace '[^A-Za-z0-9]','-'
$mem = Join-Path $env:USERPROFILE ".claude\projects\$enc\memory"
if (-not (Test-Path $mem)) {
    # fallback: single project memory dir
    $cand = Get-ChildItem (Join-Path $env:USERPROFILE ".claude\projects") -Directory -ErrorAction SilentlyContinue |
            ForEach-Object { Join-Path $_.FullName "memory" } | Where-Object { Test-Path $_ }
    if ($cand.Count -eq 1) { $mem = $cand[0] }
}
Write-Host "MEMDIR: $mem"
Write-Host "EXISTS: $(Test-Path $mem)"
```

If it does not exist, stop: "No Claude memory found for this project." Do not create one.

## Step 2 — Gather

Read `MEMORY.md` and every `*.md` in the dir. For each memory file record: filename,
`name`, `description`, `metadata.type`, body, all `[[links]]`, and any `file:line` /
symbol / date references in the body.

## Step 3 — Lint checks

Run every check. Number findings; group by severity (BLOCKER → WARN → NOTE).

1. **Index consistency** — every memory file (except `MEMORY.md`) has exactly one pointer
   line in `MEMORY.md`; every pointer in `MEMORY.md` resolves to an existing file. Flag
   missing pointers and dangling pointers.
2. **Frontmatter validity** — `name` is kebab-case and matches the filename slug;
   `description` present and one line; `metadata.type` is one of
   `user|feedback|project|reference`. Flag missing/invalid fields and slug≠filename.
3. **Broken `[[links]]`** — every `[[slug]]` resolves to an existing memory `name`. Flag
   unresolved links (note: a link to a not-yet-written memory is acceptable, but list it).
4. **Duplicates** — two files whose fact/description substantially overlap. Flag the pair
   and recommend which to keep (richer/newer) and which to merge+delete.
5. **Stale code references** — for each `file:line` or named symbol in a body, verify with
   Grep/Read against current code. Flag only if the file is gone or the symbol no longer
   exists. Quote what you found.
6. **Relative dates** — find `today|yesterday|last week|N days ago|recently` etc. Flag for
   conversion to absolute (use the current date from context).
7. **Contradictions** — two memories asserting opposite facts about the same thing. Flag
   both; do not pick a winner automatically — surface to the user.
8. **Orphans** — a memory neither pointed to by `MEMORY.md` nor referenced by any
   `[[link]]`. Flag (usually means the index pointer was dropped).

## Step 4 — Report

Print the numbered findings. For a read-only `lint` run, stop here.

## Step 5 — Apply fixes

Apply **safe fixes** automatically (default + `update`):
- Repair `MEMORY.md`: add missing pointer lines, remove dangling ones, normalize to
  `- [Title](file.md) — hook` form, keep alphabetical/topical grouping already present.
- Fix frontmatter: correct kebab-case `name` to match filename, add a missing
  `metadata.type` (infer from content), tidy a multi-line `description`.
- Convert flagged relative dates to absolute in-place.

Apply **judgement fixes** only on `update` (and confirm deletes first):
- Merge a clear duplicate pair: fold the weaker file's unique content into the stronger,
  repoint inbound `[[links]]`, update the index, then delete the weaker file.
- For a stale reference confirmed gone from code: update the citation to the current
  location if found, else append a dated `**Correction:**` note. Delete only if the whole
  memory is now false AND the user approves.
- For contradictions: present both and ask which is current; apply the user's choice.

## Step 6 — Summarize

List what changed (files edited, pointers fixed, dates converted, merges/deletes) and what
was left for the user to decide (contradictions, risky deletes).
