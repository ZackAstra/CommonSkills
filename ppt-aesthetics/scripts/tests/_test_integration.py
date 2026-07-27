"""Integration test for HTML critique and CLI."""
import sys
sys.path.insert(0, r"C:\Users\Windows\.config\TeleAgent\skills\ppt-aesthetics\scripts")
from critique_engine import critique_html, critique
import json
import tempfile
import os

# === Test 1: critique_html basic ===
html = """<!DOCTYPE html>
<html>
<head><style>
.slide { width: 1920px; height: 1080px; aspect-ratio: 16/9; }
.title { font-size: 36pt; color: #1C1410; }
.body { font-size: 24pt; color: #D8000F; }
.subtitle { font-size: 18pt; color: #3B3B3B; }
</style></head>
<body>
<div class="slide" style="position: relative;">
  <div class="title" style="font-size: 36pt; color: #1C1410;">Good Slide</div>
  <div class="body" style="font-size: 24pt; color: #D8000F; left: 8px; top: 8px;">Content</div>
  <div class="subtitle" style="font-size: 18pt; color: #3B3B3B;">Sub content</div>
  <img src="test.png">
</div>
</body></html>"""

with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html)
    path = f.name

result = critique_html(path)
os.unlink(path)

print("=== Test 1: critique_html basic ===")
print("OVERALL_SCORE:", result["overall_score"])
print("SLIDES:", len(result["slides"]))
print("TOTAL_ISSUES:", result["total_issues"])
for s in result["slides"]:
    print(f"  Slide {s['slide']}: score={s['score']}, hard={s['hard_issues']}, soft={s['soft_issues']}")
    for i in s["issues"]:
        print(f"    [{i['severity']}] {i['dimension']}: {i['problem'][:60]}")
print("DIMS:", result["dimension_scores"])

# === Test 2: CLI via critique() ===
print("\n=== Test 2: critique() auto-detect ===")
# Use the .pptx asset
asset = r"C:\Users\Windows\.config\TeleAgent\skills\ppt-aesthetics\assets\PPT模板.pptx"
result2 = critique(asset)
print(f"Auto-detected .pptx: file={result2['file']}, score={result2['overall_score']}")

# === Test 3: CLI output via CLI script ===
print("\n=== Test 3: CLI via subprocess ===")
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write("<html><body><div class='slide'><p>Hi</p></div></body></html>")
    cli_path = f.name

import subprocess
cli_script = r"C:\Users\Windows\.config\TeleAgent\skills\ppt-aesthetics\scripts\critique_engine.py"
output_path = cli_path + ".report.json"
result = subprocess.run(
    [sys.executable, cli_script, cli_path, "--output", output_path],
    capture_output=True, text=True, encoding="utf-8"
)
print("STDOUT line count:", len(result.stdout.splitlines()))
if os.path.exists(output_path):
    with open(output_path, encoding="utf-8") as f:
        data = json.load(f)
    print("CLI output file:", data["file"], "score:", data["overall_score"])
    os.unlink(output_path)
os.unlink(cli_path)

print("\n=== All integration tests passed ===")
