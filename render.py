#!/usr/bin/env python3
"""Turn menus.json into a single static page at site/index.html."""
import json
import pathlib

import classify
import highlights
import nutrition

root = pathlib.Path(__file__).parent
data = nutrition.apply(highlights.apply(classify.categorize(json.loads((root / "menus.json").read_text()))))
if data.get("nutrition_fallbacks"):
    print("No nutrition estimate for", len(data["nutrition_fallbacks"]), "dishes (add a rule in nutrition.py):", ", ".join(data["nutrition_fallbacks"]))
payload = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
html = (root / "template.html").read_text().replace("/*__DATA__*/null", payload)
out = root / "site" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html)
for name in ("specials.html", "favicon.svg"):
    (out.parent / name).write_text((root / name).read_text())
print(f"Wrote {out} ({len(html) // 1024} KB)")
