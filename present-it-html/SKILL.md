---
name: present-it-html
description: Present code, data, or a concept as a standalone offline HTML page built around graphs, plots, and diagrams. Use when the user wants something explained visually or as an HTML page, or when a delivery run needs its results briefing.
---

# Present It HTML

Make the reader *see* it: every section leads with a picture, and prose explains the picture.

## Branches

- **Explanation** (default): one question about code, data, or a concept — a mechanism, a cause, a result.
- **Briefing**: completed work packaged for a decision, e.g. from `$delivery-pipeline`.

## Rules for both branches

- **Picture first.** Each section opens with an inline SVG diagram, a plot, or a table. One figure, one idea: build a hard idea as a sequence of simple figures, from zero.
- **Plots from real data.** Read the numbers from the source files. Label axes with units. Embed as inline SVG or a PNG data URI (matplotlib is fine).
- **Evidence.** Every number and claim cites its source (`path:line`, command, or artifact) next to the claim and in a source index. Label inference as inference. Quantitative claims state baseline, units, and threshold where they exist.
- **Plain language.** Define each term at first use. Short sentences.
- **Offline single file.** Inline CSS, viewport meta, `@media print`, visible focus styles; no remote script, stylesheet, image, or font. Normal hyperlinks as citations are fine.
- **House style.** If the project already has an HTML page of this kind (same folder first), reuse its CSS.
- **Engineering drawings use third-angle projection (ASME Y14.3).** Top view above the front view, right view or section to the right, all aligned. Label each view (`TOP VIEW`, `FRONT VIEW`, `SECTION A-A`). Cutting-plane lines carry arrows in the viewing direction. Hidden edges dashed, cut faces hatched, axis triad in each view.
- Every SVG has a `<title>`; every image has `alt` text.

## Steps

### 1. Answer

Write the one-sentence answer (explanation) or outcome (briefing).

Done when the title, the lead, and the conclusion state the same evidence-backed answer.

### 2. Outline

**Explanation:**
1. header — the question, then the answer;
2. figures that build the idea, one concept each;
3. evidence table with the key numbers;
4. limits, open points, and what was left out;
5. sources.

**Briefing** — section IDs in this order:

```text
executive-summary problem investigation plan implementation validation
review cleanup takeaways sources
```

Keep Standards and Spec review as separate axes. Label a missing stage `Not run`, `Unavailable`, or `Pending`.

Done when every section has a figure or table and every claim has a source.

### 3. Write the file

Path, first match wins:
1. the caller's path;
2. a delivery run: `<run>/presentation.html`;
3. work that belongs to a ticket: the ticket folder, `present_<topic-slug>.html`;
4. otherwise the working directory, `present_<topic-slug>.html`.

### 4. Embed local images

If the page references local images, run (`<skill-dir>` = this skill's directory):

```text
python <skill-dir>/scripts/embed_local_assets.py <page.html> --asset-root <workspace> --in-place
```

Done when no `<img>` points to a local file.

### 5. Validate

```text
python <skill-dir>/scripts/validate_presentation.py <page.html>            # briefing
python <skill-dir>/scripts/validate_presentation.py <page.html> --explain  # explanation
```

Done when the validator passes.

Return the path, the one-sentence answer, and the validator result.
