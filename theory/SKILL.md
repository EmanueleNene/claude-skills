---
name: theory
description: "Explain the theory behind whatever is in play: a concept from the discussion, the reasoning behind a plan, or the math/physics/algorithm a model or code implements. Use when the user invokes /theory, asks for theory, background, or the math behind something, asks why a method, plan, or model works, wants to go deeper on a concept, or is unsure about a concept being used."
---

# Theory

Explain the **first principles** behind the topic: why it works, not only what it does. Any field — math, physics,
mechanics, numerics, algorithms, statistics, software design.

## Pick the target

- **Named topic** — explain that.
- **No topic given** — take the concept the current discussion leans on that the user is least sure about. Name it in
  one line before explaining, so the user can redirect.
- **A plan we made** — the theory that justifies each choice in the plan, and the assumption it rests on.
- **A model or code** — the theory it implements, then where the code realizes it.

## Depth

Start **short**: the core idea, the key equation or rule, and why it holds — one screen. Go deeper only when asked
("deeper", "derive it", "full theory"). A deep pass adds, as relevant:

- derivation from first principles, step by step
- assumptions and where the theory breaks down (limits, edge cases)
- alternatives and why this one was chosen

## Visual first

Write so a human can scan it. Prose is the glue between visuals, at most a few lines in a row. Pick the visual that fits:

| Content | Visual |
|---|---|
| process, algorithm, causal chain, decision | Unicode box-and-arrow drawing (`┌─┐ │ └─┘ ──► ├─`) |
| geometry, coordinates, forces, data layout | Unicode drawing |
| comparisons, symbols, options, limits | table |
| lists of facts, assumptions, steps | bullets |
| trends, behaviour of a function | Unicode plot |

- Mermaid, real plots, or richer visuals asked for → hand off to `present-it-html` with the theory content.
- Define every symbol in an equation: symbol, meaning, units where physical.
- When code or a plan is in context, map each key equation or rule to where it lives (`file:line`, plan step).
  Cite only locations you have read.

## Study further

End every answer with sources to read and discuss on your own, 2–5 entries:

| Source | What it covers | Where |
|---|---|---|
| Author, *Title* (edition, year) | the part that matters here | chapter / section |
| Paper: Author, "Title", Venue, year | ... | DOI or link |
| Online course or doc | ... | link |

- Prefer standard textbooks and the original paper of the method.
- Give a link only when it is stable and known (DOI, official docs, Wikipedia, arXiv ID); otherwise give the exact
  title and search terms. Mark any entry you are unsure of as "verify".
