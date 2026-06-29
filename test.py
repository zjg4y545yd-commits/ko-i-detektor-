import streamlit as st
import json
import os
from datetime import date, datetime
import uuid
import base64

# --- NASTAVENÍ STRÁNKY ---
st.set_page_config(page_title="Umělecké kovářství Štěpán Palla", layout="wide", initial_sidebar_state="collapsed")

# --- KONFIGURACE DAT ---
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

# --- SESSION STATE ---
if "terminy" not in st.session_state: st.session_state.terminy = nacti_json(SOUBOR_TERMINY, [])
if "prihlasen" not in st.session_state: st.session_state.prihlasen = False

# --- SLEDOVÁNÍ NÁVŠTĚVNOSTI ---
if "navsteva_zaznamenana" not in st.session_state:
    st.session_state.navsteva_zaznamenana = True
    data_navstev = nacti_json(SOUBOR_NAVSTEVNOST, {})
    dnes = str(date.today())
    if dnes not in data_navstev: data_navstev[dnes] = []
    data_navstev[dnes].append({"cas": datetime.now().strftime("%H:%M:%S")})
    uloz_json(SOUBOR_NAVSTEVNOST, data_navstev)

# --- CSS STYLING (MODERNÍ DESIGN) ---
st.markdown("""
<style>
    /* Základní barvy */
    .stApp { background-color: #121212 !important; }
    
    /* Hlavní kontejner */
    .main .block-container { 
        padding: 3rem 4rem; 
        background-color: #181818 !important; 
        border-radius: 16px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); 
        border: 1px solid #333;
    }
    
    /* Typografie */
    h1, h2, h3 { color: #d4af37 !important; font-family: 'Georgia', serif; }
    h1 { border-bottom: 2px solid #d4af37; padding-bottom: 10px; }
    p, li { font-size: 1.1rem; line-height: 1.6; color: #cccccc !important; }
    
    /* Navigační menu */
    div[role="radiogroup"] { 
        display: flex; justify-content: center; gap: 20px; 
        background: #1e1e1e; padding: 15px; border-radius: 12px; border: 1px solid #444; 
        margin-bottom: 30px;
    }
    div[role="radiogroup"] label { color: #ffffff !important; cursor: pointer; }
    
    /* Tlačítka */
    .stButton>button { 
        background: linear-gradient(135deg, #b87333 0%, #d4af37 100%) !important; 
        color: #000 !important; font-weight: bold !important; border: none !important; 
        border-radius: 6px; padding: 0.5rem 2rem !important; transition: 0.3s !important;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3); }
    
    /* Expandery */
    [data-testid="stExpander"] { background-color: #1e1e1e !important; border: 1px solid #444 !important; }
</style>
""", unsafe_allow_html=True)

# --- NAVIGACE A HLAVIČKA ---
seznam_stranek = ["Domů (Informace)", "Ukázky práce", "Kalkulačka zakázky", "Sjednat termín"]
if st.session_state.prihlasen: seznam_stranek.extend(["Administrace", "Návštěvnost"])
aktualni_stranka = st.radio("Navigace", seznam_stranek, horizontal=True, label_visibility="collapsed")

col_logo, col_login = st.columns([4, 1])
with col_logo:
    if os.path.exists("pozadi2.png"): st.image("pozadi2.png", width=400)
    else: st.title("Umělecké kovářství Štěpán Palla")
with col_login:
    if not st.session_state.prihlasen:
        if st.expander("⚙️"):
            if st.button("Administrace"): st.session_state.prihlasen = True
    else:
        if st.button("Odhlásit"): st.session_state.prihlasen = False

# --- STRÁNKY ---
if aktualni_stranka == "Domů (Informace)":
    st.markdown("## Poctivé kovářské řemeslo")
    if os.path.exists("pozadi.png"): st.image("pozadi.png", use_container_width=True)
    st.write("Vítejte v naší dílně. Specializujeme se na ruční umělecké zpracování kovů. Naším hlavním zaměřením je **zakázková výroba kovaných plotů, vjezdových bran a mříží**.")
    st.info("🔨 **Vše vyrábíme ručně a s důrazem na tradici, odolnost a moderní design.**")

elif aktualni_stranka == "Ukázky práce":
    st.markdown("## Naše realizace")
    if os.path.exists("fotogalerie"):
        fotky = [f for f in os.listdir("fotogalerie") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        cols = st.columns(3)
        for i, fotka in enumerate(fotky):
            with cols[i % 3]: st.image(os.path.join("fotogalerie", fotka), use_container_width=True)
    else: st.info("Galerie se připravuje.")

elif aktualni_stranka == "Kalkulačka zakázky":
    st.markdown("## Předběžná kalkulace")
    koef = {"Kovaná brána": {"kg": 55, "prace": 6500}, "Kovaný plot": {"kg": 35, "prace": 4200}}
    produkt = st.selectbox("Typ konstrukce:", list(koef.keys()))
    delka = st.number_input("Celková délka (m):", value=3.0)
    if st.button("Vypočítat cenu"):
        cena = (koef[produkt]["kg"] * delka * 28.5) + (koef[produkt]["prace"] * delka)
        st.markdown(f"### Odhadovaná cena: {cena:,.0f} Kč")

elif aktualni_stranka == "Sjednat termín":
    st.markdown("## Napište nám o svém projektu")
    jmeno = st.text_input("Jméno a příjmení")
    kontakt = st.text_input("Telefon nebo e-mail")
    poznamka = st.text_area("Popis poptávky")
    if st.button("Odeslat poptávku"):
        st.session_state.terminy.append({"jmeno": jmeno, "kontakt": kontakt, "poznamka": poznamka, "vyreseno": False})
        uloz_json(SOUBOR_TERMINY, st.session_state.terminy)
        st.success("Vaše poptávka byla odeslána!")

elif aktualni_stranka == "Administrace" and st.session_state.prihlasen:
    st.markdown("## Správa poptávek")
    for i, t in enumerate(st.session_state.terminy):
        if not t.get("vyreseno"):
            with st.expander(f"Poptávka: {t['jmeno']}"):
                st.write(f"Kontakt: {t['kontakt']} | Poznámka: {t['poznamka']}")
                if st.button("Vyřízeno", key=f"v_{i}"):
                    st.session_state.terminy[i]["vyreseno"] = True
                    uloz_json(SOUBOR_TERMINY, st.session_state.terminy)
                    st.rerun()
