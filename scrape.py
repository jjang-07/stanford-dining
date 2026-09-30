#!/usr/bin/env python3
"""Fetch menus for your favorite Stanford dining halls and save them to menus.json.

Data source: Stanford R&DE's official Dining Hall Menu app.
Runs once a day, with a short pause between requests to be polite to the server.
"""
import datetime
import json
import sys
import time
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

URL = "https://rdeapps.stanford.edu/dininghallmenu/"
F = "ctl00$MainContent$"

# (value used by the menu app, name shown on the page)
HALLS = [
    ("Arrillaga", "Arrillaga"),
    ("Wilbur", "Wilbur"),
    ("Lakeside", "Lakeside"),
    ("FlorenceMoore", "Florence Moore"),
]
MEALS = ["Breakfast", "Brunch", "Lunch", "Dinner"]
PAUSE = 0.25  # seconds between requests

TAG_CLASSES = {
    "clsVGN_Row": "vegan",
    "clsV_Row": "vegetarian",
    "clsGF_Row": "gf",
    "clsHALAL_Row": "halal",
}

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (personal dining brief)"


def blank_form():
    r = session.get(URL, timeout=30)
    r.raise_for_status()
    return BeautifulSoup(r.text, "lxml")


def hidden_fields(soup):
    return {i["name"]: i.get("value", "") for i in soup.find_all("input", type="hidden")}


def clean(el, drop=()):
    if el is None:
        return ""
    for d in drop:
        for s in el.select(d):
            s.extract()
    return " ".join(el.get_text(" ", strip=True).split())


def parse_dishes(soup):
    dishes = []
    for li in soup.select("li.clsMenuItem"):
        name = clean(li.select_one(".clsLabel_Name"))
        if not name:
            continue
        classes = li.get("class", [])
        tags = [t for c, t in TAG_CLASSES.items() if c in classes]
        trace = clean(li.select_one(".clsLabel_TraceAllergens"))
        trace = trace.replace("Made on shared equipment with", "").strip()
        dishes.append(
            {
                "name": name,
                "description": clean(li.select_one(".clsLabel_Description")),
                "ingredients": clean(li.select_one(".clsLabel_Ingredients"), [".clsSectionName"]),
                "allergens": clean(
                    li.select_one(".clsLabel_Allergens"),
                    [".clsSectionName", ".clsSectionNameAllegens"],
                ),
                "shared": trace,
                "tags": tags,
            }
        )
    return dishes


def fetch(hall, day, meal, retries=3):
    for attempt in range(retries):
        try:
            soup = blank_form()
            data = hidden_fields(soup)
            data.update(
                {
                    "__EVENTTARGET": "",
                    "__EVENTARGUMENT": "",
                    F + "lstLocations": hall,
                    F + "lstDay": day,
                    F + "lstMealType": meal,
                    F + "btnRefresh": "Refresh",
                }
            )
            r = session.post(URL, data=data, timeout=30)
            r.raise_for_status()
            if "application error" in r.text:
                raise RuntimeError("server returned an error page")
            return parse_dishes(BeautifulSoup(r.text, "lxml"))
        except Exception as e:  # noqa: BLE001
            if attempt == retries - 1:
                print(f"  ! gave up on {hall} {day} {meal}: {e}", file=sys.stderr)
                return None
            time.sleep(2 * (attempt + 1))


def main():
    days_available = []
    for o in blank_form().select("#MainContent_lstDay option"):
        if o.get("value"):
            days_available.append((o["value"], o.text.strip()))
    if len(sys.argv) > 1:  # e.g. `python scrape.py 2` limits to the next 2 days (for testing)
        days_available = days_available[: int(sys.argv[1])]

    out = {
        "generated": datetime.datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(timespec="minutes"),
        "halls": [{"id": h, "name": n} for h, n in HALLS],
        "days": [],
    }
    failures = 0
    for value, label in days_available:
        print(label)
        day = {"date": value, "label": label, "menus": {}}
        for hall, _ in HALLS:
            day["menus"][hall] = {}
            for meal in MEALS:
                dishes = fetch(hall, value, meal)
                time.sleep(PAUSE)
                if dishes is None:
                    failures += 1
                elif dishes:
                    day["menus"][hall][meal] = dishes
        out["days"].append(day)

    total = sum(len(d) for day in out["days"] for m in day["menus"].values() for d in m.values())
    if total == 0 or failures > 20:
        sys.exit(f"Refusing to publish: {total} dishes found, {failures} failed requests.")
    with open("menus.json", "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"Saved {total} dishes across {len(out['days'])} days ({failures} failed requests).")


if __name__ == "__main__":
    main()
