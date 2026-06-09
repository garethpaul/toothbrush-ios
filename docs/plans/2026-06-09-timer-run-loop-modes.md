# Timer Run Loop Modes

## Status: Completed

## Context

The brushing countdown used a repeating `NSTimer` created with
`scheduledTimerWithTimeInterval`. That schedules the timer on the default run
loop mode, so UI tracking interactions can pause countdown ticks until the run
loop returns to the default mode.

## Objectives

- Preserve the existing one-second repeating countdown.
- Keep the small timer tolerance already used for efficient scheduling.
- Add the countdown timer to common run-loop modes after scheduling.
- Extend static timer checks so the run-loop mode guard remains in place.

## Work Completed

- Added the scheduled timer to `NSRunLoopCommonModes` in `setupTimer()`.
- Extended `scripts/check-toothbrush-source.py` to require common-mode
  scheduling.
- Extended project checks to require this completed plan.
- Updated README, VISION, and CHANGES.

## Verification

- Negative: `python3 scripts/check-toothbrush-source.py --mode timer` failed
  before the Swift fix because the timer was not added to common run-loop modes.
- `python3 scripts/check-toothbrush-source.py --mode project`
- `python3 scripts/check-toothbrush-source.py --mode timer`
- `python3 scripts/check-toothbrush-source.py --mode color`
- `python3 scripts/check-toothbrush-source.py --mode accessibility`
- `make check`
- `make verify`
- `git diff --check`

`xcodebuild` is not installed in this environment, so `make check` reports that
the Xcode build was not run after static verification passes.

## Follow-Up Candidates

- Add simulator-backed countdown assertions when Xcode is available.
- Modernize the timer API in a dedicated Swift compatibility pass.
