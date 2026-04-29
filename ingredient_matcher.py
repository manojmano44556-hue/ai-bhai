"""
AI Bhai — Smart Ingredient Matcher Engine
Offline fuzzy matching with Hindi/English synonym support.
"""
import difflib
import re

# ============================================================
# INGREDIENT SYNONYM MAP (English ↔ Hindi ↔ Regional)
# ============================================================
SYNONYMS = {
    "potato": ["aloo", "batata", "urulaikizhangu", "bangaladumpa"],
    "tomato": ["tamatar", "thakkali", "tomato"],
    "onion": ["pyaaz", "pyaj", "vengayam", "ullipayalu", "kanda"],
    "garlic": ["lahsun", "lehsun", "poondu", "vellulli"],
    "ginger": ["adrak", "inji", "allam", "shunti"],
    "turmeric": ["haldi", "manjal", "pasupu"],
    "chili": ["mirchi", "mirch", "milagai", "mirapakaya", "chilli", "green chili", "red chili", "lal mirch", "hari mirch"],
    "cumin": ["jeera", "jeerakam", "jeerige"],
    "coriander": ["dhaniya", "dhania", "kothamalli", "kothimeera", "cilantro"],
    "mustard seeds": ["rai", "sarson", "kaduku", "aavalu"],
    "curry leaves": ["kadi patta", "karivepaku", "karivembu"],
    "coconut": ["nariyal", "kobbari", "thengai", "nalikera"],
    "rice": ["chawal", "chaval", "arisi", "biyyam", "akki"],
    "wheat flour": ["atta", "gehu ka atta", "godhuma pindi", "godhi hittu"],
    "chickpea flour": ["besan", "kadalai maavu", "senaga pindi"],
    "lentils": ["dal", "daal", "paruppu", "pappu"],
    "toor dal": ["arhar dal", "tuvar dal", "kandi pappu", "thuvaram paruppu"],
    "moong dal": ["mung dal", "green gram", "pesalu", "payaru"],
    "chana dal": ["bengal gram", "kadalai paruppu", "senaga pappu"],
    "urad dal": ["black gram", "ulundu", "minapa pappu", "uddina bele"],
    "masoor dal": ["red lentils", "mysore paruppu"],
    "paneer": ["cottage cheese", "chena"],
    "ghee": ["clarified butter", "nei", "neyyi", "tuppa"],
    "yogurt": ["dahi", "curd", "thayir", "perugu", "mosaru"],
    "butter": ["makhan", "vennai", "venna"],
    "cream": ["malai", "cream"],
    "milk": ["doodh", "paal", "paalu"],
    "chicken": ["murgh", "murg", "kozhi", "kodi"],
    "mutton": ["gosht", "goat", "aattukari", "mamsam"],
    "fish": ["machli", "machhi", "meen", "chepa"],
    "prawn": ["jhinga", "shrimp", "eral", "royyalu"],
    "egg": ["anda", "muttai", "guddu"],
    "cauliflower": ["gobi", "phool gobi", "cauliflower", "hookosu"],
    "cabbage": ["patta gobi", "bandha kosu", "muttaikose"],
    "spinach": ["palak", "keerai", "palakoora"],
    "fenugreek": ["methi", "vendhayam", "menthulu", "kasuri methi"],
    "eggplant": ["baingan", "brinjal", "kathirikkai", "vankaya", "badanekayi"],
    "okra": ["bhindi", "vendakkai", "bendakaya", "ladies finger"],
    "peas": ["matar", "pattani", "batani"],
    "capsicum": ["shimla mirch", "bell pepper", "kudai milagai"],
    "carrot": ["gajar", "carrot", "kaeru"],
    "beans": ["sem", "rajma", "avare", "french beans"],
    "drumstick": ["sahjan", "murungakkai", "munagakaya"],
    "bitter gourd": ["karela", "pavakkai", "kakarakaya", "hagalakai"],
    "bottle gourd": ["lauki", "dudhi", "sorakaya", "sorekai"],
    "ridge gourd": ["turai", "peerkangai", "beerakaya"],
    "ash gourd": ["petha", "boodida gummadikaya", "poosanikai"],
    "raw banana": ["kaccha kela", "vazhakkai", "arati kaya"],
    "jackfruit": ["kathal", "palakkai", "panasa"],
    "mango": ["aam", "maanga", "mamidi"],
    "tamarind": ["imli", "puli", "chintapandu"],
    "jaggery": ["gur", "gud", "vellam", "bellam"],
    "sugar": ["cheeni", "shakkar", "sakkarai", "panchidara"],
    "salt": ["namak", "uppu"],
    "oil": ["tel", "ennai", "nune"],
    "mustard oil": ["sarson ka tel"],
    "sesame oil": ["til ka tel", "nallennai", "nuvvula nune"],
    "coconut oil": ["nariyal tel", "kobbari nune", "velichenna"],
    "cardamom": ["elaichi", "elakkai", "yelakulu"],
    "cinnamon": ["dalchini", "pattai", "dalchina chakka"],
    "cloves": ["laung", "lavangam", "krambu"],
    "black pepper": ["kali mirch", "milagu", "miriyalu"],
    "bay leaf": ["tej patta", "biryani aaku", "piriyal ilai"],
    "saffron": ["kesar", "kungumapoo", "kumkuma puvvu"],
    "fennel": ["saunf", "sombu", "sopu"],
    "asafoetida": ["hing", "heeng", "perungayam", "inguva"],
    "star anise": ["chakri phool", "biryani poo"],
    "poppy seeds": ["khus khus", "kasa kasa", "gasagasalu"],
    "sesame seeds": ["til", "ellu", "nuvvulu"],
    "cashew": ["kaju", "mundiri", "jeedipappu"],
    "almond": ["badam", "baadaam"],
    "raisin": ["kishmish", "draksha", "ular draksha"],
    "peanut": ["moongphali", "verkadalai", "pallilu", "groundnut"],
    "lemon": ["nimbu", "elumichchai", "nimmakaya"],
    "mint": ["pudina", "pudhina"],
    "garam masala": ["garam masala mix"],
    "sambar powder": ["sambar podi"],
    "rasam powder": ["rasam podi"],
    "chaat masala": ["chaat masala mix"],
    "red chili powder": ["lal mirch powder", "molagai podi"],
    "coriander powder": ["dhaniya powder", "malli podi"],
    "cumin powder": ["jeera powder"],
    "amchur": ["dry mango powder", "amchoor"],
    "kokum": ["kokam", "kudampuli"],
    "raw mango": ["kairi", "manga inji"],
    "banana leaf": ["kela patta", "vazhailai", "arati aaku"],
    "semolina": ["suji", "sooji", "rava", "ravva"],
    "poha": ["flattened rice", "aval", "atukulu"],
    "vermicelli": ["sevai", "semiya", "seviya"],
    "maida": ["all purpose flour", "refined flour"],
    "idli rice": ["idli arisi"],
    "basmati rice": ["basmati chawal"],
    "sago": ["sabudana", "javvarisi", "saggubiyyam"],
}

# Build reverse lookup: any synonym -> canonical name
_REVERSE_MAP = {}
for canonical, synonyms in SYNONYMS.items():
    _REVERSE_MAP[canonical.lower()] = canonical
    for syn in synonyms:
        _REVERSE_MAP[syn.lower()] = canonical


def normalize_ingredient(name):
    """Convert any ingredient name (Hindi/English/regional) to canonical English."""
    name_lower = name.lower().strip()
    if name_lower in _REVERSE_MAP:
        return _REVERSE_MAP[name_lower]
    # Fuzzy match
    close = difflib.get_close_matches(name_lower, _REVERSE_MAP.keys(), n=1, cutoff=0.7)
    if close:
        return _REVERSE_MAP[close[0]]
    return name_lower


def extract_ingredient_names(ingredient_list):
    """Extract base ingredient names from recipe ingredient strings like '2 cups rice'."""
    names = []
    for item in ingredient_list:
        # Remove quantities, units, and parenthetical notes
        cleaned = re.sub(r'\d+[\./]?\d*\s*', '', item)
        cleaned = re.sub(r'\(.*?\)', '', cleaned)
        cleaned = re.sub(r'\b(cups?|tbsp|tsp|teaspoons?|tablespoons?|kg|gm?|grams?|ml|liters?|inch|pieces?|medium|large|small|pinch|handful|bunch|to taste|as needed|optional|for garnish|chopped|sliced|diced|minced|grated|ground|powder|fresh|dried|whole|crushed)\b', '', cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.strip(' ,-/')
        if cleaned and len(cleaned) > 1:
            names.append(normalize_ingredient(cleaned))
    return list(set(names))


def match_recipes(user_ingredients, all_recipes, min_match_pct=30):
    """
    Find recipes that match the given ingredients.
    Returns list of (recipe, match_percentage, matched_ingredients, missing_ingredients).
    """
    user_normalized = set(normalize_ingredient(i) for i in user_ingredients)
    results = []

    for recipe in all_recipes:
        recipe_ingredients = extract_ingredient_names(recipe.get("ingredients", []))
        recipe_set = set(recipe_ingredients)

        if not recipe_set:
            continue

        matched = user_normalized & recipe_set
        missing = recipe_set - user_normalized

        # Don't count common pantry items as missing
        pantry = {"salt", "oil", "water", "sugar", "turmeric", "red chili powder",
                  "cumin", "coriander powder", "garam masala", "mustard seeds",
                  "curry leaves", "asafoetida", "black pepper"}
        essential_missing = missing - pantry
        essential_recipe = recipe_set - pantry

        if len(essential_recipe) == 0:
            match_pct = 100
        else:
            match_pct = (len(essential_recipe) - len(essential_missing)) / len(essential_recipe) * 100

        if match_pct >= min_match_pct:
            results.append({
                "recipe": recipe,
                "match_pct": round(match_pct, 1),
                "matched": list(matched),
                "missing": list(essential_missing),
            })

    # Sort by match percentage (desc), then by difficulty
    diff_order = {"Easy": 0, "Medium": 1, "Hard": 2}
    results.sort(key=lambda x: (-x["match_pct"], diff_order.get(x["recipe"].get("diff", "Medium"), 1)))
    return results


def search_recipes(query, all_recipes):
    """
    Search recipes by name, tags, region, or category.
    Returns matching recipes sorted by relevance.
    """
    query_lower = query.lower().strip()
    query_words = set(query_lower.split())
    results = []

    for recipe in all_recipes:
        score = 0
        name = recipe.get("name", "").lower()
        tags = [t.lower() for t in recipe.get("tags", [])]
        region = recipe.get("region", "").lower()
        state = recipe.get("state", "").lower()
        cat = recipe.get("cat", "").lower()
        name_hi = recipe.get("name_hi", "").lower()

        # Exact name match
        if query_lower in name or query_lower in name_hi:
            score += 100
        # Partial name match
        elif any(w in name for w in query_words):
            score += 60
        # Tag match
        if any(q in tags for q in query_words):
            score += 40
        # Region match
        if query_lower in region or any(w in region for w in query_words):
            score += 50
        if query_lower in state or any(w in state for w in query_words):
            score += 45
        # Category match
        if query_lower in cat or any(w in cat for w in query_words):
            score += 35

        # Check ingredient match
        ingredients_text = " ".join(recipe.get("ingredients", [])).lower()
        if any(w in ingredients_text for w in query_words):
            score += 20

        if score > 0:
            results.append({"recipe": recipe, "score": score})

    results.sort(key=lambda x: -x["score"])
    return results


def get_recipes_by_category(all_recipes, category=None, region=None, veg_only=False, difficulty=None):
    """Filter recipes by category, region, veg/non-veg, and difficulty."""
    filtered = all_recipes
    if category:
        filtered = [r for r in filtered if r.get("cat", "").lower() == category.lower()]
    if region:
        filtered = [r for r in filtered if region.lower() in r.get("region", "").lower() or region.lower() in r.get("state", "").lower()]
    if veg_only:
        filtered = [r for r in filtered if r.get("veg", True)]
    if difficulty:
        filtered = [r for r in filtered if r.get("diff", "").lower() == difficulty.lower()]
    return filtered


def get_random_recipes(all_recipes, count=6, veg_only=False):
    """Get random recipe suggestions."""
    import random
    pool = [r for r in all_recipes if r.get("veg", True)] if veg_only else all_recipes
    return random.sample(pool, min(count, len(pool)))


def get_all_regions(all_recipes):
    """Get unique regions from all recipes."""
    regions = set()
    for r in all_recipes:
        regions.add(r.get("region", "Unknown"))
    return sorted(regions)


def get_all_categories(all_recipes):
    """Get unique categories from all recipes."""
    cats = set()
    for r in all_recipes:
        cats.add(r.get("cat", "Unknown"))
    return sorted(cats)
