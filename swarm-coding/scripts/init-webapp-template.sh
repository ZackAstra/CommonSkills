#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  init-webapp-template.sh --list
  init-webapp-template.sh <project-dir> <project-title> [template-name] [--no-install]

Examples:
  init-webapp-template.sh --list
  init-webapp-template.sh ./app "Market Dashboard" 0-origin
  init-webapp-template.sh ./app "Gallery" airlens-style --no-install
EOF
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "$script_dir/.." && pwd)"
templates_dir="$skill_dir/assets/templates"

list_templates() {
  find "$templates_dir" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

if [[ "${1:-}" == "--list" ]]; then
  list_templates
  exit 0
fi

if [[ $# -lt 2 || $# -gt 4 ]]; then
  usage >&2
  exit 2
fi

project_dir="$1"
project_title="$2"
template_name="${3:-0-origin}"
install_deps=1

if [[ "${4:-}" == "--no-install" ]]; then
  install_deps=0
elif [[ $# -eq 4 ]]; then
  echo "Unknown option: $4" >&2
  usage >&2
  exit 2
fi

template_dir="$templates_dir/$template_name"
template_zip="$template_dir/$template_name.zip"
template_info="$template_dir/info.md"

if [[ ! -d "$template_dir" || ! -f "$template_zip" ]]; then
  echo "Template not found: $template_name" >&2
  echo "Available templates:" >&2
  list_templates >&2
  exit 1
fi

if [[ -e "$project_dir" && -n "$(ls -A "$project_dir" 2>/dev/null)" ]]; then
  echo "Project directory already exists and is not empty: $project_dir" >&2
  exit 1
fi

mkdir -p "$project_dir"
project_dir="$(cd "$project_dir" && pwd)"

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

unzip -q "$template_zip" -d "$tmp_dir"

source_dir="$tmp_dir"
if [[ -d "$tmp_dir/$template_name" ]]; then
  source_dir="$tmp_dir/$template_name"
else
  only_child="$(find "$tmp_dir" -mindepth 1 -maxdepth 1 -type d | head -n 1 || true)"
  if [[ -n "$only_child" && "$(find "$tmp_dir" -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')" == "1" ]]; then
    source_dir="$only_child"
  fi
fi

(shopt -s dotglob nullglob; cp -R "$source_dir"/* "$project_dir"/)

if [[ -f "$template_info" ]]; then
  cp "$template_info" "$project_dir/template-info.md"
fi

if [[ -f "$project_dir/index.html" ]]; then
  python3 - "$project_dir/index.html" "$project_title" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
title = sys.argv[2]
text = path.read_text(encoding="utf-8")
text = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", text, count=1, flags=re.S)
path.write_text(text, encoding="utf-8")
PY
fi

touch "$project_dir/.gitignore"
grep -qxF "node_modules" "$project_dir/.gitignore" || printf '\nnode_modules\n' >> "$project_dir/.gitignore"
grep -qxF "dist" "$project_dir/.gitignore" || printf 'dist\n' >> "$project_dir/.gitignore"

if [[ "$install_deps" -eq 1 && -f "$project_dir/package.json" ]]; then
  cd "$project_dir"
  echo "Installing dependencies in: $project_dir"
  if [[ -f pnpm-lock.yaml && -x "$(command -v pnpm)" ]]; then
    pnpm install --no-frozen-lockfile
  elif [[ -f yarn.lock && -x "$(command -v yarn)" ]]; then
    yarn install
  else
    npm install --no-audit --no-fund
  fi
fi

echo "Template '$template_name' initialized at: $project_dir"
if [[ -f "$project_dir/template-info.md" ]]; then
  echo "Template notes: $project_dir/template-info.md"
fi
