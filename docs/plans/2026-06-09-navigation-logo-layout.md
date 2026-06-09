# Navigation Logo Layout

## Status: Completed

## Context

The custom navigation logo was centered once when the view loaded. Later layout
passes, such as simulator rotation or container size changes, could leave the
logo using an outdated horizontal position.

## Objectives

- Keep the custom logo centered after view layout changes.
- Preserve the existing logo image, tint, and lifecycle behavior.
- Keep the change static-checkable without requiring a simulator in this
  environment.
- Record the behavior in the repository verification plan.

## Work Completed

- Moved navigation logo positioning into `updateNavigationLogoFrame()`.
- Called the positioning helper during setup, layout updates, and logo
  reattachment.
- Extended `scripts/check-toothbrush-source.py` to require layout-driven logo
  recentering.
- Updated README, VISION, and CHANGES.

## Verification

- Negative: source review showed the logo frame was only positioned during
  `viewDidLoad()`.
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

- Verify logo positioning on simulator rotations when Xcode is available.
- Move the custom logo into a navigation item title view in a dedicated UI
  modernization pass.
