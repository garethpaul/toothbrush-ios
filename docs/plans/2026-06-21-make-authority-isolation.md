# Make Authority Isolation

Status: Completed

## Goal

Keep portable and native Toothbrush verification authoritative when invoked
from another directory or with hostile Make variables, modes, shell overrides,
and executable paths. Startup files are parsed before repository checks can
reject them, so they are documented as caller-supplied Make programs outside the
local trust boundary.

## Changes

- Resolve and export the repository root from the checked-in Makefile alone.
- Freeze trusted Python and Xcode executable overrides as literal values and
  fix the recipe shell.
- Reject caller-supplied `MAKEFLAGS`, `MAKEFILES`, `MAKEFILE_LIST`, dry-run,
  touch, question, and ignore-error verification modes after GNU Make has parsed
  startup metadata.
- Use double-colon public targets so later recipe replacement attempts fail
  closed instead of replacing the checked-in validation recipes.
- Expand checked-in recipe command lines from reviewed root and tool values
  before later target-specific variables can alter them.
- Pin `/bin/sh -c` target-specifically for public aliases so later non-override
  shell variables cannot intercept secondary-expansion guards or recipes.
- Add a self-contained adversarial root harness across every public target and
  an executable workflow contract covering 17 unsafe mutations.
- Invoke both hosted gates through `/usr/bin/make`.

## Verification

- repository and external-directory `make check` passed
- 35 target/authority combinations passed with quoted and literal-dollar tool
  paths
- later recipe replacement attempts are rejected for all public aliases
- later target-specific root overrides cannot redirect checked-in recipes
- later non-override target-specific shell overrides cannot spoof validation
- 17 unsafe workflow mutations were rejected
- static project, timer, color, and accessibility contracts passed locally
- hosted static baseline and Xcode/XCTest gates are required on the exact PR
  and merge commits before final tracker completion

## Trust Boundary

GNU Make parses `MAKEFILES` and earlier `-f` files before this checked-in
Makefile can reject them. Those startup files are caller-supplied Make programs,
not sandboxed repository inputs. The repository contract is fail-closed after
that parse boundary and protection against later single-colon recipe replacement
of the checked-in public aliases. Caller-supplied later makefiles that use GNU
Make `override` directives remain caller programs outside the local trust
boundary.
