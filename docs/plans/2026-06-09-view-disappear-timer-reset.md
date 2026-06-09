# View Disappear Timer Reset

## Status: Completed

## Context

The toothbrush timer invalidated existing timers before restart and during
deallocation, but an active `NSTimer` retains its target while it is running.
If the timer view leaves the screen mid-countdown, relying on `deinit` can delay
cleanup and leave the prompt animation state tied to a controller that should be
done.

## Objectives

- Stop an active countdown when the timer view leaves the screen.
- Keep timer completion and disappearance on one reset path.
- Extend the static lifecycle check so the view-disappear guard is preserved.

## Work Completed

- Added `stopTimerAndResetPrompt()` for timer invalidation and prompt reset.
- Reused the reset helper when the countdown reaches zero.
- Called the reset helper from `viewWillDisappear`.
- Extended `scripts/check-toothbrush-source.py` to require the shared reset path.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check-toothbrush-source.py --mode timer`
- `python3 scripts/check-toothbrush-source.py --mode project`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add simulator-backed UI assertions when Xcode tooling is available.
- Add a shorter test mode or injected timer so completion behavior can be tested
  without waiting two minutes.
