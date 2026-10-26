#!/usr/bin/env python3
"""Recompute SHA-256 manifest of all repository files for integrity checks."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
files={}
for p in sorted(ROOT.rglob('*')):
 if not p.is_file() or p.name=='manifest.json' or '__pycache__' in p.parts or '.git' in p.parts or p.suffix=='.pyc':continue
 files[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
output={'schema_version':'1.0','dataset_version':'0.9','interface_version':'0.9.1','files':files}
(ROOT/'manifest.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(f'Updated integrity manifest with {len(files)} entries.')
