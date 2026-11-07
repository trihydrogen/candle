# Use syrupy for approval tests

## Context and Problem Statement

The migration needs approval-style characterization tests for structured responses (for example iCal export).
The test runner will be pytest, so the snapshot library should fit that workflow and work in CI.


## Considered Options

* [syrupy](https://github.com/syrupy-project/syrupy) - pytest-native snapshots
* [ApprovalTests.Python](https://github.com/approvals/ApprovalTests.Python) - classic approval tests with scrubbers and reporters
* Hand-written assertions against committed fixture files


## Decision Outcome

Chosen option: syrupy, because:

* It integrates directly with pytest (`assert value == snapshot`, `--snapshot-update`).
* That is enough for normalized structured payloads; we do not plan full-page HTML snapshots.
* ApprovalTests adds more ceremony without clear benefit for this use case.
* It has funny name :)

### Consequences

Positive:

* Simple approve/update workflow that works in CI with committed snapshots.
* Fits the planned Django/pytest stack.

Negative:

* Volatile fields must be normalized before assertion; syrupy’s scrubbing is limited compared to ApprovalTests.
