import streamlit as st
import json
import os
from datetime import date, datetime
import uuid
import base64

# Nastavení stránky
st.set_page_config(page_title="Umělecké kovářství", layout="wide")

# --- FUNKCE PRO DATA A OBRÁZKY ---
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

# Inicializace session state
if "terminy" not in st.session_state:
    st.session_state.terminy = nacti_json(SOUBOR_TERMINY, [])
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

# --- CSS STYLING A DYNAMICKÉ POZADÍ ---
obrazek_pozadi_base64 = nacti_obrazek_base64("pozadi.png")

if obrazek_pozadi_base64:
    css_pozadi = f"""
    .stApp {{
        background-image: url("data:image/png;base64,{obrazek_pozadi_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .main .block-container {{ background-color: rgba(26, 27, 28, 0.85) !important; backdrop-filter: blur(5px); }}
    """
else:
    css_pozadi = ".stApp { background-color: #2e3033 !important; }"

st.markdown(f"""
<style>
{css_pozadi}
.main .block-container {{ padding: 3rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.6); color: #f5f5f5 !important; margin-top: 1rem; }}
h1, h2, h3 {{ color: #ff6600 !important; font-family: 'Georgia', serif; }}
.stButton>button {{ background-color: #3a1c00 !important; color: #d4af37 !important; border: 1px solid #d4af37 !important; }}
</style>
""", unsafe_allow_html=True)

# --- HLAVIČKA A LOGO ---
st.title("Umělecké kovářství")
if os.path.exists("logo.png"):
    st.image("logo.png", use_container_width=True)

# --- NAVIGACE ---
seznam_stranek = ["Informace", "Fotogalerie", "Ceník a Kalkulačka", "Termíny"]
if st.session_state.prihlasen:
    seznam_stranek.extend(["Administrace", "Návštěvnost"])
aktualni_stranka = st.radio("Navigace", seznam_stranek, horizontal=True, label_visibility="collapsed")

st.markdown("---")

# --- OBSAH STRÁNEK (zkráceno pro přehlednost, vlož sem svůj původní obsah) ---
if aktualni_stranka == "Informace":
    st.header("O naší dílně")
    st.write("Vítejte v našem kovářství...") 
# ... (sem patří zbytek tvých if/elif podmínek pro stránky) ...

# --- PATIČKA S PŘIHLÁŠENÍM ---
st.markdown("---")
col_prazdny, col_login = st.columns([4, 1])
with col_login:
    if not st.session_state.prihlasen:
        with st.expander("👤 Přihlášení správce"):
            jmeno = st.text_input("Jméno", key="in_jmeno")
            heslo = st.text_input("Heslo", type="password", key="in_heslo")
            if st.button("Přihlásit"):
                if jmeno == "1" and heslo == "1":
                    st.session_state.prihlasen = True
                    st.rerun()
                else:
                    st.error("Chyba")
    else:
        st.write("Přihlášen: kpala")
        if st.button("Odhlásit"):
            st.session_state.prihlasen = False
            st.rerun()
