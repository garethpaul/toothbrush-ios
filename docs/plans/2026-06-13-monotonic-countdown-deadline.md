# Monotonic Countdown Deadline

## Status: Completed

## Context

The countdown derives remaining time from `Date`. Delayed timer callbacks no
longer extend the session, but a manual or network-driven wall-clock adjustment
can still make a running brushing interval longer or shorter. Elapsed-duration
logic should use a monotonic clock instead of calendar time.

## Requirements

- Base the two-minute deadline on `mach_continuous_time`, which includes time
  while the device is asleep.
- Keep the remaining-seconds calculation pure and injectable for deterministic
  XCTest coverage.
- Preserve rounding up partial seconds and clamping expired intervals to zero.
- Preserve weak timer ownership, common run-loop scheduling, tolerance,
  animation reset, accessibility synchronization, and view teardown behavior.
- Extend static contracts and hosted XCTest coverage for the monotonic boundary.
- Document why wall-clock changes cannot alter a running session.
- Bundle a privacy manifest declaring system boot time reason `35F9.1` for the
  local timer calculation.

## Non-Goals

- Do not add background execution, notifications, persistence, or resume a
  countdown after process termination.
- Do not change the two-minute duration, visual animation, or navigation logo.
- Do not change the iOS 12 / Xcode 16.4 baseline.

## Implementation

1. Replace the stored `Date` deadline with a continuous monotonic deadline.
2. Change the pure remaining-time helper and existing XCTest inputs to
   `TimeInterval` values.
3. Extend the source checker, documentation, and negative mutation coverage.

## Verification

- Focused timer, color, and accessibility contracts passed, and the Python
  checker compiled successfully.
- Apple documentation review confirmed `systemUptime` is awake time and can
  stop during sleep; the implementation instead uses the continuous Mach clock
  and declares required-reason code `35F9.1` in `PrivacyInfo.xcprivacy`.
- Local and external-directory `make check` passed project, timer, color, and
  accessibility contracts with the truthful no-Xcode fallback.
- App, test, and privacy plists; workflow YAML; scheme, workspace, and SVG XML;
  asset JSON; PNG dimensions; and privacy resource linkage parsed successfully.
- Twelve hostile mutations covering sleep-pausing and wall clocks, timebase
  conversion, helper math, deadline reset, XCTest coverage, privacy reason and
  resource linkage, documentation, and plan completion were rejected.
- Exact diff, ignored-artifact, secret-pattern, and worktree audits passed; the
  ignored Python bytecode cache was preserved and excluded from commit.
- Bounded hosted Xcode/XCTest evidence is recorded at the exact pushed head.
