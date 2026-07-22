from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests.support import run_main


class TreeCommandTest(unittest.TestCase):
    def test_tree_json_normalizes_root_and_nested_index_titles(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "bundle"
            (root / "nested").mkdir(parents=True)
            (root / "index.md").write_text("paragraph\n#  Root Title  #\n# later\n", encoding="utf-8")
            (root / "nested" / "index.md").write_text("## not h1\n   # Nested Title\n", encoding="utf-8")

            payload = json.loads(run_main(["tree", str(root), "--depth", "1", "--json"])[1])
            directory = payload["data"]
            self.assertEqual(directory["index_title"], "Root Title")
            self.assertEqual(directory["children"][0]["index_title"], "Nested Title")

    def test_tree_json_uses_null_for_missing_or_titleless_indexes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "bundle"
            (root / "no-index").mkdir(parents=True)
            (root / "titleless").mkdir(parents=True)
            (root / "index.md").write_text("no heading\n", encoding="utf-8")
            (root / "titleless" / "index.md").write_text("## Only H2\n", encoding="utf-8")

            for profile in ("brief", "normal", "full"):
                payload = json.loads(run_main(["tree", str(root), "--depth", "1", "--profile", profile, "--json"])[1])
                titles = {child["path"]: child["index_title"] for child in payload["data"]["children"]}
                self.assertIsNone(payload["data"]["index_title"])
                self.assertIsNone(titles["no-index"])
                self.assertIsNone(titles["titleless"])

    def test_tree_json_index_title_is_present_and_deterministic_for_each_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "bundle"
            root.mkdir()
            (root / "index.md").write_text("# Stable\n", encoding="utf-8")
            for profile in ("brief", "normal", "full"):
                first = run_main(["tree", str(root), "--profile", profile, "--json"])[1]
                second = run_main(["tree", str(root), "--profile", profile, "--json"])[1]
                self.assertEqual(first, second)
                self.assertEqual(json.loads(first)["data"]["index_title"], "Stable")

    def test_tree_profiles_control_human_detail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "bundle"
            (root / "index.md").parent.mkdir(parents=True)
            (root / "index.md").write_text("index\n", encoding="utf-8")
            (root / "alpha.md").write_text("---\ntype: Note\n---\n", encoding="utf-8")

            plain_exit, plain_stdout, plain_stderr = run_main(["tree", str(root), "--depth", "0"])
            summary_exit, summary_stdout, summary_stderr = run_main(["tree", str(root), "--depth", "0", "--summary"])

            self.assertEqual((plain_exit, plain_stderr), (0, ""))
            self.assertEqual((summary_exit, summary_stderr), (0, ""))
            self.assertEqual(plain_stdout.splitlines()[0], f"{root}/")
            self.assertNotIn("concepts:", plain_stdout)
            self.assertNotIn("reserved:", plain_stdout)
            self.assertEqual(summary_stdout, run_main(["tree", str(root), "--depth", "0", "--profile", "brief"])[1])
            self.assertIn("Alpha", summary_stdout)
            self.assertNotIn("concepts:", summary_stdout)

    def test_tree_human_profiles_render_index_and_concepts_separately(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "bundle"
            (root / "products").mkdir(parents=True)
            (root / "index.md").write_text("# OKF Tooling Knowledge Base\n", encoding="utf-8")
            (root / "products" / "index.md").write_text("# Products\n", encoding="utf-8")
            (root / "alpha.md").write_text(
                "---\ntype: Note\ntitle: Alpha\ndescription: First note\ntags: [one, two]\n---\nbody\n",
                encoding="utf-8",
            )
            (root / "products" / "beta.md").write_text("---\ntype: Guide\ntitle: Beta\n---\n", encoding="utf-8")

            brief = run_main(["tree", str(root), "--depth", "1", "--profile", "brief"])[1]
            normal = run_main(["tree", str(root), "--depth", "1", "--profile", "normal"])[1]
            full = run_main(["tree", str(root), "--depth", "1", "--profile", "full"])[1]

            self.assertIn(f"{root}/index  OKF Tooling Knowledge Base", brief)
            self.assertIn("  Alpha\n", brief)
            self.assertIn("  products/index  Products", brief)
            self.assertNotIn("Alpha  ", brief)
            self.assertIn("  alpha  Note  Alpha  First note", normal)
            self.assertIn("    products/beta  Guide  Beta", normal)
            self.assertIn("  alpha  Note  Alpha  First note\n    description: First note", full)
            self.assertIn("    tags: ['one', 'two']", full)
            self.assertEqual(full, run_main(["tree", str(root), "--depth", "1", "--profile", "full"])[1])

    def test_tree_human_index_without_title_keeps_path_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "bundle"
            (root / "empty").mkdir(parents=True)
            (root / "index.md").write_text("no heading\n", encoding="utf-8")
            (root / "empty" / "index.md").write_text("## Not H1\n", encoding="utf-8")
            output = run_main(["tree", str(root), "--depth", "1", "--profile", "brief"])[1]
            self.assertIn(f"{root}/\n", output)
            self.assertIn("  empty/\n", output)
            self.assertNotIn("index  ", output)

    def test_tree_profiles_filter_json_concepts_without_body(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "bundle"
            (root / "area").mkdir(parents=True)
            write = {
                "index.md": "index\n",
                "log.md": "log\n",
                "root.md": "---\ntype: Note\n---\n",
                "area/index.md": "index\n",
                "area/concept.md": "---\ntype: Note\n---\n",
            }
            for relative_path, content in write.items():
                path = root / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

            arguments = ["tree", str(root), "--depth", "1"]
            exit_code, plain_stdout, plain_stderr = run_main(arguments)
            self.assertEqual((exit_code, plain_stderr), (0, ""))
            exit_code, summary_stdout, summary_stderr = run_main([*arguments, "--summary"])
            self.assertEqual((exit_code, summary_stderr), (0, ""))
            self.assertEqual(summary_stdout, run_main([*arguments, "--summary"])[1])
            self.assertIn("Concept", summary_stdout)
            self.assertNotIn("area/concept.md", plain_stdout)

            exit_code, plain_json, plain_stderr = run_main([*arguments, "--json"])
            self.assertEqual((exit_code, plain_stderr), (0, ""))
            exit_code, summary_json, summary_stderr = run_main([*arguments, "--summary", "--json"])
            self.assertEqual((exit_code, summary_stderr), (0, ""))
            self.assertEqual(json.loads(summary_json)["data"]["profile"], "brief")
            self.assertEqual(json.loads(plain_json)["data"]["profile"], "normal")
            for profile, expected in (("brief", {"concept_id", "title"}), ("normal", {"concept_id", "title", "type", "description"})):
                payload = json.loads(run_main([*arguments, "--profile", profile, "--json"])[1])
                concept = payload["data"]["concepts"][0]
                self.assertEqual(set(concept), expected)
                self.assertNotIn("body", concept)

            full = json.loads(run_main([*arguments, "--profile", "full", "--json"])[1])
            self.assertEqual(full["data"]["profile"], "full")
            self.assertNotIn("body", full["data"]["concepts"][0])

    def test_tree_discovers_bundle_from_current_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "index.md").write_text("index\n", encoding="utf-8")
            (root / "alpha.md").write_text("---\ntype: Note\ntitle: Alpha\n---\nbody\n", encoding="utf-8")
            exit_code, stdout, stderr = run_main(["tree", "--profile", "brief"], cwd=root)
            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            output = stdout.strip().splitlines()
            self.assertIn("./", output[0])
            self.assertIn("Alpha", output[1])

    def test_tree_discovers_nested_bundle_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            nested = root / "workspace" / "bundle"
            nested.mkdir(parents=True)
            (nested / "index.md").write_text("index\n", encoding="utf-8")
            (nested / "alpha.md").write_text("---\ntype: Note\n---\n", encoding="utf-8")
            exit_code, stdout, stderr = run_main(["tree", "--summary"], cwd=root)
            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertIn("workspace/bundle/", stdout)

    def test_tree_reports_ambiguous_discovery(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "artifacts").mkdir()
            (root / "tooling" / "bundles").mkdir(parents=True)
            for bundle_root in (root / "artifacts", root / "tooling" / "bundles"):
                (bundle_root / "index.md").write_text("index\n", encoding="utf-8")
                (bundle_root / "alpha.md").write_text("---\ntype: Note\n---\n", encoding="utf-8")
            exit_code, stdout, stderr = run_main(["tree", "--depth", "2", "--summary"], cwd=root)
            self.assertEqual(exit_code, 1)
            self.assertEqual(stdout, "")
            self.assertIn("More than one OKF bundle found", stderr)
            self.assertIn("artifacts -> mira-okf tree artifacts --depth 2 --summary", stderr)
            self.assertIn("tooling/bundles -> mira-okf tree tooling/bundles --depth 2 --summary", stderr)

    def test_tree_respects_depth_and_absolute_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "bundle"
            (root / "area" / "deep").mkdir(parents=True)
            (root / "index.md").write_text("index\n", encoding="utf-8")
            (root / "root.md").write_text("---\ntype: Note\n---\n", encoding="utf-8")
            (root / "area" / "index.md").write_text("index\n", encoding="utf-8")
            (root / "area" / "leaf.md").write_text("---\ntype: Note\n---\n", encoding="utf-8")
            (root / "area" / "deep" / "leaf.md").write_text("---\ntype: Note\n---\n", encoding="utf-8")
            exit_code, stdout, stderr = run_main(["tree", str(root), "--depth", "1", "--summary"])
            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            output = stdout
            self.assertIn("bundle/", output)
            self.assertIn("area/", output)
            self.assertNotIn("deep/", output)

            exit_code, stdout, stderr = run_main(["tree", str(root.resolve()), "--depth", "2", "--summary"])
            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertIn("deep/", stdout)

    def test_tree_emits_stable_json_with_tolerated_issues(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "bundle"
            root.mkdir()
            (root / "index.md").write_text("index\n", encoding="utf-8")
            (root / "broken.md").write_text("---\ntitle: Broken\n---\n", encoding="utf-8")
            exit_code, stdout, stderr = run_main(["tree", str(root), "--depth", "2", "--profile", "normal", "--json"])
            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["command"], "okf.tree")
            self.assertEqual(payload["bundle"]["source_kind"], "explicit")
            self.assertEqual(payload["data"]["profile"], "normal")
            self.assertEqual(payload["data"]["concept_count"], 1)
            self.assertNotIn("body", payload["data"]["concepts"][0])
            self.assertEqual(payload["issues"][0]["code"], "OKF_CONCEPT_MISSING_TYPE")


if __name__ == "__main__":
    unittest.main()
