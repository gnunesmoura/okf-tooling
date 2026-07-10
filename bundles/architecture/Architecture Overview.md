---
type: ArchitectureDecision
title: Architecture Overview
description: Summarizes the initial architecture for the local tooling library and OKF CLI.
tags:
  - tooling
  - architecture
  - okf
---

# Architecture Overview

## Context

This is the authoritative high-level architecture direction for the local, read-only OKF navigation MVP. Detailed command behavior and data shapes belong in the related contracts.

## Decision

`tooling` should start as a small, stdlib-first Python CLI with one domain package for OKF.

The MVP is a read-only navigation layer:

- discover a bundle;
- parse OKF concepts permissively;
- inventory directories and reserved files;
- render `tree`, `list`, and `show`;
- keep human and JSON output stable;
- surface non-fatal problems as issues instead of blocking reads.

The OKF module should stay isolated enough to extract later, but the initial code should not optimize for extraction ahead of usability.

- Use a thin CLI that delegates all bundle logic to library services.
- Keep bundle resolution, OKF read-model construction, serialization, and presentation separate from domain models.
- Preserve unknown frontmatter keys.
- Treat broken links, unknown types, missing optional fields, and extra frontmatter fields as tolerated issues.
- Use one consistent machine-readable error envelope for CLI and automation.
- Make discovery and `show` resolution deterministic before adding future interfaces.
- Normalize bundle-relative identity once and reuse it across `tree`, `list`, and `show`.
- Leave `links`, `backlinks`, `props`, `health`, and `validate` as explicit future seams.

## Alternatives Considered

A larger service-oriented architecture or an extraction-first library was rejected for the MVP because it would add operational and structural complexity before the local reader workflow is proven.

## Consequences

The architecture keeps parsing and read-model behavior reusable across commands while leaving future interfaces as bounded seams rather than implementing them in the MVP.

## Relations

- [OKF Boundaries](OKF%20Boundaries.md)
- [Discovery and Resolution](Discovery%20and%20Resolution.md)
- [Data Contracts](Data%20Contracts.md)
- [Command Flows](Command%20Flows.md)
