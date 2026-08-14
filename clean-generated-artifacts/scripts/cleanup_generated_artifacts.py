#!/usr/bin/env python3
"""Policy-driven, manifest-based cleanup for generated workspace artifacts."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = 1
CONFIRM_TOKEN = "DELETE-LISTED-GENERATED-ARTIFACTS"

CONTROL_DIR_NAMES = {".git", ".hg", ".svn", ".agents", ".codex"}
BROAD_SCAN_SKIP_NAMES = CONTROL_DIR_NAMES | {".venv", "venv", "node_modules"}
DEFAULT_DELETE_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
DEFAULT_DELETE_SUFFIXES = {".pyc", ".pyo"}
EVIDENCE_SUFFIXES = {
    ".log", ".out", ".err", ".txt", ".csv", ".json", ".xml", ".yaml", ".yml",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pdf", ".html", ".htm",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def contained(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def resolve_inside(value: str, root: Path, label: str) -> Path:
    raw = Path(value)
    resolved = (raw if raw.is_absolute() else root / raw).resolve(strict=False)
    if not contained(resolved, root):
        raise ValueError(f"{label} escapes workspace root: {value}")
    return resolved


def tracked_files(root: Path) -> set[str]:
    try:
        output = subprocess.check_output(
            ["git", "-C", str(root), "ls-files", "-z"],
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return set()
    return {
        item.decode("utf-8", errors="surrogateescape").replace("\\", "/")
        for item in output.split(b"\0") if item
    }


def matches(rel: str, patterns: list[str]) -> str | None:
    normalized = rel.replace("\\", "/")
    for pattern in patterns:
        candidate = pattern.replace("\\", "/")
        if (fnmatch.fnmatchcase(normalized, candidate)
                or fnmatch.fnmatchcase(normalized.lower(), candidate.lower())):
            return pattern
    return None


def exact_protection(path: Path, protected: list[Path]) -> Path | None:
    for candidate in protected:
        if path == candidate or candidate in path.parents:
            return candidate
    return None


def hard_protection(
    path: Path,
    rel: str,
    tracked: set[str],
    protected: list[Path],
    protect_globs: list[str],
) -> str | None:
    if rel in tracked:
        return "tracked by version control"
    exact = exact_protection(path, protected)
    if exact is not None:
        return f"explicit protected path: {exact}"
    pattern = matches(rel, protect_globs)
    if pattern:
        return f"protected by pattern: {pattern}"
    return None


def classify(
    path: Path,
    rel: str,
    tracked: set[str],
    protected: list[Path],
    protect_globs: list[str],
    delete_globs: list[str],
    review_globs: list[str],
) -> tuple[str, str]:
    protected_reason = hard_protection(path, rel, tracked, protected, protect_globs)
    if protected_reason:
        return "keep", protected_reason

    delete_pattern = matches(rel, delete_globs)
    if delete_pattern:
        return "delete", f"disposable by pattern: {delete_pattern}"
    review_pattern = matches(rel, review_globs)
    if review_pattern:
        return "review", f"review by pattern: {review_pattern}"

    parts_lower = {part.lower() for part in path.parts}
    if parts_lower & DEFAULT_DELETE_DIR_NAMES or path.suffix.lower() in DEFAULT_DELETE_SUFFIXES:
        return "delete", "conservative built-in cache rule"
    if path.suffix.lower() in EVIDENCE_SUFFIXES:
        return "review", "may contain diagnostic, result, or presentation evidence"
    return "review", "unknown generated artifact; requires an exact decision"


def iter_scope(scope: Path) -> list[Path]:
    if scope.is_symlink():
        return []
    if scope.is_file():
        return [scope]
    if not scope.exists():
        raise FileNotFoundError(f"scope does not exist: {scope}")
    if not scope.is_dir():
        return []

    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(scope, followlinks=False):
        current = Path(dirpath)
        dirnames[:] = [
            name for name in dirnames
            if name not in BROAD_SCAN_SKIP_NAMES and not (current / name).is_symlink()
        ]
        for name in filenames:
            candidate = current / name
            try:
                if not candidate.is_symlink():
                    files.append(candidate)
            except OSError:
                continue
    return files


def scan(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError(f"root is not a directory: {root}")

    manifest_path = resolve_inside(args.manifest, root, "manifest")
    scopes = [resolve_inside(value, root, "scope") for value in args.scope]
    for scope in scopes:
        rel_parts = set(scope.relative_to(root).parts) if scope != root else set()
        if rel_parts & CONTROL_DIR_NAMES:
            raise ValueError(f"scope enters a protected control directory: {scope}")

    protected = [resolve_inside(value, root, "protected path") for value in args.protect]
    if manifest_path not in protected:
        protected.append(manifest_path)
    tracked = tracked_files(root)

    unique: dict[str, Path] = {}
    for scope in scopes:
        for path in iter_scope(scope):
            try:
                resolved = path.resolve(strict=True)
                if contained(resolved, root):
                    unique.setdefault(relative_posix(resolved, root), resolved)
            except OSError:
                continue

    entries = []
    for rel, path in sorted(unique.items()):
        try:
            action, reason = classify(
                path, rel, tracked, protected, args.protect_glob,
                args.delete_glob, args.review_glob,
            )
            stat = path.stat()
            entries.append({
                "path": rel,
                "action": action,
                "reason": reason,
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            })
        except OSError:
            continue

    totals = Counter(entry["action"] for entry in entries)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "created_at": utc_now(),
        "root": str(root),
        "scopes": [relative_posix(scope, root) if scope != root else "." for scope in scopes],
        "policy": {
            "protect": [relative_posix(path, root) for path in protected],
            "protect_glob": args.protect_glob,
            "delete_glob": args.delete_glob,
            "review_glob": args.review_glob,
        },
        "summary": {
            "files": len(entries),
            "delete": totals["delete"],
            "review": totals["review"],
            "keep": totals["keep"],
            "delete_bytes": sum(e["size"] for e in entries if e["action"] == "delete"),
        },
        "entries": entries,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(
        f"Scanned {len(entries)} file(s): {totals['delete']} delete, "
        f"{totals['review']} review, {totals['keep']} keep"
    )
    print(f"Manifest: {manifest_path}")
    return 0


def same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left)) == os.path.normcase(str(right))


def apply_manifest(args: argparse.Namespace) -> int:
    if args.confirm != CONFIRM_TOKEN:
        raise ValueError(f"confirmation token must be exactly {CONFIRM_TOKEN}")

    root = Path(args.root).resolve(strict=True)
    manifest_path = resolve_inside(args.manifest, root, "manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported cleanup manifest schema")
    if not same_path(Path(manifest.get("root", "")).resolve(strict=False), root):
        raise ValueError("manifest root does not match --root")

    scopes = [resolve_inside(value, root, "manifest scope") for value in manifest.get("scopes", [])]
    if not scopes:
        raise ValueError("manifest has no explicit scopes")
    policy = manifest.get("policy", {})
    protected = [resolve_inside(value, root, "manifest protected path")
                 for value in policy.get("protect", [])]
    protect_globs = list(policy.get("protect_glob", []))
    tracked = tracked_files(root)
    results = Counter()
    deleted_bytes = 0
    candidate_parents: set[Path] = set()

    for entry in manifest.get("entries", []):
        if entry.get("action") != "delete":
            continue
        rel = str(entry.get("path", "")).replace("\\", "/")
        try:
            path = resolve_inside(rel, root, "entry")
        except ValueError:
            results["refused"] += 1
            continue
        if not any(path == scope or contained(path, scope) for scope in scopes):
            results["refused"] += 1
            continue
        if hard_protection(path, rel, tracked, protected, protect_globs) or path.is_symlink():
            results["refused"] += 1
            continue
        if not path.exists():
            results["missing"] += 1
            continue
        if not path.is_file():
            results["refused"] += 1
            continue
        stat = path.stat()
        if stat.st_size != entry.get("size") or stat.st_mtime_ns != entry.get("mtime_ns"):
            results["changed"] += 1
            continue

        path.unlink()
        results["deleted"] += 1
        deleted_bytes += stat.st_size
        parent = path.parent
        while parent != root and contained(parent, root):
            candidate_parents.add(parent)
            parent = parent.parent

    removed_dirs = 0
    for directory in sorted(candidate_parents, key=lambda item: len(item.parts), reverse=True):
        try:
            directory.rmdir()
            removed_dirs += 1
        except OSError:
            pass

    manifest["last_apply"] = {
        "applied_at": utc_now(),
        "deleted": results["deleted"],
        "deleted_bytes": deleted_bytes,
        "removed_empty_directories": removed_dirs,
        "refused": results["refused"],
        "changed": results["changed"],
        "missing": results["missing"],
    }
    temporary = manifest_path.with_suffix(manifest_path.suffix + ".tmp")
    temporary.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    temporary.replace(manifest_path)
    print(
        f"Deleted {results['deleted']} file(s), {deleted_bytes} byte(s); "
        f"refused {results['refused']}, changed {results['changed']}, missing {results['missing']}"
    )
    print(f"Manifest updated: {manifest_path}")
    return 0 if not results["refused"] and not results["changed"] else 2


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="write a dry-run cleanup manifest")
    scan_parser.add_argument("--root", required=True, help="workspace root")
    scan_parser.add_argument("--scope", action="append", required=True,
                             help="generated directory or exact file; repeat as needed")
    scan_parser.add_argument("--protect", action="append", default=[],
                             help="exact protected file or directory")
    scan_parser.add_argument("--protect-glob", action="append", default=[],
                             help="protected workspace-relative pattern")
    scan_parser.add_argument("--delete-glob", action="append", default=[],
                             help="known disposable workspace-relative pattern")
    scan_parser.add_argument("--review-glob", action="append", default=[],
                             help="pattern that must remain review by default")
    scan_parser.add_argument("--manifest", required=True, help="manifest path within root")
    scan_parser.set_defaults(handler=scan)

    apply_parser = subparsers.add_parser("apply", help="delete exact approved manifest entries")
    apply_parser.add_argument("--root", required=True, help="workspace root")
    apply_parser.add_argument("--manifest", required=True, help="approved manifest path")
    apply_parser.add_argument("--confirm", required=True, help="explicit confirmation token")
    apply_parser.set_defaults(handler=apply_manifest)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        return args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
