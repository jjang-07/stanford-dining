#!/usr/bin/env python3
"""Turn menus.json into a single static page at site/index.html."""
import json
import pathlib

import classify
import highlights

root = pathlib.Path(__file__).parent
data = highlights.apply(classify.categorize(json.loads((root / "menus.json").read_text())))
payload = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
html = (root / "template.html").read_text().replace("/*__DATA__*/null", payload)
out = root / "site" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html)
print(f"Wrote {out} ({len(html) // 1024} KB)")
