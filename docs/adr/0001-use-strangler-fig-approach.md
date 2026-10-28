# Use Strangler Fig Approach

## Context and Problem Statement

We are doing a rewrite of a legacy faculty time table application. The app is still in use, but it is based on obsolete technology. There are no requirements on new features so far.


## Considered Options

* Big Bang Rewrite - complete rewrite of the application from scratch and deployment at the end
* Strangler Fig - incremental rewrite of the application by parts while the app is still in use


## Decision Outcome

Chosen option: Strangler Fig, because:

* It is a part of the thesis assingment.
* The application is usable during entire time, and rewritten parts are immediately deliverable.
* Even if the rewrite does not finish completely, the partial result is usable.
* Big Bang rewrites usually do not end with success: <https://neverrewrite.com/software-rewrite>.

### Consequences

Positive:

* New functionality can be delivered incrementally.
* Each migrated part can be tested and deployed independently.
* Risks are reduced because changes are made in smaller, isolated steps.

Negative:

* We need to build and maintain a facade that routes requests between the legacy and rewritten parts.
* The legacy and new systems must run in parallel for some time.
* The migration may take longer and require more infrastructure than a Big Bang rewrite.
* The legacy system cannot be decommissioned until all relevant parts have been migrated.
