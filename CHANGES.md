# Changes

## 2026-06-09

- Reattached the custom navigation logo on view appearance and removed it on
  view disappearance, not only controller teardown.
- Extended static timer checks to require navigation logo appearance and
  disappearance lifecycle coverage.
- Added a small scheduling tolerance to the repeating countdown timer and
  extended static timer checks to require it.
- Reset the brushing prompt alpha when the shared timer reset path stops the
  repeating animation.
- Reset the countdown value and synchronized timer label when the shared reset
  path runs.
- Extended timer lifecycle checks to require reset-state label synchronization.
- Added a shared timer reset path and call it when the view disappears.
- Extended timer lifecycle checks to require the view-disappear reset path.

## 2026-06-08

- Removed the custom navigation logo during controller teardown and tightened
  the static deinit lifecycle check.
- Ignored Python bytecode caches produced by local checker syntax validation.
- Added timer/start/prompt accessibility labels and static checks that keep the
  timer accessibility value synchronized with visible countdown text.
- Added `make check` as the shared repository verification alias.
- Hardened the hex color helper so invalid or partially parsed color strings
  fall back to gray instead of silently becoming black.
- Extended `make test` with a source check for hex color parser validation.
- Added a Makefile verification gate for project metadata and timer lifecycle
  source checks.
- Fixed repeated Start taps so an existing countdown timer is invalidated before
  scheduling a new one.
- Clamped countdown completion at zero and stopped repeating brush-text
  animations when the timer finishes.
- Invalidated the timer when the view controller is deallocated.
- Added canonical `docs/plans` coverage and made project checks require
  completed plans.
