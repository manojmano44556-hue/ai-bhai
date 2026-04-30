import streamlit as st
import os
import sys

# Ensure the root directory is in the python path for deployments
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import json
import io
import re
import urllib.parse
import time
import random
from PIL import Image
from gradio_client import Client, handle_file
from duckduckgo_search import DDGS
from streamlit_lottie import st_lottie

# Import local modules
import ingredient_matcher
import storyteller
from recipes import get_all_recipes, get_recipe_count, get_regions, get_categories

# ==========================================
# 🌌 2026 ULTIMATIC AGENTIC CONFIG
# ==========================================
st.set_page_config(
    page_title="AI Bhai | The Ultimate Desi Chef",
    page_icon="👨🏽‍🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

lottie_chef = load_lottieurl("https://lottie.host/8863f6c2-0731-417e-9762-c07a0e106967/I4z3Y5E8oI.json") 
lottie_cooking = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_tll0j4bb.json")

def apply_ultimatic_theme():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;900&family=Fredoka:wght@300;700&family=Playfair+Display:ital,wght@0,900;1,900&display=swap');

:root {
    --bhai-orange: #F28C28;
    --bhai-dark: #22262B;
    --bhai-green: #6BAA4A;
    --bhai-red: #E64B3C;
    --bhai-purple: #7C4D9C;
    --bhai-cream: #FFF9F3;
    --pure-white: #FFFFFF;
}

.stApp {
    background-color: var(--bhai-cream);
    color: var(--bhai-dark) !important;
    font-family: 'Outfit', sans-serif;
}

/* Typography */
h1, h2, h3 { 
    color: var(--bhai-dark) !important; 
    font-family: 'Fredoka', sans-serif !important; 
    font-weight: 700;
}

.hero-text {
    font-family: 'Fredoka', sans-serif;
    font-size: 4rem;
    color: var(--bhai-orange) !important;
    text-align: center;
    margin-bottom: 0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--bhai-dark) !important;
    color: white !important;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Bento Cards */
.bento-card {
    background: var(--pure-white);
    border: 2px solid rgba(242, 140, 40, 0.1);
    border-radius: 24px;
    padding: 24px;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.bento-card:hover {
    transform: translateY(-5px);
    border-color: var(--bhai-orange);
    box-shadow: 0 15px 40px rgba(242, 140, 40, 0.15);
}

/* Recipe Step Styling */
.recipe-step {
    border-left: 6px solid var(--bhai-orange);
    padding: 20px;
    margin: 20px 0;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

/* Custom Buttons */
.stButton>button {
    background: var(--bhai-orange) !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 50px !important;
    padding: 0.5rem 2rem !important;
    border: none !important;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.05);
    background: #d97a1d !important;
}

/* Chat Bubbles */
[data-testid="stChatMessage"] {
    background: white !important;
    border-radius: 20px !important;
    border: 1px solid rgba(0,0,0,0.05);
    color: var(--bhai-dark) !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 ULTIMATIC BRAIN
# ==========================================

@st.cache_resource
def get_recipe_db():
    return get_all_recipes()

@st.cache_data
def get_cached_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def get_vision_analysis(image_file):
    """Robust Vision Logic for scanning ingredients."""
    try:
        img = Image.open(image_file).convert("RGB")
        img.save("temp_scan.jpg", "JPEG")
        with st.status("🔮 Bhai is looking at your ingredients..."):
            client = Client("vikhyatk/moondream2", timeout=30)
            result = client.predict(handle_file("temp_scan.jpg"), "List ingredients.", api_name="/answer_question")
            return str(result) if result else "RETRY_MANUAL"
    except Exception as e:
        return f"Scan error: {str(e)}"

def get_web_recipe_research(query):
    """Real-time internet research using DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(f"authentic Indian recipe for {query}", max_results=3))
            return "\n".join([f"Source: {r['title']}\nSnippet: {r['body']}" for r in results])
    except:
        return "No specific web results found, but I will use my internal elder sibling knowledge!"

def get_ai_bhai_response(prompt, language="English", context_recipes=None):
    """Generates warm, friendly sibling-style responses."""
    research_context = "" if context_recipes else get_web_recipe_research(prompt)
    
    lang_map = {"Hindi": "Hinglish", "Telugu": "Tenglish", "Tamil": "Tanglish", "Kannada": "Kanglish", 
                "Malayalam": "Manglish", "Bengali": "Benglish", "Marathi": "Maranglish", "English": "English"}
    target_lang = lang_map.get(language, "English")
    
    local_context = "I found these in our family diary:\n" + "\n".join([f"- {r['recipe']['name']}" for r in context_recipes[:3]]) if context_recipes else ""

    system_prompt = f"You are 'AI Bhai', a caring elder sibling. Speak in {target_lang}. Use local terms naturally. Context: {local_context} {research_context}"
    encoded = urllib.parse.quote(f"{system_prompt}\nUser: {prompt}")
    
    try:
        r = requests.get(f"https://text.pollinations.ai/{encoded}", timeout=30)
        return r.text
    except:
        return "Arre bhai, connection issue! Try again?"

def apply_ultimatic_theme():
    # Only inject once to save performance
    if 'theme_applied' not in st.session_state:
        st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;900&family=Fredoka:wght@300;700&family=Playfair+Display:ital,wght@0,900;1,900&display=swap');

:root {
    --bhai-orange: #F28C28;
    --bhai-dark: #22262B;
    --bhai-green: #6BAA4A;
    --bhai-red: #E64B3C;
    --bhai-purple: #7C4D9C;
    --bhai-cream: #FFF9F3;
    --pure-white: #FFFFFF;
}

.stApp {
    background-color: var(--bhai-cream);
    color: var(--bhai-dark) !important;
    font-family: 'Outfit', sans-serif;
}

h1, h2, h3 { 
    color: var(--bhai-dark) !important; 
    font-family: 'Fredoka', sans-serif !important; 
    font-weight: 700;
}

.hero-text {
    font-family: 'Fredoka', sans-serif;
    font-size: 4rem;
    color: var(--bhai-orange) !important;
    text-align: center;
    margin-bottom: 0;
}

[data-testid="stSidebar"] {
    background: var(--bhai-dark) !important;
}

.bento-card {
    background: var(--pure-white);
    border: 2px solid rgba(242, 140, 40, 0.1);
    border-radius: 24px;
    padding: 24px;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.recipe-step-card {
    background: white;
    padding: 20px;
    margin: 10px 0;
    border-radius: 16px;
    border-left: 5px solid var(--bhai-orange);
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}
</style>
""", unsafe_allow_html=True)
        st.session_state.theme_applied = True

def render_recipe_structured(data):
    """Modern structured rendering with fail-safe for transition."""
    # Fail-safe: If data is a string (old format), just show it
    if isinstance(data, str):
        st.markdown(data)
        return

    # Modern Bento UI for dictionaries
    st.markdown(f"<h1 style='color:#F28C28;'>{data.get('icon', '👨‍🍳')} {data.get('name', 'Recipe')}</h1>", unsafe_allow_html=True)
    if data.get('name_hi'): st.markdown(f"*{data['name_hi']}*")
    
    st.write(f"### {data.get('greeting', 'Namaste!')}")
    st.write(data.get('intro', 'Let\'s cook something special!'))
    
    # Bento Quick Info
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("🗺️ Region", data['region'])
    with c2: st.metric("⏱️ Prep", f"{data['prep']}m")
    with c3: st.metric("🔥 Cook", f"{data['cook']}m")
    with c4: st.metric("📏 Difficulty", data['diff'])
    
    tab1, tab2, tab3 = st.tabs(["🛒 Ingredients", "👨‍🍳 Cooking Steps", "📖 Story & Tips"])
    
    with tab1:
        st.markdown("### Necessary Ingredients")
        for i, ing in enumerate(data['ingredients']):
            st.markdown(f"✅ **{ing}**")
            
    with tab2:
        st.markdown("### Let's cook it right!")
        for i, step in enumerate(data['steps']):
            st.markdown(f"""<div class='recipe-step-card'>
                <b>Step {i+1}</b><br>{step}
            </div>""", unsafe_allow_html=True)
            
    with tab3:
        if data['story']:
            st.info(f"**The Origin Story:**\n\n{data['story']}")
        if data['tips']:
            st.warning("**AI Bhai's Pro Tips:**\n\n" + "\n".join([f"- {t}" for t in data['tips']]))
        
        if data['nutrition']:
            st.write("---")
            st.write("**Nutrition Facts:**")
            st.json(data['nutrition'])

    st.divider()
    st.write(f"*{data['signoff']}*")

def main():
    apply_ultimatic_theme()
    recipes_db = get_recipe_db()
    
    # Load Lottie animations with caching
    lottie_chef = get_cached_lottie("https://lottie.host/8863f6c2-0731-417e-9762-c07a0e106967/I4z3Y5E8oI.json")

    # Sidebar
    with st.sidebar:
        st_lottie(lottie_chef, height=150) if lottie_chef else st.title("AI Bhai")
        st.markdown("<h2 style='text-align: center; color: #F28C28;'>The Desi Chef</h2>", unsafe_allow_html=True)
        
        mode = st.radio("🛠️ ACTIONS", ["Chat & Recipes", "Ingredient Scanner", "Explore Regions"])
        lang = st.selectbox("🗣️ Language", ["English", "Hindi", "Telugu", "Tamil", "Kannada", "Malayalam", "Bengali", "Marathi"])
        
        st.divider()
        if st.button("🎲 Surprise Me!"):
            st.session_state.selected_recipe = random.choice(recipes_db)
            st.rerun()

    # App Logic
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if st.session_state.get('selected_recipe'):
        if st.button("← Back to Menu"):
            st.session_state.selected_recipe = None
            st.rerun()
        
        recipe_data = storyteller.format_recipe_story(st.session_state.selected_recipe)
        render_recipe_structured(recipe_data)
        return

    # Landing Page
    if not st.session_state.messages:
        st.markdown("<h1 class='hero-text'>ai bhai</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>YOUR ULTIMATE AI COOKING SIBLING</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='bento-card'><h3>Daily Special</h3>{storyteller.get_daily_special()}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='bento-card'><h3>Stats</h3>🔥 <b>{len(recipes_db)}</b> Local Recipes</div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='bento-card'><h3>Mood</h3>Feeling hungry? Let's fix that!</div>", unsafe_allow_html=True)

    # Chat / Explore Modes
    if mode == "Chat & Recipes":
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Ask me for a recipe..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            matches = ingredient_matcher.search_recipes(prompt, recipes_db)
            with st.chat_message("assistant"):
                if matches:
                    st.write(f"I found some recipes for you! Click one to see details:")
                    for m in matches[:5]:
                        if st.button(f"🥘 {m['recipe']['name']}", key=f"chat_{m['recipe']['name']}"):
                            st.session_state.selected_recipe = m['recipe']
                            st.rerun()
                else:
                    with st.spinner("Bhai is thinking..."):
                        response = get_ai_bhai_response(prompt, lang)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})

    elif mode == "Ingredient Scanner":
        st.header("📸 Visual Ingredient Scanner")
        
        uploaded_file = st.file_uploader("Show me your ingredients...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            st.image(uploaded_file, width=300)
            if st.button("🔍 Analyze Ingredients"):
                detected = get_vision_analysis(uploaded_file)
                st.info(f"Bhai detected: {detected}")
                
                detected_list = [i.strip() for i in detected.split(",")]
                matches = ingredient_matcher.match_recipes(detected_list, recipes_db)
                
                if matches:
                    st.success(f"I found {len(matches)} matching recipes!")
                    for m in matches[:5]:
                        if st.button(f"🥘 {m['recipe']['name']} ({m['match_pct']}% match)", key=f"scan_{m['recipe']['name']}"):
                            st.session_state.selected_recipe = m['recipe']
                            st.rerun()
                else:
                    st.warning("No exact matches in our diary, but I can create a custom one!")
                    if st.button("👨‍🍳 Create Custom Recipe"):
                        response = get_ai_bhai_response(f"I have: {detected}. Make a recipe.", lang)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()

    elif mode == "Explore Regions":
        st.header("🗺️ Regional Specialties")
        regions = sorted(list(set(r.get('region', 'Other') for r in recipes_db)))
        sel_region = st.selectbox("Select Region", regions)
        
        filtered = [r for r in recipes_db if r.get('region') == sel_region]
        
        # Grid Display with Bento styling
        for i in range(0, len(filtered), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(filtered):
                    r = filtered[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='bento-card' style='padding:15px; margin-bottom:10px;'><b>{r['name']}</b><br><small>{r.get('state', '')}</small></div>", unsafe_allow_html=True)
                        if st.button("View Details", key=f"expl_{r['name']}"):
                            st.session_state.selected_recipe = r
                            st.rerun()

if __name__ == "__main__":
    main()
