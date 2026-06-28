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

# Nastavení stavu přihlášení
if "prihlasen" not in st.session_state:
    st.session_state.prihlasen = False

# Vložení vlastního CSS pro kovářský vzhled a opravu expanderů
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
    margin-top: 1rem;
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

/* OPRAVA EXPANDERŮ (Požadavky v administraci) - Vynucení tmavého pozadí */
[data-testid="stExpander"] details, [data-testid="stExpander"] {
    background-color: #26282b !important;
    border: 1px solid #444 !important;
    border-radius: 8px;
}
[data-testid="stExpander"] summary {
    background-color: #33363a !important;
    color: #ff6600 !important;
}
[data-testid="stExpander"] summary:hover {
    background-color: #42464c !important;
    color: #ff6600 !important;
}
[data-testid="stExpanderDetails"] {
    background-color: #1a1b1c !important;
}
</style>
""", unsafe_allow_html=True)

# --- HLAVIČKA A PŘIHLAŠOVÁNÍ ---
# Rozdělení horní části na nadpis (vlevo) a přihlášení (vpravo)
col_nadpis, col_login = st.columns([3, 1])

with col_nadpis:
    st.title("Umělecké kovářství")

with col_login:
    # Pokud není uživatel přihlášený, zobrazíme mu formulář
    if not st.session_state.prihlasen:
        with st.expander("👤 Přihlášení pro správce"):
            jmeno_prihlaseni = st.text_input("Jméno", key="in_jmeno")
            heslo_prihlaseni = st.text_input("Heslo", type="password", key="in_heslo")
            if st.button("Přihlásit"):
                if jmeno_prihlaseni == "kpala" and heslo_prihlaseni == "123":
                    st.session_state.prihlasen = True
                    st.rerun()  # Okamžitě obnoví stránku a ukáže skrytou záložku
                else:
                    st.error("Špatné jméno nebo heslo!")
    # Pokud přihlášený je, ukážeme ikonku a tlačítko pro odhlášení
    else:
        st.markdown("### 👤 Vítej, kpala")
        if st.button("Odhlásit se"):
            st.session_state.prihlasen = False
            st.rerun()

st.markdown("---")

# --- VYTVOŘENÍ ZÁLOŽEK ---
# Logika: Administrace se přidá do seznamu jen pokud je uživatel přihlášen
seznam_zalozek = ["Informace", "Fotogalerie", "Ceník a Kalkulačka", "Termíny"]
if st.session_state.prihlasen:
    seznam_zalozek.append("Administrace")

tabs = st.tabs(seznam_zalozek)

# ZÁLOŽKA 1: INFORMACE
with tabs[0]:
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
with tabs[1]:
    st.header("Ukázky naší práce")
    st.write("Prohlédněte si naše nedávné realizace.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1622359487565-d60321262d08?q=80&w=800&auto=format&fit=crop", caption="Detail kované brány")
    with col2:
        st.image("https://images.unsplash.com/photo-1533038590840-1cbea9766434?q=80&w=800&auto=format&fit=crop", caption="Kovářská práce v dílně")
        
    st.info("Administrátorská poznámka: Pro nahrávání nových fotografií přímo z aplikace lze do budoucna přidat modul.")

# ZÁLOŽKA 3: KALKULAČKA A CENÍK
with tabs[2]:
    st.header("Orientační kalkulačka zakázky")
    st.write("Vyberte typ výrobku a zadejte požadovanou délku pro získání orientační ceny.")
    
    aktualni_cena_zeleza_za_kg = 28.50 
    
    koeficienty = {
        "Kovaná brána": {"kg_na_metr": 55, "prace_na_metr": 6500},
        "Kovaný plot": {"kg_na_metr": 35, "prace_na_metr": 4200},
        "Kované dveře": {"kg_na_metr": 45, "prace_na_metr": 7000}
    }
    
    vybrany_produkt = st.selectbox("Vyberte typ výrobku:", list(koeficienty.keys()))
    delka_v_metrech = st.number_input("Zadejte celkovou délku (v metrech):", min_value=0.5, value=2.0, step=0.5)
    
    if st.button("Vypočítat orientační cenu"):
        data_produktu = koeficienty[vybrany_produkt]
        spotreba_zeleza_kg = data_produktu["kg_na_metr"] * delka_v_metrech
        cena_za_material = spotreba_zeleza_kg * aktualni_cena_zeleza_za_kg
        cena_za_praci = data_produktu["prace_na_metr"] * delka_v_metrech
        celkova_cena = cena_za_material + cena_za_praci
        
        st.markdown("### Výsledek výpočtu")
        st.write(f"Zadaný rozměr: **{delka_v_metrech} m**")
        st.write(f"Typ konstrukce: **{vybrany_produkt}**")
        st.metric(label="Odhadovaná celková cena", value=f"{celkova_cena:,.0f} CZK".replace(",", " "))

# ZÁLOŽKA 4: TERMÍNY (Pro zákazníky)
with tabs[3]:
    st.header("Sjednejte si s námi termín")
    st.write("Vyberte si datum v kalendáři a zanechte nám na sebe kontakt.")
    
    vybrane_datum = st.date_input("Zvolte preferované datum:", min_value=date.today())
    jmeno = st.text_input("Vaše jméno a příjmení:")
    kontakt_volba = st.radio("Jak si přejete být kontaktováni?", ["Telefonicky", "E-mailem"])
    
    if kontakt_volba == "Telefonicky":
        kontakt_udaj = st.text_input("Váš telefonní kód a číslo:")
    else:
        kontakt_udaj = st.text_input("Vaše e-mailová adresa:")
        
    poznamka = st.text_area("O co máte zájem? (Volitelná poznámka)")
    
    if st.button("Odeslat požadavek na termín"):
        if not jmeno or not kontakt_udaj:
            st.error("Pro odeslání prosím vyplňte své jméno a kontaktní údaj.")
        else:
            novy_pozadavek = {
                "datum": str(vybrane_datum),
                "jmeno": jmeno,
                "typ_kontaktu": kontakt_volba,
                "kontakt": kontakt_udaj,
                "poznamka": poznamka,
                "vyreseno": False
            }
            st.session_state.terminy.append(novy_pozadavek)
            uloz_terminy(st.session_state.terminy)
            st.success("Děkujeme! Váš požadavek byl úspěšně odeslán. Brzy se vám ozveme.")

# ZÁLOŽKA 5: ADMINISTRACE (Jen pro přihlášené)
if st.session_state.prihlasen:
    with tabs[4]:
        st.header("Administrace požadavků")
        
        nevyresene_terminy = [t for t in st.session_state.terminy if not t.get("vyreseno", False)]
        
        if not nevyresene_terminy:
            st.info("Aktuálně nemáte žádné nové požadavky od zákazníků.")
        else:
            for i, term in enumerate(nevyresene_terminy):
                with st.expander(f"📅 Požadavek na datum: {term['datum']} - Zákazník: {term['jmeno']}"):
                    st.write(f"**Preferovaný kontakt:** {term['typ_kontaktu']}")
                    st.write(f"**Kontakt:** {term['kontakt']}")
                    st.write(f"**Poznámka od zákazníka:** {term['poznam
