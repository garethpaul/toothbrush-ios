# Reset Label Sync

## Status: Completed

## Context

The shared timer reset path invalidated the timer, stopped the prompt animation,
and restored the start button. When the view disappeared mid-countdown, the same
path ran but left the countdown label and accessibility value at the last
remaining second count.

## Objectives

- Reset the countdown value whenever the shared reset path runs.
- Keep visible timer text and accessibility value synchronized after reset.
- Extend static lifecycle checks so view-disappear and completion resets cannot
  leave stale timer state behind.

## Work Completed

- Updated `stopTimerAndResetPrompt()` to set `second = 0` and call
  `updateTimerLabel()`.
- Extended `scripts/check-toothbrush-source.py --mode timer` to require the
  reset-state synchronization inside the shared reset helper.
- Updated README, VISION, and CHANGES with the new guardrail.

## Verification

- `python3 scripts/check-toothbrush-source.py --mode timer`
- `make lint`
- `make test`
- `make build`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add simulator-backed assertions for label state when Xcode tooling is
  available.
- Consider a dedicated completion message separate from the numeric countdown.
