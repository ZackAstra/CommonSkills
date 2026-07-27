---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '943b96f4-5924-4bc7-bb99-f8b27e9c3a47'
  PropagateID: '943b96f4-5924-4bc7-bb99-f8b27e9c3a47'
  ReservedCode1: '0c51b52d-37a8-43c5-9c17-94d08bdae491'
  ReservedCode2: '0c51b52d-37a8-43c5-9c17-94d08bdae491'
---

# Batch 3 — Design Token Extractions (Templates 25-34)

## 25. raw-grid

```json
{
  "name": "raw-grid",
  "title": "RAW GRID — Neobrutalist Presentation Template",
  "scheme": "light",
  "colors": {
    "background": "#ffffff",
    "background_alt": "#f5f5f5",
    "primary_accent": "#f2d4cf",
    "secondary_accent": "#e5edd6",
    "text_primary": "#0a0a0a",
    "text_secondary": "#333333",
    "decorative": {
      "pink_fill": "#f2d4cf",
      "green_fill": "#e5edd6",
      "black_fill": "#0a0a0a",
      "gray_fill": "#f5f5f5"
    }
  },
  "fonts": {
    "display": "system-ui, 'Segoe UI', -apple-system, Helvetica, Arial, sans-serif",
    "body": "system-ui, 'Segoe UI', -apple-system, Helvetica, Arial, sans-serif",
    "mono": null,
    "google_fonts": []
  },
  "type_scale": {
    "display": "clamp(48px, 7vw, 96px) / weight:900 / uppercase / tracking:-0.02em",
    "headline": "clamp(32px, 4.5vw, 64px) / weight:900 / uppercase / tracking:-0.01em",
    "title": "clamp(24px, 2.5vw, 36px) / weight:800 / uppercase",
    "subtitle": "clamp(16px, 1.4vw, 22px) / weight:700 / uppercase / tracking:0.04em",
    "body": "clamp(16px, 1.3vw, 20px) / weight:500 / line-height:1.6",
    "caption": "clamp(11px, 1vw, 13px) / weight:700 / uppercase / tracking:0.08em",
    "number": "clamp(64px, 8vw, 120px) / weight:900 / tracking:-0.04em"
  },
  "spacing": {
    "pad_lg": "clamp(32px, 4vw, 64px)",
    "pad_md": "clamp(20px, 2.5vw, 40px)",
    "pad_sm": "clamp(12px, 1.5vw, 20px)",
    "gap_sm": "clamp(8px, 1vw, 16px)",
    "gap_md": "clamp(16px, 2vw, 32px)",
    "gap_lg": "clamp(24px, 3vw, 48px)"
  },
  "decorative_elements": [
    "3px solid black borders throughout",
    "6px 6px 0 black box-shadow (brutalist shadow)",
    "4px 4px 0 black box-shadow-sm",
    "60×4px horizontal rule lines",
    "4×60px vertical rule lines",
    "Black label badges (bg:black, color:white, padding:6px 14px)",
    "Arrow prefix (→) via CSS ::before"
  ],
  "layout": {
    "dimensions": "100vw × 100vh (responsive, no deck-stage)",
    "grid_system": "CSS Grid variants: 1fr 1fr, 45% 55%, 55% 45%, 1fr 1fr 1fr 1fr",
    "density": "medium-high",
    "navigation": "custom JS (keydown/touch)"
  }
}
```

---

## 26. retro-windows

```json
{
  "name": "retro-windows",
  "title": "Retro Presentation Template (Windows 3.1)",
  "scheme": "light",
  "colors": {
    "background": "#c0c0c0",
    "background_alt": "#d4d0c8",
    "background_dark": "#808080",
    "primary_accent": "#000080",
    "secondary_accent": "#0000a0",
    "tertiary_accent": "#1084d0",
    "text_primary": "#222222",
    "text_secondary": "#555",
    "decorative": {
      "green_retro": "#008000",
      "red_retro": "#800000",
      "yellow_retro": "#808000",
      "cyan_retro": "#008080",
      "alt_row": "#f0f0f0"
    }
  },
  "fonts": {
    "display": "'Press Start 2P', cursive",
    "body": "'MS Sans Serif', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    "mono": "'VT323', monospace",
    "google_fonts": ["Press Start 2P", "VT323"]
  },
  "type_scale": {
    "pixel_title": "24px / 'Press Start 2P'",
    "text_xl": "32px",
    "text_lg": "22px",
    "text_md": "18px",
    "text_sm": "14px",
    "text_xs": "12px",
    "terminal": "22px / 'VT323'"
  },
  "spacing": {
    "gap_1": "6px",
    "gap_2": "10px",
    "gap_3": "16px",
    "gap_4": "24px",
    "grid_gap": "18-20px"
  },
  "decorative_elements": [
    "CRT scanline overlay (repeating-linear-gradient at 3px intervals, 0.03 opacity)",
    "Win3.1 window chrome (title bars with gradient blue, min/max/close buttons)",
    "3D beveled button borders (highlight+shadow technique)",
    "Progress bars (navy fill, sunken panel)",
    "Retro checkboxes (16×16px sunken squares with × mark)",
    "Marquee scrolling text animation",
    "Tree view items with > prefix bullets",
    "Retro horizontal rules (shadow+highlight 1px lines)",
    "Navigation dots with 3D beveled borders",
    "Hourglass &#x231B; emoji decoration"
  ],
  "layout": {
    "dimensions": "100vw × 100vh (responsive)",
    "grid_system": "grid-2, grid-3, grid-4 (CSS Grid)",
    "density": "high (data-dense Win3.1 aesthetic)",
    "navigation": "custom JS + Chart.js for charts",
    "extra_js": "Chart.js 4.4.7 (CDN)"
  }
}
```

---

## 27. retro-zine

```json
{
  "name": "retro-zine",
  "title": "Retro Zine Business Presentation",
  "scheme": "light",
  "colors": {
    "background": "#C8B99A",
    "background_dark": "#B8A98A",
    "primary_accent": "#008F4D",
    "secondary_accent": "#00A85D",
    "text_primary": "#1A1A1A",
    "text_secondary": null,
    "decorative": {
      "white": "#F4EFE6",
      "line_color": "#1A1A1A"
    }
  },
  "fonts": {
    "display": "'Bebas Neue', sans-serif",
    "body": "'Space Grotesk', sans-serif",
    "handwritten": "'Caveat', cursive",
    "google_fonts": ["Bebas Neue", "Caveat:wght@400;600;700", "Space Grotesk:wght@300-700"]
  },
  "type_scale": {
    "hero_title": "clamp(48px, 10vw, 140px) / 'Bebas Neue' / line-height:0.88 / uppercase / tracking:4px",
    "hero_date": "clamp(32px, 5vw, 72px) / 'Bebas Neue'",
    "split_heading": "clamp(42px, 6vw, 90px) / 'Bebas Neue' / line-height:0.95",
    "split_stat": "clamp(80px, 12vw, 160px) / 'Bebas Neue'",
    "split_stat_label": "clamp(24px, 3vw, 36px) / 'Caveat'",
    "statement_quote": "clamp(36px, 6vw, 90px) / 'Bebas Neue' / line-height:1.1",
    "grid_header": "clamp(48px, 7vw, 100px) / 'Bebas Neue'",
    "body": "clamp(14px, 1.3vw, 18px) / 'Space Grotesk' / line-height:1.6",
    "closing_title": "clamp(56px, 10vw, 160px) / 'Bebas Neue' / line-height:0.85"
  },
  "spacing": {
    "slide_padding": "60px",
    "grid_gap": "0 (border-separated)",
    "collage_gap": "absolute positioned",
    "editorial_columns_gap": "60px"
  },
  "decorative_elements": [
    "SVG grain texture overlay (fractalNoise filter, 0.07 opacity)",
    "3px solid black borders (lines, boxes, stamps)",
    "Stamp rotation transforms (-8deg, 6deg)",
    "Tape effects (rgba(255,255,255,0.4) strips with border)",
    "Green progress bar (4px height, fixed bottom)",
    "Slide counter (Bebas Neue, 14px, black bg + white border)",
    "Nav hint (appears on hover, black bg + cream text)",
    "RSVP card green shadow offset (::before pseudo-element)",
    "Green RSVP stamp badge (rotate -8deg, black bg + green text)"
  ],
  "layout": {
    "dimensions": "100vw × 100vh (responsive)",
    "grid_system": "CSS Grid (2×2 info boxes, 3-column numbers, 2-column editorial)",
    "density": "medium",
    "navigation": "custom JS (click/touch/keyboard)"
  }
}
```

---

## 28. sakura-chroma

```json
{
  "name": "sakura-chroma",
  "title": "Sakura Chroma — Slide Template",
  "scheme": "light",
  "colors": {
    "background": "#F1E6CB",
    "background_dark": "#E5D6B0",
    "primary_accent": "#E5392A",
    "secondary_accent": "#E54489",
    "additional_accents": {
      "orange": "#F09131",
      "green": "#3D9F47",
      "blue": "#3F8BC4",
      "yellow": "#F0BC2A"
    },
    "text_primary": "#3A2516",
    "text_secondary": null,
    "decorative": "same as accent colors (multi-color system)"
  },
  "fonts": {
    "display": "'Big Shoulders Display', sans-serif",
    "body": "'Albert Sans', 'Helvetica Neue', sans-serif",
    "mono": "'JetBrains Mono', ui-monospace, monospace",
    "cjk": "'Noto Sans JP', sans-serif",
    "google_fonts": ["Big Shoulders Display:wght@500;700;800;900", "Albert Sans:wght@400-700", "JetBrains Mono:wght@400;500", "Noto Sans JP:wght@500;700"]
  },
  "type_scale": {
    "display": "font-weight:900 / line-height:0.84 / tracking:-0.012em",
    "cover_hero_number": "clamp(120px, min(14vw, 22vh), 280px) / weight:900 / line-height:0.84",
    "cover_lockup": "clamp(56px, min(7vw, 11vh), 130px) / weight:900",
    "manifesto_stmt": "clamp(70px, min(8.4vw, 14vh), 168px) / weight:900 / line-height:0.86",
    "catalogue_title": "clamp(52px, min(5.6vw, 9vh), 100px) / weight:900",
    "card_name": "clamp(28px, min(2.6vw, 4.6vh), 48px) / weight:900",
    "data_big_stat": "clamp(110px, min(11vw, 18vh), 240px) / weight:900 / color:var(--red)",
    "body": "'Albert Sans' weight:400 / line-height:1.5",
    "micro_label": "'Albert Sans' weight:700 / uppercase / tracking:0.16em",
    "specs_mono": "'JetBrains Mono' / tracking:0.02em"
  },
  "spacing": {
    "frame_inset": "clamp(36px, 3.6vw, 72px)",
    "frame_bottom": "clamp(72px, 7vh, 110px)",
    "grid_gap": "clamp(16px, 1.6vw, 26px)",
    "section_gap": "clamp(18px, 2vh, 32px)"
  },
  "decorative_elements": [
    "Halftone-dot paper texture (::before radial-gradient, 0.16 opacity, 4px size)",
    "Five overlapping circular petal blobs (border-radius:50%, aspect-ratio:1/1) in red/orange/blue/green/yellow",
    "Diagonal multi-color stripe ribbons (rotate(-22deg), 5 colored bars)",
    "12-point starburst rosette badges (complex clip-path polygon, ink bg + paper text)",
    "Red stamps (bg:var(--red), color:var(--paper), rotate(-3deg))",
    "Spec checkbox columns (bordered squares, checked with × mark)",
    "Donut chart via SVG circles",
    "Equalizer bar chart (8-column grid, colored segments stacking bottom-up)",
    "Color-coded chip badges (6 accent colors)",
    "Dashed ink borders for card specs separation"
  ],
  "layout": {
    "dimensions": "100vw × 100vh (responsive with clamp())",
    "grid_system": "4-column catalogue grid, 8-column equalizer, 5-column ledger",
    "density": "medium-high (Japanese cassette packaging aesthetic)",
    "navigation": "custom JS (keydown/click/touch)"
  }
}
```

---

## 29. scatterbrain

```json
{
  "name": "scatterbrain",
  "title": "Scatterbrain — Post-it Inspired Presentation Template",
  "scheme": "light",
  "colors": {
    "background": {
      "cream": "#faf8f3",
      "paper": "#f7f5f0",
      "cork_light": "#e8ddd0",
      "cork_mid": "#d4c5b0",
      "cork_dark": "#c9b8a0",
      "warm_gradient": ["#fdf8f0", "#f7f0e6"]
    },
    "primary_accent": "#ffe066",
    "primary_accent_deep": "#ffd43b",
    "secondary_accent": "#a5d8ff",
    "secondary_accent_deep": "#74c0fc",
    "additional": {
      "pink": "#ffc9c9",
      "pink_deep": "#ff9f9f",
      "green": "#b2f2bb",
      "green_deep": "#8ce99a",
      "orange": "#ffcc80",
      "purple": "#d0bfff"
    },
    "text_primary": "#2d2a26",
    "text_secondary": "#5c5750",
    "decorative": {
      "shadow": "rgba(45, 42, 38, 0.15)",
      "shadow_deep": "rgba(45, 42, 38, 0.25)",
      "pin_red": "radial-gradient(#ff6b6b, #c92a2a)",
      "pin_blue": "radial-gradient(#4dabf7, #1864ab)",
      "pin_green": "radial-gradient(#69db7c, #2f9e44)",
      "pin_gold": "radial-gradient(#ffd43b, #f59f00)"
    }
  },
  "fonts": {
    "display": "'Shrikhand', cursive",
    "body": "'Zilla Slab', serif",
    "handwritten": "'Caveat', cursive",
    "google_fonts": ["Shrikhand", "Zilla Slab:wght@300-700;ital", "Caveat:wght@400-700"]
  },
  "type_scale": {
    "h1": "clamp(2.5rem, 5vw, 4.5rem) / 'Shrikhand' / line-height:1.1",
    "h2": "clamp(1.8rem, 3.5vw, 3rem) / 'Shrikhand'",
    "h3": "clamp(1.3rem, 2.5vw, 1.8rem) / 'Shrikhand'",
    "body": "clamp(1rem, 1.5vw, 1.25rem) / 'Zilla Slab' / line-height:1.7",
    "handwritten": "clamp(1.2rem, 2vw, 1.6rem) / 'Caveat' / line-height:1.4",
    "label": "0.9rem / 'Caveat' / uppercase / tracking:0.15em",
    "stat_value": "1.8rem / 'Shrikhand'"
  },
  "spacing": {
    "slide_padding": "3rem",
    "post_it_padding": "2rem",
    "grid_gap": "2.5rem-3rem",
    "chart_container_padding": "2.5rem"
  },
  "decorative_elements": [
    "Paper grain overlay (SVG feTurbulence noise, 0.04 opacity, 200px tile)",
    "Cork board texture (radial gradients + SVG cross-hatch pattern)",
    "Post-it notes (gradient backgrounds + box-shadow:2px 3px 15px)",
    "Pin decorations (radial-gradient circles with inset shadow, 16×16px)",
    "Tape decorations (rgba(255,255,255,0.4) strips, 80×25px, border + box-shadow)",
    "SVG doodle circles/squiggles/triangles/diamonds (0.15 opacity ink)",
    "Photo frame (white border + shadow + rotate(-2deg))",
    "Compare 'vs' circle (60×60px, black bg, Shrikhand font)",
    "Custom thumbtack cursor (SVG red/white dot)",
    "Sketch-style SVG bar chart with hand-drawn rounded corners"
  ],
  "layout": {
    "dimensions": "100vw × 100vh (responsive)",
    "grid_system": "2-col, 3-col CSS Grid",
    "density": "medium",
    "navigation": "custom JS (keyboard/touch/wheel with 700ms/1000ms lock)"
  }
}
```

---

## 30. signal

```json
{
  "name": "signal",
  "title": "Signal Template",
  "scheme": "mixed (dark navy + warm cream)",
  "colors": {
    "background_dark": "#1c2644",
    "background_dark_alt": "#232f55",
    "background_light": "#f0ece3",
    "background_light_alt": "#e6e0d4",
    "primary_accent": "#c8a870",
    "text_dark_primary": "#e2dcd0",
    "text_dark_secondary": "#8a96a8",
    "text_dark_tertiary": "#4e5a6e",
    "text_light_primary": "#1a2030",
    "text_light_secondary": "#5a6270",
    "text_light_tertiary": "#9aa0a8",
    "border_dark": "#2e3d5c",
    "border_light": "#cac4b4"
  },
  "fonts": {
    "display": "'Source Serif 4', 'Noto Serif SC', Georgia, serif",
    "heading": "'Source Serif 4', 'Noto Serif SC', Georgia, serif",
    "body": "'DM Sans', 'Noto Sans SC', system-ui, sans-serif",
    "mono": "'IBM Plex Mono', 'JetBrains Mono', monospace",
    "google_fonts": ["Source Serif 4:ital,opsz,wght@8..60,300-700", "DM Sans:opsz,wght@9..40,300-600", "IBM Plex Mono:wght@300-500", "Noto Serif SC:wght@300-700", "Noto Sans SC:wght@300-500"]
  },
  "type_scale": {
    "display": "9.5vw / weight:700 / line-height:0.96 / tracking:-0.02em",
    "h1": "5.2vw / weight:600 / line-height:1.08",
    "h2": "3vw / weight:600 / line-height:1.18",
    "h3": "1.9vw / weight:500 / line-height:1.3",
    "lead": "1.4vw / weight:400 / line-height:1.58",
    "body": "1.05vw / weight:400 / line-height:1.65",
    "caption": "0.82vw / weight:400 / line-height:1.5",
    "label": "0.7vw / weight:500 / uppercase / tracking:0.14em",
    "stat_value": "5.5vw / weight:600 / line-height:1 / tracking:-0.02em",
    "quote_text": "3.6vw / weight:400 / line-height:1.28",
    "flow_num": "4.5vw / weight:700 / color:accent"
  },
  "spacing": {
    "pad_x": "7.5vw",
    "pad_y": "5.5vh",
    "gap_lg": "4vh",
    "gap_md": "2.5vh",
    "gap_sm": "1.2vh"
  },
  "decorative_elements": [
    "Subtle grid overlay on dark slides (80px×80px, 3% opacity white lines)",
    "Italic serif <em> tags in antique gold (#c8a870) for emphasis",
    "Gold rule lines (36px×1px, accent color)",
    "Kicker labels (mono, uppercase, accent gold)",
    "Outlined tags (border:1px solid accent, padding:0.3em 0.8em)",
    "Chrome bars (top header + bottom footer with thin border)",
    "Pyramid levels using color-mix(in srgb, accent X%, bg)",
    "Vertical timeline spine with accent dot markers",
    "Cycle process 2×2 grid with accent top borders"
  ],
  "layout": {
    "dimensions": "100vw × 100vh per slide (horizontal strip deck)",
    "grid_system": "1fr 1fr splits, 3-4 column stats, 5-column flow diagrams",
    "density": "medium (editorial spacing)",
    "navigation": "horizontal translateX with nav dots + counter",
    "animation": "5 types (fade-up, fade-in, reveal-right, reveal-left, scale-in) with 7-step stagger"
  }
}
```

---

## 31. soft-editorial

```json
{
  "name": "soft-editorial",
  "title": "Soft Editorial — Slide Template",
  "scheme": "light",
  "colors": {
    "background": "#F2EEDF",
    "background_alt": "#ECE6D2",
    "primary_accent": "#E1A4C2",
    "secondary_accent": "#D6DD63",
    "additional": {
      "blush": "#E8C9B6",
      "sage": "#B7C7A8",
      "lilac": "#C9BEDC"
    },
    "text_primary": "#2A241B",
    "text_secondary": "#5C5345"
  },
  "fonts": {
    "display": "'Cormorant Garamond', 'Garamond', serif",
    "body": "'Work Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif",
    "google_fonts": ["Cormorant Garamond:ital,wght@0,400-600;1,400-500", "Work Sans:wght@300-600"]
  },
  "type_scale": {
    "cover_h1": "232px / weight:500 / line-height:0.92 / tracking:-0.02em",
    "display": "188px / weight:500 / line-height:0.95 / tracking:-0.015em",
    "title": "124px / weight:500 / line-height:0.98",
    "closer_h2": "168px / weight:500 / line-height:0.95",
    "numbers_big": "320px / weight:500 (spanning 2 cols)",
    "numbers_stat": "200px / weight:500 / line-height:0.9",
    "quote_block": "88px / weight:500 / line-height:1.05",
    "subtitle": "44px / weight:500 / line-height:1.1",
    "body": "26px / weight:400 / line-height:1.5",
    "method_step_num": "92px / weight:500 ('Caveat'-style italic)",
    "eyebrow": "28px / weight:400"
  },
  "spacing": {
    "horizontal_margin": "80px",
    "vertical_margin": "48-60px",
    "grid_gap": "24-28px",
    "card_padding": "36-64px",
    "border_radius": "22-36px (large rounded corners)"
  },
  "decorative_elements": [
    "Large rounded corner cards (border-radius:22-36px)",
    "Soft pastel color blocks (pink, lemon, blush, sage)",
    "Drop-cap first-letter styling (132px float:left)",
    "Dashed borders for subtle separation",
    "Swatch circles on cover (56px border-radius:50%)",
    "Color legend swatches (rectangular with border-radius:6px)",
    "Pill badges (border-radius:999px)",
    "Frosted glass card backgrounds (rgba(255,255,255,0.55))",
    "Lemon action banner across top",
    "Serif italic for emphasis (<em> tags, weight:400/italic)"
  ],
  "layout": {
    "dimensions": "1920×1080 (fixed, deck-stage.js)",
    "grid_system": "4-column method steps, 3-column insight cards, 2-column next actions, 12-column design system grid, 3-column consult",
    "density": "medium",
    "navigation": "deck-stage.js"
  }
}
```

---

## 32. stencil-tablet

```json
{
  "name": "stencil-tablet",
  "title": "Stencil & Tablet — Slide Template",
  "scheme": "mixed (bone/light default + black dark slides)",
  "colors": {
    "background": "#E2DCC9",
    "background_dark": "#000000",
    "background_paper": "#F4EFE0",
    "primary_accent": "#C73B7A",
    "secondary_accent": "#EE7A2E",
    "additional": {
      "sienna": "#A06A3C",
      "teal": "#2D7E73",
      "blue": "#3F73B7",
      "mustard": "#D8A93B",
      "olive": "#6F7A2E"
    },
    "text_primary": "#0A0A0A",
    "text_dark_mode": "#E2DCC9"
  },
  "fonts": {
    "display": "'Stardos Stencil', serif",
    "display_alt": "'Bowlby One', serif",
    "condensed": "'Barlow Condensed', sans-serif",
    "body": "'Inter', sans-serif",
    "google_fonts": ["Bowlby One", "Stardos Stencil:wght@400;700", "Barlow Condensed:wght@500-900", "Inter:wght@400-600"]
  },
  "type_scale": {
    "cover_h1": "220px / 'Stardos Stencil' / weight:700 / line-height:0.82 / uppercase / tracking:-0.015em",
    "section_num": "540px / 'Stardos Stencil' / weight:700 / line-height:0.8 / color:orange",
    "principles_num": "240px / 'Stardos Stencil' / weight:700 / line-height:0.85",
    "tablet_num": "220px / 'Stardos Stencil' / weight:700 / line-height:0.9",
    "stats_big": "160px / 'Stardos Stencil' / weight:700 / line-height:0.85",
    "section_title": "120px / 'Stardos Stencil' / weight:700 / line-height:0.92",
    "process_h2": "92px / 'Stardos Stencil' / weight:700 / line-height:0.92",
    "quote_block": "60px / 'Stardos Stencil' / weight:400 / line-height:1.05",
    "quote_mark": "320px / 'Bowlby One' / line-height:0.8",
    "chrome_top": "32px / 'Barlow Condensed' / weight:800 / uppercase / tracking:0.04em",
    "card_h3": "30px / 'Stardos Stencil' / weight:700 / uppercase",
    "body": "22px / 'Inter' / line-height:1.4",
    "pill": "18px / 'Barlow Condensed' / weight:700 / tracking:0.08em"
  },
  "spacing": {
    "horizontal_margin": "64px",
    "vertical_top": "48px",
    "vertical_bottom": "36px",
    "grid_gap": "22-28px",
    "card_padding": "30-38px",
    "border_radius": "14-26px"
  },
  "decorative_elements": [
    "Organic SVG shapes on agenda slides (figure-8, octagon, hourglass, pinched-X)",
    "Large stencil numerals as graphic objects (220-540px)",
    "Pill-shaped badges (border-radius:999px, 6-16px padding)",
    "Rounded tablet cards (border-radius:26px)",
    "Color-coded process nodes (5 distinct colors)",
    "SVG arrow connectors between process steps",
    "Dashed borders for table cells",
    "Dark slide section dividers with oversized stencil numbers",
    "Magenta quote panel with rounded corners",
    "Orange rounded square mark (56×56px, border-radius:14px)",
    "Teal organic SVG shape on cover (right-aligned)",
    "Barlow Condensed heavy uppercase labels"
  ],
  "layout": {
    "dimensions": "1920×1080 (deck-stage.js)",
    "grid_system": "4-column agenda/principles, 5-column process, 3-column stats, 2-column CTA",
    "density": "high (agency-style, bold typography)",
    "navigation": "deck-stage.js"
  }
}
```

---

## 33. studio

```json
{
  "name": "studio",
  "title": "Studio Presentation",
  "scheme": "mixed (dark near-black + acid yellow)",
  "colors": {
    "background_dark": "#1c1c1c",
    "background_dark_alt": "#242422",
    "background_light": "#f5d200",
    "background_light_alt": "#f0cc00",
    "primary_accent": "#f5d200",
    "text_dark_primary": "#f5d200",
    "text_dark_secondary": "rgba(245, 210, 0, 0.58)",
    "text_dark_tertiary": "rgba(245, 210, 0, 0.32)",
    "text_light_primary": "#1c1c1c",
    "text_light_secondary": "rgba(28, 28, 28, 0.62)",
    "text_light_tertiary": "rgba(28, 28, 28, 0.35)",
    "border_dark": "#2e2e2c",
    "border_light": "rgba(28, 28, 28, 0.18)"
  },
  "fonts": {
    "display": "'Barlow', 'Noto Sans SC', sans-serif",
    "heading": "'Barlow', 'Noto Sans SC', sans-serif",
    "body": "'Barlow', 'Noto Sans SC', system-ui, sans-serif",
    "mono": "'IBM Plex Mono', monospace",
    "google_fonts": ["Barlow:wght@400-900", "IBM Plex Mono:wght@300-500", "Noto Sans SC:wght@400-900"]
  },
  "type_scale": {
    "display": "12vw / weight:900 / line-height:0.9 / uppercase / tracking:-0.02em",
    "h1": "7.5vw / weight:900 / line-height:0.92 / uppercase / tracking:-0.02em",
    "h2": "4.8vw / weight:900 / line-height:0.95 / uppercase / tracking:-0.01em",
    "h3": "2.8vw / weight:700 / line-height:1.1 / uppercase",
    "lead": "1.6vw / weight:500 / line-height:1.45",
    "body": "1.15vw / weight:400 / line-height:1.6",
    "caption": "0.85vw / weight:400 / line-height:1.5",
    "label": "0.72vw / weight:500 / 'IBM Plex Mono' / tracking:0.06em",
    "stat_value": "5.5vw / weight:900 / line-height:0.9 / uppercase / tracking:-0.03em",
    "quote_text": "3.8vw / weight:900 / line-height:1.05 / uppercase / tracking:-0.02em"
  },
  "spacing": {
    "pad_x": "5vw",
    "pad_y": "5vh",
    "gap_lg": "3.5vh",
    "gap_md": "2vh",
    "gap_sm": "1vh"
  },
  "decorative_elements": [
    "NO decorative elements — type IS the design",
    "Em-dash (—) bullet markers in accent color",
    "Three-column metadata footer on cover (mono, border-top)",
    "2px heavy baselines on charts",
    "2px heavy dividers in compare panels",
    "Image placeholder boxes (dark bg, mono label)",
    "Chrome bars with thin 1px borders"
  ],
  "layout": {
    "dimensions": "100vw × 100vh per slide (horizontal strip deck)",
    "grid_system": "1fr 1fr splits, 3-column stats, 2fr 3fr list layout, 1fr 1fr compare",
    "density": "high (type fills slides, agency urgency)",
    "navigation": "horizontal translateX with nav dots + counter",
    "animation": "5 types with 7-step stagger (same engine as Signal)"
  }
}
```

---

## 34. vellum

```json
{
  "name": "vellum",
  "title": "Vellum Presentation",
  "scheme": "dark-only (deep navy + warm yellow, .light aliased to .dark)",
  "colors": {
    "background": "#2a3870",
    "background_alt": "#343f80",
    "primary_accent": "#3a7878",
    "emphasis": "#F5E168",
    "text_primary": "#E8D85C",
    "text_secondary": "rgba(232, 216, 92, 0.62)",
    "text_tertiary": "rgba(232, 216, 92, 0.32)",
    "border": "rgba(232, 216, 92, 0.20)",
    "compare_left_bg": "#1f2858",
    "compare_right_bg": "#34407a"
  },
  "fonts": {
    "display": "'Cormorant Garamond', 'Noto Serif SC', Georgia, serif",
    "heading": "'Cormorant Garamond', 'Noto Serif SC', Georgia, serif",
    "body": "'DM Sans', 'Noto Sans SC', system-ui, sans-serif",
    "mono": "'Courier Prime', 'Courier New', monospace",
    "annotation": "'Courier Prime', 'Courier New', monospace",
    "google_fonts": ["Cormorant Garamond:ital,wght@0,400-600;1,300-600", "DM Sans:wght@300-500", "Courier Prime:wght@400;700", "Noto Serif SC:wght@300-500", "Noto Sans SC:wght@400-500"]
  },
  "type_scale": {
    "display": "11vw / weight:400 / italic / line-height:0.92 / tracking:-0.01em",
    "h1": "7vw / weight:400 / italic / line-height:0.95",
    "h2": "4vw / weight:400 / italic / line-height:1.05",
    "h3": "2.4vw / weight:500 / italic / line-height:1.15",
    "lead": "1.5vw / weight:400 / line-height:1.6",
    "body": "1.05vw / weight:400 / line-height:1.65",
    "caption": "0.85vw / weight:400 / line-height:1.5",
    "label": "0.72vw / weight:400 / 'Courier Prime' / tracking:0.06em",
    "stat_value": "5.5vw / weight:400 / italic / line-height:1 / tracking:-0.02em",
    "quote_mark": "7vw / weight:400 / italic / line-height:0.6 / color:teal",
    "quote_text": "3.2vw / weight:400 / italic / line-height:1.25",
    "pin_note": "1.15vw / weight:500 / 'Courier Prime' / line-height:1.5 / color:teal"
  },
  "spacing": {
    "pad_x": "6vw",
    "pad_y": "6vh",
    "gap_lg": "5vh",
    "gap_md": "3vh",
    "gap_sm": "1.5vh"
  },
  "decorative_elements": [
    "Pin-annotation notes (bottom-left, Courier Prime, teal color)",
    "Teal quote-mark glyph at 7vw (the only use of --c-accent)",
    "Counter-reset numbered bullet list (teal numbers in mono)",
    "Italic serif headlines with roman <em> emphasis in brighter yellow (#F5E168)",
    "Short rule lines (28px×1px, teal)",
    "Kicker labels (mono, uppercase, teal)",
    "Dashed borders in charts (1px rgba yellow)",
    "Compare panels in two navy shades (#1f2858 vs #34407a)",
    "NO animation (--dur-slide:0s, --dur-enter:0s) — fully static"
  ],
  "layout": {
    "dimensions": "100vw × 100vh per slide (horizontal strip deck)",
    "grid_system": "centered float layout, 3-column stats, 2-column compare, horizontal bar chart",
    "density": "low-medium (generous spacing, breathing room)",
    "navigation": "horizontal translateX with nav dots + counter + wheel lock"
  }
}
```

---

## Summary Table

| # | Template | Scheme | Display Font | Primary Accent | Body Font | deck-stage? |
|---|----------|--------|-------------|----------------|-----------|-------------|
| 25 | raw-grid | light | system-ui (no GF) | #f2d4cf pink | system-ui | No |
| 26 | retro-windows | light | Press Start 2P | #000080 navy | MS Sans Serif | No |
| 27 | retro-zine | light | Bebas Neue | #008F4D green | Space Grotesk | No |
| 28 | sakura-chroma | light | Big Shoulders Display | #E5392A red | Albert Sans | No |
| 29 | scatterbrain | light | Shrikhand | #ffe066 yellow | Zilla Slab | No |
| 30 | signal | mixed | Source Serif 4 | #c8a870 gold | DM Sans | No |
| 31 | soft-editorial | light | Cormorant Garamond | #E1A4C2 dusty pink | Work Sans | Yes |
| 32 | stencil-tablet | mixed | Stardos Stencil | #C73B7A magenta | Inter | Yes |
| 33 | studio | mixed | Barlow 900 | #f5d200 acid yellow | Barlow 400 | No |
| 34 | vellum | dark-only | Cormorant Garamond italic | #3a7878 dusty teal | DM Sans | No |