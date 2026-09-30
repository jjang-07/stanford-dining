"""The catalog of foods visitors can choose to be alerted about.

The page lets each visitor tick the ones they care about (their picks are remembered in the browser).
Edit this list to add, rename, or remove options.

Each entry:
  id, label   the option's name in the picker
  short       (optional) shorter name used in the summary sentence
  tag         the little word shown on matching dishes and halls
  group       "Dishes" or "Cuisines", for layout in the picker
  pattern     regex matched against dish names (case-insensitive)   -- or --
  test        a function(dish) -> bool, for custom logic
Optional:
  halls       only look at these halls, e.g. ["Wilbur"]
  cats        only count dishes in these sections (main, protein, veg, other)
  usual_days  weekdays it usually happens (0=Mon ... 6=Sun), for things Stanford's menu site
              doesn't list. These appear as dashed "unconfirmed" days.
  note        small explanation shown under the row
  include_staples  set True to also match everyday standing items (burger bar, etc.)

Dishes that appear on most lunch and dinner menus (the standing bars) are ignored by default,
so highlights point at specials rather than things that are always there.
"""
import datetime
import re

import classify

MAIN = ["main", "protein"]

HIGHLIGHTS = [
    # ---- Dishes
    {"id": "steak", "label": "Steak", "tag": "steak", "group": "Dishes",
     "test": lambda d: classify.is_steak(d["name"])},
    {"id": "fried_chicken", "label": "Fried chicken and wings", "short": "Fried chicken", "tag": "fried chicken", "group": "Dishes",
     "pattern": r"fried chicken|chicken wings?|wings\b|chicken & waffles|chicken and waffles|general chicken|chicken tenders|nuggets|katsu|popcorn chicken"},
    {"id": "pizza", "label": "Pizza", "tag": "pizza", "group": "Dishes",
     "pattern": r"pizza|flatbread|calzone"},
    {"id": "sandwich", "label": "Burgers and sandwiches", "short": "Burgers and sandwiches", "tag": "sandwich", "group": "Dishes",
     "pattern": r"burger|sandwich|melt\b|grilled cheese|hot dog|po'?boy|banh mi|\bsub\b|gyro"},
    {"id": "pasta", "label": "Pasta and Italian", "short": "Pasta", "tag": "pasta", "group": "Dishes",
     "cats": MAIN,
     "pattern": r"ravioli|tortellini|lasagna|meatballs|parmesan|risotto|linguine|orecchiette|fettuccini|spaghetti|gnocchi|carbonara|bolognese|alfredo|pasta"},
    {"id": "seafood", "label": "Seafood", "tag": "seafood", "group": "Dishes",
     "pattern": r"\bfish\b|\bcod\b|salmon|shrimp|crab|cioppino|frutti di mare|seafood|tuna|scallop|mussel|clam|lobster|oyster|prawn|tilapia|halibut"},
    {"id": "comfort", "label": "Comfort food", "tag": "comfort", "group": "Dishes",
     "cats": MAIN + ["other"],
     "pattern": r"meatloaf|poutine|cheesy mac|mac and cheese|mac & cheese|chili con carne|\bchili\b|pot roast|fish & chips|fish and chips|mashed potatoes|pot pie|cornbread|biscuit|oxtail|stew|baked potato bar|cheese curds"},
    {"id": "sweet_breakfast", "label": "Sweet breakfast", "tag": "sweet breakfast", "group": "Dishes",
     "pattern": r"pancake|french toast|crepe|cinnamon|beignet|doughnut|donut|muffin|danish|churro|chicken & waffles"},

    # ---- Cuisines
    {"id": "korean", "label": "Korean", "tag": "korean", "group": "Cuisines",
     "pattern": r"korean|gochujang|bulgogi|kimchi|bibimbap|japchae|tteok|galbi|kalbi|bokkeum|jjigae|dakgalbi|doenjang|gochugaru"},
    {"id": "pho", "label": "Pho at Wilbur", "short": "Pho", "tag": "pho", "group": "Cuisines",
     "pattern": r"\bpho\b|phở", "halls": ["Wilbur"], "usual_days": [0, 2, 4],
     "note": "Not listed on Stanford's menu site. Dashed days follow the usual Mon, Wed, Fri schedule reported by the Stanford Daily in fall 2025."},
    {"id": "japanese", "label": "Japanese", "tag": "japanese", "group": "Cuisines",
     "cats": MAIN,
     "pattern": r"japanese|teriyaki|miso|sushi|ramen|udon|soba|yakisoba|tempura|katsu|agedashi|gyoza|donburi|okonomiyaki"},
    {"id": "chinese", "label": "Chinese", "tag": "chinese", "group": "Cuisines",
     "pattern": r"char siu|general chicken|szechuan|sichuan|kung pao|mapo|lo mein|chow mein|dumpling|dim sum|\bbao\b|egg roll|orange chicken|sweet and sour|mongolian|cantonese"},
    {"id": "curry", "label": "Curry and Indian", "short": "Curry", "tag": "curry", "group": "Cuisines",
     "pattern": r"curry|curried|masala|tikka|butter chicken|paneer|aloo|biryani|\bdal\b|korma|vindaloo"},
    {"id": "mexican", "label": "Mexican", "tag": "mexican", "group": "Cuisines",
     "pattern": r"taco|burrito|quesadilla|nacho|enchilada|fajita|carnitas|chilaquiles|sofritas|carne asada|tamale|pozole"},
    {"id": "mediterranean", "label": "Mediterranean", "tag": "mediterranean", "group": "Cuisines",
     "cats": MAIN,
     "pattern": r"shawarma|harissa|tagine|falafel|hummus|gyro|kebab|kofta|mezze|moroccan|mediterranean|shakshuka"},
    {"id": "caribbean", "label": "Caribbean", "tag": "caribbean", "group": "Cuisines",
     "pattern": r"jerk|jamaican|oxtail|plantain|rasta|caribbean|cuban|jollof"},
]


def _matcher(h):
    if "test" in h:
        return h["test"]
    rx = re.compile(h["pattern"], re.I)
    return lambda d: bool(rx.search(d["name"]))


def apply(data):
    """Tag each dish with the highlights it matches and add the catalog to the data."""
    matchers = {h["id"]: _matcher(h) for h in HIGHLIGHTS}
    stap = classify.staples(data)
    confirmed = {h["id"]: set() for h in HIGHLIGHTS}  # (date, hall) pairs with a real match

    for day in data["days"]:
        for hall_id, meals in day["menus"].items():
            for dishes in meals.values():
                for d in dishes:
                    d["hl"] = []
                    is_staple = d["name"].strip().lower() in stap
                    for h in HIGHLIGHTS:
                        if h.get("halls") and hall_id not in h["halls"]:
                            continue
                        if is_staple and not h.get("include_staples"):
                            continue
                        if h.get("cats") and d.get("cat") not in h["cats"]:
                            continue
                        if matchers[h["id"]](d):
                            d["hl"].append(h["id"])
                            confirmed[h["id"]].add((day["date"], hall_id))

    meta, unconfirmed = [], []
    for h in HIGHLIGHTS:
        meta.append({
            "id": h["id"], "label": h["label"], "short": h.get("short", h["label"]),
            "tag": h["tag"], "group": h["group"], "note": h.get("note", ""),
        })
        for day in data["days"]:
            weekday = datetime.datetime.strptime(day["date"], "%m/%d/%Y").weekday()
            if weekday in h.get("usual_days", []):
                for hall_id in h.get("halls") or [x["id"] for x in data["halls"]]:
                    if (day["date"], hall_id) not in confirmed[h["id"]]:
                        name = next((x["name"] for x in data["halls"] if x["id"] == hall_id), hall_id)
                        unconfirmed.append({"id": h["id"], "date": day["date"], "hall": name})
    data["highlights"] = meta
    data["unconfirmed"] = unconfirmed
    return data
