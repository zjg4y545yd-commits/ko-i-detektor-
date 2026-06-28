import streamlit as st
import json
import os
from datetime import date

# Nastavení stránky musí být první příkaz
st.set_page_config(page_title="Umělecké kovářství", layout="wide")

# --- FUNKCE PRO UKLÁDÁNÍ TERMÍNŮ ---
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

# Vložení vlastního CSS pro kovářský vzhled (šedé pozadí a temný design)
st.markdown("""
<style>
/* Nastavení celkového šedého pozadí webu (břidlicová / ocelová šedá) */
.stApp {
    background-color: #2e3033 !important;
}

/* Hlavní kontejner s obsahem - tmavší šedá pro maximální kontrast textu */
.main .block-container {
    background-color: #1a1b1c !important;
    padding: 3rem;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.6);
    color: #f5f5f5 !important;
    margin-top: 2rem;
}

/* Barva pro nadpisy - evokuje rozžhavený kov a zajišťuje skvělou čitelnost */
h1, h2, h3 {
    color: #ff6600 !important;
    font-family: 'Georgia', serif;
}

/* Úprava běžných textů, popisků a markdownu na čistě bílou/světle šedou */
p, label, .stMarkdown, [data-testid="stMarkdownContainer"] {
    color: #ffffff !important;
    font-size: 1.1rem;
}

/* Stylování tlačítek s kovovým detailem */
.stButton>button {
    background-color: #3a1c00 !important;
    color: #d4af37 !important;
    border: 1px solid #d4af37 !important;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #d4af37 !important;
    color: #111111 !important;
}

/* Zajištění, aby byly čitelné i záložky (Tabs) */
.stTabs [data-baseweb="tab"] {
    color: #b0b5bc !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #ff6600 !important;
    border-bottom-color: #ff6600 !important;
}
</style>
""", unsafe_allow_html=True)

# Hlavní hlavička
st.title("Umělecké kovářství")
st.markdown("---")

# Vytvoření záložek pro navigaci
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Informace", "Fotogalerie", "Ceník a Kalkulačka", "Termíny", "Termíny editace"])

# ZÁLOŽKA 1: INFORMACE
with tab1:
    st.header("O naší dílně")
    st.write("""
    Vítejte na stránkách našeho uměleckého kovářství. Specializujeme se na ruční výrobu a umělecké zpracování kovů s hlavním zaměřením na zakázkovou výrobu kovaných plotů a vjezdových bran.
    
    Každý kus, který opustí naši dílnu, je výsledkem poctivé řemeslné práce, kde se tradiční kovářské postupy setkávají s přesností a důrazem na detail. Ať už hledáte robustní ochranu vašeho pozemku nebo elegantní vstupní prvek, navrhneme a vyrobíme řešení přesně na míru vašim představám a architektonickému stylu vašeho domu.
    
    Naše práce se vyznačuje vysokou odolností, kvalitní povrchovou úpravou a nadčasovým designem, který vydrží generace.
    """)
    
    st.subheader("Naše hlavní služby")
    st.markdown("""
    * Kované brány (křídlové i posuvné)
    * Kované ploty a výplně
    * Vstupní dveře s kovanými prvky
    * Restaurování historických kovářských děl
    """)

# ZÁLOŽKA 2: FOTOGALERIE
with tab2:
    st.header("Ukázky naší práce")
    st.write("Prohlédněte si naše nedávné realizace.")
    
    # Rozvržení do sloupců pro lepší prezentaci
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1622359487565-d60321262d08?q=80&w=800&auto=format&fit=crop", caption="Detail kované brány")
    with col2:
        st.image("https://images.unsplash.com/photo-1533038590840-1cbea9766434?q=80&w=800&auto=format&fit=crop", caption="Kovářská práce v dílně")
        
    st.info("Administrátorská poznámka: Pro nahrávání nových fotografií přímo z aplikace lze do budoucna přidat modul. Nyní se fotografie nahrávají umístěním do složky programu.")

# ZÁLOŽKA 3: KALKULAČKA A CENÍK
with tab3:
    st.header("Orientační kalk
