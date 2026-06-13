# Monotonic Countdown Deadline

## Status: In Progress

## Context

The countdown derives remaining time from `Date`. Delayed timer callbacks no
longer extend the session, but a manual or network-driven wall-clock adjustment
can still make a running brushing interval longer or shorter. Elapsed-duration
logic should use a monotonic clock instead of calendar time.

## Requirements

- Base the two-minute deadline on `ProcessInfo.processInfo.systemUptime`.
- Keep the remaining-seconds calculation pure and injectable for deterministic
  XCTest coverage.
- Preserve rounding up partial seconds and clamping expired intervals to zero.
- Preserve weak timer ownership, common run-loop scheduling, tolerance,
  animation reset, accessibility synchronization, and view teardown behavior.
- Extend static contracts and hosted XCTest coverage for the monotonic boundary.
- Document why wall-clock changes cannot alter a running session.

## Non-Goals

- Do not add background execution, notifications, persistence, or resume a
  countdown after process termination.
- Do not change the two-minute duration, visual animation, or navigation logo.
- Do not change the iOS 12 / Xcode 16.4 baseline.

## Implementation

1. Replace the stored `Date` deadline with a monotonic uptime deadline.
2. Change the pure remaining-time helper and existing XCTest inputs to
   `TimeInterval` values.
3. Extend the source checker, documentation, and negative mutation coverage.

## Verification

- Run focused project and timer contracts.
- Run local and external-directory `make check` with the truthful no-Xcode
  fallback.
- Parse project, plist, workflow, scheme, asset JSON, and SVG artifacts.
- Reject hostile mutations for wall-clock use, uptime capture, helper math,
  stored deadline reset, XCTest coverage, documentation, and plan completion.
- Inspect the exact diff, ignored artifacts, secret patterns, and worktree.
- Record bounded hosted Xcode/XCTest evidence at the exact pushed head.
