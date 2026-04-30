"""
AI Bhai — Storytelling Engine
Wraps recipes in warm, friendly Indian narratives.
"""
import random, datetime

GREETINGS = [
    "Arre mere pyaare bhai! 🙏 Welcome back to our kitchen!",
    "Namaste meri pyaari behan! 🙏 Your elder sibling is ready to help!",
    "Mera dost! 🙏 Let's cook something amazing together today!",
    "Anna! Akka! 🙏 Ready to make some magic? Your sibling is here!",
    "Namaskaram! 🙏 AI Bhai is so happy to see you again!",
    "Swaagatam! 🙏 Let's start our cooking journey!",
    "Namaskar! 🙏 Cooking buddy ready for action!",
]

INTROS = [
    "{name} is not just food — it's a memory from our childhood! 💛",
    "I remember the smell of {name} in our kitchen, feels like {region}! ✨",
    "Every bite of {name} brings back the warmth of {region}! 🌟",
    "{name}... ah, just the thought makes me so happy, mere dost! 💎",
    "A warm home, family around, and {name} on the stove... 🍳",
    "{name} from {region} is like a warm hug from a sibling! 🤗",
]

STEP_INTROS = ["Ab dekho, follow my lead! 🎯", "Pay attention, this is how we make it perfect! ✨",
    "Step by step, just like I taught you! 👨‍🍳", "Let me walk you through it, mere bhai/behan! 🔥"]

TIP_INTROS = ["💡 *AI Bhai's Secret Sibling Tip:*", "🤫 *Chalo, a secret between us:*",
    "⭐ *Our grandmother used to do this:*", "🎯 *The secret to that perfect taste:*"]

DIFF_MSG = {"Easy": "You'll nail this easily, don't worry! 😊",
    "Medium": "A little bit of effort, but I'm right here with you! 💪", "Hard": "It's tricky, but I know you can do it, my talented sibling! 🤯"}

SIGNOFF = ["Happy cooking, mere bhai! 💛 — AI Bhai", "Khana bana lo, khushi bana lo! 🙏 — AI Bhai",
    "Cook with love, it always tastes better! ❤️ — AI Bhai", "Can't wait to see what you make, meri behan! 😊 — AI Bhai"]


def format_recipe_story(recipe):
    """Generate a structured recipe presentation."""
    name = recipe.get("name", "Dish")
    name_hi = recipe.get("name_hi", "")
    region = recipe.get("region", "India")
    state = recipe.get("state", "")
    story = recipe.get("story", "")
    veg = recipe.get("veg", True)
    diff = recipe.get("diff", "Medium")
    prep = recipe.get("prep", "")
    cook = recipe.get("cook", "")
    serves = recipe.get("serves", 4)
    ingredients = recipe.get("ingredients", [])
    steps = recipe.get("steps", [])
    tips = recipe.get("tips", [])
    nutrition = recipe.get("nutrition", {})
    icon = "🥬" if veg else "🍗"
    
    # Generate the narrative intro
    greeting = random.choice(GREETINGS)
    intro = random.choice(INTROS).format(name=name, region=region)
    signoff = random.choice(SIGNOFF)
    
    return {
        "name": name,
        "name_hi": name_hi,
        "region": region,
        "state": state,
        "story": story,
        "veg": veg,
        "diff": diff,
        "prep": prep,
        "cook": cook,
        "serves": serves,
        "ingredients": ingredients,
        "steps": steps,
        "tips": tips,
        "nutrition": nutrition,
        "greeting": greeting,
        "intro": intro,
        "signoff": signoff,
        "icon": icon
    }


def format_search_results(results, query):
    if not results:
        return f"## 🔍 No results for \"{query}\"\n\nTry different keywords, browse by category, or tell me your ingredients! 🍳\n\n*AI Bhai never gives up!* 💪"
    return f"## 🔍 Found {len(results)} recipes for \"{query}\"!\n\nPick any one and let's cook! 🍳\n"


def format_ingredient_results(results, ingredients):
    if not results:
        return "## 🥘 Tough combination!\n\nTry adding onion, tomato, or basic spices!\n\n*AI Bhai believes in you!* 💪"
    return f"## 🥘 Found {len(results)} recipes with your ingredients!\n\nYou have: **{', '.join(ingredients)}**\n\nBest matches sorted by ingredient coverage! 🎯\n"


def get_welcome_message():
    return """## 🙏 Namaste! Welcome to AI Bhai!
### Your Desi Cooking Bestie! 🍛

I'm **AI Bhai** — your friendly cooking companion with **500+ authentic Indian recipes**!

🔍 **Search** — Type any dish name! | 🥘 **Ingredients** — Tell me what you have! | 📸 **Scan** — Upload ingredient photos! | 🗺️ **Explore** — Browse by region! | 🎲 **Surprise Me!**

*100% offline, zero API needed!* ❤️ **Let's cook!** 👇"""


def get_daily_special():
    specials = {"Monday": "**Dal Makhani** 🥘", "Tuesday": "**Chole Bhature** 🍛",
        "Wednesday": "**Hyderabadi Biryani** 🍚", "Thursday": "**Masala Dosa** 🥞",
        "Friday": "**Butter Chicken / Paneer Tikka** 🍗", "Saturday": "**Pav Bhaji** 🍔",
        "Sunday": "**Biryani & Gulab Jamun** 🍮"}
    day = datetime.datetime.now().strftime("%A")
    return f"### 📅 {day} Special: {specials.get(day, 'Cook from the heart! ❤️')}"
