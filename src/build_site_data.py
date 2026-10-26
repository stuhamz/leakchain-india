#!/usr/bin/env python3
"""Embed the validated export for a zero-dependency offline/GitHub Pages app.
No network requests or sensitive incident images. Update after the source CSVs change.
"""
from pathlib import Path
import json
from export_ui_data import ROOT,build

def build_site():
    data=build()
    script='/* Generated from source CSVs. Do not edit manually. */\nwindow.LEAKCHAIN_DATA = '+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+';\n'
    out=ROOT/'assets'/'data.js'
    out.parent.mkdir(exist_ok=True)
    out.write_text(script,encoding='utf-8')
    print(f'Wrote {out.relative_to(ROOT)} ({out.stat().st_size:,} bytes)')
if __name__=='__main__':
    build_site()
