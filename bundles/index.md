# Tooling

Knowledge bundle for the local Python library and CLI `tooling`.

## Areas

- [PRDs](prds/) - Product requirements and product decisions for `tooling`.
- [Features](features/) - Guides for features supported by the CLI and library.
- [Architecture](architecture/) - Initial architecture decisions for the local `tooling` library and CLI.
- [References](references/) - Reference specifications used by the product and OKF module.

## SDD area roles

Use this map to choose the right source before editing or implementing a change:

| Area | SDD role and content character | Look here for |
| --- | --- | --- |
| Product documents | Stable, contextual product scope, principles, and roadmap direction | Overall intent and constraints |
| [PRDs](prds/) | Normative product intent and scope | Why the change exists and what it must achieve |
| [Features](features/) | Normative observable behavior and user-facing guidance | Expected behavior and use cases |
| [Architecture](architecture/) | Normative decisions and contracts, plus reusable technical guidance | Technical boundaries, invariants, and interfaces |
| [References](references/) | Normative external or local specifications | OKF rules and other governing references |
| `changes/` (when created) | Normative change-specific scope and execution state | Approved spec, plan, tasks, acceptance tests, agent contract, and status |
| `log.md` and area logs | Historical, chronological record | What changed and when; not current authority |

When sources disagree, use the applicable change package for the current
approved scope and record the discrepancy; do not resolve it silently.

## Authority and conflict resolution

Resolve questions in this order, from governing structure to observed
implementation:

1. The local OKF specification and repository policy govern bundle structure,
   contribution rules, and process constraints.
2. Product context and PRDs govern intent, scope, and desired outcomes.
3. Feature concepts govern observable behavior and user-facing expectations.
4. Architecture concepts govern technical boundaries, invariants, and
   contracts.
5. The current change package governs the approved scope and execution state
   for that change.
6. Source code and tests show implemented behavior and validation evidence.

This order does not authorize an agent to silently reinterpret a higher-level
artifact. If two sources conflict, record the conflict in the change package,
identify which source must be updated, and pause work that depends on the
decision. Source or test behavior that differs from the approved contract is
evidence of drift, not an implicit specification change.

## Change lifecycle and evidence

Future change packages use:

`draft -> specified -> planned -> ready -> in_progress -> implemented -> validated`

`deprecated` is reserved for a package or decision that no longer applies.
Advance a status only when the package records the corresponding evidence:

| Status | Required evidence before transition |
| --- | --- |
| `specified` | Approved outcome, scope, non-goals, dependencies, and observable acceptance criteria linked to the relevant product and feature context. |
| `planned` | A technical plan names affected architecture boundaries, contracts, source areas, tests, risks, and explicit decisions. |
| `ready` | Ordered tasks, acceptance tests, dependencies, agent constraints, and required completion evidence are actionable and reviewed. |
| `implemented` | The scoped source change is complete; tests exist or a justification is recorded, and task-level implementation evidence is reported. |
| `validated` | Acceptance checks and focused repository checks pass, and affected durable bundle knowledge, indexes, and logs are synchronized. |

`in_progress` means ready work has started; it is not evidence of completion.
An absent change package cannot be treated as a source of current change
status.

## SDD-007 relation audit (2026-07-09)

The matrix below records candidate cross-links that are absent from the
source document's `Relations` section or area navigation. A relation is
**confirmed** only when the source and target roles are supported by explicit
scope, dependency, or authority statements in the cited documents. **Uncertain**
rows are retained for human review and must not be applied by SDD-008 without
an explicit decision. Existing links were inspected but are not repeated here.

| Relation | Source path | Target path | Status | Evidence |
| --- | --- | --- | --- | --- |
| roadmap sequences health feature | `bundles/Tooling Roadmap.md` | `bundles/features/Feature - OKF Health.md` | Confirmed | `Feature Sequence` names `health` as completed, while `Relations` omits the health feature; the target defines that command. |
| roadmap baseline includes health PRD | `bundles/Tooling Roadmap.md` | `bundles/prds/PRD - OKF Health.md` | Confirmed | `Current Baseline` lists the health PRD, but the roadmap `Relations` section does not. |
| module context supports show | `bundles/prds/PRD - OKF Module.md` | `bundles/features/Feature - OKF Show.md` | Confirmed | The module defines `show` in MVP scope and the feature defines the canonical single-concept read path; the module relations stop before `show`. |
| module context supports links | `bundles/prds/PRD - OKF Module.md` | `bundles/features/Feature - OKF Links.md` | Confirmed | `Future Interfaces` lists `links`, and the feature defines that command on the module's shared read model; no feature link exists in the module relations. |
| module context supports backlinks | `bundles/prds/PRD - OKF Module.md` | `bundles/features/Feature - OKF Backlinks.md` | Confirmed | `Future Interfaces` lists `backlinks`, and the feature defines it as an OKF module command; no feature link exists in the module relations. |
| module context supports validation | `bundles/prds/PRD - OKF Module.md` | `bundles/features/Feature - OKF Validation.md` | Confirmed | `Future Interfaces` lists `validate`, and the feature defines the read-only validation command; no feature link exists in the module relations. |
| module context supports health | `bundles/prds/PRD - OKF Module.md` | `bundles/features/Feature - OKF Health.md` | Confirmed | `Future Interfaces` lists `health`, and the feature defines the profile-based health command; no feature link exists in the module relations. |
| backlinks reuses links PRD semantics | `bundles/features/Feature - OKF Backlinks.md` | `bundles/prds/PRD - OKF Links.md` | Confirmed | Backlinks scope explicitly reuses the same extraction and normalization rules as `links`; only the general product/module PRDs are listed. |
| backlinks uses semantic normalization boundary | `bundles/features/Feature - OKF Backlinks.md` | `bundles/prds/PRD - OKF Semantic Analysis Boundary.md` | Confirmed | Backlinks scope explicitly excludes fenced code and inline code, matching the boundary PRD's stated consumer set; the target is not listed. |
| health uses semantic normalization boundary | `bundles/features/Feature - OKF Health.md` | `bundles/prds/PRD - OKF Semantic Analysis Boundary.md` | Confirmed | Health scope explicitly ignores fenced code and inline code, and the boundary PRD names health as a consumer; the feature relations omit the target. |
| validation is governed by OKF specification | `bundles/features/Feature - OKF Validation.md` | `bundles/references/Open Knowledge Format Specification.md` | Confirmed | The feature's conformance scope covers reserved files and frontmatter rules, while its relations omit the normative reference that the validation PRD already cites. |
| health is governed by OKF specification | `bundles/features/Feature - OKF Health.md` | `bundles/references/Open Knowledge Format Specification.md` | Confirmed | The health PRD explicitly grounds its permissive model in the local OKF specification; the feature carries the same conformance behavior but omits the reference. |
| validation contract is governed by OKF specification | `bundles/architecture/Validation Report Contract.md` | `bundles/references/Open Knowledge Format Specification.md` | Confirmed | The contract explicitly invokes the local OKF specification for reserved-file and frontmatter rules, but its relations omit the reference. |
| health contract is governed by OKF specification | `bundles/architecture/Health Report Contract.md` | `bundles/references/Open Knowledge Format Specification.md` | Confirmed | The contract explicitly states that the OKF specification separates conformance from soft quality guidance, but its relations omit the reference. |
| roadmap context for semantic boundary | `bundles/Tooling Roadmap.md` | `bundles/prds/PRD - OKF Semantic Analysis Boundary.md` | Uncertain | The PRD and architecture boundary support active links, backlinks, and health work, but the roadmap's baseline and sequence do not name this cross-cutting PRD. Decide whether foundational PRDs belong in roadmap relations. |
| feature-to-reference links for links/backlinks | `bundles/features/Feature - OKF Links.md` and `bundles/features/Feature - OKF Backlinks.md` | `bundles/references/Open Knowledge Format Specification.md` | Uncertain | Both features implement OKF link behavior, but their bodies do not explicitly claim a specification rule; confirm whether the shared module/PRD reference is sufficient. |
| release roadmap relation to active health/validation concepts | `bundles/Going Open Source Roadmap.md` | `bundles/prds/PRD - OKF Health.md`, `bundles/prds/PRD - OKF Validation.md`, `bundles/features/Feature - OKF Health.md`, `bundles/features/Feature - OKF Validation.md` | Uncertain | The release roadmap links health and validation PRDs but not their feature concepts; decide whether release sequencing should mirror the product roadmap or remain a separate context layer. |
| roadmap relation to `props` concepts | `bundles/Tooling Roadmap.md` | no target concept exists | Unresolved | `props` is explicitly the next product feature, but no PRD or feature concept exists. Do not create one or add a speculative target during SDD-007; decide in a future roadmap/PRD task. |

### Human-review decisions

- Approve or reject the five confirmed module-to-feature links and the
  confirmed reference links before SDD-008 applies them.
- Decide whether the cross-cutting semantic-boundary PRD belongs in roadmap
  relations, and whether release-roadmap links should mirror product-roadmap
  feature coverage.
- Decide whether links and backlinks need a direct reference relation or may
  rely on their existing PRD/module references.
- Keep `props` as roadmap context only until a dedicated PRD and feature
  concept are intentionally created.

## Documents

- [Tooling Overview](Tooling%20Overview.md) - Scope, principles, and initial organization for `tooling`.
- [Tooling Roadmap](Tooling%20Roadmap.md) - Roadmap spine for the remaining OKF work in `tooling`.
- [Going Open Source Roadmap](Going%20Open%20Source%20Roadmap.md) - Product and project roadmap for public release and distribution.
- [PRD - Python Tooling Library and CLI](prds/PRD%20-%20Python%20Tooling%20Library%20and%20CLI.md) - Main product PRD for `tooling`.
- [Architecture Overview](architecture/Architecture%20Overview.md) - Initial architecture decisions for the local `tooling` library and CLI.
- [Open Knowledge Format Specification](references/Open%20Knowledge%20Format%20Specification.md) - Local copy of the OKF v0.1 draft specification.
