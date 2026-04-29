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
    """Generate a storytelling-style recipe presentation."""
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
    L = []
    L.append(f"# {icon} {name}")
    if name_hi: L.append(f"### *{name_hi}*")
    L.append("")
    L.append(random.choice(GREETINGS))
    L.append("")
    L.append(random.choice(INTROS).format(name=name, region=region))
    L.append("")
    if story:
        L.append(f"📖 **The Story:** *{story}*")
        L.append("")
    L.append("---")
    L.append("### 📊 Quick Info")
    info = f"🗺️ {region}"
    if state: info += f" • 📍 {state}"
    info += f" • {icon} {'Veg' if veg else 'Non-Veg'} • 📏 {diff}"
    if prep: info += f" • ⏱️ Prep: {prep}min"
    if cook: info += f" • 🔥 Cook: {cook}min"
    info += f" • 🍽️ Serves: {serves}"
    L.append(info)
    L.append("")
    L.append(DIFF_MSG.get(diff, ""))
    L.append("")
    L.append("---")
    L.append("### 🛒 Ingredients")
    for i, ing in enumerate(ingredients):
        L.append(f"  {i+1}. {ing}")
    L.append("")
    L.append("---")
    L.append("### 👨‍🍳 Let's Cook!")
    L.append(random.choice(STEP_INTROS))
    L.append("")
    emojis = ["🔥","🍳","✨","💫","🎯","⭐","🌟","💎","🎨","👆"]
    for i, step in enumerate(steps):
        L.append(f"**Step {i+1}:** {emojis[i%len(emojis)]} {step}")
        L.append("")
    if tips:
        L.append("---")
        L.append(f"### {random.choice(TIP_INTROS)}")
        for tip in tips: L.append(f"  ✅ {tip}")
        L.append("")
    if nutrition:
        L.append("---")
        L.append("### 📈 Nutrition (per serving)")
        np = []
        if "cal" in nutrition: np.append(f"🔋 {nutrition['cal']} cal")
        if "protein" in nutrition: np.append(f"💪 {nutrition['protein']}g protein")
        if "carbs" in nutrition: np.append(f"🌾 {nutrition['carbs']}g carbs")
        if "fat" in nutrition: np.append(f"🧈 {nutrition['fat']}g fat")
        L.append(" | ".join(np))
        L.append("")
    L.append("---")
    L.append(f"*{random.choice(SIGNOFF)}*")
    return "\n".join(L)


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
