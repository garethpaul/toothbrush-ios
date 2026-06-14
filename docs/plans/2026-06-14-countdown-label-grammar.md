# Countdown Label Grammar

## Status: Completed

## Context

The countdown label always appends `seconds`, so the final running value is
shown and announced as `1 seconds`. Visible and accessibility text already
share one update path, making this a narrow formatting correction with direct
XCTest coverage.

## Priority

Render grammatically correct singular and plural countdown labels without
changing deadline arithmetic, timer lifecycle behavior, or reset semantics.

## Requirements

- Return `1 second` for a one-second value.
- Return plural labels for zero and values greater than one.
- Route visible and accessibility label updates through the same formatter.
- Preserve the continuous clock, countdown state boundaries, shared reset
  path, weak timer ownership, and iOS 12 deployment floor.
- Add mutation-sensitive XCTest and static contracts plus maintained project
  documentation.

## Verification

- Focused label-formatting XCTest contracts and the full static suite
- Repository and external-directory `make check`
- Mutations covering singular handling, plural handling, controller use,
  accessibility synchronization, documentation, and plan status
- Generated-artifact, credential-pattern, exact-diff, staged-path, and
  whitespace audits

## Verification Results

- The focused timer and accessibility contracts passed with singular, zero,
  and larger plural XCTest assertions present in the shared test target.
- Repository and external-directory `make check` passed project, timer, color,
  accessibility, and static XCTest contracts.
- Six hostile label mutations were rejected across singular selection, plural
  selection, controller integration, accessibility synchronization,
  maintained documentation, and completed-plan evidence.
- Native XCTest remains assigned to the hosted Xcode 16.4 simulator because
  `xcodebuild` is unavailable on the Linux workstation.

## Scope Boundary

This change does not alter the two-minute duration, countdown rounding,
completion presentation, timer scheduling, lifecycle reconciliation, or
localization architecture.
