# Make Authority Isolation

Status: Completed

## Goal

Keep portable and native Toothbrush verification authoritative when invoked
from another directory or with hostile Make variables, startup files, modes,
shell overrides, and executable paths.

## Changes

- Resolve and export the repository root from the checked-in Makefile alone.
- Freeze trusted Python and Xcode executable overrides as literal values and
  fix the recipe shell.
- Reject caller-supplied `MAKEFLAGS`, `MAKEFILES`, `MAKEFILE_LIST`, dry-run,
  touch, question, and ignore-error verification modes.
- Add a self-contained adversarial root harness across every public target and
  an executable workflow contract covering 17 unsafe mutations.
- Invoke both hosted gates through `/usr/bin/make`.

## Verification

- repository and external-directory `make check` passed
- 35 target/authority combinations passed with quoted and literal-dollar tool
  paths
- 17 unsafe workflow mutations were rejected
- static project, timer, color, and accessibility contracts passed locally
- hosted static baseline and Xcode/XCTest gates are required on the exact PR
  and merge commits before final tracker completion
