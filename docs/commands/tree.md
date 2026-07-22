---
type: Command
title: tree
description: Summarize an OKF bundle tree.
tags: [command, tree]
---

# `tree`

```text
mira-okf tree docs --depth <n> [--profile {brief,normal,full}] [--summary] [--json]
```

`--depth` defaults to `2`; `--profile` defaults to `normal`. `--summary` is an
alias for `--profile brief`. If both options are supplied, `--summary` wins and
the active profile is `brief`.

| Profile | Human output | JSON concept fields |
| --- | --- | --- |
| `brief` | `<path>index  <index_title>` when available, then one indented title-only line per concept | `concept_id`, `title` |
| `normal` | The directory line, then one indented `concept_id  type  title  description` line per concept; description is optional | `concept_id`, `title`, `type`, `description` |
| `full` | The normal concept line plus sorted `key: value` frontmatter lines indented beneath it | All concept fields except `body` |

Tree JSON includes `data.profile` with the active profile. Directory structure
metadata, including nullable `index_title`, remains in the directory objects.
Directories without a usable index title retain only their path line. Tree
never emits concept bodies. Directory and concept ordering is deterministic.
