import streamlit as st
import json
import os
from datetime import date, datetime
import uuid
import base64

# Nastavení stránky
st.set_page_config(page_title="Umělecké kovářství", layout="wide")

# Funkce pro načítání
def nacti_json(soubor, default):
    return json.load(open(soubor, "r", encoding="utf-8")) if os.path.exists(soubor) else default

def uloz_json(soubor, data):
    with open(soubor, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "prihlasen" not in st.session_state: st.session_state.prihlasen = False
if "terminy" not in st.session_state: st.session_state.terminy = nacti_json("terminy.json", [])

# Stylizace
st.markdown("""
<style>
.stApp { background-color: #2e3033; color: white; }
h1, h2 { color: #ff6600 !important; }
.main .block-container { background-color: rgba(0,0,0,0.7); padding: 2rem; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# HLAVIČKA
st.title("Umělecké kovářství")
if os.path.exists("logo.png"):
    st.image("logo.png", use_container_width=True)

# NAVIGACE
menu = ["Informace", "Fotogalerie", "Ceník", "Termíny"]
if st.session_state.prihlasen: menu.extend(["Administrace"])
stranka = st.radio("Menu", menu, horizontal=True)

# OBSAH
if stranka == "Informace":
    st.write("Vítejte v naší dílně.")
elif stranka == "Fotogalerie":
    st.write("Zde budou fotky.")
elif stranka == "Ceník":
    st.write("Ceník služeb.")
elif stranka == "Termíny":
    st.write("Objednávkový formulář.")

# PATIČKA S PŘIHLÁŠENÍM
st.markdown("---")
col1, col2 = st.columns([4, 1])
with col2:
    if not st.session_state.prihlasen:
        with st.expander("👤 Přihlášení"):
            j = st.text_input("Jméno")
            h = st.text_input("Heslo", type="password")
            if st.button("Přihlásit"):
                if j == "1" and h == "1":
                    st.session_state.prihlasen = True
                    st.rerun()
    else:
        st.write("Přihlášen: kpala")
        if st.button("Odhlásit"):
            st.session_state.prihlasen = False
            st.rerun()
