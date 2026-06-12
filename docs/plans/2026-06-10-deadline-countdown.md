# Deadline-Based Countdown

## Status: Completed

## Context

The timer subtracted one second for every callback. If the main run loop was
busy or the app was temporarily suspended, missed or delayed callbacks made a
nominal two-minute brushing interval last longer than two real minutes.

## Work Completed

- Recorded a two-minute deadline whenever the timer starts.
- Derived each visible countdown value from the deadline and current time.
- Cleared the deadline through the existing shared reset path.
- Added pure XCTest coverage for the initial value, delayed callbacks, and an
  expired deadline.
- Extended static checks to reject tick-count subtraction and preserve the
  deadline helper, reset, and test contracts.

## Verification

- `make check`
- Negative tick-count and missing-deadline source mutations
- `git diff --check`

The hosted macOS job compiles both the app and XCTest target with Xcode 16.4.
