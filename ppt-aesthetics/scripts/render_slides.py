#!/usr/bin/env python3
"""
PPT Slide Renderer — convert PPTX to one PNG per slide.

Usage:
    python render_slides.py <pptx_path> [--output-dir OUT] [--dpi 150]
                            [--method auto|libreoffice|powerpoint]
                            [--slides 1,3,5]

Render strategies (auto picks the first that works):
  - libreoffice : soffice --headless --convert-to pdf, then PyMuPDF -> PNG.
                  Cross-platform, works in headless/sandboxed environments.
                  Fidelity is slightly lower than native PowerPoint
                  (some SmartArt, fonts, gradients may differ).
  - powerpoint  : PowerPoint COM automation (pywin32). Windows + installed
                  PowerPoint only. Highest fidelity. Requires a desktop
                  session (does NOT work inside a headless sandbox).

Output:
    <output-dir>/slide_001.png ... slide_NNN.png
    <output-dir>/render_manifest.json (records method, dpi, slide count, paths)

Dependencies:
    pip install python-pptx Pillow PyMuPDF
    Optional (for powerpoint method): pip install pywin32
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

EMU_PER_INCH = 914400


# --------------------------------------------------------------------------- #
# Renderer: LibreOffice (soffice) → PDF → PyMuPDF → PNG
# --------------------------------------------------------------------------- #
def _find_soffice() -> str | None:
    """Locate the LibreOffice executable on Windows / Linux / macOS."""
    candidates = [
        shutil.which("soffice"),
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        "/usr/bin/soffice",
        "/usr/bin/libreoffice",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None


def _convert_pptx_to_pdf_libreoffice(
    pptx_path: str, out_dir: str, timeout: int = 120
) -> str:
    """Convert a single PPTX to PDF using LibreOffice headless. Returns PDF path."""
    soffice = _find_soffice()
    if not soffice:
        raise RuntimeError(
            "LibreOffice (soffice) not found. Install LibreOffice or use --method powerpoint."
        )

    # LibreOffice refuses to run two instances in parallel; use a unique
    # user-installation profile to avoid clashes with a running GUI instance.
    profile_dir = os.path.join(tempfile.gettempdir(), f"lo_profile_{os.getpid()}")
    cmd = [
        soffice,
        "--headless",
        "--nologo",
        "--nofirststartwizard",
        "--norestore",
        f"-env:UserInstallation=file:///{profile_dir.replace(os.sep, '/')}",
        "--convert-to",
        "pdf",
        "--outdir",
        out_dir,
        pptx_path,
    ]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout, check=False
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"LibreOffice conversion failed (rc={proc.returncode}):\n"
            f"stdout: {proc.stdout}\nstderr: {proc.stderr}"
        )

    pdf_path = os.path.join(out_dir, Path(pptx_path).stem + ".pdf")
    if not os.path.exists(pdf_path):
        raise RuntimeError(f"Expected PDF not found: {pdf_path}")
    return pdf_path


def _pdf_to_pngs_pymupdf(
    pdf_path: str, out_dir: str, dpi: int, slide_indices: list[int] | None = None
) -> list[str]:
    """Render each PDF page to PNG. slide_indices are 1-indexed; None = all."""
    import fitz  # PyMuPDF

    zoom = dpi / 72.0  # 72 = base PDF DPI
    matrix = fitz.Matrix(zoom, zoom)
    paths: list[str] = []
    with fitz.open(pdf_path) as doc:
        total = len(doc)
        indices = slide_indices or list(range(1, total + 1))
        for idx in indices:
            if idx < 1 or idx > total:
                print(f"  warn: slide {idx} out of range (1..{total}), skipping",
                      file=sys.stderr)
                continue
            page = doc[idx - 1]
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            out_png = os.path.join(out_dir, f"slide_{idx:03d}.png")
            pix.save(out_png)
            paths.append(out_png)
    return paths


def render_with_libreoffice(
    pptx_path: str, out_dir: str, dpi: int, slide_indices: list[int] | None = None
) -> list[str]:
    """Full LibreOffice pipeline: PPTX → PDF → PNGs. Returns list of PNG paths."""
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = _convert_pptx_to_pdf_libreoffice(pptx_path, out_dir)
    pngs = _pdf_to_pngs_pymupdf(pdf_path, out_dir, dpi, slide_indices)
    # Keep the PDF around (useful for downstream tooling); do not delete.
    return pngs


# --------------------------------------------------------------------------- #
# Renderer: PowerPoint COM (Windows only, highest fidelity)
# --------------------------------------------------------------------------- #
def render_with_powerpoint(
    pptx_path: str, out_dir: str, dpi: int, slide_indices: list[int] | None = None
) -> list[str]:
    """Render each slide via PowerPoint COM (pywin32). Windows-only."""
    try:
        import win32com.client  # noqa: F401
        import pythoncom
    except ImportError as e:
        raise RuntimeError(
            "pywin32 not installed. Run: pip install pywin32"
        ) from e

    os.makedirs(out_dir, exist_ok=True)
    abs_pptx = os.path.abspath(pptx_path)
    abs_out = os.path.abspath(out_dir)

    # Slide width × height in EMU determines pixel dimensions at chosen DPI.
    # Read them from python-pptx so we honor the deck's actual aspect ratio.
    from pptx import Presentation
    from pptx.util import Emu

    prs_tmp = Presentation(abs_pptx)
    sw_in = prs_tmp.slide_width / EMU_PER_INCH
    sh_in = prs_tmp.slide_height / EMU_PER_INCH
    px_w = int(round(sw_in * dpi))
    px_h = int(round(sh_in * dpi))

    pythoncom.CoInitialize()
    ppt = None
    pres = None
    try:
        ppt = win32com.client.Dispatch("PowerPoint.Application")
        ppt.DisplayAlerts = 0
        # WithWindow=False avoids flashing a window but may fail in some
        # security contexts; fall back to WithWindow=True if needed.
        try:
            pres = ppt.Presentations.Open(abs_pptx, WithWindow=False)
        except Exception:
            pres = ppt.Presentations.Open(abs_pptx, WithWindow=True)

        total = pres.Slides.Count
        indices = slide_indices or list(range(1, total + 1))
        paths: list[str] = []
        for idx in indices:
            if idx < 1 or idx > total:
                print(f"  warn: slide {idx} out of range (1..{total}), skipping",
                      file=sys.stderr)
                continue
            slide = pres.Slides(idx)
            out_png = os.path.join(abs_out, f"slide_{idx:03d}.png")
            slide.Export(out_png, "PNG", px_w, px_h)
            paths.append(out_png)
        return paths
    finally:
        if pres is not None:
            try:
                pres.Close()
            except Exception:
                pass
        if ppt is not None:
            try:
                ppt.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


# --------------------------------------------------------------------------- #
# Method auto-selection
# --------------------------------------------------------------------------- #
def render_pptx(
    pptx_path: str,
    out_dir: str,
    dpi: int = 150,
    method: str = "auto",
    slides: str | None = None,
) -> dict:
    """Render PPTX to PNGs. Returns a manifest dict."""
    pptx_path = os.path.abspath(pptx_path)
    if not os.path.exists(pptx_path):
        raise FileNotFoundError(pptx_path)
    os.makedirs(out_dir, exist_ok=True)

    slide_indices = None
    if slides:
        slide_indices = [
            int(s.strip()) for s in slides.split(",") if s.strip().isdigit()
        ]

    # Try methods in priority order when method == "auto".
    if method == "auto":
        # Prefer PowerPoint when a desktop session is available (better fonts,
        # better SmartArt). Fall back to LibreOffice in headless/sandbox envs.
        attempted: list[tuple[str, str]] = []
        for m in ("powerpoint", "libreoffice"):
            try:
                return _dispatch(m, pptx_path, out_dir, dpi, slide_indices)
            except Exception as e:
                attempted.append((m, str(e)))
                continue
        raise RuntimeError(
            "All render methods failed:\n" +
            "\n".join(f"  - {m}: {e}" for m, e in attempted)
        )

    return _dispatch(method, pptx_path, out_dir, dpi, slide_indices)


def _dispatch(method, pptx_path, out_dir, dpi, slide_indices) -> dict:
    if method == "libreoffice":
        paths = render_with_libreoffice(pptx_path, out_dir, dpi, slide_indices)
    elif method == "powerpoint":
        paths = render_with_powerpoint(pptx_path, out_dir, dpi, slide_indices)
    else:
        raise ValueError(f"Unknown method: {method!r}")

    return {
        "pptx_path": pptx_path,
        "method": method,
        "dpi": dpi,
        "slide_count": len(paths),
        "slides": paths,
    }


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(
        description="Render PPTX slides to PNG images for visual scoring."
    )
    ap.add_argument("pptx_path", help="Path to the .pptx file")
    ap.add_argument(
        "--output-dir", "-o", default=None,
        help="Output directory (default: <pptx>_slides/ next to the file)"
    )
    ap.add_argument(
        "--dpi", type=int, default=150,
        help="Output resolution DPI (default: 150; use 200+ for crisp text)"
    )
    ap.add_argument(
        "--method", choices=["auto", "libreoffice", "powerpoint"], default="auto",
        help="Render backend (default: auto — tries powerpoint then libreoffice)"
    )
    ap.add_argument(
        "--slides", "-s", default=None,
        help="Comma-separated 1-indexed slide numbers (default: all)"
    )
    args = ap.parse_args()

    out_dir = args.output_dir or os.path.join(
        os.path.dirname(os.path.abspath(args.pptx_path)),
        Path(args.pptx_path).stem + "_slides",
    )

    t0 = time.time()
    manifest = render_pptx(
        args.pptx_path, out_dir, dpi=args.dpi, method=args.method, slides=args.slides
    )
    elapsed = time.time() - t0

    manifest["output_dir"] = out_dir
    manifest["elapsed_seconds"] = round(elapsed, 2)

    # Write manifest JSON next to the PNGs.
    manifest_path = os.path.join(out_dir, "render_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"Rendered {manifest['slide_count']} slide(s) via {manifest['method']} "
          f"in {elapsed:.1f}s at {manifest['dpi']} DPI")
    print(f"Output: {out_dir}")
    print(f"Manifest: {manifest_path}")
    for p in manifest["slides"]:
        size_kb = os.path.getsize(p) // 1024
        print(f"  {os.path.basename(p)}  ({size_kb} KB)")


if __name__ == "__main__":
    main()
