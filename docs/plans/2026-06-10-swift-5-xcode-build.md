# Swift 5 And Hosted Xcode Build

## Status: Completed

## Context

The toothbrush app still used Swift 2-era UIKit and Foundation APIs with an iOS
8.3 deployment target. Its hosted gate ran text contracts on Linux but never
compiled the project, so source and project-file drift could merge without an
Xcode signal.

## Objectives

- Restore compilation under a current, explicitly selected Xcode release.
- Preserve the two-minute timer, accessibility state, and navigation-logo
  lifecycle.
- Compile the app and XCTest target without signing credentials.
- Replace placeholder tests with meaningful offline assertions.

## Work Completed

- Migrated the application entry point, timer, run-loop, animation, visibility,
  image-rendering, geometry, and string/scanner APIs to Swift 5 syntax.
- Made timer ownership optional and clear the timer after invalidation.
- Raised the deployment target to iOS 12 and set explicit app/test bundle IDs.
- Removed the obsolete armv7-only device capability from the app plist.
- Completed the modern app icon catalog with iPad Pro and App Store sizes
  derived from the existing high-resolution toothbrush artwork.
- Replaced placeholder XCTest methods with valid and partial hex-color parser
  assertions.
- Changed `make build` to compile the app and XCTest target for the simulator
  with code signing disabled.
- Added a fixed macOS 15/Xcode 16.4 build job alongside the Ubuntu 24.04 static
  contract job, with concurrency cancellation and immutable action pins.
- Extended the static checker and documentation for the modern build contract.

## Verification

- `python3 -m py_compile scripts/check-toothbrush-source.py`
- `python3 scripts/check-toothbrush-source.py --mode project`
- `python3 scripts/check-toothbrush-source.py --mode timer`
- `python3 scripts/check-toothbrush-source.py --mode color`
- `python3 scripts/check-toothbrush-source.py --mode accessibility`
- `make check`
- `make -C /path/to/toothbrush-ios check`
- Mutation checks for legacy Swift/project settings, floating runners, and a
  missing macOS build job
- `xcodebuild -project toothbrush.xcodeproj -target toothbrushTests -sdk
  iphonesimulator -configuration Debug CODE_SIGNING_ALLOWED=NO build`
- `git diff --check`

The hosted Xcode job compiles XCTest sources but does not launch a simulator or
execute UI behavior. No Twilio, health, analytics, or network credentials are
required.
