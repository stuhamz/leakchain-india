#!/usr/bin/env python3
"""Verify every hash in archive manifest.json against actual files; no network needed."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf8'))
issues=[]
for rel,expected in manifest['files'].items():
 p=ROOT/rel
 if not p.is_file():issues.append(f'MISSING {rel}');continue
 actual=hashlib.sha256(p.read_bytes()).hexdigest()
 if actual!=expected:issues.append(f'HASH MISMATCH {rel}')
actuals={str(f.relative_to(ROOT)) for f in ROOT.rglob('*') if f.is_file() and f.name!='manifest.json' and '__pycache__' not in f.parts and '.pyc' not in f.suffix}
untracked=actuals-set(manifest['files'])
if untracked:issues.extend(f'UNTRACKED {x}' for x in sorted(untracked))
for issue in issues:print(issue)
print(f"Verified {len(manifest['files'])} manifest entries; unexpected/missing/hash errors: {len(issues)}")
sys.exit(bool(issues))
