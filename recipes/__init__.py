"""
AI Bhai Recipe Database — Aggregator
Loads all regional recipe modules and provides unified access.
"""

from .north_indian import RECIPES as NORTH
from .south_indian import RECIPES as SOUTH
from .east_indian import RECIPES as EAST
from .west_indian import RECIPES as WEST
from .street_food import RECIPES as STREET
from .desserts import RECIPES as DESSERTS
from .extras import RECIPES as EXTRAS

ALL_RECIPES = NORTH + SOUTH + EAST + WEST + STREET + DESSERTS + EXTRAS

def get_all_recipes():
    return ALL_RECIPES

def get_recipe_count():
    return len(ALL_RECIPES)

def get_regions():
    return sorted(set(r.get("region","") for r in ALL_RECIPES))

def get_categories():
    return sorted(set(r.get("cat","") for r in ALL_RECIPES))

def get_states():
    return sorted(set(r.get("state","") for r in ALL_RECIPES if r.get("state")))
