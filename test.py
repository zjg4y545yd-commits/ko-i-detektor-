import streamlit as st
import json
import os
from datetime import date, datetime
import uuid

# Nastavení stránky
st.set_page_config(page_title="Umělecké kovářství", layout="wide")

# --- FUNKCE PRO DATA ---
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

# Inicializace session state
if "terminy" not in st.session_state:
    st.session_state.terminy = nacti_json(SOUBOR_TERMINY, [])
if "prihlasen" not in st.session_state:
    st.session_state.prihlasen = False

# --- SYSTÉM SLEDOVÁNÍ NÁVŠTĚVNOSTI ---
if "navsteva_zaznamenana" not in st.session_state:
    st.session_state.navsteva_zaznamenana = True
    # Vytvoření unikátního ID pro tohoto návštěvníka (prvních 8 znaků)
    st.session_state.visitor_id = str(uuid.uuid4())[:8] 
    
    data_navstev = nacti_json(SOUBOR_NAVSTEVNOST, {})
    dnes = str(date.today())
    cas = datetime.now().strftime("%H:%M:%S")
    
    if dnes not in data_navstev:
        data_navstev[dnes] = []
        
    data_navstev[dnes].append({"cas": cas, "id": st.session_state.visitor_id})
    uloz_json(SOUBOR_NAVSTEVNOST, data_navstev)

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

# --- HLAVIČKA A PŘIHLAŠOVÁNÍ ---
col_nadpis, col_login = st.columns([3, 1])
with col_nadpis:
    st.title("Umělecké kovářství")
with col_login:
    if not st.session_state.prihlasen:
        with st.expander("👤 Přihlášení pro správce"):
            jmeno_prihlaseni = st.text_input("Jméno", key="in_jmeno")
            heslo_prihlaseni = st.text_input("Heslo", type="password", key="in_heslo")
            if st.button("Přihlásit"):
                if jmeno_prihlaseni == "kpala" and heslo_prihlaseni == "123":
                    st.session_state.prihlasen = True
                    st.rerun()
                else:
                    st.error("Špatné jméno nebo heslo!")
    else:
        st.markdown("### 👤 Přihlášen: kpala")
        if st.button("Odhlásit se"):
            st.session_state.prihlasen = False
            st.rerun()

st.markdown("---")

# --- NAVIGACE ---
seznam_zalozek = ["Informace", "Fotogalerie", "Ceník a Kalkulačka", "Termíny"]
if st.session_state.prihlasen:
    seznam_zalozek.extend(["Administrace", "Návštěvnost"])

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
    
    if st.session_state.prihlasen:
        st.subheader("📸 Správa fotografií (Administrátor)")
        if not os.path.exists("fotogalerie"): 
            os.makedirs("fotogalerie")
            
        uploaded_file = st.file_uploader("Vyberte obrázek (JPG, PNG) pro přidání do galerie", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            if st.button("Uložit fotku do galerie"):
                with open(os.path.join("fotogalerie", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Fotka {uploaded_file.name} byla úspěšně uložena!")
                st.rerun()
        st.markdown("---")

    if os.path.exists("fotogalerie"):
        fotky = [f for f in os.listdir("fotogalerie") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not fotky: 
            st.write("Zatím zde nejsou žádné nahrané fotografie.")
        else:
            cols = st.columns(2)
            for i, fotka in enumerate(fotky):
                with cols[i % 2]:
                    st.image(os.path.join("fotogalerie", fotka), caption=fotka, use_container_width=True)
                    if st.session_state.prihlasen:
                        if st.button(f"🗑️ Smazat fotku", key=f"smazat_{i}_{fotka}"):
                            try:
                                os.remove(os.path.join("fotogalerie", fotka))
                                st.rerun()
                            except Exception as e:
                                st.error(f"Nepodařilo se smazat soubor: {e}")
    else: 
        st.write("Složka pro fotky zatím nebyla vytvořena.")

# ZÁLOŽKA 3: KALKULAČKA
with tabs[2]:
    st.header("Orientační kalkulačka zakázky")
    st.write("Vyberte typ výrobku a zadejte požadovanou délku pro získání orientační ceny. Výpočet zohledňuje aktuální tržní cenu železa a náročnost ruční práce.")
    
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

# ZÁLOŽKA 4: TERMÍNY
with tabs[3]:
    st.header("Sjednejte si s námi termín")
    vybrane_datum = st.date_input("Zvolte preferované datum:", min_value=date.today())
    jmeno = st.text_input("Vaše jméno a příjmení:")
    kontakt_volba = st.radio("Jak si přejete být kontaktováni?", ["Telefonicky", "E-mailem"])
    
    if kontakt_volba == "Telefonicky":
        kontakt_udaj = st.text_input("Váš telefon a předvolba:")
    else:
        kontakt_udaj = st.text_input("Vaše e-mailová adresa:")
        
    poznamka = st.text_area("O co máte zájem? (Volitelná poznámka)")
    
    if st.button("Odeslat požadavek na termín"):
        if not jmeno or not kontakt_udaj:
            st.error("Pro odeslání prosím vyplňte své jméno a kontaktní údaj.")
        else:
            st.session_state.terminy.append({
                "datum": str(vybrane_datum), "jmeno": jmeno, "typ_kontaktu": kontakt_volba,
                "kontakt": kontakt_udaj, "poznamka": poznamka, "vyreseno": False
            })
            uloz_json(SOUBOR_TERMINY, st.session_state.terminy)
            st.success("Děkujeme! Váš požadavek byl odeslán.")

# ZÁLOŽKA 5: ADMINISTRACE
if st.session_state.prihlasen:
    with tabs[4]:
        st.header("Administrace webu")
        st.subheader("📅 Požadavky od zákazníků")
        nevyresene = [t for t in st.session_state.terminy if not t.get("vyreseno", False)]
        
        if not nevyresene:
            st.info("Aktuálně nemáte žádné nové požadavky.")
        else:
            for i, term in enumerate(nevyresene):
                with st.expander(f"Zákazník: {term['jmeno']} ({term['datum']})"):
                    st.write(f"**Kontakt:** {term['kontakt']} ({term.get('typ_kontaktu', 'Nezadáno')})")
                    st.write(f"**Poznámka:** {term.get('poznamka', '')}")
                    if st.button("Označit jako vyřízené", key=f"btn_{i}"):
                        for idx, t in enumerate(st.session_state.terminy):
                            if t == term:
                                st.session_state.terminy[idx]["vyreseno"] = True
                                break
                        uloz_json(SOUBOR_TERMINY, st.session_state.terminy)
                        st.rerun()

# ZÁLOŽKA 6: NÁVŠTĚVNOST
if st.session_state.prihlasen:
    with tabs[5]:
        st.header("📊 Statistiky návštěvnosti")
        
        data_navstev = nacti_json(SOUBOR_NAVSTEVNOST, {})
        
        if not data_navstev:
            st.info("Zatím nebyla zaznamenána žádná návštěvnost.")
        else:
            # Příprava dat pro graf
            graf_data = {den: len(navstevnici) for den, navstevnici in data_navstev.items()}
            
            st.subheader("Návštěvy po dnech")
            st.bar_chart(graf_data)
            
            st.markdown("---")
            
            # Zobrazení detailů pro dnešek
            dnesni_datum = str(date.today())
            st.subheader(f"Dnešní provoz ({dnesni_datum})")
            
            if dnesni_datum in data_navstev:
                dnesni_navstevy = data_navstev[dnesni_datum]
                st.write(f"**Celkem návštěv dnes:** {len(dnesni_navstevy)}")
                
                # Vypsání historie od nejnovějšího
                for zaznam in reversed(dnesni_navstevy):
                    st.write(f"🕒 **{zaznam['cas']}** | 🆔 Návštěvník (ID sezení): `{zaznam['id']}`")
            else:
                st.write("Dnes zatím žádné návštěvy.")
