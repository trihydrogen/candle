# Use pytest-docker for characterization tests

## Context and Problem Statement

Characterization tests exercise the real stack through the Caddy gateway.
They need an isolated Compose project so a long-running dev database with
exploratory data is not wiped or asserted against.


## Considered Options

* Shared long-running Compose for both development and tests
* Isolated test Compose project started by a shell script, pytest on the host
* Isolated test Compose project managed by [pytest-docker](https://pypi.org/project/pytest-docker/), pytest on the host
* Pytest running inside a Compose `test` service


## Decision Outcome

Chosen option: isolated test Compose project + pytest-docker + host pytest, because:

* The dev stack stays independent of tests.
* `uv run pytest tests/` brings up required Compose services automatically.
* Running pytest locally is simpler and somwhat faster.
* Can move to containerized pytest in future (if needed).

`compose.test.yaml` overrides test-only concerns (gateway port, MySQL test volume, fixtures mount).
Profiles may later toggle optional services; they do not replace the override file.

### Consequences

Positive:

* Tests run independently of the developer stack.
* Local and CI can share the same pytest entrypoint.

Negative:

* First characterization run pays the cost of booting the whole Compose plus import of fixtures.
