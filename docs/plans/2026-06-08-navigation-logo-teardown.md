# Navigation Logo Teardown

## Status: Completed

## Context

`ViewController` adds a custom logo image view directly to the navigation
controller's view in `viewDidLoad`. The controller invalidated its timer during
`deinit`, but it did not remove the custom navigation view, so repeated
controller lifecycles could leave stale logo views behind.

## Objectives

- Preserve the existing custom logo behavior.
- Remove the logo view when the controller is deallocated.
- Tighten the static lifecycle check to inspect the actual `deinit` body.
- Keep README, VISION, and CHANGES aligned with the teardown guard.

## Work Completed

- Added `logoView?.removeFromSuperview()` to `ViewController.deinit`.
- Updated `scripts/check-toothbrush-source.py --mode timer` to parse the
  `deinit` body and require both timer invalidation and logo removal there.
- Updated repository maintenance documentation.

## Verification

- `python3 scripts/check-toothbrush-source.py --mode timer`
- `python3 scripts/check-toothbrush-source.py --mode project`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Move the logo into the navigation item when modernizing the Swift/Xcode
  project.
- Add simulator-backed lifecycle assertions when Xcode is available.
