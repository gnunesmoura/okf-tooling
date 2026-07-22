from __future__ import annotations

import json
import sys
from argparse import Namespace
from typing import Any

from .read_model import bundle_payload, concept_payload, issue_payload, scan_bundle
from .resolution import BundleResolutionError, resolve_bundle


def run_list(args: Namespace) -> int:
    try:
        bundle = resolve_bundle(args.bundle, "list")
        bundle, _ = scan_bundle(bundle, None)
    except BundleResolutionError as error:
        return _emit_error(args, error)

    concepts = _filtered_concepts(bundle.concepts, getattr(args, "type", None), getattr(args, "tag", None))
    offset = max(0, getattr(args, "offset", 0))
    limit = getattr(args, "limit", None)
    window = concepts[offset:] if limit is None else concepts[offset : offset + max(0, limit)]
    profile = getattr(args, "profile", "normal")
    payload = {
        "ok": True,
        "command": "okf.list",
        "bundle": bundle_payload(bundle),
        "data": {
            "concepts": [_filter_list_concept(concept_payload(concept), profile) for concept in window],
            "total": len(concepts),
            "returned": len(window),
            "offset": offset,
            "limit": limit,
            "truncated": len(window) < len(concepts),
            "profile": profile,
        },
        "issues": [issue_payload(issue) for issue in bundle.issues],
    }
    _emit_payload(args, payload)
    return 0


def _filtered_concepts(concepts, concept_type, tag):
    return [
        concept
        for concept in concepts
        if (concept_type is None or concept.type == concept_type) and (tag is None or tag in concept.tags)
    ]


def _filter_list_concept(c: dict, profile: str) -> dict:
    if profile == "brief":
        return {key: c[key] for key in ("concept_id", "title")}
    if profile == "normal":
        return {key: c[key] for key in ("concept_id", "title", "type", "description", "relative_path")}
    return {key: value for key, value in c.items() if key != "body"}


def _render_list_summary(data: dict[str, Any]) -> str:
    summary = f"concepts: {data['returned']} of {data['total']}"
    if data["offset"] or data["limit"] is not None:
        window_bits = [f"offset {data['offset']}"]
        if data["limit"] is not None:
            window_bits.append(f"limit {data['limit']}")
        summary += f" ({', '.join(window_bits)})"
    if data["truncated"]:
        summary += " [truncated]"
    lines = [summary]
    for concept in data["concepts"]:
        if data.get("profile") == "brief":
            lines.append(f"{concept['concept_id']}  {concept['title']}".rstrip())
        elif data.get("profile") == "full":
            lines.extend(f"  {key}: {concept[key]}" for key in sorted(concept))
            lines.extend(f"  {key}: {concept['frontmatter'][key]}" for key in sorted(concept["frontmatter"]))
        else:
            line = concept["relative_path"]
            if concept["type"]:
                line += f"  [{concept['type']}]"
            if concept["title"]:
                line += f"  {concept['title']}"
            lines.append(line)
    return "\n".join(lines)


def _emit_error(args: Namespace, error: BundleResolutionError) -> int:
    payload = {
        "ok": False,
        "command": "okf.list",
        "bundle": None,
        "data": None,
        "issues": [],
        "error": {
            "code": error.code,
            "message": error.message,
            "details": error.details,
        },
    }
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(error.message, file=sys.stderr)
        for candidate in error.details.get("candidates", []):
            print(f"- {candidate['path']} -> {candidate['command']}", file=sys.stderr)
    return 1


def _emit_payload(args: Namespace, payload: dict[str, Any]) -> None:
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
        return
    print(_render_list_summary(payload["data"]))
