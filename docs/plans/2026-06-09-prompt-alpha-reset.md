# Prompt Alpha Reset

## Status: Completed

## Context

The shared timer reset path invalidates the timer, removes the prompt
animation, and hides the prompt label. The repeating animation changes the
prompt's presentation alpha, so reset should also restore the model alpha to a
known value before the next timer run.

## Objectives

- Preserve the existing two-minute countdown behavior.
- Keep the prompt hidden and transparent after completion or view disappearance.
- Extend static lifecycle checks so the reset visual state stays complete.

## Work Completed

- Set `brushText.alpha = 0` inside `stopTimerAndResetPrompt()`.
- Extended `scripts/check-toothbrush-source.py --mode timer` to require the
  prompt alpha reset in the shared timer reset path.
- Documented the prompt reset-state guard in README, VISION, and CHANGES.

## Verification

- `python3 scripts/check-toothbrush-source.py --mode timer`
- `python3 scripts/check-toothbrush-source.py --mode project`
- `make check`
- `make verify`
- `git diff --check`

## Xcode Notes

XcodeBuildMCP tools and `xcodebuild` were not available in this environment, so
simulator build verification was not run here. The repository `make check`
wrapper still runs `xcodebuild` when that tool is available locally.
