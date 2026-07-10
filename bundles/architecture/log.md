# Architecture Log

## 2026-07-09

- **Creation**: Added the [Semantic Analysis Boundary](semantic-analysis-boundary.md) decision for the shared raw-body normalization boundary used by semantic scanners and kept separate from `show`.

## 2026-07-06

- **Creation**: Added the [Health Report Contract](health-report-contract.md) decision for `health` payload shape, local quality signals, and non-fatal soft signal semantics.

## 2026-07-05

- **Update**: Expanded the [Validation Report Contract](validation-report-contract.md) with reserved `index.md` and `log.md` conformance rules from the local OKF specification.
- **Creation**: Added the [Validation Report Contract](validation-report-contract.md) decision for `validate` summary payload, issue ordering, and process failure semantics.

## 2026-07-04

- **Update**: Audited the architecture bundle against the OKF spec and confirmed the link-contract references stay aligned with the feature docs.
- **Creation**: Added the [Links Command Contract](links-command-contract.md) decision for outbound link extraction, classification, and output.
- **Creation**: Added the [List Command Contract](list-command-contract.md) decision for concept-only inventory, deterministic filtering, and ordering.
- **Creation**: Added the initial architecture bundle for `tooling` with decisions, boundaries, contracts, command flows, test strategy, and implementation notes.
