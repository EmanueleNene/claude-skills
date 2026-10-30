---
name: html-explain-it
description: "Turn the last discussion, problem, solution, or conclusion from the conversation into a standalone visual HTML file (SVG diagrams, tables, math, code, flowcharts). Output: explain_<topic>.html in the current working directory. Trigger: /html-explain-it, or a request for an HTML of what we discussed."
trigger: /html-explain-it
---

# /html-explain-it

Turn the latest topic in the conversation into one self-contained HTML page. The reader wants to see it, not read about it: **the visuals carry the explanation, and text only labels them.**

```
/html-explain-it                        # auto-detect last topic
/html-explain-it <topic>                # explicit topic
/html-explain-it <topic> --out <path>   # custom path
```

## 1. Extract the topic

Use the explicit `<topic>` if one was given. Otherwise take the most recent substantive problem, bug, concept, or brainstorm. Don't ask the user for clarification. Pull out:

- the **problem**: what is wrong or what was asked
- the **solution(s)** or conclusion, plus any open alternatives
- the real code, equations, data, and file:line references involved

Problem and solution are the core of the page. Everything else supports them.

## 2. Writing rules: be terse

This is the main quality bar. Pages that are too wordy are the most common failure.

- **Say each fact once.** Don't restate a point in a summary, a caption, and a takeaways box. If the diagram shows it, don't also write it out as prose.
- **No filler.** Cut intros ("In this section we will..."), transitions, restated headings, and generic advice. Leave out anything that doesn't add information.
- **Short text only.** Captions get one line. Any paragraph is at most 2 sentences. Prefer labels, table cells, and bullets of a few words.
- **Small sections are fine.** Don't pad a section to make it look complete. Drop any section that has nothing specific to say.
- **Be specific.** Use real names, numbers, and file:line references, never generic descriptions.

## 3. Structure

1. Title, plus one sentence on what this is about
2. **Problem**: a visual (diagram, before/after, table) with minimal text
3. **Solution(s)**: a visual. Use side-by-side or a table if there are several
4. Supporting detail only if needed: code, math, data flow
5. Optional: a "Next / open questions" list, only if there really is something open

There is no closing "key takeaways" or recap section. It would only repeat the page.

Pick visuals that fit the content, and use at least two kinds:

| Visual | Use for |
|---|---|
| SVG flowchart / diagram | data flow, pipelines, state, geometry, call chains |
| Table | comparing options, cases, parameters, before/after |
| Side-by-side panels | wrong vs right, approach A vs B |
| Annotated code block | the actual lines that matter |
| MathJax | equations (`\( \)` inline, `\[ \]` block) |

## 4. HTML conventions

- One file. No external assets except the MathJax CDN (`https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js`), and include that only if the page has math.
- Body `#f8f9fa`, text `#1a1a2e`, font `"Segoe UI", Arial, sans-serif`, max-width 900px centered.
- Use one accent color per topic: red `#e63946` for bugs, blue `#2196f3` for flow, green `#4caf50` for fixes.
- Cards: white, `border-radius:8px`, light shadow, `padding:24px`.
- Code: dark `#1e1e1e`, monospace, highlighted with span classes.
- SVG: inline, `viewBox="0 0 800 N"`, rounded boxes, `<marker>` arrowheads, every element labelled, a `<title>`. Color nodes by role: input blue, compute orange, output green, error red. Add a legend only if there are more than 3 roles.
- Tables: collapsed borders, an accent header, the buggy row light red and the fix row light green.
- Mobile: `max-width:100%` on SVG, `overflow-x:auto` on wide tables.

## 5. Write and report

Save with `Write` to `explain_<kebab-slug>.html`. Don't open a browser. Reply with just:

```
HTML saved: explain_<slug>.html: <one-line summary>
```

## Checklist

- [ ] Problem and solution are both shown visually
- [ ] No fact appears twice, there is no recap section, and no paragraph is over 2 sentences
- [ ] SVGs are labelled and not blank
- [ ] Code and file:line references are real, taken from the conversation
