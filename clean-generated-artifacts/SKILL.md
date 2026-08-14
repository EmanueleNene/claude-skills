---
name: clean-generated-artifacts
description: Inventory, classify, and safely remove generated artifacts through an auditable manifest and explicit apply gate. Use after builds, tests, simulations, analyses, data generation, debugging, or delivery workflows when disposable outputs must be cleaned while preserving project files, dependencies, user work, and cited evidence.
---

# Clean Generated Artifacts

Clean from an exact manifest. Derive policy from the current project's instructions and the commands that generated the files; no extension is universally disposable.

## Safety contract

- Scan only explicit workspace-contained scopes produced or named by the current task.
- Convert project safety instructions into exact paths or `--protect-glob` rules.
- Preserve tracked files, pre-existing user work, dependencies, credentials, configuration, and cited evidence.
- Default unknown outputs, logs, errors, datasets, and images to `review`.
- Apply deletion only after the user approves the exact manifest entries.

## Process

### 1. Build policy and preservation sets

Read project instructions, ignore rules, build/test configuration, generation commands, and delivery artifacts. Record:

- exact protected paths and patterns;
- exact run directories or files in scope;
- known disposable patterns supported by project evidence;
- reports, logs, plots, datasets, and baselines required for reproducibility or presentation.

Preserve cited evidence in a durable location before proposing deletion.

Complete this step when every delete rule has a project or command-level rationale and every cited artifact is protected.

### 2. Scan explicit scopes

Resolve `<skill-dir>` to this skill's installed directory, then run its helper:

```text
python <skill-dir>/scripts/cleanup_generated_artifacts.py scan \
  --root <workspace> \
  --scope <generated-run-directory> \
  --protect-glob <project-protected-pattern> \
  --delete-glob <known-disposable-pattern> \
  --manifest <delivery-run>/cleanup-manifest.json
```

Repeat `--scope`, `--protect`, `--protect-glob`, `--delete-glob`, and `--review-glob` as needed. Prefer a narrow scope over a broad pattern.

Manifest actions:

- `delete`: a caller-supplied disposable pattern or a conservative built-in cache rule;
- `review`: an unknown or potentially evidentiary artifact;
- `keep`: tracked content or an explicit protection rule.

Complete this step when every file in every scope appears exactly once and summary totals match the entries.

### 3. Review the exact list

Compare every `delete` entry with the generation commands, preservation set, and current workspace state. Change useful evidence to `keep`. Promote a `review` item to `delete` only by editing that exact manifest entry and recording why it is no longer needed.

Complete this step when the proposed list is exact, evidence-safe, and understandable without glob expansion.

### 4. Apply with approval

After explicit approval of that manifest, run:

```text
python <skill-dir>/scripts/cleanup_generated_artifacts.py apply \
  --root <workspace> \
  --manifest <delivery-run>/cleanup-manifest.json \
  --confirm DELETE-LISTED-GENERATED-ARTIFACTS
```

The helper rechecks containment, scopes, tracked state, protection rules, symlinks, size, and modification time before deleting individual files. It removes only resulting empty directories.

Complete this step when the manifest records every deletion, refusal, changed file, and missing file.

### 5. Verify

Run focused status and existence checks. Confirm protected paths and evidence remain available and only approved entries disappeared. Record totals and pending review items in the delivery ledger.

## Completion check

- Explicit scopes and policy rules are stored in the manifest.
- Every cited artifact remains available.
- No tracked or protected path was removed.
- Applied deletions match approved entries exactly.
- Changed and refused files remain untouched and are reported.
- Pending review items are visible.

Return the manifest path, policy, scan totals, applied totals, refusals, preserved evidence, and pending review items.
