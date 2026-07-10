# Architecture

Initial architecture decisions for the local `tooling` library and CLI.

## Normative architecture

The decisions and contracts below are authoritative technical guidance for
the tooling library and CLI. Use them to understand the boundaries and
behaviors that implementations must preserve.

### Decisions

These documents record consequential architecture choices and their
boundaries.

- [Architecture Overview](architecture-overview.md) - Summary of the initial design and scope.
- [Discovery and Resolution](discovery-and-resolution.md) - Bundle discovery, ambiguity handling, and show target resolution.
- [OKF Boundaries](okf-boundaries.md) - Domain, CLI, parsing, discovery, and serialization boundaries.
- [Semantic Analysis Boundary](semantic-analysis-boundary.md) - Shared normalization boundary for semantic scanners over raw concept bodies.

### Contracts

These documents define normative data shapes, command behavior, and issue
semantics.

- [Data Contracts](data-contracts.md) - Core contracts for bundle, concept, directory, link, and issue records.
- [Output and Errors](output-and-errors.md) - Stable JSON envelope, human output rules, and issue semantics.
- [List Command Contract](list-command-contract.md) - Concept-only inventory rules, filters, and ordering for `list`.
- [List Result Windowing](list-result-windowing.md) - Windowed `list` payload shape, totals, and truncation semantics.
- [Links Command Contract](links-command-contract.md) - Outbound link extraction, classification, and output for `links`.
- [Validation Report Contract](validation-report-contract.md) - Read-only validation report payload, ordering, and pass/fail semantics.
- [Health Report Contract](health-report-contract.md) - Read-only health report payload and soft signal semantics.

## Guidance

These documents are non-normative implementation and delivery guidance. Use
them to plan flows, testing, and incremental work while treating the
normative decisions and contracts above as the authority for behavior.

- [Command Flows](command-flows.md) - Behavior of `tree`, `list`, `show`, and future interfaces.
- [Test Strategy](test-strategy.md) - Minimum fixtures and test boundaries for the MVP.
- [Incremental Plan and Risks](incremental-plan-and-risks.md) - Small-step implementation order and known risks.
