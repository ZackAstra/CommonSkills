"""Debug the stage violation test."""
import sys, json, tempfile, os
sys.path.insert(0, r"C:\Users\Windows\.config\TeleAgent\skills\ppt-aesthetics\scripts")
from critique_engine import critique_html

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

with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html)
    path = f.name
result = critique_html(path)
os.unlink(path)
print("Issues:")
for i in result["slides"][0]["issues"]:
    print(f"  [{i['severity']}] {i['dimension']}: {i['problem'][:80]}")
print(f"\nDimension scores: {result['dimension_scores']}")
print(f"Stage_fit: {result['dimension_scores']['stage_fit']}")
