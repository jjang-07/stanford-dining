"""Sort dishes into mains / protein / veggies / sides, and flag steak.

Stanford's menu data has no station info, so this uses two signals:
  1. Position: on lunch and dinner menus the first two dishes are the day's headline mains.
  2. Keywords in the dish name (meat, seafood, tofu, eggs, vegetables, and so on).
"""
import re
from collections import defaultdict

def rx(words):
    return re.compile(r"\b(?:" + "|".join(words) + r")", re.I)

MEATLESS = rx(["vegan", "vegetarian", "veggie", "plant-based", "meatless", "jackfruit", "impossible", "beyond", "tofu", "tempeh", "seitan", "mushroom"])
MEAT = rx([
    "chicken", "beef", "pork", "turkey", "lamb", "duck", "bacon", "ham\\b", "sausage", "chorizo", "meatball", "brisket",
    "ribs?\\b", "short rib", "steak", "sirloin", "ribeye", "tri-?tip", "filet", "flank", "carne", "carnitas", "al pastor",
    "gyro", "kebab", "pepperoni", "hot dog", "wings?\\b", "cutlet", "fish", "cod\\b", "salmon", "tuna", "tilapia", "halibut",
    "shrimp", "prawn", "crab", "scallop", "seafood", "cioppino", "mahi", "trout", "catfish", "snapper", "sea bass", "clam",
    "mussel", "calamari", "oyster", "lobster", "pot roast", "meatloaf", "schnitzel", "burger", "oxtail",
])
PLANT_PROTEIN = rx(["tofu", "tempeh", "seitan", "impossible", "beyond", "plant-based", "falafel"])
EVERYDAY_PROTEIN = rx(["egg(?!plant| roll)", "legume", "(?<!green )(?<!string )beans?\\b", "lentil", "chickpea", "hummus", "edamame", "grilled vegan", "protein"])
BREAKFAST_MAIN = rx(["scrambled", "omelet", "frittata", "benedict", "burrito", "breakfast sandwich", "taco", "sausage", "bacon", "ham\\b", "chorizo", "tofu scramble"])
VEG = rx([
    "vegetable", "veggie", "broccoli", "broccolini", "carrot", "spinach", "kale", "green beans?", "squash", "zucchini",
    "eggplant", "cauliflower", "asparagus", "brussels", "cabbage", "slaw", "salad", "peppers?\\b", "onions?\\b", "gai lan", "gobi",
    "corn\\b", "peas\\b", "beets?\\b", "greens", "collard", "cucumber", "bok choy", "artichoke", "sprouts", "kabocha",
    "radish", "fennel", "celery", "leeks?\\b", "pumpkin", "okra", "mushroom", "chard", "bean sprouts", "cole", "pickled",
    "roasted root", "stir-?fry", "ratatouille", "sweet potato",
])

NOT_VEG = re.compile(r"gravy|sauce|topping|dressing|macaroni|\b(?:rice|noodles?|yakisoba|pasta|soup)\b", re.I)

STEAK = re.compile(r"\b(?:steak|sirloin|ribeye|rib-eye|tri-?tip|filet mignon|flank|skirt|hanger|carne asada|prime rib|new york strip|ny strip)", re.I)
NOT_STEAK = re.compile(r"steak[- ]cut|steak fries|steak sauce|steak seasoning|\b(?:cauliflower|tofu|portobello|mushroom|eggplant|vegan|vegetable|plant|cabbage|seitan|tempeh|jackfruit)\b[^/]{0,12}steak", re.I)


def is_steak(name):
    return bool(STEAK.search(name)) and not NOT_STEAK.search(name)


def is_meat(d):
    n = d["name"]
    return bool(MEAT.search(n)) and not MEATLESS.search(n) and not {"vegan", "vegetarian"} & set(d["tags"])


def staples(data):
    """Dishes that show up on most lunch/dinner menus: the standing bars and sides."""
    seen, total = defaultdict(int), 0
    for day in data["days"]:
        for hall in day["menus"].values():
            for meal in ("Lunch", "Dinner"):
                if meal in hall:
                    total += 1
                    for n in {x["name"].strip().lower() for x in hall[meal]}:
                        seen[n] += 1
    return {n for n, c in seen.items() if total and c / total >= 0.5}


def categorize(data):
    stap = staples(data)
    for day in data["days"]:
        for hall in day["menus"].values():
            for meal, dishes in hall.items():
                for i, d in enumerate(dishes):
                    n = d["name"]
                    is_staple = n.strip().lower() in stap
                    d["steak"] = is_steak(n)
                    if meal in ("Breakfast", "Brunch") and BREAKFAST_MAIN.search(n) and not MEATLESS.search(n.replace("Tofu Scramble", "")):
                        cat = "main"
                    elif meal in ("Breakfast", "Brunch") and re.search(r"tofu scramble", n, re.I):
                        cat = "main"
                    elif meal in ("Lunch", "Dinner") and i < 2 and not is_staple:
                        cat = "main"
                    elif not is_staple and (is_meat(d) or PLANT_PROTEIN.search(n)):
                        cat = "main"
                    elif is_meat(d) or PLANT_PROTEIN.search(n) or EVERYDAY_PROTEIN.search(n):
                        cat = "protein"
                    elif VEG.search(n) and not NOT_VEG.search(n):
                        cat = "veg"
                    else:
                        cat = "other"
                    d["cat"] = cat
    return data
