---
name: graphify-memory
description: "Lint and update the graphify knowledge-graph memory in graphify-out/ (graph.json + GRAPH_REPORT.md). Update = incremental re-extract of changed/new files and prune of deleted-file ghost nodes. Lint = structural audit: ghost nodes, malformed source_file, dangling edges, duplicate/isolated nodes, low-confidence + AMBIGUOUS edges, manifest drift, community fragmentation. Use when the user asks to lint / audit / clean / refresh / update the graphify graph or graphify memory."
trigger: /graphify-memory
---

# /graphify-memory

Keep the persistent graphify knowledge graph honest and current. Operates on
`graphify-out/` produced by `/graphify`. Two halves: **update** (re-sync the graph with the
filesystem) and **lint** (audit graph health and fix drift).

## Usage

```
/graphify-memory            # update (incremental) + lint audit + report, apply safe fixes
/graphify-memory lint       # audit only — no re-extraction, no LLM, no writes
/graphify-memory update     # incremental re-extract only (delegates to /graphify --update)
/graphify-memory <path>     # operate on a specific path (default: .)
```

Default = update then lint. `lint` = read-only structural audit (free, no model calls).
`update` = re-extraction only.

## Preconditions

`graphify-out/graph.json` must exist. If not, stop and tell the user to run `/graphify`
first. Resolve the graphify Python interpreter the same way graphify does:

```powershell
$py = (Get-Content graphify-out\.graphify_python -ErrorAction SilentlyContinue).Trim()
if (-not $py) { Write-Host "No graphify python recorded — run /graphify first." }
```

Always set `$env:PYTHONIOENCODING='utf-8'` before running Python (graph labels contain
Unicode like ε, ×, →).

> **Run pattern:** Do NOT pipe Python via a PowerShell here-string chained with
> `Remove-Item` — some harness sandboxes mis-scan the inline script and block the cleanup.
> Instead: create the script with the **Write tool** at `graphify-out\_glint.py` (or
> `_gprune.py`), run it with `& $py graphify-out\_glint.py`, then delete it in a separate
> step. The script bodies below are the exact contents to write.

## Step 1 — Update (skip if `lint`)

Invoke the **graphify** skill's `--update` path on the target path (default `.`): it
detects new/changed/deleted files, re-extracts only those, **prunes ghost nodes from
deleted files**, re-clusters, and regenerates `graph.json`, `GRAPH_REPORT.md`,
`graph.html`. Report its graph diff (new nodes/edges, pruned ghosts). Code-only changes
need no model calls; doc/image changes trigger semantic re-extraction.

If you only want the audit, skip this step.

## Step 2 — Lint audit (always, unless `update`-only)

Write `graphify-out\_glint.py` with this content, run it, then delete it.

```python
import json
from pathlib import Path
from collections import defaultdict
import networkx as nx
from networkx.readwrite import json_graph

raw = json.loads(Path("graphify-out/graph.json").read_text(encoding="utf-8"))
G = json_graph.node_link_graph(raw, edges="links")

mani = {}
mp = Path("graphify-out/manifest.json")
if mp.exists():
    mani = json.loads(mp.read_text(encoding="utf-8"))
mani_files = set()
if isinstance(mani, dict):
    for v in mani.values():
        if isinstance(v, list):
            mani_files.update(v)
        elif isinstance(v, str):
            mani_files.add(v)

def src(n):
    return (G.nodes[n].get("source_file") or "").strip()

def resolves(sf):
    return bool(sf) and Path(sf).exists()

# 1. TRUE ghost nodes: source_file that graphify ONCE TRACKED (in manifest) but is now
#    gone. This is real filesystem drift — safe to prune.
mani_missing = {f for f in mani_files if f and not Path(f).exists()}
mani_missing_base = {Path(f).name for f in mani_missing}
ghosts = sorted({n for n in G.nodes
                 if src(n) and not resolves(src(n))
                 and Path(src(n)).name in mani_missing_base})
ghost_files = sorted({src(n) for n in ghosts})

# 1b. MALFORMED source_file: non-empty, does not resolve, and was never a tracked file
#     (loose label, stem, or comma-joined multi-file from a flaky extraction). NOT a ghost
#     — never pruned. A data-quality signal; fix by re-extracting that file.
malformed = sorted({n for n in G.nodes
                    if src(n) and not resolves(src(n))
                    and Path(src(n)).name not in mani_missing_base})
malformed_sf = sorted({src(n) for n in malformed})

# 2. Dangling edges
ids = {n["id"] for n in raw["nodes"]}
dangling = [(e.get("source"), e.get("target")) for e in raw["links"]
            if e.get("source") not in ids or e.get("target") not in ids]

# 3. Duplicate-label nodes (same label, different id)
bylabel = defaultdict(list)
for n in G.nodes:
    bylabel[(G.nodes[n].get("label", "") or "").strip().lower()].append(n)
dupes = {k: v for k, v in bylabel.items() if k and len(v) > 1}

# 4. Isolated nodes (degree <= 1)
iso = sorted([n for n in G.nodes if G.degree(n) <= 1], key=lambda n: G.degree(n))

# 5. Low-trust edges: AMBIGUOUS, or INFERRED with score < 0.6
lowtrust = []
for u, v, d in G.edges(data=True):
    conf = d.get("confidence", "")
    sc = d.get("confidence_score", 1.0)
    if conf == "AMBIGUOUS" or (conf == "INFERRED" and isinstance(sc, (int, float)) and sc < 0.6):
        lowtrust.append((u, v, conf, sc))

# 6. Self-loops
selfloops = list(nx.selfloop_edges(G))

# 7. Manifest entries missing on disk (real drift count)
indexed_missing = sorted(mani_missing)

print("=== graphify-memory lint ===")
print(f"nodes={G.number_of_nodes()} edges={G.number_of_edges()}")
print(f"[1] TRUE ghost nodes (tracked, now deleted): {len(ghosts)} across {len(ghost_files)} file(s)")
for f in ghost_files[:20]:
    print(f"      - {f}")
print(f"[1b] malformed source_file (NOT ghosts, never pruned): {len(malformed)}")
for f in malformed_sf[:20]:
    print(f"      - {f}")
print(f"[2] dangling edges (missing endpoint): {len(dangling)}")
for s, t in dangling[:20]:
    print(f"      - {s} -> {t}")
print(f"[3] duplicate-label node groups: {len(dupes)}")
for k, v in list(dupes.items())[:20]:
    print(f"      - '{k}': {v}")
print(f"[4] isolated nodes (deg<=1): {len(iso)}")
for n in iso[:25]:
    print(f"      - {G.nodes[n].get('label', n)} (deg {G.degree(n)})")
print(f"[5] low-trust edges (AMBIGUOUS / INFERRED<0.6): {len(lowtrust)}")
for u, v, c, s in lowtrust[:25]:
    print(f"      - {G.nodes[u].get('label', u)} -> {G.nodes[v].get('label', v)} [{c} {s}]")
print(f"[6] self-loops: {len(selfloops)}")
print(f"[7] manifest entries missing on disk: {len(indexed_missing)}")
for f in indexed_missing[:20]:
    print(f"      - {f}")
```

Run + clean up:

```powershell
$env:PYTHONIOENCODING='utf-8'
$py = (Get-Content graphify-out\.graphify_python).Trim()
& $py graphify-out\_glint.py
Remove-Item -ErrorAction SilentlyContinue graphify-out\_glint.py
```

Cross-reference check [4] with the "Knowledge Gaps" section of `GRAPH_REPORT.md`.

## Step 3 — Report

Present the numbered findings concisely. For a `lint`-only run, **stop here** — propose
fixes but do not write anything.

## Step 4 — Apply fixes (only on default / `update`, never on `lint`)

**Safe (auto):**
- **Prune TRUE ghost nodes** (check [1]) — only the manifest-confirmed set — and **remove
  self-loops** (check [6]). Dangling edges (check [2]) are dropped at build time; if any
  remain, drop them too. Then **re-cluster + regenerate report** via graphify's
  `--cluster-only` path so outputs match the cleaned graph.
- Pruning uses the SAME manifest-confirmed predicate as the audit — it must NEVER remove a
  node whose `source_file` is merely malformed/loose (check [1b]) or still resolves.

**Judgement (confirm with the user first):**
- **Malformed source_file** (check [1b]) — fix by **re-extracting** that file
  (`/graphify <file> --update`), not by deleting the node. If the file is genuinely gone,
  it would show under [1] instead.
- **Merge duplicate-label nodes** (check [3]) — same label often = genuinely distinct
  things (e.g. `richardson_gci()` defined in several `sweep*.py`; two different `index.md`).
  Show the groups and ask before merging any ids. Default to NOT merging.
- **Isolated / low-trust** (checks [4],[5]) — a *documentation* signal, not a graph bug. Do
  not delete. Offer `/graphify query` to explore, or a targeted re-extract if a real edge
  is missing.
- **Manifest drift** (check [7]) — if many tracked files are gone, recommend a full
  `/graphify` rebuild over incremental.

Prune script — write `graphify-out\_gprune.py`, run, delete:

```python
import json
from pathlib import Path
import networkx as nx
from networkx.readwrite import json_graph

raw = json.loads(Path("graphify-out/graph.json").read_text(encoding="utf-8"))
G = json_graph.node_link_graph(raw, edges="links")

mani = json.loads(Path("graphify-out/manifest.json").read_text(encoding="utf-8")) \
    if Path("graphify-out/manifest.json").exists() else {}
mani_files = set()
if isinstance(mani, dict):
    for v in mani.values():
        if isinstance(v, list):
            mani_files.update(v)
        elif isinstance(v, str):
            mani_files.add(v)
mani_missing_base = {Path(f).name for f in mani_files if f and not Path(f).exists()}

def src(n):
    return (G.nodes[n].get("source_file") or "").strip()

# Manifest-confirmed ghosts ONLY — never touch malformed/loose source_file or live nodes.
ghosts = {n for n in G.nodes
          if src(n) and not Path(src(n)).exists()
          and Path(src(n)).name in mani_missing_base}
G.remove_nodes_from(ghosts)
G.remove_edges_from(list(nx.selfloop_edges(G)))

Path("graphify-out/graph.json").write_text(
    json.dumps(json_graph.node_link_data(G, edges="links"), indent=2, ensure_ascii=False),
    encoding="utf-8")
print(f"pruned {len(ghosts)} confirmed-ghost node(s); self-loops removed; "
      f"{G.number_of_nodes()} nodes / {G.number_of_edges()} edges remain")
```

```powershell
$env:PYTHONIOENCODING='utf-8'
$py = (Get-Content graphify-out\.graphify_python).Trim()
& $py graphify-out\_gprune.py
Remove-Item -ErrorAction SilentlyContinue graphify-out\_gprune.py
```

After pruning, run the graphify skill's **`--cluster-only`** path to rebuild
`GRAPH_REPORT.md` and re-label communities from the cleaned graph.

## Step 5 — Summarize

Report: update diff (if run), lint counts per check, what was pruned/fixed automatically,
and what needs a user decision (malformed re-extract, merges, rebuild).

## Honesty rules

- A node is a ghost ONLY if its file was tracked (in the manifest) and is now missing.
  Loose/garbled `source_file` is a data-quality flag, never a delete trigger.
- Never silently delete a node whose `source_file` still resolves. Isolated ≠ wrong.
- Never invent edges to "connect" isolated nodes. Missing edges are re-extracted from
  source, not fabricated.
- Always report the true-ghost prune count so the user sees the drift that was corrected.
