# Timer Lifecycle Gate

## Problem

The app had no local verification command. Pressing Start repeatedly could
schedule multiple timers, the countdown stopped only when it hit exactly zero,
and the repeating brush-text animation was not stopped at completion.

## TDD Evidence

1. Added `scripts/check-toothbrush-source.py` and Makefile targets.
2. Ran `make test` before implementation changes and confirmed the timer
   lifecycle checks failed.
3. Updated timer invalidation/completion handling and reran the full
   verification gate.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `git diff --check`
