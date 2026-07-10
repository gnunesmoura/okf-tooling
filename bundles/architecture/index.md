# Architecture

Initial architecture decisions for the local `tooling` library and CLI.

## Normative architecture

The decisions and contracts below are authoritative technical guidance for
the tooling library and CLI. Use them to understand the boundaries and
behaviors that implementations must preserve.

### Decisions

These documents record consequential architecture choices and their
boundaries.

- [Architecture Overview](Architecture%20Overview.md) - Summary of the initial design and scope.
- [Discovery and Resolution](Discovery%20and%20Resolution.md) - Bundle discovery, ambiguity handling, and show target resolution.
- [OKF Boundaries](OKF%20Boundaries.md) - Domain, CLI, parsing, discovery, and serialization boundaries.
- [Semantic Analysis Boundary](Semantic%20Analysis%20Boundary.md) - Shared normalization boundary for semantic scanners over raw concept bodies.

### Contracts

These documents define normative data shapes, command behavior, and issue
semantics.

- [Data Contracts](Data%20Contracts.md) - Core contracts for bundle, concept, directory, link, and issue records.
- [Output and Errors](Output%20and%20Errors.md) - Stable JSON envelope, human output rules, and issue semantics.
- [List Command Contract](List%20Command%20Contract.md) - Concept-only inventory rules, filters, and ordering for `list`.
- [List Result Windowing](List%20Result%20Windowing.md) - Windowed `list` payload shape, totals, and truncation semantics.
- [Links Command Contract](Links%20Command%20Contract.md) - Outbound link extraction, classification, and output for `links`.
- [Validation Report Contract](Validation%20Report%20Contract.md) - Read-only validation report payload, ordering, and pass/fail semantics.
- [Health Report Contract](Health%20Report%20Contract.md) - Read-only health report payload and soft signal semantics.

## Guidance

These documents are non-normative implementation and delivery guidance. Use
them to plan flows, testing, and incremental work while treating the
normative decisions and contracts above as the authority for behavior.

- [Command Flows](Command%20Flows.md) - Behavior of `tree`, `list`, `show`, and future interfaces.
- [Test Strategy](Test%20Strategy.md) - Minimum fixtures and test boundaries for the MVP.
- [Incremental Plan and Risks](Incremental%20Plan%20and%20Risks.md) - Small-step implementation order and known risks.
