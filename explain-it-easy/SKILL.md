---
name: explain-it-easy
description: "Explain complex technical topics, bugs, simulations, code, or mathematics in plain, jargon-free language followed by intuitive analogies, ASCII diagrams, comparison tables, and bullet points. Use when the user asks to 'explain simply', 'explain it easy', 'ELI5', 'in plain English', or invokes /explain-it-easy."
---

# Explain It Easy

Transform complex technical problems, algorithms, physical models, or code flows into plain, crystal-clear explanations that build instant intuition without sacrificing truth.

## The 5-Step Explanation Architecture

Always structure the explanation using these five sequential sections:

### 1. The Core Intuition (The One-Liner)
Start with a single sentence that captures the essence of the problem or concept.
- **Zero jargon**: No unexplained acronyms, internal flags, or Greek letters.
- **Answer the "what" and "why"**: What is happening, and why does it matter?
- *Example*: "Instead of twisting the entire beam, our contact force was only twisting a tiny slice in the middle, creating a localized kink."

### 2. The Everyday Analogy (The Mental Model)
Ground the abstract concept in an intuitive, physical, real-world metaphor (e.g., sponges, ropes, trains, springs, rubber bands, layered sandwiches).
- State the analogy clearly: *"Think of this like..."*
- Map the analogy directly to the technical components:
  - Analogy component $A \rightarrow$ Technical component $X$
  - Analogy component $B \rightarrow$ Technical component $Y$
- Explain what goes wrong or how it works using the analogy.

### 3. The Step-by-Step Mechanics (What Is Actually Happening)
Break down the actual technical sequence into simple, numbered chronological cause-and-effect steps:
1. **Trigger / Action**: What starts the sequence?
2. **Internal Reaction**: How does the system / code respond?
3. **The Consequence**: What is the observable outcome or discrepancy?

Keep sentences short and active. If a technical term is unavoidable, define it immediately in parentheses using plain words.

### 4. Visual Representation (Diagram or Table)
Always include an ASCII/Unicode diagram or a comparison table to give the concept visual shape.

*Example ASCII flow / drawing:*
```text
      WHAT WAS HAPPENING                       WHAT SHOULD HAPPEN
   (Over-localized shear kink)               (Smooth distributed twist)

        Master Fibre                             Master Fibre
      ────────┬────────                        ────────┬────────
              │   ◄── Point force                      │   ◄── Distributed
              ▼       at single node                   ▼       over bond length
          ────┼────                                ───╱ ╲───
           Local Kink                           Smooth Gradual Curve
```

*Or Before vs. After comparison table:*
| Aspect | What Happened Before | What Happens Now | Why It Matters |
| :--- | :--- | :--- | :--- |
| **Input** | Raw uncalibrated angle | Cosine-corrected projection | Eliminates acute-angle drift |
| **Output** | 15% discrepancy at tips | Within 1.2% of 3D solid truth | Passes validation gate |

### 5. Key Takeaways (The Wrap-Up)
Conclude with 3 to 5 concise bullet points:
- What the root problem/concept was
- What the fix or rule is
- What to expect next

---

## Completion Criteria

The explanation is complete when:
- [ ] A non-specialist engineer could grasp the core idea from the first two sections alone.
- [ ] No technical jargon remains without an immediate plain-language translation.
- [ ] At least one visual artifact (ASCII diagram, flowchart, or comparison table) is present.
- [ ] The explanation ends with actionable takeaway bullet points.
