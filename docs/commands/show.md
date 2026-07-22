---
type: Command
title: show
description: Read one OKF concept.
tags: [command, show]
---

# `show`

```text
mira-okf show docs <concept-id-or-path>
  [--profile {brief,normal,full}] [--summary] [--json]
```

Resolve a concept by id or bundle-relative Markdown path. `--profile` defaults
to `normal`. `--summary` is an alias for `--profile brief`; if both are
supplied, `--summary` wins and the active profile is `brief`.

| Profile | Human output | JSON concept fields |
| --- | --- | --- |
| `brief` | Path, type, title, description, and tags; no body | `concept_id`, `title`, `description`, `type`, `tags`, `relative_path` |
| `normal` | Existing output, including body and the `Issues` section | Current fields, including body and frontmatter |
| `full` | Existing output, including body and issues, plus a sorted `Frontmatter` `key: value` section | Current fields, including body and frontmatter |

Show JSON includes `data.profile` with the active profile. Tolerated issues
remain visible in the existing `Issues` section where applicable. The deferred
`raw_frontmatter` field is not part of this contract.
