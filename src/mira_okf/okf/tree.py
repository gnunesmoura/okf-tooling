from __future__ import annotations

import json
import sys
from argparse import Namespace
from typing import Any

from .read_model import bundle_payload, directory_payload, issue_payload, scan_bundle
from .resolution import BundleResolutionError, resolve_bundle


def run_tree(args: Namespace) -> int:
    profile = getattr(args, "profile", "normal")
    try:
        reference_suffix = f"--depth {getattr(args, 'depth', 2)} --summary"
        bundle = resolve_bundle(args.bundle, "tree", reference_suffix)
        bundle, root_directory = scan_bundle(bundle, args.depth)
    except BundleResolutionError as error:
        return _emit_error(args, error)

    payload = {
        "ok": True,
        "command": "okf.tree",
        "bundle": bundle_payload(bundle),
        "data": directory_payload(root_directory),
        "issues": [issue_payload(issue) for issue in bundle.issues],
    }
    payload["data"]["profile"] = profile
    _filter_tree_directory(payload["data"], profile)
    _emit_payload(args, payload)
    return 0


def _emit_error(args: Namespace, error: BundleResolutionError) -> int:
    payload = {
        "ok": False,
        "command": "okf.tree",
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
    print(_render_directory_summary(payload["data"], getattr(args, "profile", "normal")))


def _render_directory_summary(directory: dict[str, Any], profile: str) -> str:
    return _render_directory(directory, 0, profile)


def _render_directory(directory: dict[str, Any], indent: int, profile: str) -> str:
    label = directory["path"] if indent == 0 else directory["name"]
    path = f"{label or directory['name']}/"
    if directory.get("index_title"):
        path += f"index  {directory['index_title']}"
    lines = [f"{'  ' * indent}{path}"]
    for concept in directory["concepts"]:
        concept_line = f"{'  ' * (indent + 1)}{_render_concept(concept, profile)}"
        lines.append(concept_line)
        if profile == "full":
            lines.extend(
                f"{'  ' * (indent + 2)}{key}: {concept['frontmatter'][key]}"
                for key in sorted(concept.get("frontmatter", {}))
            )
    for child in directory["children"]:
        lines.append(_render_directory(child, indent + 1, profile))
    return "\n".join(lines)


def _render_concept(concept: dict[str, Any], profile: str) -> str:
    if profile == "brief":
        return concept["title"]
    fields = [concept["concept_id"], concept.get("type") or "", concept["title"]]
    if concept.get("description"):
        fields.append(concept["description"])
    return "  ".join(fields)


def _filter_tree_concept(c: dict, profile: str) -> dict:
    if profile == "brief":
        fields = ("concept_id", "title")
    elif profile == "normal":
        fields = ("concept_id", "title", "type", "description")
    else:
        fields = tuple(key for key in c if key != "body")
    return {key: c[key] for key in fields if key in c}


def _filter_tree_directory(directory: dict[str, Any], profile: str) -> None:
    directory["concepts"] = [_filter_tree_concept(concept, profile) for concept in directory["concepts"]]
    for child in directory["children"]:
        _filter_tree_directory(child, profile)
