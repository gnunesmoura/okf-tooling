---
type: Command
title: list
description: List concepts in an OKF bundle.
tags: [command, list]
---

# `list`

```text
mira-okf list docs [--type <type>] [--tag <tag>]
  [--offset <n>] [--limit <n>] [--profile {brief,normal,full}] [--json]
```

`--profile` defaults to `normal`. Results are sorted deterministically.
`--type` and `--tag` apply together; `--offset` and `--limit` window the result
using non-negative integers.

| Profile | Human output | JSON concept fields |
| --- | --- | --- |
| `brief` | `concept_id` and `title` | `concept_id`, `title` |
| `normal` | Existing relative path, type, and title output | `concept_id`, `title`, `type`, `description`, `relative_path` |
| `full` | Deterministic sorted `key: value` lines for every non-body field and frontmatter field | All concept fields except `body` |

List JSON includes `data.profile` with the active profile. List never emits
concept bodies.
