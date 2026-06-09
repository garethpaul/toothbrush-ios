# Countdown Timer Tolerance

## Status: Completed

## Context

The app uses a repeating one-second `NSTimer` for the two-minute brushing
countdown. Exact wakeups are unnecessary for this UI, so the scheduled timer can
give iOS a small tolerance while keeping the visible countdown behavior intact.

## Objectives

- Preserve the 120-second countdown flow.
- Add a small tolerance to the repeating countdown timer.
- Extend static timer checks so the tolerance is not removed.

## Work Completed

- Set `timer.tolerance = 0.1` after scheduling the repeating countdown timer.
- Extended `scripts/check-toothbrush-source.py --mode timer` to require the
  timer tolerance.
- Updated README, VISION, and CHANGES with the new timer scheduling guard.

## Verification

- Negative check before implementation:
  `python3 scripts/check-toothbrush-source.py --mode timer` failed with
  `setupTimer must set a small tolerance on the repeating timer`.
- `python3 scripts/check-toothbrush-source.py --mode timer`
- `python3 scripts/check-toothbrush-source.py --mode project`
- `python3 scripts/check-toothbrush-source.py --mode color`
- `python3 scripts/check-toothbrush-source.py --mode accessibility`
- `make check`
- `make verify`
- `git diff --check`

## Xcode Notes

`xcodebuild` was not installed in this environment, so simulator compilation
was not run here. The repository `make check` wrapper still attempts the
simulator build with code signing disabled when `xcodebuild` is available.
