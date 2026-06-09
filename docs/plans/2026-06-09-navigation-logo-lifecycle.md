# Navigation Logo Lifecycle

## Status: Completed

## Context

The app adds a custom logo view directly to the navigation controller's view.
Earlier teardown coverage removed that view when the controller deallocated,
but a controller can leave the screen while still retained. In that case the
logo could stay attached to the navigation controller during another screen.

## Objectives

- Reattach the custom navigation logo when the brushing screen appears.
- Remove the custom navigation logo when the brushing screen disappears.
- Preserve deallocation cleanup for the logo view.
- Keep the lifecycle behavior covered by static checks under `make check`.

## Work Completed

- Added `showNavigationLogo()` and `removeNavigationLogo()` helpers.
- Reattached the logo in `viewWillAppear`.
- Removed the logo in `viewWillDisappear` and through the deinit cleanup path.
- Extended `scripts/check-toothbrush-source.py` to require the appearance,
  disappearance, and teardown logo lifecycle paths.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check-toothbrush-source.py --mode timer`
- `make check`
- `git diff --check`

`xcodebuild` is not installed in this environment, so simulator build and test
verification were not available after static source checks passed.

## Follow-Up Candidates

- Add simulator-backed UI coverage for navigation-logo visibility when Xcode is
  available.
- Modernize the controller lifecycle code in a dedicated Swift syntax pass.
