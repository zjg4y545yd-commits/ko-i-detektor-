import streamlit as st
import json
import os
from datetime import date, datetime
import uuid
import base64

# Nastavení stránky na široký profil
st.set_page_config(page_title="Umělecké kovářství Štěpán Palla", layout="wide", initial_sidebar_state="expanded")

# --- FUNKCE PRO DATA A OBRÁZKY ---
SOUBOR_TERMINY = "terminy.json"
SOUBOR_NAVSTEVNOST = "navstevnost.json"
SOUBOR_GALERIE = "galerie.json"
SOUBOR_CENIK = "cenik.json"

DEFAULT_CENIK = {
    "zelezo_kg": 28.50,
    "produkty": {
        "Kovaná brána (vjezdová)": {"kg_na_metr": 55, "prace_na_metr": 6500},
        "Kovaný plot (plotové dílce)": {"kg_na_metr": 35, "prace_na_metr": 4200},
        "Kované dveře / mříže": {"kg_na_metr": 45, "prace_na_metr": 7000}
    }
}

def nacti_json(soubor, default_hodnota):
    if os.path.exists(soubor):
        with open(soubor, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_hodnota

def uloz_json(soubor, data):
    with open(soubor, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def nacti_obrazek_base64(cesta_k_souboru):
    if os.path.exists(cesta_k_souboru):
        with open(cesta_k_souboru, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# Inicializace session state
if "terminy" not in st.session_state:
    st.session_state.terminy = nacti_json(SOUBOR_TERMINY, [])
if "galerie" not in st.session_state:
    st.session_state.galerie = nacti_json(SOUBOR_GALERIE, [])
if "cenik" not in st.session_state:
    st.session_state.cenik = nacti_json(SOUBOR_CENIK, DEFAULT_CENIK)
if "prihlasen" not in st.session_state:
    st.session_state.prihlasen = False

# --- SYSTÉM SLEDOVÁNÍ NÁVŠTĚVNOSTI ---
if "navsteva_zaznamenana" not in st.session_state:
    st.session_state.navsteva_zaznamenana = True
    st.session_state.visitor_id = str(uuid.uuid4())[:8] 
    
    data_navstev = nacti_json(SOUBOR_NAVSTEVNOST, {})
    dnes = str(date.today())
    cas = datetime.now().strftime("%H:%M:%S")
    
    if dnes not in data_navstev:
        data_navstev[dnes] = []
    if not isinstance(data_navstev[dnes], list):
        data_navstev[dnes] = []
        
    data_navstev[dnes].append({"cas": cas, "id": st.session_state.visitor_id})
    uloz_json(SOUBOR_NAVSTEVNOST, data_navstev)

# --- INJEKCE FONTŮ PŘÍMO DO HTML ---
st.markdown('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Allura&family=Pinyon+Script&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# --- CSS STYLING (Zlaté nadpisy, tenký elegantní podpisový styl) ---
st.markdown("""
<style>
/* Pojistka přes @import pro jistotu stažení fontu */
@import url('https://fonts.googleapis.com/css2?family=Allura&family=Pinyon+Script&family=Inter:wght@400;500;600&display=swap');

[data-testid="stAppViewContainer"] { background-color: #110f16 !important; color: #e2e8f0; }
[data-testid="stSidebar"] { background-color: #171520 !important; border-right: 1px solid #2a2538; }
[data-testid="stHeader"] { background-color: transparent !important; }
[data-testid="stSidebarNav"] { display: none; }

/* ZMĚNA: Elegantní tenký font podobný logu na fotce, barva vrácena na zlatou */
h1, h2, h3, h4 { 
    font-family: 'Pinyon Script', 'Allura', cursive !important; 
    color: #c5a059 !important; 
    letter-spacing: 1px; 
    font-weight: 400 !important; 
}
/* Kaligrafické fonty jsou vizuálně menší, proto jsou hodnoty rem zvětšené */
h1 { font-size: 5.5rem !important; } 
h2 { font-size: 4.2rem !important; }
h3 { font-size: 3.4rem !important; }
h4 { font-size: 2.8rem !important; }

p, span, div, label { font-family: 'Inter', sans-serif; }

.sidebar-logo-container { text-align: center; padding: 15px 0 25px 0; border-bottom: 1px solid #2a2538; margin-bottom: 20px; }
.sidebar-logo-img { max-width: 90%; height: auto; display: block; margin: 0 auto; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.5)); }

/* Náhradní podpis v menu */
.sidebar-logo-text { 
    font-family: 'Pinyon Script', 'Allura', cursive !important; 
    font-size: 3.5rem; 
    font-weight: 400; 
    color: #c5a059; 
    padding: 10px 0 20px 0; 
    border-bottom: 1px solid #2a2538; 
    margin-bottom: 20px; 
    text-align: center; 
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span[data-baseweb="radio"] { display: none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label { padding: 12px 15px; border-radius: 8px; margin-bottom: 6px; cursor: pointer; background-color: transparent; transition: all 0.3s ease; display: flex; align-items: center; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover { background-color: rgba(197, 160, 89, 0.08); border-left: 3px solid #c5a059; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div { font-size: 0.95rem; font-weight: 500; margin-left: 5px; color: #cbd5e1; }

.menu-section-title { font-size: 0.75rem; color: #71717a; text-transform: uppercase; font-weight: 600; margin-top: 25px; margin-bottom: 10px; padding-left: 5px; letter-spacing: 1px; }

.hero-banner { background: linear-gradient(135deg, #1c1924 0%, #121017 100%); border: 1px solid #36304a; border-radius: 16px; padding: 3.5rem 2rem; text-align: center; margin-bottom: 2.5rem; box-shadow: 0 15px 35px rgba(0,0,0,0.6); }
.hero-banner h1 { margin-bottom: 15px; border: none; }
.hero-banner p { font-size: 1.15rem; color: #94a3b8; max-width: 750px; margin: 0 auto; line-height: 1.6; }

.content-card { background-color: #16141d; border: 1px solid #2a2538; border-radius: 12px; padding: 24px; margin-bottom: 20px; transition: transform 0.3s ease, box-shadow 0.3s ease; }
.content-card:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(197, 160, 89, 0.12); border-color: #453d5a; }

.stImage img { border-radius: 8px !important; border: 1px solid #2a2538 !important; transition: transform 0.3s ease; }
.stImage img:hover { transform: scale(1.02); }

.stButton>button { background-color: #c5a059 !important; color: #110f16 !important; border: none !important; border-radius: 8px !important; padding: 0.6rem 1.8rem !important; font-weight: 700 !important; letter-spacing: 0.5px; transition: all 0.3s ease !important; box-shadow: 0 4px 12px rgba(197, 160, 89, 0.2) !important; }
.stButton>button:hover { background-color: #e5c17b !important; transform: translateY(-1px); box-shadow: 0 6px 15px rgba(197, 160, 89, 0.
