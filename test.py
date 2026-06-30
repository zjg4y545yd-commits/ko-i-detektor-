import streamlit as st
import json
import os
from datetime import date, datetime
import uuid
import base64

# Nastavení stránky
st.set_page_config(page_title="Umělecké kovářství Štěpán Palla", layout="wide", initial_sidebar_state="expanded")

# --- FUNKCE ---
SOUBOR_TERMINY = "terminy.json"
SOUBOR_NAVSTEVNOST = "navstevnost.json"

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

# Inicializace session
if "terminy" not in st.session_state: st.session_state.terminy = nacti_json(SOUBOR_TERMINY, [])
if "prihlasen" not in st.session_state: st.session_state.prihlasen = False

# --- CSS STYLING ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #13111c !important; color: #e2e8f0; }
[data-testid="stSidebar"] { background-color: #1e1b30 !important; border-right: 1px solid #2d2a45; }
[data-testid="stSidebarNav"] { display: none; }
.sidebar-logo-text { font-size: 1.2rem; font-weight: 700; color: #ffffff; padding: 10px 0 20px 0; border-bottom: 1px solid #2d2a45; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; }
.hero-banner { background: #000000; border: 1px solid #3d355c; border-radius: 16px; padding: 2rem; text-align: center; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.8); }
.hero-banner img { max-width: 90%; height: auto; margin-bottom: 1.5rem; }
.content-card { background-color: #1a1829; border: 1px solid #2d2a45; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
.stButton>button { background-color: #6941c6 !important; color: white !important; border-radius: 8px !important; }
[data-testid="stPopover"] > button { background-color: #c05c5c !important; color: white !important; border-radius: 50% !important; width: 45px !important; height: 45px !important; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<div class='sidebar-logo-text'>Kovářství<br>Štěpán Palla</div>", unsafe_allow_html=True)
    seznam_stranek = ["Domů (Informace)", "Ukázky práce", "Kalkulačka zakázky", "Sjednat termín"]
    if st.session_state.prihlasen: seznam_stranek.extend(["Administrace", "Návštěvnost"])
    vybrana_polozka = st.radio("Menu", seznam_stranek, label_visibility="collapsed")

# --- HLAVNÍ LOGIKA ---
col_spacer1, col_spacer2, col_login = st.columns([8, 1, 1])
with col_login:
    with st.popover("ŠP"):
        if not st.session_state.prihlasen:
            if st.text_input("Jméno") == "1" and st.text_input("Heslo", type="password") == "1":
                st.session_state.prihlasen = True; st.rerun()
        else:
            if st.button("Odhlásit"): st.session_state.prihlasen = False; st.rerun()

if vybrana_polozka == "Domů (Informace)":
    # Tady se načítá tvoje fotka jako PNG
    nazev_souboru = "pozadi2.png"
    logo_base64 = nacti_obrazek_base64(nazev_souboru)
    
    if logo_base64:
        zobrazeni = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo">'
    else:
        st.error(f"Fotka '{nazev_souboru}' nenalezena v: {os.getcwd()}")
        zobrazeni = '<h1>Umělecké kovářství Štěpán Palla</h1>'

    st.markdown(f'<div class="hero-banner">{zobrazeni}<p>Poctivé kovářské řemeslo.</p></div>', unsafe_allow_html=True)

elif vybrana_polozka == "Ukázky práce":
    st.markdown("<h2>Ukázky naší práce</h2>", unsafe_allow_html=True)
    if not os.path.exists("fotogalerie"): os.makedirs("fotogalerie")
    fotky = [f for f in os.listdir("fotogalerie") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    cols = st.columns(3)
    for i, fotka in enumerate(fotky):
        with cols[i % 3]: st.image(os.path.join("fotogalerie", fotka), use_container_width=True)

elif vybrana_polozka == "Kalkulačka zakázky":
    st.markdown("<h2>Kalkulačka</h2>", unsafe_allow_html=True)
    produkt = st.selectbox("Typ:", ["Kovaná brána", "Kovaný plot"])
    delka = st.number_input("Metry:", value=3.0)
    if st.button("Vypočítat"): st.write("Výsledek: ...")

elif vybrana_polozka == "Sjednat termín":
    st.write("Kontaktuj nás...")
