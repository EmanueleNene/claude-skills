#!/usr/bin/env python3
"""Embed local image sources into an HTML file as data URIs."""

from __future__ import annotations

import argparse
import base64
import mimetypes
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


IMG_SRC = re.compile(
    r"(<img\b[^>]*?\bsrc\s*=\s*)(['\"])([^'\"]+)\2",
    re.IGNORECASE,
)


def contained(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", help="HTML file to process")
    parser.add_argument("--asset-root", default=None,
                        help="maximum directory boundary; defaults to HTML directory")
    parser.add_argument("--in-place", action="store_true", help="replace the input file")
    parser.add_argument("--output", help="output file when not using --in-place")
    args = parser.parse_args()

    html_path = Path(args.html).resolve(strict=True)
    asset_root = Path(args.asset_root).resolve(strict=True) if args.asset_root else html_path.parent
    if not asset_root.is_dir():
        print(f"error: asset root is not a directory: {asset_root}", file=sys.stderr)
        return 1
    if args.in_place and args.output:
        print("error: choose --in-place or --output, not both", file=sys.stderr)
        return 1
    output_path = html_path if args.in_place else Path(args.output or html_path.with_name(
        html_path.stem + "_embedded" + html_path.suffix
    ))

    source = html_path.read_text(encoding="utf-8")
    embedded = 0
    failures: list[str] = []

    def replace(match: re.Match[str]) -> str:
        nonlocal embedded
        raw_src = match.group(3).strip()
        lowered = raw_src.lower()
        if lowered.startswith(("data:", "http://", "https://", "//", "#")):
            return match.group(0)

        local_value = unquote(urlsplit(raw_src).path)
        candidates = [html_path.parent / local_value, asset_root / local_value]
        asset = None
        for candidate in candidates:
            resolved = candidate.resolve(strict=False)
            if contained(resolved, asset_root) and resolved.is_file():
                asset = resolved
                break
        if asset is None:
            failures.append(raw_src)
            return match.group(0)

        mime, _ = mimetypes.guess_type(asset.name)
        if not mime or not mime.startswith("image/"):
            failures.append(raw_src)
            return match.group(0)
        payload = base64.b64encode(asset.read_bytes()).decode("ascii")
        embedded += 1
        return f"{match.group(1)}{match.group(2)}data:{mime};base64,{payload}{match.group(2)}"

    result = IMG_SRC.sub(replace, source)
    if failures:
        print("error: could not embed: " + ", ".join(sorted(set(failures))), file=sys.stderr)
        return 1
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result, encoding="utf-8")
    print(f"Embedded {embedded} image(s): {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
