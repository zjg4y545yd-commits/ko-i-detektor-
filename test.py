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

# Vložení vlastního CSS pro kovářský vzhled (tapeta a tmavý design)
st.markdown("""
<style>
/* Nastavení tapety na pozadí celého webu */
.stApp {data:"image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAUVBMVEV3d3f///9wcHCJiYnGxsZ0dHT19fWZmZltbW1ra2vPz8+2trabm5v5+fl7e3uAgIDs7OyioqKurq7f39/W1ta6urqoqKiQkJDj4+PBwcHc3NwKRuvRAAAC3UlEQVR4nO3Yy3baMBgAYSSQESY2lwAlvP+D1jaXGoa03cGJZpas5O9I+m0mwR6bPPtxXS83v6Y/vY/t7Nj8n8nnts0xphKKOc3rf5vUq5wmBZViWj5ulnuTXVuWyFDM++9NmnmBIn2x/fzG5JjKFOlK+eupSb149cpeWT48MZkVTdKhfMCk7F3SFzcPJsfiSbqdsr8zadpir9dRi+PYZBNfvZ53KLUjk5MnZygu/5isPDnncnU12eVXr+VdSturydRtci03Z5O12+RWnJ1Nlg6dW2l6NvHojIpVb1J5dEblXW/i1BnXv6JMwpfXyag0700OXiej0qo3mWsyrtUEpUaTx7phrMlDmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhg8mHJuM0YanpTA6a3BU6k3189SreqbTqTWpNRqV5b7LOr17HOxX3vUloX72OdyqfBhMHz6jYDCa1h+dWf530JsF9civvLiZbUW6Fi0m1ePVK3qX4dTUJB19RhlIbbiaNh2douE0uJmHm6Jlchs7NxD9R+rpP4rFJWImSj+HepEqloyx24cEkrNuyUXIdYBKqVcETOS1O4YlJ9zFY7PSJq3V4bhLqVORWSXk7Vrg3Cc1yUZxKWnysw19MOpV9mwsaQSnH7YMITbpO22nMsYByXm1qPv8zk67qWM9+fPWpevrw35iU3W+G/SY3Y3HcVQAAAABJRU5ErkJggg==");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}

/* Ztmavení pozadí za textem pro lepší čitelnost */
.main .block-container {
    background-color: rgba(15, 15, 15, 0.85);
    padding: 3rem;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    color: #e0e0e0;
    margin-top: 2rem;
}

/* Zlatavá barva pro nadpisy evokující žhavý kov */
h1, h2, h3 {
    color: #5c0b0b !important;
    font-family: 'Georgia', serif;
}

/* Úprava textů a popisků */
p, label, .stMarkdown {
    color: #f0f0f0 !important;
    font-size: 1.1rem;
}

/* Stylování tlačítek */
.stButton>button {
    background-color: #3a1c00;
    color: #d4af37;
    border: 1px solid #d4af37;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #d4af37;
    color: #111;
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
    st.header("Orientační kalkulačka zakázky")
    st.write("Vyberte typ výrobku a zadejte požadovanou délku pro získání orientační ceny. Výpočet zohledňuje aktuální tržní cenu železa a náročnost ruční práce.")
    
    aktualni_cena_zeleza_za_kg = 28.50  # Hodnota v CZK
    
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
        st.caption("Uvedená cena je pouze orientační. Přesná kalkulace bude stanovena po osobním zaměření.")

# ZÁLOŽKA 4: TERMÍNY (Pro zákazníky)
with tab4:
    st.header("Sjednejte si s námi termín")
    st.write("Vyberte si datum v kalendáři a zanechte nám na sebe kontakt. Ozveme se vám zpět pro potvrzení a domluvení detailů.")
    
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

# ZÁLOŽKA 5: TERMÍNY EDITACE (Pro majitele/správce)
with tab5:
    st.header("Administrace požadavků")
    st.write("Zde vidíte všechny nové poptávky od zákazníků. Pro zobrazení zadejte administrátorské heslo.")
    
    heslo = st.text_input("Zadejte heslo:", type="password")
    
    # Heslo je nastaveno na 1234
    if heslo == "1234":
        st.success("Přístup povolen.")
        
        # Filtrujeme jen ty termíny, které ještě nejsou vyřešené
        nevyresene_terminy = [t for t in st.session_state.terminy if not t.get("vyreseno", False)]
        
        if not nevyresene_terminy:
            st.info("Aktuálně nemáte žádné nové požadavky od zákazníků.")
        else:
            for i, term in enumerate(nevyresene_terminy):
                with st.expander(f"Požadavek na datum: {term['datum']} - Zákazník: {term['jmeno']}"):
                    st.write(f"**Preferovaný kontakt:** {term['typ_kontaktu']}")
                    st.write(f"**Kontakt:** {term['kontakt']}")
                    st.write(f"**Poznámka od zákazníka:** {term['poznamka']}")
                    
                    # Tlačítko pro vyřízení a skrytí požadavku
                    if st.button("Označit jako vyřízené", key=f"btn_vyridit_{i}"):
                        # Najdeme tento konkrétní záznam v hlavní databázi a změníme ho
                        for index_v_hlavni, t in enumerate(st.session_state.terminy):
                            if t == term:
                                st.session_state.terminy[index_v_hlavni]["vyreseno"] = True
                                break
                        uloz_terminy(st.session_state.terminy)
                        st.rerun()
    elif heslo != "":
        st.error("Nesprávné heslo.")
