# Make Root Override Protection

## Status: Planned

## Context

The Makefile derives static checker, Xcode project, and XCTest paths from its
own location, but environment and command-line assignments can replace `ROOT`.
A caller can therefore redirect verification and native commands away from the
checked-out toothbrush application.

## Priority

Verification paths are a trust boundary. The repository must authoritatively
select its own root while preserving intentional Python and Xcode executable
overrides.

## Objectives

- Protect the repository-derived root from caller assignments.
- Preserve root-first declaration order and both tool overrides.
- Preserve all aliases, static modes, hosted XCTest destination, and build
  flags.
- Exercise every alias from repository and external working directories under
  hostile environment and command-line root values.
- Add mutation-sensitive source, README, and completed-plan contracts.

## Implementation Units

### U1. Protect verification paths

**Files:** `Makefile`

Make `ROOT` authoritative without changing tool variables, targets, checker
modes, XCTest invocation, or native build arguments.

### U2. Preserve native and static contracts

**Files:** `scripts/check-toothbrush-source.py`, `README.md`

Require one root assignment total, the exact protected declaration, root-first
tool ordering, alias graph, root-anchored checker/Xcode paths, README indexing,
and this plan's completed evidence.

## Verification

- Project, timer, color, accessibility, and full `make check` gates.
- Repository/external working directories and hostile root assignments.
- Declaration, duplicate, placement, alias, path, README, and plan mutations.
- Exact diff, protected Swift/project/scheme/workflow/asset paths, artifacts,
  secrets, and whitespace audits.
- Exact-head static-baseline and hosted Xcode/XCTest verification.

## Scope Boundary

This change does not alter Swift behavior, timer lifecycle, accessibility,
project settings, schemes, assets, workflow policy, or deployment targets.
