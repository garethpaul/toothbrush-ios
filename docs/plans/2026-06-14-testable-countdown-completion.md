# Testable Countdown Completion

## Status: Completed

## Context

Countdown duration arithmetic is independently testable, but the controller
still decides whether to keep running or enter its completed reset state inside
the timer callback. Verifying that transition currently requires controller
state or a live timer.

## Priority

Represent the deadline-derived running/completed decision as a pure value so
XCTest can exercise the completion boundary immediately without waiting two
minutes.

## Requirements

- Derive a running state with the remaining whole-second value while time
  remains.
- Derive a completed state at and beyond the deadline.
- Route normal ticks and application-activation reconciliation through the
  same state decision.
- Preserve continuous-clock timing, shared completion reset, weak timer
  ownership, accessibility synchronization, and the iOS 12 floor.
- Add mutation-sensitive XCTest and static contracts plus maintained project
  documentation.

## Verification

- The focused countdown-state XCTest coverage passed its static suite contract;
  native execution remains the hosted Xcode authority.
- The repository and external-directory `make check` passed.
- Seven hostile countdown-state mutations were rejected across the
  running/completed boundary, controller integration, test contract,
  documentation, and plan status.
- Final generated-artifact, credential, and exact-diff audits passed. Hosted
  Xcode/XCTest remains the native exact-head authority.

## Scope Boundary

This change does not shorten the two-minute brushing interval, persist timer
state across process termination, add a new completion screen, or alter the
existing prompt animation and reset presentation.
