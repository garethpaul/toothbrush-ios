# Countdown Label Grammar

## Status: Planned

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

## Scope Boundary

This change does not alter the two-minute duration, countdown rounding,
completion presentation, timer scheduling, lifecycle reconciliation, or
localization architecture.
