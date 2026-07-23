---
name: baoyu-diagram
description: Create professional, dark-themed SVG diagrams of any type 鈥?architecture diagrams, flowcharts, sequence diagrams, structural diagrams, mind maps, timelines, illustrative/conceptual diagrams, and more. Use this skill whenever the user asks for any kind of technical or conceptual diagram, visualization of a system, process flow, data flow, component relationship, network topology, decision tree, org chart, state machine, or any visual representation of structure/logic/process. Also trigger when the user says "鐢讳釜鍥? "鐢讳竴涓灦鏋勫浘" "diagram" "flowchart" "sequence diagram" "draw me a ..." or uploads content and asks to visualize it. Output is always a standalone .svg file.
version: 1.117.3
---

# Diagram Generator

Create professional SVG diagrams across multiple diagram types. All output is a single self-contained `.svg` file with embedded styles and fonts.

## Supported Diagram Types

| Type | When to Use | Key Characteristics |
|------|-------------|-------------------|
| **Architecture** | System components & relationships | Grouped boxes, connection arrows, region boundaries |
| **Flowchart** | Decision logic, process steps | Diamond decisions, rounded step boxes, directional flow |
| **Sequence** | Time-ordered interactions between actors | Vertical lifelines, horizontal messages, activation bars |
| **Structural** | Class diagrams, ER diagrams, org charts | Compartmented boxes, typed relationships (inheritance, composition) |
| **Mind Map** | Brainstorming, topic exploration | Central node, radiating branches, organic layout |
| **Timeline** | Chronological events | Horizontal/vertical axis, event markers, period spans |
| **Illustrative** | Conceptual explanations, comparisons | Free-form layout, icons, annotations, visual metaphors |
| **State Machine** | State transitions, lifecycle | Rounded state nodes, labeled transitions, start/end markers |
| **Data Flow** | Data transformation pipelines | Process bubbles, data stores, external entities |

## Design System

### Color Palette

Semantic colors for component categories:

| Category | Fill (rgba) | Stroke | Use For |
|----------|-------------|--------|---------|
| Primary | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan) | Frontend, user-facing, inputs |
| Secondary | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald) | Backend, services, processing |
| Tertiary | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet) | Database, storage, persistence |
| Accent | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber) | Cloud, infrastructure, regions |
| Alert | `rgba(136, 19, 55, 0.4)` | `#fb7185` (rose) | Security, errors, warnings |
| Connector | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange) | Buses, queues, middleware |
| Neutral | `rgba(30, 41, 59, 0.5)` | `#94a3b8` (slate) | External, generic, unknown |
| Highlight | `rgba(59, 130, 246, 0.3)` | `#60a5fa` (blue) | Active state, focus, current step |

For flowcharts and sequence diagrams, assign colors by role (actor, decision, process) rather than by technology.

### Typography

Use embedded SVG `@font-face` or system monospace fallback:

```svg
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&amp;display=swap');
  text { font-family: 'JetBrains Mono', 'SF Mono', 'Cascadia Code', monospace; }
</style>
```

Font sizes by role:
- **Title:** 16px, weight 700
- **Component name:** 11-12px, weight 600
- **Sublabel / description:** 9px, weight 400, color `#94a3b8`
- **Annotation / note:** 8px, weight 400
- **Tiny label (on arrows):** 7-8px

### Core Visual Elements

**Background:** `#0f172a` (slate-900) with subtle grid:
```svg
<defs>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
  </pattern>
</defs>
<rect width="100%" height="100%" fill="#0f172a"/>
<rect width="100%" height="100%" fill="url(#grid)"/>
```

**Arrowhead marker (standard):**
```svg
<marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
  <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
</marker>
```

**Arrowhead marker (colored) 鈥?create per-color as needed:**
```svg
<marker id="arrow-cyan" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
  <polygon points="0 0, 10 3.5, 0 7" fill="#22d3ee"/>
</marker>
```

**Open arrowhead (for async/return messages):**
```svg
<marker id="arrow-open" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
  <polyline points="0 0, 10 3.5, 0 7" fill="none" stroke="#64748b" stroke-width="1.5"/>
</marker>
```

### SVG Structure & Layering

Draw elements in this order to get correct z-ordering (SVG paints back-to-front):

1. Background fill + grid pattern
2. Region/group boundaries (dashed outlines)
3. Connection arrows and lines
4. Opaque masking rects (same position as component boxes, `fill="#0f172a"`)
5. Component boxes (semi-transparent fill + stroke)
6. Text labels
7. Legend (bottom-right or bottom area, outside all boundaries)
8. Title block (top-left)

The opaque masking rect trick is essential 鈥?semi-transparent component fills will show arrows underneath without it:
```svg
<!-- Mask layer: opaque background to hide arrows -->
<rect x="100" y="100" width="160" height="60" rx="6" fill="#0f172a"/>
<!-- Visual layer: styled component -->
<rect x="100" y="100" width="160" height="60" rx="6" fill="rgba(8,51,68,0.4)" stroke="#22d3ee" stroke-width="1.5"/>
<text x="180" y="125" fill="white" font-size="11" font-weight="600" text-anchor="middle">API Gateway</text>
<text x="180" y="141" fill="#94a3b8" font-size="9" text-anchor="middle">Kong / Nginx</text>
```

### Spacing Rules

These prevent overlapping 鈥?follow them strictly:

- **Component box height:** 50-70px (standard), 80-120px (large/complex)
- **Minimum gap between components:** 40px vertical, 30px horizontal
- **Arrow label clearance:** 10px from any box edge
- **Region boundary padding:** 20px inside edges around contained components
- **Legend placement:** At least 20px below the lowest diagram element
- **Title block:** 20px from top-left, outside diagram content area
- **viewBox:** Always extend to fit all content + 30px padding on all sides

### Component Patterns

**Standard box (service/process):**
```svg
<rect x="X" y="Y" width="160" height="60" rx="6" fill="#0f172a"/>
<rect x="X" y="Y" width="160" height="60" rx="6" fill="FILL" stroke="STROKE" stroke-width="1.5"/>
<text x="CX" y="Y+24" fill="white" font-size="11" font-weight="600" text-anchor="middle">Name</text>
<text x="CX" y="Y+40" fill="#94a3b8" font-size="9" text-anchor="middle">description</text>
```

**Decision diamond (flowchart):**
```svg
<g transform="translate(CX, CY)">
  <polygon points="0,-35 50,0 0,35 -50,0" fill="#0f172a"/>
  <polygon points="0,-35 50,0 0,35 -50,0" fill="rgba(120,53,15,0.3)" stroke="#fbbf24" stroke-width="1.5"/>
  <text y="4" fill="white" font-size="10" font-weight="600" text-anchor="middle">Condition?</text>
</g>
```

**Database cylinder:**
```svg
<g transform="translate(X, Y)">
  <rect x="0" y="10" width="120" height="50" rx="2" fill="#0f172a"/>
  <ellipse cx="60" cy="10" rx="60" ry="12" fill="#0f172a"/>
  <ellipse cx="60" cy="60" rx="60" ry="12" fill="#0f172a"/>
  <rect x="0" y="10" width="120" height="50" fill="rgba(76,29,149,0.4)"/>
  <ellipse cx="60" cy="10" rx="60" ry="12" fill="rgba(76,29,149,0.4)" stroke="#a78bfa" stroke-width="1.5"/>
  <ellipse cx="60" cy="60" rx="60" ry="12" fill="rgba(76,29,149,0.4)" stroke="#a78bfa" stroke-width="1.5"/>
  <line x1="0" y1="10" x2="0" y2="60" stroke="#a78bfa" stroke-width="1.5"/>
  <line x1="120" y1="10" x2="120" y2="60" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="60" y="40" fill="white" font-size="11" font-weight="600" text-anchor="middle">PostgreSQL</text>
</g>
```

**Region boundary:**
```svg
<rect x="X" y="Y" width="W" height="H" rx="12" fill="none" stroke="#fbbf24" stroke-width="1" stroke-dasharray="8,4"/>
<text x="X+12" y="Y+16" fill="#fbbf24" font-size="9" font-weight="600">AWS us-east-1</text>
```

**Security group:**
```svg
<rect x="X" y="Y" width="W" height="H" rx="8" fill="none" stroke="#fb7185" stroke-width="1" stroke-dasharray="4,4"/>
<text x="X+10" y="Y+14" fill="#fb7185" font-size="8" font-weight="500">VPC / Security Group</text>
```

## Type-Specific Layout Guidance

Determine this SKILL.md file's directory path as `{baseDir}`. Read the reference file for the specific diagram type before starting layout. Reference files are located at `{baseDir}/references/` and contain detailed layout algorithms and examples.

### Architecture Diagrams
鈫?Read `{baseDir}/references/architecture.md`

Key points: left-to-right or top-to-bottom data flow. Group related services in region boundaries. Use buses/connectors between layers. Place databases at the bottom or right.

### Flowcharts
鈫?Read `{baseDir}/references/flowchart.md`

Key points: top-to-bottom primary flow. Diamonds for decisions with Yes/No labels on exit arrows. Rounded rectangles for start/end. Use the Highlight color for the happy path.

### Sequence Diagrams
鈫?Read `{baseDir}/references/sequence.md`

Key points: actors as boxes at top, vertical dashed lifelines, horizontal arrows for messages (solid=sync, dashed=return). Time flows downward. Activation bars show processing. Number messages if complex.

### Structural Diagrams
鈫?Read `{baseDir}/references/structural.md`

Key points: compartmented boxes (name / attributes / methods for class diagrams). Relationship lines: solid with filled diamond=composition, solid with empty diamond=aggregation, dashed arrow=dependency, solid triangle=inheritance.

### Mind Maps
Free-form radiating layout from a central concept. Use organic curves (`<path>` with cubic beziers) for branches. Vary branch colors using the palette. Larger font for central node, decreasing as you go outward.

### Timelines
Horizontal or vertical axis line. Event markers as circles or diamonds on the axis. Description text offset to alternating sides to avoid overlap. Use color to categorize event types.

### State Machines
Rounded-rect states with double-border for composite states. Filled circle for initial state, bullseye for final state. Curved arrows for self-transitions. Label all transitions with `event [guard] / action` format.

## Output Rules

1. Output a **single `.svg` file** 鈥?no external dependencies except the Google Fonts import
2. Set `viewBox` to fit all content with 30px padding; do NOT set fixed `width`/`height` attributes (let the SVG scale responsively)
3. Include `xmlns="http://www.w3.org/2000/svg"` on the root `<svg>` element
4. Put all `<style>`, `<defs>`, markers, and patterns at the top of the SVG
5. Use `text-anchor="middle"` for centered labels; ensure text doesn't overflow boxes
6. **Chinese text support:** When labels contain Chinese characters, use `font-family: 'JetBrains Mono', 'Noto Sans SC', 'PingFang SC', sans-serif'` and increase box widths 鈥?CJK characters are wider
7. **Save location:** If the input is a file, save to `{inputFileDir}/diagram/`. Otherwise save to `{projectDir}/diagram/{topic-slug}/`. Create the directory if it doesn't exist

## Script

Determine this SKILL.md file's directory path as `{baseDir}`. Script path: `{baseDir}/scripts/main.ts`.

Resolve `${BUN_X}` runtime: if `bun` installed 鈫?`bun`; if `npx` available 鈫?`npx -y bun`; else suggest installing bun.

### SVG 鈫?@2x PNG

After saving the SVG, convert it to a @2x PNG:

```bash
${BUN_X} {baseDir}/scripts/main.ts <svg-path> [options]
```

Options:
- `-s, --scale <n>` 鈥?Scale factor (default: 2)
- `-o, --output <path>` 鈥?Custom output path (default: `<input>@2x.png`)
- `--json` 鈥?JSON output


## SVG-to-PPTX Conversion

After saving the SVG, convert it to an editable PowerPoint presentation using the bundled script:

```bash
python {baseDir}/scripts/svg2pptx.py <svg-path> [-o output.pptx]
```

The script parses SVG elements (rect, ellipse, line, text, polygon) and rebuilds them as native
PowerPoint shapes with matching colors, positions, and styles. The output is a 16:9 dark-themed
slide where every shape and text box is individually editable in PowerPoint.

**Prerequisites:** Install python-pptx in a writable directory:

```powershell
python -m pip install python-pptx --target "$env:USERPROFILE\Documents\Codex\python-libs" --proxy http://127.0.0.1:7897 --trusted-host pypi.org --trusted-host files.pythonhosted.org
$env:PYTHONPATH = "$env:USERPROFILE\Documents\Codex\python-libs"
```

**Options:**
- `-o, --output <path>` — Custom output path (default: `<input>.pptx`)

## Process

1. Identify the diagram type from the user's request
2. Read the relevant reference file if one exists for that type
3. Plan the layout: list all components, determine grouping and flow direction, calculate positions
4. Write the SVG following the layering order above
5. Verify spacing rules 鈥?no overlaps, legends outside boundaries, viewBox large enough
6. Save the SVG file
7. Run `${BUN_X} {baseDir}/scripts/main.ts <svg-path>` to generate @2x PNG
8. Run `python {baseDir}/scripts/svg2pptx.py <svg-path>` to generate an editable PPTX
9. Present both files to the user
锘?## Real-World Troubleshooting Notes

This section captures practical issues encountered when installing and using this skill in restricted/sandboxed environments (e.g., Windows Codex CLI with network sandboxing).

### 1. Git Clone Timeouts / GitHub Not Reachable

**Symptom:** git clone https://github.com/... hangs or fails with Failed to connect to github.com port 443.

**Root Cause:** Direct outbound HTTPS to GitHub is blocked; a local proxy (e.g., Clash) may be available.

**Solution:**
1. Detect open local proxy ports (common: 7890, 7897, 1080, 10808, 10809):
   `powershell
    = @(7890,7897,1080,10808,10809)
   foreach ( in ) {
     try {  = New-Object System.Net.Sockets.TcpClient;  = .BeginConnect('127.0.0.1',,,);  = .AsyncWaitHandle.WaitOne(500,False); if ( -and .Connected) { " open" } else { " closed" }; .Close() } catch { " closed" }
   }
   `
2. Configure Git to use the open proxy and OpenSSL backend:
   `powershell
   git config --global http.proxy http://127.0.0.1:7897
   git config --global https.proxy http://127.0.0.1:7897
   git config --global http.sslBackend openssl
   `
3. If you cannot modify ~/.gitconfig due to sandbox permissions, set an isolated config file:
   `powershell
    = "C:\Users\zhaox\Documents\Codex\.gitconfig_codex"
   `
4. Re-run clone and verify with git ls-remote.

### 2. Copying Skills to ~/.codex/skills Is Denied

**Symptom:** Copy-Item / 
obocopy to ~/.codex/skills returns Access is denied.

**Root Cause:** The sandbox process lacks write access to that directory.

**Solution:** Run the copy command with elevated permissions. In Codex CLI this is done by passing the escalation request:
`powershell
robocopy "<source>" "C:\Users\zhaox\.codex\skills\baoyu-diagram" /E /COPY:DAT
`

### 3. SVG-to-PNG: bun Is Not Available

**Symptom:** The recommended ${BUN_X} {baseDir}/scripts/main.ts <svg> fails because un/
ode is not installed and cannot be downloaded.

**Workaround (Windows + Edge):** Use Microsoft Edge in headless mode to screenshot an HTML page containing the SVG at 2脳 scale:
`powershell
 = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
 = "diagram@2x.png"
 = "render.html"   # HTML that loads the SVG at 2240x1560
 = "C:\Users\zhaox\Documents\Codex\edge-temp"
New-Item -ItemType Directory -Path  -Force | Out-Null
Start-Process  -ArgumentList "--headless --disable-gpu --user-data-dir= --screenshot= --window-size=2240,1560 --hide-scrollbars --no-sandbox file:///" -WindowStyle Hidden -Wait
`

### 4. General Restricted-Environment Checklist

- **Network:** Always check for local proxy ports first; direct HTTPS is often blocked.
- **Permissions:** If writing to user home fails, write to the workspace root ($env:USERPROFILE\Documents\Codex) and request escalation only when copying to protected destinations.
- **Dependencies:** Prefer already-installed system tools (Edge, Python/Pillow/selenium) over downloading new runtimes.
- **Verification:** After each output, check file existence, size, and format (PIL for images, pptx for slides).
