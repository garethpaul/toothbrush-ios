# Foreground Countdown Reconciliation

## Status: Completed

## Context

The brushing deadline uses `mach_continuous_time`, so sleep and wall-clock
changes cannot extend the interval. While the app is inactive, repeating timer
callbacks may be suspended. On activation, the label and accessibility value
can therefore remain stale until the run loop delivers another timer callback.

## Priority

Reconcile the active countdown immediately when the application becomes active,
using the same deadline-based update path as normal timer ticks.

## Requirements

- R1. Observe `UIApplication.didBecomeActiveNotification` while the controller
  is alive.
- R2. On activation, update only an active countdown through `subtractTime()`.
- R3. Remove the notification observer during controller teardown.
- R4. Preserve the continuous deadline, weak timer callback, common run-loop
  mode, tolerance, view-disappearance reset, prompt animation, accessibility
  synchronization, privacy manifest, and iOS 12 floor.
- R5. Add fail-closed static contracts, hostile mutations, documentation, and
  full `make check` verification.

## Implementation Units

### Active-state reconciliation

**Files:** `toothbrush/ViewController.swift`

Register the application-active notification after controller setup, remove it
in `deinit`, and route active countdown reconciliation through the existing
deadline-derived tick method.

### Contracts and maintenance record

**Files:** `scripts/check-toothbrush-source.py`, `README.md`, `SECURITY.md`,
`VISION.md`, `CHANGES.md`,
`docs/plans/2026-06-13-foreground-countdown-reconciliation.md`

Reject a missing observer, mismatched notification, unconditional reset,
duplicated countdown math, missing teardown, documentation drift, and stale
plan status.

## Verification Plan

- focused timer and accessibility source contracts
- full `make check` locally and from an external working directory
- hosted Xcode 16.4 XCTest execution on the existing simulator job
- focused foreground-lifecycle mutations
- workflow/plist/privacy/scheme/SVG/asset parsing, Python syntax, artifact,
  secret-pattern, and `git diff --check` audits

## Scope Boundaries

- Do not persist the timer across process termination or change its two-minute
  duration, clock source, display format, animation, navigation, or privacy
  declaration.
- Do not claim physical-device background scheduling or sleep-transition
  validation from static checks or simulator XCTest.

## Work Completed

- Registered for application-active notifications after controller setup.
- Reconciled only an active deadline through the existing `subtractTime()`
  path, preserving countdown and accessibility synchronization.
- Removed the matching notification observer during controller teardown.
- Added fail-closed lifecycle and documentation contracts.

## Verification

- Focused timer and accessibility source contracts passed.
- Full `make check` passed project, timer, color, and accessibility contracts
  with the documented local no-Xcode fallbacks.
- The same full gate passed from an external working directory.
- Eight focused mutations covering registration, notification identity,
  matching teardown, active-state guarding, shared reconciliation, duplicated
  deadline math, documentation drift, and plan status were rejected.
- Parsed 1 workflow YAML file, 3 plist/privacy files, 3 JSON files, and 4 scheme,
  workspace, and SVG XML files; Python syntax, diff whitespace, generated-
  artifact, and intended-diff secret audits passed.
- Plan-aware lifecycle, correctness, accessibility, testing, and maintainability
  review found no actionable findings. Browser testing is not applicable.
- XcodeBuildMCP and local `xcodebuild` are unavailable; the exact-head hosted
  Xcode 16.4 XCTest job is required native evidence.
