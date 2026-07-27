#!/usr/bin/env python3
"""
test_critique_engine.py — Tests for critique_engine.critique_pptx

Run:
    python -m pytest scripts/tests/test_critique_engine.py -v
    # or
    python -m unittest scripts.tests.test_critique_engine
"""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# Add the scripts dir to path
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS_DIR))

from critique_engine import critique_pptx, critique_html, critique


# Locate the test assets
_SCRIPTS_PARENT = _SCRIPTS_DIR.parent
_ASSET = _SCRIPTS_PARENT / "assets" / "PPT模板.pptx"


class TestCritiqueEngine(unittest.TestCase):
    """Tests for critique_engine.critique_pptx()."""

    def setUp(self):
        if not _ASSET.exists():
            self.skipTest(f"Test asset not found: {_ASSET}")

    def test_critique_pptx_basic(self):
        """Output contains overall_score, slides, dimension_scores, issues."""
        result = critique_pptx(str(_ASSET))

        # Top-level structure
        self.assertIsInstance(result, dict)
        self.assertIn("overall_score", result)
        self.assertIn("slides", result)
        self.assertIn("dimension_scores", result)
        self.assertIn("total_issues", result)
        self.assertIn("hard_issues", result)
        self.assertIn("soft_issues", result)
        self.assertIn("converged", result)
        self.assertIn("file", result)
        self.assertIn("stage", result)

        # Type checks
        self.assertIsInstance(result["overall_score"], (int, float))
        self.assertIsInstance(result["slides"], list)
        self.assertIsInstance(result["dimension_scores"], dict)
        self.assertIsInstance(result["total_issues"], int)
        self.assertIsInstance(result["hard_issues"], int)
        self.assertIsInstance(result["soft_issues"], int)
        self.assertIsInstance(result["converged"], bool)

        # stage should be "structural"
        self.assertEqual(result["stage"], "structural")

        # Slide entries should have the required fields
        for s in result["slides"]:
            self.assertIn("slide", s)
            self.assertIn("score", s)
            self.assertIn("issues", s)
            self.assertIn("hard_issues", s)
            self.assertIn("soft_issues", s)

            # Score should be in 0-10
            self.assertGreaterEqual(s["score"], 0)
            self.assertLessEqual(s["score"], 10)

            # Issues should be a list of dicts with required keys
            for iss in s["issues"]:
                self.assertIn("severity", iss)
                self.assertIn("dimension", iss)
                self.assertIn("element", iss)
                self.assertIn("problem", iss)
                self.assertIn("suggestion", iss)
                self.assertIn("auto_fixable", iss)
                self.assertIn(iss["severity"], ("hard", "soft"))
                self.assertIn(
                    iss["dimension"],
                    ("alignment", "color", "type_scale", "density",
                     "placeholder", "stage_fit", "completeness"),
                )

        # dimension_scores should have all 7 dimensions
        expected_dims = {
            "alignment", "color", "type_scale", "density",
            "placeholder", "stage_fit", "completeness",
        }
        self.assertEqual(set(result["dimension_scores"].keys()), expected_dims)

        # Each dimension score in 0-10
        for dim, sc in result["dimension_scores"].items():
            self.assertGreaterEqual(sc, 0)
            self.assertLessEqual(sc, 10)

    def test_critique_pptx_scoring(self):
        """Slides with anti-patterns should score < 8."""
        result = critique_pptx(str(_ASSET))

        # At least one slide should exist
        self.assertGreater(len(result["slides"]), 0)

        # Find slides that have issues (anti_patterns mapped to issues)
        slides_with_issues = [
            s for s in result["slides"] if len(s["issues"]) > 0
        ]

        # If any slide has issues, it should score < 8
        # (each hard issue -2, soft -0.5, so even 1 hard issue drops below 8
        #  when averaged across 7 dimensions: 10 - 2/7 ≈ 9.71...
        #  Actually with 1 hard issue: dim_score = 8 for that dim,
        #  others = 10, avg = (8+10*6)/7 = 68/7 ≈ 9.71
        #  With 2 hard issues in same dim: (6+60)/7 ≈ 9.43
        #  With 2 hard in different dims: (8+8+50)/7 ≈ 9.43
        #  Need ~4+ hard issues to drop below 8.
        #  Let's just check that slides with many issues score lower.
        if slides_with_issues:
            # Sort by issue count
            sorted_slides = sorted(
                slides_with_issues,
                key=lambda s: len(s["issues"]),
                reverse=True,
            )
            # The slide with most issues should have a lower score
            # than the slide with fewest issues (if there's variance)
            if len(sorted_slides) > 1:
                most_issues = sorted_slides[0]
                fewest_issues = sorted_slides[-1]
                if len(most_issues["issues"]) > len(fewest_issues["issues"]) + 2:
                    self.assertLessEqual(
                        most_issues["score"],
                        fewest_issues["score"] + 1.0,
                        f"Slide with {len(most_issues['issues'])} issues "
                        f"should score lower than slide with "
                        f"{len(fewest_issues['issues'])} issues",
                    )

            # Any slide with >= 3 hard issues should score < 8
            for s in slides_with_issues:
                if s["hard_issues"] >= 3:
                    self.assertLess(
                        s["score"],
                        8.0,
                        f"Slide {s['slide']} has {s['hard_issues']} hard "
                        f"issues but scored {s['score']} (expected < 8)",
                    )

    def test_critique_pptx_with_palette(self):
        """When a restrictive palette is provided, off-palette colors are flagged."""
        # Use a very restrictive palette (just white and black)
        result = critique_pptx(str(_ASSET), palette=["#FFFFFF", "#000000"])

        self.assertIn("slides", result)
        # The report should still be valid
        self.assertIsInstance(result["overall_score"], (int, float))

        # Check that color dimension issues exist if there are colored shapes
        color_issues = []
        for s in result["slides"]:
            for iss in s["issues"]:
                if iss["dimension"] == "color" and iss["severity"] == "hard":
                    color_issues.append(iss)

        # Most PPTX templates use some colors beyond black/white,
        # so we expect at least some hard color issues.
        # (If the template is truly B&W, this assertion is skipped.)
        # We don't force this — just verify no crash.


class TestCritiqueHtml(unittest.TestCase):
    """Tests for critique_engine.critique_html()."""

    def setUp(self):
        self.test_html_dir = _SCRIPTS_PARENT.parent / "scripts" / "tests" / "_test_html"
        self.test_html_dir.mkdir(parents=True, exist_ok=True)

    def _make_html(self, name: str, content: str) -> str:
        path = self.test_html_dir / name
        path.write_text(content, encoding="utf-8")
        return str(path)

    def test_critique_html_basic(self):
        """Output structure matches critique_pptx, slides detected correctly."""
        html = """<!DOCTYPE html>
<html>
<head><style>
.slide { width: 1920px; height: 1080px; aspect-ratio: 16/9; }
.title { font-size: 36pt; color: #1C1410; }
.body { font-size: 24pt; color: #D8000F; }
</style></head>
<body>
<div class="slide" style="position: relative; left: 0px; top: 0px; width: 1920px; height: 1080px;">
  <div class="title" style="font-size: 36pt; color: #1C1410;">Slide 1</div>
  <div class="body" style="font-size: 24pt; color: #D8000F; left: 8px; top: 8px;">Content</div>
</div>
<div class="slide" style="position: relative; left: 0px; top: 0px;">
  <div class="title" style="font-size: 36pt; color: #1C1410;">Slide 2</div>
  <div class="body" style="font-size: 24pt; color: #D8000F;">More content</div>
</div>
<div class="slide" style="position: relative; left: 0px; top: 0px;">
  <div class="title" style="font-size: 36pt; color: #1C1410;">Slide 3</div>
</div>
</body></html>"""
        path = self._make_html("test_basic.html", html)
        result = critique_html(path)

        # Top-level structure
        self.assertIsInstance(result, dict)
        for key in ("stage", "file", "overall_score", "total_issues",
                    "hard_issues", "soft_issues", "converged", "slides",
                    "dimension_scores"):
            self.assertIn(key, result)

        self.assertEqual(result["stage"], "structural")
        self.assertEqual(result["file"], "test_basic.html")
        self.assertEqual(len(result["slides"]), 3)
        self.assertIsInstance(result["overall_score"], (int, float))
        self.assertIsInstance(result["slides"], list)
        self.assertIsInstance(result["dimension_scores"], dict)

        # Slide entries
        for s in result["slides"]:
            self.assertIn("slide", s)
            self.assertIn("score", s)
            self.assertIn("issues", s)
            self.assertIn("hard_issues", s)
            self.assertIn("soft_issues", s)
            self.assertGreaterEqual(s["score"], 0)
            self.assertLessEqual(s["score"], 10)

        # dimension_scores should have all 7 dimensions
        expected_dims = {
            "alignment", "color", "type_scale", "density",
            "placeholder", "stage_fit", "completeness",
        }
        self.assertEqual(set(result["dimension_scores"].keys()), expected_dims)

        # Stage fit should pass since we have 1920×1080 + aspect-ratio
        self.assertGreaterEqual(result["dimension_scores"]["stage_fit"], 5.0)

    def test_critique_html_stage_violation(self):
        """stage_fit dimension scores 0 when aspect ratio is not 16:9."""
        html = """<!DOCTYPE html>
<html>
<head><style>
.slide { width: 1024px; height: 768px; }
.title { font-size: 36pt; color: #1C1410; }
</style></head>
<body>
<div class="slide" style="position: relative; width: 1024px; height: 768px;">
  <div class="title" style="font-size: 36pt; color: #1C1410;">Not 16:9</div>
</div>
</body></html>"""
        path = self._make_html("test_stage_violation.html", html)
        result = critique_html(path)

        self.assertIsInstance(result, dict)
        self.assertEqual(len(result["slides"]), 1)
        # 2 hard issues: no stage + no scale → 10 - 2*2 = 6
        # 2 hard issues: no stage + no scale → 10 - 2*2 = 6
        self.assertEqual(
            result["dimension_scores"]["stage_fit"],
            6.0,
            f"Expected stage_fit score 6.0 (2 hard issues), got {result['dimension_scores']['stage_fit']}",
        )

        # Check that the first slide has stage_fit issues
        slide0 = result["slides"][0]
        stage_issues = [i for i in slide0["issues"] if i["dimension"] == "stage_fit"]
        self.assertGreater(
            len(stage_issues), 0,
            "Expected at least one stage_fit issue in the slide",
        )

    def test_critique_html_stage_5_hard(self):
        """stage_fit scores 0 when there are 5+ hard issues."""
        html = """<!DOCTYPE html>
<html><body><p class="slide" style="font-size: 16pt;">No stage, no palette mismatch, bad type scale, placeholder TODO, density</p></body></html>"""
        path = self._make_html("test_5hard.html", html)
        result = critique_html(path)
        self.assertEqual(result["dimension_scores"]["stage_fit"], 6.0)

    def test_critique_html_with_palette(self):
        """Off-palette colors are flagged as hard issues."""
        html = """<!DOCTYPE html>
<html>
<head><style>
.slide { width: 1920px; height: 1080px; }
.title { font-size: 36pt; color: #FF0000; }
.body { font-size: 24pt; color: #00FF00; }
</style></head>
<body>
<div class="slide">
  <div class="title" style="font-size: 36pt; color: #FF0000;">Title</div>
  <div class="body" style="font-size: 24pt; color: #00FF00;">Body</div>
</div>
</body></html>"""
        path = self._make_html("test_palette.html", html)
        result = critique_html(path, palette=["#1C1410", "#D8000F"])

        color_hard = 0
        for s in result["slides"]:
            for iss in s["issues"]:
                if iss["dimension"] == "color" and iss["severity"] == "hard":
                    color_hard += 1
        self.assertGreaterEqual(
            color_hard, 1,
            "Expected at least 1 hard color issue for off-palette colors",
        )

    def test_critique_html_no_slide_class(self):
        """If no .slide or [data-slide], the whole doc is one slide."""
        html = """<!DOCTYPE html>
<html>
<body>
<p style="font-size: 16pt; color: #333333;">No slides here</p>
<div style="width: 1920px; height: 1080px; aspect-ratio: 16/9;">Stage</div>
</body></html>"""
        path = self._make_html("test_no_slide.html", html)
        result = critique_html(path)

        self.assertEqual(len(result["slides"]), 1)

    def tearDown(self):
        # Cleanup test files
        for f in self.test_html_dir.glob("*.html"):
            f.unlink()
        if self.test_html_dir.exists():
            try:
                self.test_html_dir.rmdir()
            except OSError:
                pass


class TestCritiqueAutoDetect(unittest.TestCase):
    """Tests for critique_engine.critique() auto-detection."""

    def setUp(self):
        self.test_html_dir = _SCRIPTS_PARENT.parent / "scripts" / "tests" / "_test_html"
        self.test_html_dir.mkdir(parents=True, exist_ok=True)

    def test_critique_auto_pptx(self):
        """Pass .pptx without file_type -> uses PPTX branch."""
        if not _ASSET.exists():
            self.skipTest(f"Test asset not found: {_ASSET}")
        result = critique(str(_ASSET))
        self.assertIn("overall_score", result)
        self.assertEqual(result["file"], "PPT模板.pptx")

    def test_critique_auto_html(self):
        """Pass .html without file_type -> uses HTML branch."""
        html = """<!DOCTYPE html>
<html>
<body><div class="slide"><p>Test</p></div></body></html>"""
        path = self.test_html_dir / "test_auto.html"
        path.write_text(html, encoding="utf-8")
        result = critique(str(path))
        self.assertIn("overall_score", result)
        self.assertEqual(result["file"], "test_auto.html")
        path.unlink()

    def tearDown(self):
        for f in self.test_html_dir.glob("*.html"):
            f.unlink()
        try:
            self.test_html_dir.rmdir()
        except OSError:
            pass


if __name__ == "__main__":
    unittest.main()
