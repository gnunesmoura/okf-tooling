---
type: Agent Workflow Contract
title: CHANGE-001 props agent contract
description: Constrains agents implementing and validating the props export pilot.
tags: [sdd, change, props, contract]
status: draft
---

# Authority and Constraints

## Related Product and Architecture Context

- [Tooling Product](/product/product-overview.md)
- [Summarized OKF Navigation](/product/features/summarized-okf-navigation.md)
- [Data Contracts](/architecture/data-contracts.md)
- [Output and Errors](/architecture/output-and-errors.md)
- [Command Flows](/architecture/command-flows.md)

## Affected Source Paths

- `/src/tooling/okf/read_model.py`
- `/src/tooling/okf/models.py`
- `/src/tooling/okf/commands.py`
- `/src/tooling/cli.py`
- `/tests/test_list.py`
- `/tests/test_show.py`
- `/tests/test_cli_bootstrap.py`
- `/tests/support.py`

## Citations

- [Open Knowledge Format Specification](/references/open-knowledge-format-specification.md)
- [Tooling Roadmap](/tooling-roadmap.md)
- [Going Open Source Roadmap](/going-open-source-roadmap.md)

Follow repository policy and the [OKF specification](../../../references/open-knowledge-format-specification.md) first, then product intent in the
[spec](spec.md), technical boundaries in the [plan](plan.md), and implemented
behavior in source and tests. Record conflicts; do not silently redefine an
existing contract.

## Allowed Work

- Implement only CHANGE-001's read-only projection and its tests.
- Use the existing resolver, read model, issue semantics, and output envelope.
- Modify only the planned source/test areas unless a directly required narrow
  dependency is documented in the plan.

## Invariants

- Never write or mutate bundle files or frontmatter.
- Support only `type`, `title`, `description`, and `tags`.
- Reject explicitly selected unknown fields.
- Keep rows sorted by `concept_id`, selected fields in request order, and tags
  in source order.
- Preserve readable concepts and tolerated issues under mixed frontmatter.
- Do not create a props PRD, feature, schema, release work, or speculative
  package artifact.

## Validation and Closeout Evidence

Run the focused and full unittest commands in [acceptance tests](acceptance-tests.md), inspect exact
outputs for all acceptance checks, run available structural/link checks, and
run `git diff --check`. Closeout must identify changed source/test files,
commands and results, edge-case evidence, and any unresolved risk. A status
change to `implemented` or `validated` requires actual implementation or
passing acceptance evidence respectively; this draft package claims neither.
