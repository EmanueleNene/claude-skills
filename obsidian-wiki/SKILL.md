---
name: obsidian-wiki
description: "Update and maintain the project Obsidian wiki. Use on /obsidian-wiki or explicit requests to update wiki pages, ingest sources, audit wiki health, or scaffold a project wiki. Owns all wiki writes, citations, index maintenance, and append-only logging. Wiki-backed answers and task context belong to obsidian."
trigger: /obsidian-wiki
---

# /obsidian-wiki — Maintain the wiki

Own all project wiki writes. Preserve the existing structure:

```text
<project-vault>/
  raw/             immutable source material
  wiki/
    index.md       table of contents
    log.md         append-only operation history
    *.md           knowledge pages
```

## Usage

```text
/obsidian-wiki update <topic>       # targeted update from verified findings
/obsidian-wiki update              # refresh stale pages and ingest new sources
/obsidian-wiki ingest <file>       # incorporate a specified source
/obsidian-wiki lint                # read-only health audit
/obsidian-wiki scaffold <path>     # explicitly create a project wiki
/obsidian-wiki                     # ask what to update; no implicit writes
```

## 1. Locate and scope

Prefer the supplied path or the project/vault path in applicable instructions. Otherwise search the current project for `wiki/index.md`. Ask if candidates are ambiguous or absent. Create a new wiki only for an explicit scaffold request, at the specified or confirmed path.

Read `index.md`, relevant `log.md` entries, and pages and sources within the requested scope. Targeted updates need not audit the entire wiki. For an unqualified full update or lint, inspect all wiki Markdown pages and inventory `raw/`.

**Completion:** the target wiki, operation, and affected scope are identified.

## 2. Verify evidence

- Read sources supporting each proposed change. Verify code symbols and line references against current source before calling a claim stale.
- Cite factual claims with `(source: path/to/source)`; include symbols, sections, or line ranges where useful. Use the actual source type, not a hard-coded `.F` suffix.
- Mark unsupported claims `[needs verification]`. Present conflicting evidence explicitly; ask when it cannot be resolved from authoritative sources.
- Keep raw snapshots distinct from live code: record which version supports a claim.
- Follow applicable project ingestion/approval rules. An explicit targeted update authorizes changes within that scope, not unrelated restructuring.

**Completion:** each proposed factual change has evidence or an explicit uncertainty marker.

## 3. Audit when requested

For `lint`, report numbered findings grouped as BLOCKER, WARN, or NOTE, then stop without writes. Check:

- Broken wikilinks, including aliases, headings, and relative paths using the vault's existing resolution convention.
- Index coverage, dangling index entries, and orphan pages.
- Missing page metadata and related-page links.
- Stale claims, contradictions, and unsupported factual claims.
- Ambiguous relative dates; convert only when the actual date is known.
- Source concepts that merit documentation, without automatically creating a page for every symbol.
- Raw-source integrity where a baseline exists. A timestamp alone does not prove modification; report inability to verify when no baseline exists.

For updates, apply the relevant checks to affected pages and their links rather than automatically running a full audit.

**Completion:** findings distinguish verified defects from uncertainties; read-only lint ends here.

## 4. Write scoped changes

- Never modify, move, or delete existing `raw/` material. If a requested source is outside the vault, cite it in place unless the user authorizes adding a raw snapshot.
- Preserve existing page names and organization. Avoid bulk renames and unrelated formatting changes.
- Content pages use YAML `tags`, `**Summary**`, `**Sources**`, `**Last updated**` (absolute date), a `---` separator, and `## Related pages`. Index and log retain their own formats.
- For ingest, read the full source and update or create only useful source-summary and concept pages, linked to related knowledge.
- Correct stale knowledge visibly: append a dated `**Correction:**` note and make the current interpretation clear while retaining meaningful history.
- Resolve links only when the intended target is verified. Preserve superseded pages as clearly marked stubs with forward pointers. Confirm destructive changes before proceeding.
- Scaffold creates `wiki/index.md` and `wiki/log.md`; create an empty `raw/` directory only if absent. Preserve existing files and confirm before overwriting anything.

**Completion:** changes stay within scope, sources are preserved, and factual additions are cited.

## 5. Index, log, and validate

After every wiki change:

1. Update `index.md` so changed/new pages are represented with accurate descriptions; refresh its update date.
2. Append a dated entry to `log.md` listing every created/edited page, supporting sources, and unresolved questions. Never rewrite prior log entries.
3. Verify links in changed pages and index entries resolve, metadata is complete, citations identify accessible sources or explicit gaps, and this operation did not alter existing `raw/` files.
4. Summarize what changed, what was verified, and what still needs a decision. Do not claim checks that were not performed.

**Completion:** all changed pages are indexed and logged, and validation results are reported.

## Companion skill

Use `/obsidian <question or task>` to consult the wiki as a knowledge base. Read that skill when routing a consultation request; use the available tools rather than assuming a particular Skill tool exists. This skill remains the sole owner of wiki-write rules.
