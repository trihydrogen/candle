# Use Markdown Architectural Decision Records

## Context and Problem Statement

We want to record architectural decisions made in this project independent whether decisions concern the architecture ("architectural decision record"), the code, or other fields.
Which format and structure should these records follow?

## Considered Options

* [MADR](https://adr.github.io/madr/) 4.0.0 – The Markdown Architectural Decision Records
* [Michael Nygard's template](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions) – The first incarnation of the term "ADR"
* [Sustainable Architectural Decisions](https://www.infoq.com/articles/sustainable-architectural-design-decisions) – The Y-Statements
* Other templates listed at <https://github.com/joelparkerhenderson/architecture_decision_record>
* Formless – No conventions for file format and structure

## Decision Outcome

Chosen option: "MADR 4.0.0", because

* MADR allows for structured capturing of any decision.
* The minimal version of MADR is easily understandable.
* Reading markdown requires no special software and ensures future compatibility.
