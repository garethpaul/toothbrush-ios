# Weak Timer Ownership

## Status: Completed

## Context

The controller stores a repeating `Timer` created with itself as the timer
target. The timer retains its target while the controller retains the timer,
forming a cycle until a normal reset path invalidates it. `deinit` cannot be the
fallback that breaks a cycle preventing deinitialization.

## Priority

Use the iOS 10+ block timer API with weak controller capture so timer ownership
does not keep a departed controller alive when lifecycle cleanup is delayed or
bypassed.

## Requirements

- R1. Schedule the repeating timer with a block that captures the controller
  weakly and forwards ticks to the existing deadline-based method.
- R2. Preserve one-second cadence, 0.1 tolerance, common run-loop mode, the
  two-minute deadline, and shared reset paths.
- R3. Keep explicit invalidation during setup, disappearance, completion, and
  deinitialization.
- R4. Extend static contracts and hostile mutations for weak capture and tick
  forwarding without claiming unavailable local Xcode execution.
- R5. Update maintenance documentation and pass full portable verification.

## Scope Boundaries

- Do not change countdown duration, visible text, animation, accessibility,
  navigation-logo behavior, deployment target, project settings, or workflow.
- Do not add dependencies.

## Implementation Units

### Timer ownership

**Files:** `toothbrush/ViewController.swift`

- Replace target-selector scheduling with `scheduledTimer(withTimeInterval:)`.
- Capture `self` weakly and call the existing `subtractTime()` implementation.

### Contracts and maintenance record

**Files:** `scripts/check-toothbrush-source.py`, `README.md`, `SECURITY.md`,
`VISION.md`, `CHANGES.md`, `docs/plans/2026-06-12-weak-timer-ownership.md`

## Verification Plan

- timer, project, color, and accessibility contracts
- focused weak-capture mutations
- local and external-directory `make check`
- Python checker compilation
- `git diff --check`
- hosted Xcode/XCTest snapshot after push

## Verification Record

- Timer and project contract modes passed with block scheduling, weak capture,
  tick forwarding, tolerance, common run-loop mode, deadline, and reset
  invariants enforced.
- Four focused mutations were rejected: missing weak capture, forced strong
  self use, target-selector regression, and missing tick forwarding.
- `git diff --check` passed.
- Local and external-directory `make check` passed project, timer, color, and
  accessibility contracts. `xcodebuild` was unavailable, so no local Swift
  compile, simulator run, or XCTest execution is claimed.

## Remaining Risks

- Linux verification cannot compile Swift or exercise UIKit lifecycle behavior.
- Hosted XCTest covers pure countdown/color behavior, not controller retention on
  a simulator navigation stack.
