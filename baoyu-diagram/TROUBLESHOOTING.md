# Baoyu Diagram Skill — Real-World Troubleshooting Guide

This guide captures practical issues encountered when installing and using `baoyu-diagram` in restricted or sandboxed environments (e.g., Windows Codex CLI with network sandboxing and limited home-directory permissions).

---

## 1. Git Clone Timeouts / GitHub Not Reachable

### Symptom
`git clone https://github.com/...` hangs for a long time and eventually fails with:
```text
Failed to connect to github.com port 443 after ... ms: Could not connect to server
```

### Root Cause
Direct outbound HTTPS to GitHub is blocked. A local proxy (e.g., Clash, v2rayN) is often already running on a common port such as `7890` or `7897`.

### Solution
1. Detect open local proxy ports:
   ```powershell
   $ports = @(7890, 7897, 1080, 10808, 10809)
   foreach ($p in $ports) {
     try {
       $c = New-Object System.Net.Sockets.TcpClient
       $r = $c.BeginConnect('127.0.0.1', $p, $null, $null)
       $w = $r.AsyncWaitHandle.WaitOne(500, $false)
       if ($w -and $c.Connected) { "$p open" } else { "$p closed" }
       $c.Close()
     } catch { "$p closed" }
   }
   ```
2. Configure Git to use the open proxy and the OpenSSL backend (avoids Windows schannel certificate issues):
   ```powershell
   git config --global http.proxy http://127.0.0.1:7897
   git config --global https.proxy http://127.0.0.1:7897
   git config --global http.sslBackend openssl
   ```
3. If you cannot modify `~/.gitconfig` due to sandbox permissions, use an isolated config file:
   ```powershell
   $env:GIT_CONFIG_GLOBAL = "$env:USERPROFILE\Documents\Codex\.gitconfig_codex"
   git config --global http.proxy http://127.0.0.1:7897
   git config --global https.proxy http://127.0.0.1:7897
   ```
4. Verify connectivity before cloning:
   ```powershell
   git ls-remote https://github.com/oven-sh/bun.git HEAD
   ```

---

## 2. Copying Skills to ~/.codex/skills Is Denied

### Symptom
`Copy-Item` / `robocopy` to `$env:USERPROFILE\.codex\skills` returns `Access is denied`.

### Root Cause
The sandbox process does not have write access to that directory.

### Solution
Run the copy operation with elevated permissions. In Codex CLI, request escalation:
```powershell
robocopy "$source" "$env:USERPROFILE\.codex\skills\baoyu-diagram" /E /COPY:DAT
```

---

## 3. SVG-to-PNG: bun Is Not Available

### Symptom
The recommended command fails because `bun`/`node` is not installed and cannot be downloaded from GitHub or npm due to network restrictions.

### Workaround: Microsoft Edge Headless Screenshot
On Windows, use the system-installed Edge browser to capture the SVG at 2x scale.

1. Create an HTML wrapper that renders the SVG at the desired size.
2. Run Edge in headless mode:
   ```powershell
   $edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
   $png = "diagram@2x.png"
   $html = "render.html"
   $userData = "$env:USERPROFILE\Documents\Codex\edge-temp"
   New-Item -ItemType Directory -Path $userData -Force | Out-Null
   Start-Process $edge -ArgumentList "--headless --disable-gpu --user-data-dir=$userData --screenshot=$png --window-size=2240,1560 --hide-scrollbars --no-sandbox file:///$($html.Replace('\','/'))" -WindowStyle Hidden -Wait
   ```
3. Verify the output with Pillow:
   ```python
   from PIL import Image
   img = Image.open("diagram@2x.png")
   print(img.size, img.format, img.mode)  # (2240, 1560) PNG RGB
   ```

---

## 4. SVG-to-Editable-PPTX

### Symptom
User wants the architecture diagram as editable PowerPoint shapes rather than a static image.

### Solution
Use `python-pptx` to draw native PowerPoint shapes and text boxes programmatically.

### Installation in Sandbox
If pip cannot install into the default user path, install into a workspace directory and add it to `PYTHONPATH`:
```powershell
python -m pip install python-pptx `
  --target "$env:USERPROFILE\Documents\Codex\python-libs" `
  --proxy http://127.0.0.1:7897 `
  --trusted-host pypi.org `
  --trusted-host files.pythonhosted.org

$env:PYTHONPATH = "$env:USERPROFILE\Documents\Codex\python-libs"
```

### Basic Pattern
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(16)
prs.slide_height = Inches(11)
slide = prs.slides.add_slide(prs.slide_layouts[6])

shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(1), Inches(3), Inches(1.5))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(8, 51, 68)
shape.line.color.rgb = RGBColor(34, 211, 238)

tf = shape.text_frame
tf.text = "Component"
p = tf.paragraphs[0]
p.font.size = Pt(13)
p.font.color.rgb = RGBColor(248, 250, 252)
p.alignment = PP_ALIGN.CENTER

prs.save("output.pptx")
```

---

## 5. General Restricted-Environment Checklist

- **Network first:** Always check for a local proxy before trying direct HTTPS.
- **Permissions:** If writing to the user home directory fails, write to the workspace root first.
- **Dependencies:** Prefer tools already installed on the system (Edge, Python, Pillow) over downloading new runtimes.
- **Verification:** After every output, verify existence, size, and format.
