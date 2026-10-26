#!/usr/bin/env python3
"""Verify published repository files against their SHA-256 manifest.

Git may normalize CRLF to LF (or LF to CRLF) when files move between
Windows and Linux. We allow only this byte-level EOL equivalence; other
content modifications still fail integrity verification.
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf8"))


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def matches_manifest(data, expected):
    if sha256(data) == expected:
        return True
    # Only canonical newline conversions may be regarded as equivalent.
    # Preserve the actual bytes for all remaining content checks.
    if b"\n" not in data:
        return False
    lf = data.replace(b"\r\n", b"\n")
    return sha256(lf) == expected or sha256(lf.replace(b"\n", b"\r\n")) == expected


def is_project_file(path):
    rel = path.relative_to(ROOT)
    return (
        path.is_file()
        and not any(part in {".git", "__pycache__", ".pytest_cache"} for part in rel.parts)
        and path.name != "manifest.json"
        and path.suffix != ".pyc"
    )


issues = []
for rel, expected in manifest["files"].items():
    path = ROOT / rel
    if not path.is_file():
        issues.append(f"MISSING {rel}")
        continue
    if not matches_manifest(path.read_bytes(), expected):
        issues.append(f"HASH MISMATCH {rel}")

actuals = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if is_project_file(p)}
for rel in sorted(actuals - set(manifest["files"])):
    issues.append(f"UNTRACKED {rel}")
for issue in issues:
    print(issue)
print(f"Verified {len(manifest['files'])} manifest entries; unexpected/missing/hash errors: {len(issues)}")
sys.exit(bool(issues))
