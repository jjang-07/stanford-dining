"""Rough nutrition estimates for every dish.

Stanford's menu site publishes no calories or macros, so these are ESTIMATES for one typical dining-hall
serving, worked out from the dish name. They are meant for comparing options (which main has more protein
for its calories), not for tracking intake. Each rule below is (pattern, (kcal, protein_g, fat_g, carbs_g)).
The first rule that matches a dish name wins, so put specific rules above general ones.
Edit any number you disagree with; the page rebuilds from this file.
"""
import re

R = lambda p: re.compile(p, re.I)

RULES = [
    # ---------- specific overrides (must come first)
    (R(r"quiche"), (360, 15, 26, 15)),
    (R(r"potato salad"), (240, 5, 14, 22)),
    (R(r"jackfruit cioppino"), (220, 5, 5, 36)),
    (R(r"veggie hot dog"), (150, 14, 6, 8)),
    (R(r"hot dog bun"), (120, 4, 2, 21)),
    (R(r"hot dog"), (300, 11, 27, 3)),
    (R(r"egg noodles"), (230, 8, 4, 42)),
    (R(r"lumpia"), (190, 4, 9, 22)),
    (R(r"po'?boy"), (650, 28, 32, 60)),
    (R(r"chowder"), (300, 10, 17, 24)),
    (R(r"fried chicken"), (450, 30, 26, 22)),
    (R(r"pork belly"), (520, 16, 48, 8)),

    # ---------- breakfast
    (R(r"hard boiled egg"), (80, 6, 5, 1)),
    (R(r"scrambled eggs"), (190, 13, 14, 2)),
    (R(r"egg special"), (260, 15, 19, 4)),
    (R(r"plant powered|tofu scramble"), (150, 12, 8, 6)),
    (R(r"vegan breakfast"), (260, 10, 10, 34)),
    (R(r"breakfast special"), (330, 14, 16, 30)),
    (R(r"overnight oats"), (210, 7, 6, 32)),
    (R(r"oatmeal"), (160, 6, 3, 28)),
    (R(r"chicken (&|and) waffles"), (720, 34, 36, 62)),
    (R(r"gluten-free waffles"), (230, 5, 10, 30)),
    (R(r"waffles"), (220, 6, 10, 28)),
    (R(r"pancakes"), (300, 8, 9, 46)),
    (R(r"french toast"), (310, 10, 12, 38)),
    (R(r"breakfast burrito"), (460, 18, 18, 52)),
    (R(r"breakfast taco"), (340, 14, 16, 32)),
    (R(r"breakfast sandwich"), (360, 16, 17, 33)),
    (R(r"chilaquiles"), (380, 12, 18, 42)),
    (R(r"breakfast fried rice"), (320, 9, 11, 46)),
    (R(r"breakfast potatoes"), (170, 3, 6, 27)),
    (R(r"hash brown"), (150, 1, 9, 15)),
    (R(r"tater tots"), (190, 2, 10, 23)),
    (R(r"seasonal fruit"), (70, 1, 0, 18)),
    (R(r"chicken apple sausage"), (170, 14, 9, 7)),
    (R(r"pork sausage"), (210, 10, 18, 1)),
    (R(r"chorizo|sausage bar"), (260, 13, 22, 3)),
    (R(r"\bbacon\b"), (140, 10, 11, 0)),
    (R(r"allergy-friendly"), (200, 4, 6, 32)),
    (R(r"honey butter biscuit|biscuit"), (210, 3, 11, 25)),

    # ---------- standing stations
    (R(r"^burger bar"), (540, 28, 29, 37)),
    (R(r"^grilled chicken$"), (200, 30, 6, 1)),
    (R(r"grilled vegan"), (200, 12, 10, 14)),
    (R(r"flavor forward legumes"), (210, 12, 4, 33)),
    (R(r"panini station"), (460, 20, 22, 40)),
    (R(r"performance bar"), (330, 16, 12, 34)),
    (R(r"composed salad"), (150, 5, 9, 12)),
    (R(r"seasonal vegetable board"), (110, 4, 6, 12)),
    (R(r"seasonal steamed vegetables"), (60, 3, 1, 12)),
    (R(r"soup of the day"), (160, 6, 6, 20)),
    (R(r"craveable grains"), (230, 7, 5, 40)),
    (R(r"assorted dinner rolls"), (110, 3, 3, 19)),
    (R(r"handmade pizza|pizza"), (300, 13, 11, 38)),

    # ---------- composite mains (specific first)
    (R(r"vegan.{0,3}meatballs"), (330, 18, 10, 38)),
    (R(r"spaghetti and meatballs"), (560, 26, 20, 62)),
    (R(r"fish (&|and) chips"), (680, 28, 34, 62)),
    (R(r"chicken parmesan"), (450, 38, 20, 24)),
    (R(r"eggplant parmesan"), (380, 14, 20, 36)),
    (R(r"chicken alfredo"), (720, 40, 32, 62)),
    (R(r"shrimp linguine"), (560, 30, 20, 58)),
    (R(r"tortellini"), (400, 17, 14, 50)),
    (R(r"ravioli"), (360, 14, 12, 46)),
    (R(r"alfredo"), (620, 18, 30, 66)),
    (R(r"orecchiette"), (380, 12, 10, 58)),
    (R(r"creamy pesto"), (480, 13, 24, 52)),
    (R(r"pesto sauce"), (120, 2, 12, 2)),
    (R(r"pasta pesto"), (430, 13, 18, 54)),
    (R(r"marinara"), (330, 11, 5, 60)),
    (R(r"rasta pasta"), (460, 14, 20, 52)),
    (R(r"pasta with garlic|garlic herb spaghetti"), (380, 11, 12, 56)),
    (R(r"gluten-free pasta|penne pasta"), (330, 7, 2, 70)),
    (R(r"linguine|spaghetti|^pasta$"), (320, 11, 4, 62)),
    (R(r"risotto"), (310, 8, 10, 46)),
    (R(r"poutine \(topping\)"), (260, 18, 16, 8)),
    (R(r"mushroom.*poutine"), (470, 15, 24, 50)),
    (R(r"poutine"), (560, 24, 32, 44)),
    (R(r"cheesy mac"), (420, 16, 20, 42)),
    (R(r"baked potato bar"), (300, 7, 8, 52)),
    (R(r"grilled cheese"), (470, 16, 24, 46)),
    (R(r"quesadilla"), (430, 18, 24, 34)),
    (R(r"tacos"), (440, 28, 20, 36)),
    (R(r"sofritas"), (260, 14, 12, 22)),
    (R(r"chili con carne"), (380, 26, 18, 28)),
    (R(r"meatloaf"), (360, 24, 22, 14)),
    (R(r"cioppino|frutti di mare"), (320, 34, 9, 18)),
    (R(r"crab sandwich"), (420, 20, 20, 36)),
    (R(r"magnolia boil"), (420, 28, 20, 28)),
    (R(r"jerk pork"), (520, 16, 48, 6)),
    (R(r"oxtail"), (420, 32, 28, 8)),
    (R(r"short ribs"), (520, 30, 38, 14)),
    (R(r"char siu pork"), (300, 25, 16, 12)),
    (R(r"char siu tofu"), (230, 16, 11, 14)),
    (R(r"general chicken"), (520, 24, 28, 44)),
    (R(r"steak protein bowl"), (660, 46, 24, 56)),
    (R(r"protein bowl"), (620, 42, 18, 62)),
    (R(r"beef teriyaki.*noodle|noodle bowl"), (580, 30, 16, 72)),
    (R(r"smothered steak"), (500, 38, 28, 16)),
    (R(r"japanese chicken teriyaki"), (350, 33, 14, 18)),
    (R(r"miso black cod"), (320, 28, 18, 12)),
    (R(r"agedashi"), (220, 12, 12, 14)),
    (R(r"teriyaki tofu"), (240, 15, 11, 18)),
    (R(r"japanese tofu"), (260, 17, 11, 20)),
    (R(r"japchae"), (360, 7, 10, 60)),
    (R(r"korean sweet and spicy fish"), (330, 26, 12, 28)),
    (R(r"gochujang.*tofu"), (250, 15, 11, 22)),
    (R(r"thai green curry chicken"), (360, 26, 24, 10)),
    (R(r"thai red curry tempeh"), (340, 17, 24, 14)),
    (R(r"butter chicken"), (430, 28, 30, 12)),
    (R(r"palak paneer"), (350, 15, 27, 12)),
    (R(r"aloo gobi"), (200, 4, 10, 25)),
    (R(r"curried vegetables"), (170, 4, 9, 19)),
    (R(r"chicken shawarma"), (390, 34, 22, 10)),
    (R(r"harissa braised chicken"), (350, 34, 18, 8)),
    (R(r"harissa tofu"), (230, 15, 13, 10)),
    (R(r"tagine"), (260, 9, 9, 38)),
    (R(r"jackfruit"), (250, 9, 5, 42)),
    (R(r"white bean stew"), (230, 11, 4, 36)),
    (R(r"rosemary fried chicken wings|chicken wings"), (430, 30, 30, 10)),
    (R(r"chicken cutlets"), (370, 33, 17, 16)),
    (R(r"red beans and rice"), (340, 14, 8, 52)),

    (R(r"carne asada"), (360, 34, 20, 3)),
    (R(r"mushroom.*(cream|tarragon)"), (250, 6, 18, 14)),
    (R(r"portobello|portabello"), (320, 9, 16, 34)),
    (R(r"mushroom"), (130, 4, 8, 10)),
    (R(r"cabbage"), (90, 2, 4, 12)),
    (R(r"biryani|biriyani"), (420, 12, 14, 62)),
    (R(r"samosa"), (260, 4, 14, 28)),
    (R(r"pancit"), (340, 12, 10, 52)),
    (R(r"dan dan"), (420, 11, 18, 52)),
    (R(r"grits"), (260, 8, 12, 30)),
    (R(r"mac (&|and) cheese"), (430, 16, 22, 42)),
    (R(r"texas toast"), (150, 3, 7, 19)),
    (R(r"hawaiian roll"), (90, 3, 2, 15)),
    (R(r"baguette|sourdough"), (160, 5, 4, 28)),
    (R(r"orzo"), (330, 11, 9, 50)),
    (R(r"gratin"), (280, 6, 16, 28)),
    (R(r"patatas bravas"), (260, 4, 14, 30)),
    (R(r"romesco"), (110, 2, 10, 5)),
    (R(r"couscous"), (200, 6, 4, 36)),
    (R(r"hush-?puppies"), (240, 4, 12, 30)),
    (R(r"garlic parmesan fries"), (360, 5, 18, 43)),
    (R(r"brown butter"), (110, 2, 8, 8)),
    (R(r"yams|sweet potato"), (180, 3, 4, 34)),
    (R(r"butter pasta"), (480, 12, 20, 60)),
    (R(r"dirty rice"), (320, 12, 14, 36)),
    (R(r"succotash"), (180, 8, 5, 28)),
    (R(r"maque choux"), (150, 3, 6, 22)),

    # ---------- rice, noodles, potatoes, bread
    (R(r"thai pineapple fried rice"), (320, 7, 10, 52)),
    (R(r"fried rice"), (300, 7, 10, 46)),
    (R(r"yakisoba"), (380, 9, 12, 58)),
    (R(r"jollof"), (300, 6, 9, 50)),
    (R(r"pilaf"), (230, 5, 6, 40)),
    (R(r"jeweled basmati"), (260, 5, 7, 45)),
    (R(r"garlic rice"), (260, 5, 6, 45)),
    (R(r"rice"), (210, 4, 2, 45)),
    (R(r"waffle fries|garlic fries|steak-cut fries"), (340, 4, 17, 43)),
    (R(r"mashed potatoes"), (240, 4, 10, 34)),
    (R(r"potatoes"), (190, 3, 7, 30)),
    (R(r"focaccia|foccacia"), (170, 4, 7, 23)),
    (R(r"breadstick"), (130, 4, 3, 22)),
    (R(r"garlic bread"), (150, 4, 7, 18)),
    (R(r"cornbread"), (190, 3, 8, 27)),
    (R(r"naan"), (260, 8, 5, 45)),
    (R(r"pita"), (165, 5, 1, 33)),
    (R(r"egg roll"), (190, 6, 9, 21)),
    (R(r"cheese curds"), (160, 10, 12, 2)),

    # ---------- vegetable sides and salads
    (R(r"fried eggplant"), (310, 5, 20, 29)),
    (R(r"plantain"), (190, 1, 9, 30)),
    (R(r"parmesan broccolini"), (130, 7, 8, 9)),
    (R(r"edamame salad"), (140, 10, 6, 11)),
    (R(r"edamame"), (120, 11, 5, 9)),
    (R(r"goma-ae"), (70, 4, 4, 6)),
    (R(r"wakame"), (50, 1, 1, 8)),
    (R(r"macaroni salad"), (320, 5, 22, 25)),
    (R(r"coleslaw"), (130, 1, 10, 10)),
    (R(r"cucumber"), (50, 1, 2, 7)),
    (R(r"beets"), (130, 4, 5, 18)),
    (R(r"caponata"), (110, 2, 7, 12)),
    (R(r"miso glaze"), (140, 2, 7, 18)),
    (R(r"corn on the cob"), (130, 3, 5, 21)),
    (R(r"root vegetables"), (140, 2, 5, 24)),
    (R(r"squash"), (110, 2, 4, 20)),
    (R(r"green beans"), (95, 2, 6, 9)),
    (R(r"broccoli rabe|broccolini|gai lan|spinach"), (85, 5, 5, 7)),
    (R(r"carrots"), (80, 1, 3, 13)),
    (R(r"grilled pineapple"), (80, 1, 0, 20)),
    (R(r"mushroom gravy"), (60, 1, 3, 7)),
    (R(r"bruschetta"), (50, 1, 2, 7)),

    # ---------- generic protein fallbacks (new dishes that match no rule above)
    (R(r"\bsteak|sirloin|ribeye|flank|tri-?tip"), (460, 40, 28, 6)),
    (R(r"beef|brisket|burger"), (380, 30, 24, 6)),
    (R(r"pork|ham\b|ribs"), (380, 26, 27, 6)),
    (R(r"lamb"), (400, 28, 28, 4)),
    (R(r"turkey"), (280, 30, 13, 4)),
    (R(r"chicken"), (310, 32, 16, 5)),
    (R(r"salmon"), (340, 30, 22, 4)),
    (R(r"shrimp|prawn"), (160, 24, 4, 4)),
    (R(r"fish|cod\b|tilapia|halibut|tuna|seafood"), (250, 28, 12, 6)),
    (R(r"tempeh"), (230, 18, 12, 12)),
    (R(r"tofu"), (220, 15, 12, 10)),
    (R(r"\beggs?\b"), (200, 13, 14, 3)),
    (R(r"lentil|chickpea|bean"), (230, 12, 4, 36)),
    (R(r"curry"), (340, 20, 22, 14)),

    # ---------- generic vegetable catch-all (last, so "roasted chicken" is not treated as a vegetable)
    (R(r"stir fry|bok choy|asparagus|cauliflower|collard|greens|peppers|onions|eggplant|zucchini|fennel|vegetable|roasted|charred|glazed"), (100, 3, 5, 13)),
]

# fallbacks by menu section when nothing above matches
FALLBACK = {
    "main": (350, 18, 16, 32),
    "protein": (220, 14, 9, 18),
    "veg": (100, 3, 5, 13),
    "other": (220, 5, 8, 32),
}

# fried, creamy, cheesy, or processed: ranked a bit lower in "best picks"
HEAVY = re.compile(r"fried|crispy|crusted|breaded|battered|tempura|creamy|alfredo|cheesy|cheese|poutine|gravy|bacon|sausage|chorizo|belly|butter\b|buttered", re.I)


STATION = re.compile(r"\b(?:bar|station)\b", re.I)


def estimate(dish):
    name = dish["name"].strip()
    for rx, vals in RULES:
        if rx.search(name):
            return vals, True
    return FALLBACK.get(dish.get("cat", "other"), FALLBACK["other"]), False


def score(name, vals):
    """Estimated protein per 100 kcal, nudged down for fried, creamy, or very fatty dishes."""
    kcal, protein, fat, _ = vals
    pd = protein / max(kcal, 100) * 100
    if fat >= 28 or HEAVY.search(name):
        pd *= 0.8
    return round(pd, 2)


def apply(data):
    missed = set()
    for day in data["days"]:
        for hall in day["menus"].values():
            for dishes in hall.values():
                for d in dishes:
                    vals, matched = estimate(d)
                    if not matched:
                        # No rule fits this dish: show no number rather than a made-up one
                        missed.add(d["name"])
                        d["n"], d["score"], d["heavy"], d["station"] = None, 0, False, False
                        continue
                    kcal, p, f, c = vals
                    d["n"] = [int(round(kcal / 10.0) * 10), p, f, c]
                    d["score"] = score(d["name"], vals)
                    d["station"] = bool(STATION.search(d["name"]))  # build-your-own, too variable to rank
                    d["heavy"] = bool(f >= 28 or HEAVY.search(d["name"]))
    data["nutrition_fallbacks"] = sorted(missed)
    return data
