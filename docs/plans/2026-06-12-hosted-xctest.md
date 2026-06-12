# Hosted XCTest Execution

## Status: Completed

## Context

The macOS validation job compiled the app and XCTest target but never launched
the tests. A broken assertion, test-host configuration, or runtime-only failure
could therefore pass the hosted gate as long as the sources still compiled.

## Objectives

- Execute the existing hex-color and deadline tests on a hosted simulator.
- Keep the Xcode release and simulator destination explicit and reproducible.
- Preserve the portable Linux static baseline and signing-free build.
- Reject a future compile-only regression through the static contract.

## Work Completed

- Added a shared `toothbrush` scheme containing the app and unit-test targets.
- Added `xcodebuild test` to `make test` when Xcode is available, using the
  Xcode 16.4 iPhone 16 Pro simulator and disabled code signing.
- Changed the macOS job from compile-only validation to XCTest execution.
- Extended project checks to require the scheme, testable target, simulator
  destination, test action, and hosted workflow command.
- Updated repository documentation to distinguish portable contracts from
  simulator-backed XCTest execution.

## Verification

- `python3 -m py_compile scripts/check-toothbrush-source.py`
- `make check` on Linux: portable contracts passed; Xcode steps skipped because
  `xcodebuild` is unavailable
- Shared scheme parsed as XML
- Mutations removing the test action, destination, testable target, or workflow
  command were rejected
- `git diff --check`
- Hosted Xcode 16.4 XCTest result: pending exact-head pull-request run

No signing credentials, network services, health data, or user data are used.
