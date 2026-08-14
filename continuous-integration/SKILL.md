---
name: continuous-integration
description: Automate repository checks in continuous integration. Use when the user wants a CI pipeline created, repaired, or simplified, or wants builds and tests enforced on repository changes; use after `unit-testing` establishes a reliable test command.
---

# Continuous Integration

Turn proven local checks into the smallest automated merge gate. CI runs repository contracts; it does not invent them.

## 1. Inventory the contract

Read the repository instructions, build files, test configuration, and existing CI. Identify:

- the current CI provider and supported runner,
- exact local commands already used for build and validation,
- required toolchain, environment, and protected artifacts,
- repository events that should trigger validation.

Use the broader deterministic command supplied by `unit-testing` when available. Proceed when every proposed CI check already has a local command and a reason to gate changes.

## 2. Define the minimum gate

Select only checks required to catch a broken build or violated repository contract. Use the repository's existing package manager, lockfile, scripts, and CI provider. Add matrices, services, caches, artifacts, or third-party actions only for a present requirement.

Proceed when the gate covers the supported environment without speculative jobs or duplicated commands.

## 3. Implement the pipeline

Create or simplify one workflow that checks out the repository, installs the declared toolchain and dependencies, and runs the selected commands. Keep commands in project scripts when they must also run locally; keep CI-specific orchestration in the workflow. Use least-privilege permissions and pass sensitive values through the provider's secret mechanism.

Proceed when a clean runner has all declared inputs and each failure returns a nonzero status at the responsible step.

## 4. Verify the gate

Run the exact project commands locally. Validate workflow syntax with an available native or already-installed tool; otherwise inspect it against the provider schema and state that remote execution remains unverified. Report triggers, jobs, commands, required secrets, and validation results.

Hand structural simplification to `yagni-refactor`; hand missing or unreliable behavioral checks to `unit-testing`. CI work is complete when the workflow is minimal, reproducible from a clean checkout, and every required gate has concrete validation evidence.
