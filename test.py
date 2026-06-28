import streamlit as st
import json
import os
from datetime import date

# Nastavení stránky
st.set_page_config(page_title="Umělecké kovářství", layout="wide")

# --- FUNKCE ---
SOUBOR_TERMINY = "terminy.json"

def nacti_terminy():
    if os.path.exists(SOUBOR_TERMINY):
        with open(SOUBOR_TERMINY, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def uloz_terminy(data):
    with open(SOUBOR_TERMINY, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "terminy" not in st.session_state:
    st.session_state.terminy = nacti_terminy()
if "prihlasen" not in st.session_state:
    st.session_state.prihlasen = False

# --- CSS STYLING ---
st.markdown("""
<style>
.stApp { background-color: #2e3033 !important; }
.main .block-container { background-color: #1a1b1c !important; padding: 3rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.6); color: #f5f5f5 !important; margin-top: 1rem; }
h1, h2, h3 { color: #ff6600 !important; font-family: 'Georgia', serif; }
p, label, .stMarkdown, [data-testid="stMarkdownContainer"] { color: #ffffff !important; font-size: 1.1rem; }
.stButton>button { background-color: #3a1c00 !important; color: #d4af37 !important; border: 1px solid #d4af37 !important; transition: 0.3s; }
.stButton>button:hover { background-color: #d4af37 !important; color: #111111 !important; }
.stTabs [data-baseweb="tab"] { color: #b0b5bc !important; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { color: #ff6600 !important; border-bottom-color: #ff6600 !important; }
[data-testid="stExpander"] details, [data-testid="stExpander"] { background-color: #26282b !important; border: 1px solid #444 !important; border-radius: 8px; }
[data-testid="stExpander"] summary { background-color: #33363a !important; color: #ff6600 !important; }
</style>
""", unsafe_allow_html=True)

# --- HLAVIČKA ---
col_nadpis, col_login = st.columns([3, 1])
with col_nadpis:
    st.title("Umělecké kovářství")
with col_login:
    if not st.session_state.prihlasen:
        with st.expander("👤 Přihlášení"):
            if st.text_input("Jméno", key="in_jmeno") == "kpala" and st.text_input("Heslo", type="password", key="in_heslo") == "123":
                if st.button("Přihlásit"):
                    st.session_state.prihlasen = True
                    st.rerun()
    else:
        st.markdown("### 👤 Přihlášen: kpala")
        if st.button("Odhlásit se"):
            st.session_state.prihlasen = False
            st.rerun()

st.markdown("---")

# --- NAVIGACE ---
seznam_zalozek = ["Informace", "Fotogalerie", "Ceník a Kalkulačka", "Termíny"]
if st.session_state.prihlasen:
    seznam_zalozek.append("Administrace")

tabs = st.tabs(seznam_zalozek)

# ZÁLOŽKA 1: INFORMACE
with tabs[0]:
    st.header("O naší dílně")
    st.write("Specializujeme se na ruční umělecké kovářství, brány a ploty.")

# ZÁLOŽKA 2: FOTOGALERIE
with tabs[1]:
    st.header("Ukázky naší práce")
    if os.path.exists("fotogalerie"):
        fotky = [f for f in os.listdir("fotogalerie") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not fotky: st.write("Zatím zde nejsou žádné fotky.")
        else:
            cols = st.columns(3)
            for i, fotka in enumerate(fotky):
                cols[i % 3].image(os.path.join("fotogalerie", fotka), use_container_width=True)
    else: st.write("Složka fotogalerie zatím neexistuje.")

# ZÁLOŽKA 3: KALKULAČKA
with tabs[2]:
    st.header("Orientační kalkulačka")
    produkt = st.selectbox("Typ výrobku:", ["Kovaná brána", "Kovaný plot", "Kované dveře"])
    delka = st.number_input("Délka (m):", min_value=0.5, value=2.0)
    if st.button("Vypočítat"):
        st.metric("Odhadovaná cena", f"{int(delka * 5000):,} CZK".replace(",", " "))

# ZÁLOŽKA 4: TERMÍNY
with tabs[3]:
    st.header("Sjednejte si termín")
    datum = st.date_input("Datum:", min_value=date.today())
    jmeno = st.text_input("Jméno:")
    kontakt = st.text_input("Kontakt:")
    if st.button("Odeslat požadavek"):
        st.session_state.terminy.append({"datum": str(datum), "jmeno": jmeno, "kontakt": kontakt, "vyreseno": False})
        uloz_terminy(st.session_state.terminy)
        st.success("Odesláno!")

# ZÁLOŽKA 5: ADMINISTRACE
if st.session_state.prihlasen:
    with tabs[4]:
        st.header("Administrace")
        st.subheader("📸 Nahrát fotku")
        if not os.path.exists("fotogalerie"): os.makedirs("fotogalerie")
        uploaded_file = st.file_uploader("Vyberte obrázek", type=["jpg", "png"])
        if uploaded_file and st.button("Uložit fotku"):
            with open(os.path.join("fotogalerie", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.rerun()
            
        st.subheader("📅 Požadavky")
        nevyresene = [t for t in st.session_state.terminy if not t.get("vyreseno", False)]
        for i, term in enumerate(nevyresene):
            with st.expander(f"Zákazník: {term['jmeno']} ({term['datum']})"):
                st.write(f"Kontakt: {term['kontakt']}")
                if st.button("Vyřízeno", key=f"btn_{i}"):
                    term["vyreseno"] = True
                    uloz_terminy(st.session_state.terminy)
                    st.rerun()
