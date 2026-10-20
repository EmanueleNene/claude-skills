---
name: rewrite-it
description: "Rewrite and polish text, technical documentation, commit messages, or explanations for clarity, elegance, conciseness, and flow while strictly preserving original meaning, facts, and structure. Use when the user asks to rewrite, rephrase, polish, proofread, clean up text, or invokes /rewrite-it."
---

# Rewrite It

Rewrite and polish rough drafts, notes, technical descriptions, or explanations for maximum clarity, conciseness, and natural flow, while strictly preserving technical precision and the author's original intent.

## Core Rules

1. **Preserve Technical Integrity**: Never alter code identifiers, variable names, file paths, numbers, units, mathematical symbols, or core technical assertions.
2. **Eliminate Fluff & Clutter**: Cut throat-clearing phrases (*"it is important to note that"*, *"in order to"*, *"as a matter of fact"*, *"basically"*).
3. **Use Active Voice & Strong Verbs**: Prefer direct actions (*"the subroutine computes"* rather than *"is utilized for the computation of"*).
4. **Vary Sentence Cadence**: Mix short, punchy statements with well-balanced explanatory clauses to create engaging, natural rhythm.
5. **Preserve Original Structure**: Maintain the author's logical outline and ordering; elevate the expression rather than inventing a completely different document.

---

## The 4 Registers (Tone Modes)

Identify the appropriate register (or default to **Technical & Engineering**):

| Register | Best For | Voice & Style Characteristics |
| :--- | :--- | :--- |
| **Technical & Engineering** *(Default)* | PR descriptions, docstrings, technical reports, commit messages | Direct, objective, concise, active voice, zero filler |
| **Academic & Scientific** | Papers, theses, theory sections, formal documentation | Rigorous, scholarly, precise terminology, measured claims |
| **Executive & Summary** | Briefings, high-level overviews, client notes | High-signal, punchy, bullet-driven, decision-focused |
| **Clear & Conversational** | Emails, Slack/Teams updates, team handover notes | Professional, warm, fluent, approachable |

---

## Process

### Step 1: Diagnose the Draft
Read the original draft and identify:
- The core message and intended audience.
- Weaknesses: awkward syntax, repetitive words, run-on sentences, passive voice, or ambiguity.
- Protected elements (variable names, numbers, deck files, Fortran symbols).

### Step 2: Polish the Prose
Apply sentence restructuring:
- Break up run-on sentences into distinct logical thoughts.
- Replace weak nominalizations (*"performed an examination of"*) with active verbs (*"examined"*).
- Ensure consistent tense throughout each paragraph.

### Step 3: Present the Result
Always present:
1. **The Polished Version**: The clean, publication-ready text.
2. **What Changed & Why**: A brief 2–3 bullet summary highlighting the key improvements (e.g. tightened run-ons, replaced passive constructions, removed redundant filler).
3. *(Optional)* If the edit is extensive, provide a quick Before vs. After diff or comparison table.

---

## Completion Criteria

The rewrite is complete when:
- [ ] Every technical fact, variable name, and number from the original is preserved bit-identically.
- [ ] All grammatical errors and awkward sentence structures are eliminated.
- [ ] Unnecessary filler words are pruned.
- [ ] The text reads naturally and authoritatively in the chosen register.
