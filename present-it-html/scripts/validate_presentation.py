#!/usr/bin/env python3
"""Validate the structural and offline quality bar for present-it-html output."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_IDS = (
    "executive-summary", "problem", "investigation", "plan", "implementation",
    "validation", "review", "cleanup", "takeaways", "sources",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", help="presentation HTML file")
    args = parser.parse_args()

    path = Path(args.html)
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    errors: list[str] = []

    if "<!doctype html" not in lower:
        errors.append("missing HTML5 doctype")
    for token, message in (
        ("<html", "missing html element"),
        ("<title", "missing title"),
        ("<main", "missing main landmark"),
        ("<nav", "missing navigation landmark"),
        ("@media print", "missing print stylesheet"),
    ):
        if token not in lower:
            errors.append(message)
    if not re.search(r"<meta\b[^>]*\bname\s*=\s*(['\"])viewport\1", text, re.IGNORECASE):
        errors.append("missing viewport metadata")

    for section_id in REQUIRED_IDS:
        pattern = rf"\bid\s*=\s*(['\"]){re.escape(section_id)}\1"
        if not re.search(pattern, text, re.IGNORECASE):
            errors.append(f"missing required section id: {section_id}")

    remote_asset_patterns = (
        r"<(?:script|img)\b[^>]*\bsrc\s*=\s*['\"]\s*(?:https?:)?//",
        r"<link\b[^>]*\bhref\s*=\s*['\"]\s*(?:https?:)?//",
        r"url\(\s*['\"]?\s*(?:https?:)?//",
    )
    if any(re.search(pattern, text, re.IGNORECASE) for pattern in remote_asset_patterns):
        errors.append("remote asset dependency found")

    for tag in re.findall(r"<img\b[^>]*>", text, re.IGNORECASE):
        if not re.search(r"\balt\s*=\s*(['\"]).*?\1", tag, re.IGNORECASE | re.DOTALL):
            errors.append("image without alt text")
            break

    for svg in re.findall(r"<svg\b.*?</svg>", text, re.IGNORECASE | re.DOTALL):
        if not re.search(r"<title\b", svg, re.IGNORECASE):
            errors.append("SVG without title")
            break

    visual_types = {
        "svg": bool(re.search(r"<svg\b", text, re.IGNORECASE)),
        "table": bool(re.search(r"<table\b", text, re.IGNORECASE)),
        "figure": bool(re.search(r"<figure\b", text, re.IGNORECASE)),
        "code": bool(re.search(r"<(?:pre|code)\b", text, re.IGNORECASE)),
    }
    if sum(visual_types.values()) < 2:
        errors.append("fewer than two distinct visual types")

    if re.search(r"\{\{.*?\}\}|\[TODO\]|\bTODO\b", text, re.IGNORECASE | re.DOTALL):
        errors.append("unresolved placeholder found")
    if len(text.encode("utf-8")) < 2500:
        errors.append("presentation is too small to contain the required briefing")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    used = ", ".join(name for name, present in visual_types.items() if present)
    print(f"Presentation valid: {path} ({used})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
