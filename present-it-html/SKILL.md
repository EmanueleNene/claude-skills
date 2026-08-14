---
name: present-it-html
description: Turn completed technical work and its investigation, plan, implementation, validation, review, cleanup, and plain-language explanation into a polished standalone HTML briefing. Use when the user wants to present project results visually, create a decision-ready engineering report, or package delivery evidence into one offline HTML file.
---

# Present It HTML

Create a decision briefing from existing evidence. Preserve uncertainty rather than rediagnosing the work or filling gaps with plausible claims.

## Inputs

Collect:

- objective, audience, and requested output path;
- investigation or problem analysis;
- implementation plan;
- changed-component summary or diff;
- validation commands, results, artifacts, and limitations;
- separate Standards and Spec review results when available;
- cleanup manifest and apply status;
- plain-language explanation.

Label missing artifacts `Not run`, `Unavailable`, or `Pending`.

## Process

### 1. Establish the message

Write the one-sentence outcome, the audience's decision or takeaway, the strongest supporting evidence, and the material limitation.

Complete this step when title, executive summary, status, and conclusion express the same evidence-backed state.

### 2. Build the storyboard

Use this order:

1. hero with outcome and status badges;
2. executive summary in plain language;
3. problem and impact;
4. investigation evidence and causal chain;
5. plan and change map;
6. implementation summary with real components;
7. validation results and acceptance criteria;
8. Standards and Spec review as separate axes;
9. cleanup status and preserved evidence;
10. takeaways, risks, and next actions;
11. source index with files, commands, artifacts, and URLs.

Complete this step when every material claim has a source and every delivery stage is represented honestly.

### 3. Design visual evidence

Use at least two visual types selected for the content:

- inline SVG for a pipeline, causal chain, architecture, state, or before/after flow;
- table for acceptance criteria, change maps, comparisons, or review findings;
- metric cards for exact measured results;
- timeline for the delivery sequence;
- embedded plot for trends;
- annotated code block for a decisive implementation seam.

Put `<title>` in every SVG and `alt` text on every image. Prefer direct labels and semantic HTML over decoration.

### 4. Write one standalone file

Write to the caller's path. Otherwise write `presentation.html` in the caller's delivery-run directory.

Required section IDs:

```text
executive-summary problem investigation plan implementation validation
review cleanup takeaways sources
```

Requirements:

- inline CSS, responsive layout, visible focus styles, and `@media print` rules;
- no remote script, stylesheet, image, font, or CDN dependency;
- embedded plots as data URIs or inline SVG;
- concise plain-language summary with progressively disclosed technical detail;
- exact statuses such as passed, failed, limited, pending, waived, or not run;
- source references next to consequential claims and a complete source index.

Normal external hyperlinks are allowed as citations; visual and executable assets remain offline.

### 5. Embed local images

Resolve `<skill-dir>` to this skill's installed directory. If the draft references local images, run:

```text
python <skill-dir>/scripts/embed_local_assets.py \
  <presentation.html> --asset-root <workspace> --in-place
```

Complete this step when every local image is embedded in the HTML file.

### 6. Validate

Run:

```text
python <skill-dir>/scripts/validate_presentation.py <presentation.html>
```

Visually inspect desktop, mobile, and print layouts when a safe browser-capable tool is available. Correct overflow, empty diagrams, unreadable labels, and evidence mismatches.

Complete this step when the validator passes and every displayed number, status, component, and citation agrees with its source.

## Completion check

- The file opens offline with no external asset dependency.
- At least two visual types materially improve understanding.
- All required sections exist, including separate review axes.
- Missing and blocked stages are visibly labelled.
- Quantitative claims include baseline, units, threshold, and evidence path where applicable.
- Cleanup claims match the manifest.
- The source index makes every major claim auditable.

Return the HTML path, one-sentence outcome, evidence used, validator result, and pending or unavailable stages.
