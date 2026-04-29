import streamlit as st
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

@st.cache_data
def get_recipe_db():
    return get_all_recipes()

def get_vision_analysis(image_file):
    """
    Ultra-Robust Vision Logic with detailed error reporting.
    """
    try:
        # Prepare image
        img = Image.open(image_file).convert("RGB")
        img.save("temp_scan.jpg", "JPEG")
            
        # Strategy 1: Moondream (Fastest)
        try:
            with st.status("🔮 Accessing Sibling Vision..."):
                client = Client("vikhyatk/moondream2", timeout=30)
                result = client.predict(handle_file("temp_scan.jpg"), "List ingredients.", api_name="/answer_question")
                if result: return str(result)
        except Exception as e:
            st.info(f"Sibling Vision busy, trying Research Node... (Error: {str(e)[:50]})")

        # Strategy 2: InternVL2 (Powerful)
        try:
            with st.status("🔮 Querying Research Node..."):
                client = Client("OpenGVLab/InternVL2-8B", timeout=30)
                result = client.predict(handle_file("temp_scan.jpg"), "List ingredients.", api_name="/predict")
                if result: return str(result)
        except: pass

        # Strategy 3: BLIP2
        try:
            with st.status("🔮 Final Check..."):
                client = Client("Salesforce/BLIP2", timeout=30)
                result = client.predict(handle_file("temp_scan.jpg"), "List ingredients.", api_name="/predict")
                if result: return str(result)
        except: pass

        return "RETRY_MANUAL"

    except Exception as e:
        return f"Scan error: {str(e)}"

def get_web_recipe_research(query):
    """
    Real-time internet research using DuckDuckGo.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(f"authentic Indian recipe for {query}", max_results=3))
            research_data = "\n".join([f"Source: {r['title']}\nSnippet: {r['body']}" for r in results])
            return research_data
    except:
        return "No specific web results found, but I will use my internal elder sibling knowledge!"

def get_ai_bhai_response(prompt, language="English", context_recipes=None):
    """
    Combines local database, internet research, and LLM creativity.
    """
    research_context = ""
    if not context_recipes:
        with st.status("🌐 Researching the Global Culinary Web..."):
            research_context = get_web_recipe_research(prompt)
    
    lang_map = {
        "Hindi": "Hinglish (Hindi in English script)",
        "Telugu": "Tenglish (Telugu in English script)",
        "Tamil": "Tanglish (Tamil in English script)",
        "Kannada": "Kanglish (Kannada in English script)",
        "Malayalam": "Manglish (Malayalam in English script)",
        "Bengali": "Benglish (Bengali in English script)",
        "Marathi": "Maranglish (Marathi in English script)",
        "English": "Clean, friendly English"
    }
    
    target_lang = lang_map.get(language, "English")
    
    local_context = ""
    if context_recipes:
        local_context = f"I found these relevant recipes in our family diary:\n"
        for r in context_recipes[:3]:
            local_context += f"- {r['recipe']['name']} ({r['recipe']['region']})\n"

    system_prompt = f"""You are 'AI Bhai', the user's Caring Elder Sibling.
    LANGUAGE: Speak in {target_lang}. Mix local words and English naturally.
    
    PERSONALITY:
    - Extremely friendly, caring, and professional.
    - Use terms like 'Mere pyaare bhai', 'Meri behan', 'Dost', 'Anna', 'Akka'.
    
    RESOURCES:
    - Local Diary Context: {local_context}
    - Internet Research Context: {research_context}
    
    TASK:
    - If local recipes exist, use them.
    - If not, use the Internet Research context to provide a professional, 2026-grade recipe.
    - If the user provides ingredients from a scan, 'research' your knowledge to give the best dish.
    
    FORMAT:
    1. Warm Sibling Greeting.
    2. A loving story about why you 'searched' the web for this special request.
    3. Ingredients.
    4. [STEP: Description] (Professional).
    5. A 'Secret Sibling Tip'.
    """
    
    full_prompt = f"{system_prompt}\n\nUser: {prompt}"
    encoded = urllib.parse.quote(full_prompt)
    
    try:
        r = requests.get(f"https://text.pollinations.ai/{encoded}", timeout=30)
        return r.text
    except:
        return "Arre bhai, connection issue! Let me try again."

def render_styled_recipe(text):
    """Renders text with custom step cards WITHOUT images."""
    # Split by various step markers
    pattern = r'\[STEP:\s*(.*?)\]|\*\*Step\s*\d+:\*\*\s*(.*?)(?=\n|$)|Step\s*\d+:\s*(.*?)(?=\n|$)'
    parts = re.split(pattern, text, flags=re.MULTILINE)
    
    cleaned_parts = []
    for i, p in enumerate(parts):
        if p is None: continue
        if i % 4 == 0:
            cleaned_parts.append(p)
        else:
            if p.strip():
                cleaned_parts.append(p.strip())
    
    if len(cleaned_parts) <= 1:
        st.markdown(text)
        return

    step_count = 1
    for i in range(0, len(cleaned_parts), 2):
        if cleaned_parts[i].strip():
            st.markdown(cleaned_parts[i])
            
        if i + 1 < len(cleaned_parts):
            step_desc = cleaned_parts[i+1]
            st.markdown(f"<div class='recipe-step'><b>🔥 Step {step_count}:</b> {step_desc}</div>", unsafe_allow_html=True)
            # Removed image generation as per user request
            step_count += 1

# ==========================================
# 🚀 MAIN APP
# ==========================================
def main():
    apply_ultimatic_theme()
    recipes_db = get_recipe_db()

    # Sidebar
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: #F28C28; font-family: Fredoka, sans-serif;'>ai bhai</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: white; opacity: 0.8; letter-spacing: 2px; font-size: 0.8rem;'>YOUR AI COOKING ASSISTANT</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color: white; opacity:0.5; font-size: 0.7rem;'>v2.0 | {get_recipe_count()} Recipes</p>", unsafe_allow_html=True)
        
        st.divider()
        
        st.subheader("🗣️ AI BHAI SPEAKS")
        lang = st.selectbox("Choose Tone", ["English", "Hindi", "Telugu", "Tamil", "Kannada", "Malayalam", "Bengali", "Marathi"], help="AI Bhai will speak in your preferred local transliterated language!")
        
        st.divider()
        
        mode = st.radio("🛠️ ACTIONS", ["Chat & Recipes", "Ingredient Scanner", "Explore Regions"])
        
        st.divider()
        
        with st.expander("🌶️ Dietary Filters"):
            veg_only = st.checkbox("Veg Only", value=True)
            spicy_level = st.select_slider("Spice Level", options=["Mild", "Medium", "Desi Hot"])
            
        st.info("💡 **Pro Tip:** Upload a photo of your fridge to see what AI Bhai can cook!")

    # Main Hero Section
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "scanner_results" not in st.session_state:
        st.session_state.scanner_results = None
    if "selected_recipe" not in st.session_state:
        st.session_state.selected_recipe = None
        
    if not st.session_state.messages and not st.session_state.selected_recipe:
        st.markdown("<h1 class='hero-text'>ai bhai</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.2rem; opacity: 0.8;'>YOUR AI COOKING ASSISTANT</p>", unsafe_allow_html=True)
        
        # Featured Icons row (as seen in mockup)
        cols = st.columns(4)
        icons = [
            ("🍃", "INDIAN RECIPES", "Authentic flavors"),
            ("👨🏽‍🍳", "STEP BY STEP", "Easy to follow"),
            ("🌶️", "MADE EASY", "Simple cooking"),
            ("✨", "AI POWERED", "Smart assistant")
        ]
        for i, (icon, title, sub) in enumerate(icons):
            with cols[i]:
                st.markdown(f"""
                <div style='text-align: center; padding: 20px; background: white; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid rgba(242, 140, 40, 0.1);'>
                    <div style='font-size: 2.5rem;'>{icon}</div>
                    <div style='font-weight: 700; font-size: 0.9rem; margin-top: 10px; color: #F28C28;'>{title}</div>
                    <div style='font-size: 0.7rem; opacity: 0.6;'>{sub}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='bento-card'><h3>📅 Daily Special</h3>{storyteller.get_daily_special()}</div>", unsafe_allow_html=True)
            if st.button("Get Daily Recipe"):
                r = random.choice(recipes_db)
                st.session_state.selected_recipe = r
                st.rerun()
                
        with col2:
            st.markdown("<div class='bento-card'><h3>🎲 Surprise Me</h3>Feel lucky? Let AI Bhai pick a random dish!</div>", unsafe_allow_html=True)
            if st.button("🎲 Random Recipe"):
                r = random.choice(recipes_db)
                st.session_state.selected_recipe = r
                st.rerun()
                
        with col3:
            st.markdown(f"<div class='bento-card'><h3>Stats</h3>👨‍🍳 <b>{get_recipe_count()}</b> Local Recipes<br>🚀 <b>Zero-Key</b> AI Engaged</div>", unsafe_allow_html=True)

    # Global Selected Recipe View
    if st.session_state.selected_recipe:
        if st.button("← Back"):
            st.session_state.selected_recipe = None
            st.rerun()
        story = storyteller.format_recipe_story(st.session_state.selected_recipe)
        render_styled_recipe(story)
        return

    # --- MODE: CHAT ---
    if mode == "Chat & Recipes":
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                render_styled_recipe(msg["content"])

        if prompt := st.chat_input("What should we cook today, Bhai?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            matches = ingredient_matcher.search_recipes(prompt, recipes_db)
            with st.chat_message("assistant"):
                with st.status("🧠 Consulting the spices..."):
                    response = get_ai_bhai_response(prompt, lang, matches)
                render_styled_recipe(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    # --- MODE: SCANNER ---
    elif mode == "Ingredient Scanner":
        st.header("📸 Visual Ingredient Scanner")
        
        if st.button("🗑️ Reset Scanner"):
            st.session_state.scanner_results = None
            st.rerun()

        tab1, tab2 = st.tabs(["📤 Upload Photo", "✍️ Manual Entry"])
        
        with tab1:
            uploaded_file = st.file_uploader("Show me your ingredients...", type=["jpg", "jpeg", "png"])
        with tab2:
            manual_input = st.text_area("Tell me what ingredients you have (e.g. Tomato, Onion, Chicken)...")
            if st.button("🔍 Research My Ingredients"):
                if manual_input:
                    matches = ingredient_matcher.match_recipes(manual_input.split(","), recipes_db)
                    st.session_state.scanner_results = {"detected": manual_input, "matches": matches}

        active_file = uploaded_file
        
        if active_file:
            st.image(active_file, caption="Selected Image", width=300)
            c1, c2 = st.columns(2)
            if c1.button("🔍 Start AI Analysis"):
                detected_text = get_vision_analysis(active_file)
                
                if detected_text == "RETRY_MANUAL":
                    st.warning("Arre bhai, the AI servers are a bit busy! Can you please use the 'Manual Entry' tab or tell me in chat?")
                elif "Scan error" in detected_text:
                    st.error(f"Technical glitch! {detected_text}")
                else:
                    detected_list = [i.strip() for i in detected_text.split(",")]
                    matches = ingredient_matcher.match_recipes(detected_list, recipes_db)
                    st.session_state.scanner_results = {"detected": detected_text, "matches": matches}
            
            if c2.button("❌ Cancel Photo"):
                st.rerun() # Simple rerun will clear the temporary state if file uploader is not interacted with
            
            if st.session_state.scanner_results:
                res = st.session_state.scanner_results
                st.markdown(f"<div class='bento-card'><h3>🔍 AI Findings</h3>{res['detected']}</div>", unsafe_allow_html=True)
                if res['matches']:
                    st.success(f"Found {len(res['matches'])} family recipes!")
                    for m in res['matches'][:5]:
                        col_a, col_b = st.columns([3, 1])
                        col_a.write(f"🥘 **{m['recipe']['name']}** ({m['match_pct']}% match)")
                        if col_b.button("Cook This", key=f"scan_{m['recipe']['name']}"):
                            st.session_state.selected_recipe = m['recipe']
                            st.rerun()
                else:
                    st.info("No exact matches, but I can create something special!")
                    if st.button("👨‍🍳 Create Custom Recipe"):
                        with st.status("🧠 Consulting sibling diary..."):
                            ai_res = get_ai_bhai_response(f"I have: {res['detected']}. Make a professional recipe.", lang)
                            st.session_state.messages.append({"role": "assistant", "content": ai_res})
                            st.session_state.selected_recipe = None # Clear this to show chat history
                            st.rerun()

    # --- MODE: EXPLORE ---
    elif mode == "Explore Regions":
        st.header("🗺️ Explore Regional Cuisines")
        
        # Two-tier filtering: Region -> State
        all_regions = sorted(list(set(r.get("region") for r in recipes_db if r.get("region"))))
        sel_region = st.selectbox("1. Select Region", ["All"] + all_regions)
        
        filtered_by_region = recipes_db
        if sel_region != "All":
            filtered_by_region = [r for r in recipes_db if r.get("region") == sel_region]
            
        all_states = sorted(list(set(r.get("state") for r in filtered_by_region if r.get("state"))))
        sel_state = st.selectbox("2. Select State", ["All"] + all_states)
        
        final_recipes = filtered_by_region
        if sel_state != "All":
            final_recipes = [r for r in filtered_by_region if r.get("state") == sel_state]
            
        st.write(f"Showing **{len(final_recipes)}** recipes")
        
        # Grid Display
        for i in range(0, len(final_recipes), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(final_recipes):
                    r = final_recipes[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='bento-card'><h4>{r['name']}</h4><p>{r.get('cat', 'Main Course')} • {r.get('diff', 'Medium')}</p></div>", unsafe_allow_html=True)
                        if st.button("View Recipe", key=f"expl_{r['name']}"):
                            st.session_state.selected_recipe = r
                            st.rerun()

if __name__ == "__main__":
    main()
