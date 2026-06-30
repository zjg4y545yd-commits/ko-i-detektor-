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

# --- CSS STYLING (Vzhled podle předlohy dashboardu) ---
st.markdown("""
<style>
/* Základní barvy a pozadí podle obrázku */
[data-testid="stAppViewContainer"] {
    background-color: #13111c !important; /* Tmavé pozadí hlavní části */
    color: #e2e8f0;
}
[data-testid="stSidebar"] {
    background-color: #1e1b30 !important; /* Tmavě fialové/modré pozadí menu */
    border-right: 1px solid #2d2a45;
}
[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* Skrytí horního panelu u postranního menu pro čistší vzhled */
[data-testid="stSidebarNav"] { display: none; }

/* Stylování textů */
h1, h2, h3, p, span, div {
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

/* Název v levém rohu (nahrazuje logo z obrázku) */
.sidebar-logo-text {
    font-size: 1.2rem;
    font-weight: 700;
    color: #ffffff;
    padding: 10px 0 20px 0;
    border-bottom: 1px solid #2d2a45;
    margin-bottom: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* --- HACK NA MENU (Úprava Radio buttonů na vzhled seznamu) --- */
/* Skrytí klasických kroužků u výběru */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span[data-baseweb="radio"] {
    display: none;
}
/* Obal položky v menu */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    padding: 12px 15px;
    border-radius: 8px;
    margin-bottom: 5px;
    cursor: pointer;
    background-color: transparent;
    transition: background-color 0.2s, color 0.2s;
    display: flex;
    align-items: center;
}
/* Efekt po najetí myší */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background-color: rgba(255, 255, 255, 0.05);
}
/* Text položky menu */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div {
    font-size: 0.95rem;
    font-weight: 500;
    margin-left: 5px;
}

/* Nadpisy sekcí v menu (např. "Programy" z obrázku) */
.menu-section-title {
    font-size: 0.75rem;
    color: #8b8a9d;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 10px;
    padding-left: 5px;
}

/* Hlavní poutač (Hero Banner - nahrazuje ten zelený z obrázku) */
.hero-banner {
    background: linear-gradient(135deg, #2b1f42 0%, #171527 100%);
    border: 1px solid #3d355c;
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.hero-banner h1 {
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 10px;
    color: #ffffff;
    border: none;
}
.hero-banner p {
    font-size: 1.1rem;
    color: #a09eb5;
    max-width: 700px;
    margin: 0 auto;
}

/* Karta / Obsahové bloky */
.content-card {
    background-color: #1a1829;
    border: 1px solid #2d2a45;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}

/* Styl tlačítek (fialové podle obrázku) */
.stButton>button {
    background-color: #6941c6 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton>button:hover {
    background-color: #7f56d9 !important;
}

/* Skrytí výchozího tlačítka popoveru pro přihlášení a jeho úprava */
[data-testid="stPopover"] > button {
    background-color: #c05c5c !important; /* Barva profilového kolečka z předlohy */
    color: white !important;
    border-radius: 50% !important;
    width: 45px !important;
    height: 45px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-weight: bold !important;
    border: none !important;
}
[data-testid="stPopover"] > button > div > div > p {
    color: white !important;
    font-weight: bold;
    margin: 0;
}
[data-testid="stPopover"] > button svg {
    display: none; /* Skryje šipku v tlačítku */
}
</style>
""", unsafe_allow_html=True)

# --- LEVÉ POSTrANNÍ MENU (SIDEBAR) ---
with st.sidebar:
    st.markdown("<div class='sidebar-logo-text'>Umělecké kovářství<br>Štěpán Palla</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='menu-section-title'>Navigace</div>", unsafe_allow_html=True)
    
    # Položky menu s emoji (suplují ikony z obrázku)
    seznam_stranek = ["🏠 Domů (Informace)", "🔨 Ukázky práce", "🧮 Kalkulačka zakázky", "✉️ Sjednat termín"]
    
    if st.session_state.prihlasen:
        st.markdown("<div class='menu-section-title'>Správa webu</div>", unsafe_allow_html=True)
        seznam_stranek.extend(["⚙️ Administrace", "📊 Návštěvnost"])

    vybrana_polozka = st.radio("Menu", seznam_stranek, label_visibility="collapsed")
    
    # Získání čistého názvu stránky bez emoji pro logiku
    aktualni_stranka = vybrana_polozka.split(" ", 1)[1]

# --- HORNÍ LIŠTA A PŘIHLÁŠENÍ (PRAVÝ HORNÍ ROH) ---
# Využijeme sloupce pro natlačení profilového tlačítka doprava
col_spacer1, col_spacer2, col_login = st.columns([8, 1, 1])

with col_login:
    # Používáme st.popover (vyskakovací okno po kliknutí), které stylizujeme jako profilové kolečko
    with st.popover("ŠP"): 
        if not st.session_state.prihlasen:
            st.markdown("**Správa webu**")
            jmeno = st.text_input("Jméno")
            heslo = st.text_input("Heslo", type="password")
            if st.button("Vstoupit", use_container_width=True):
                if jmeno == "1" and heslo == "1":
                    st.session_state.prihlasen = True
                    st.rerun()
                else:
                    st.error("Přístup odepřen.")
        else:
            st.success("Přihlášen: Administrátor")
            if st.button("Odhlásit", use_container_width=True):
                st.session_state.prihlasen = False
                st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# --- HLAVNÍ OBSAHOVÉ STRÁNKY ---

if aktualni_stranka == "Domů (Informace)":
    # Hlavní Banner ve stylu "OK RADAR" z obrázku
    st.markdown("""
    <div class="hero-banner">
        <h1>Poctivé kovářské řemeslo</h1>
        <p>Zakázková výroba kovaných plotů, vjezdových bran a mříží. Každý kus, který opustí naši kovadlinu, je výsledkem tradičních postupů, kde se surová síla ohně potkává s absolutní přesností a citem pro detail.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_text, col_vyhody = st.columns([1, 1])
    
    with col_text:
        st.markdown("""
        <div class="content-card">
            <h3 style='margin-top:0; color:#fff;'>Naše služby</h3>
            <ul style='color:#a09eb5; line-height: 1.8;'>
                <li><b>Kované vjezdové brány</b> (křídlové i posuvné automatické)</li>
                <li><b>Kované ploty a výplně zídek</b></li>
                <li><b>Mříže, zábradlí a ocelové prvky</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_vyhody:
        st.markdown("""
        <div class="content-card">
            <h3 style='margin-top:0; color:#fff;'>Proč si vybrat nás?</h3>
            <p style='color:#a09eb5;'>🛡️ <b>Maximální odolnost:</b> Používáme kvalitní žárové zinkování a barvy proti rzi.</p>
            <p style='color:#a09eb5;'>🔨 <b>100% Ruční práce:</b> Žádné sériové odlitky. Každý spoj tvořen ručně.</p>
            <p style='color:#a09eb5;'>📐 <b>Návrh na míru:</b> Zaměření a konzultace přímo na místě instalace.</p>
        </div>
        """, unsafe_allow_html=True)


elif aktualni_stranka == "Ukázky práce":
    st.markdown("<h2>Ukázky naší práce</h2>", unsafe_allow_html=True)
    
    if st.session_state.prihlasen:
        with st.expander("📸 Přidat nové fotografie"):
            if not os.path.exists("fotogalerie"): 
                os.makedirs("fotogalerie")
            uploaded_file = st.file_uploader("Vyberte obrázek (JPG, PNG)", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                if st.button("Nahrát na web"):
                    with open(os.path.join("fotogalerie", uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.success("Uloženo!")
                    st.rerun()

    if os.path.exists("fotogalerie"):
        fotky = [f for f in os.listdir("fotogalerie") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not fotky: 
            st.info("Galerie se momentálně připravuje. Brzy zde uvidíte naše realizace.")
        else:
            cols = st.columns(3)
            for i, fotka in enumerate(fotky):
                with cols[i % 3]:
                    st.image(os.path.join("fotogalerie", fotka), use_container_width=True)
                    if st.session_state.prihlasen:
                        if st.button("🗑️ Smazat", key=f"del_{i}"):
                            os.remove(os.path.join("fotogalerie", fotka))
                            st.rerun()
    else: 
        st.info("Galerie se momentálně připravuje.")


elif aktualni_stranka == "Kalkulačka zakázky":
    st.markdown("<h2>Získejte okamžitý odhad ceny</h2>", unsafe_allow_html=True)
    st.write("Výpočet v reálném čase zohledňuje aktuální ceny hutních materiálů a časovou náročnost.")
    
    col_kalk, col_vysledek = st.columns([1, 1])
    
    koeficienty = {
        "Kovaná brána (vjezdová)": {"kg_na_metr": 55, "prace_na_metr": 6500},
        "Kovaný plot (plotové dílce)": {"kg_na_metr": 35, "prace_na_metr": 4200},
        "Kované dveře / mříže": {"kg_na_metr": 45, "prace_na_metr": 7000}
    }
    
    with col_kalk:
        with st.container():
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            vybrany_produkt = st.selectbox("Typ konstrukce:", list(koeficienty.keys()))
            delka_v_metrech = st.number_input("Celková šířka/délka v metrech:", min_value=0.5, value=3.0, step=0.5)
            pocitat = st.button("Vypočítat cenu", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
    with col_vysledek:
        if pocitat:
            aktualni_cena_zeleza_za_kg = 28.50 
            data = koeficienty[vybrany_produkt]
            cena = (data["kg_na_metr"] * delka_v_metrech * aktualni_cena_zeleza_za_kg) + (data["prace_na_metr"] * delka_v_metrech)
            
            st.markdown(f"""
            <div class="content-card" style='border-left: 5px solid #6941c6;'>
                <h4 style='margin-top: 0; color: white;'>Předběžná kalkulace</h4>
                <p style='margin-bottom: 5px; color:#a09eb5;'>Produkt: <b>{vybrany_produkt}</b></p>
                <p style='margin-bottom: 15px; color:#a09eb5;'>Rozměr: <b>{delka_v_metrech} m</b></p>
                <h2 style='color: #fff; margin: 0;'>{cena:,.0f} Kč</h2>
                <p style='font-size: 0.85rem; color: #666; margin-top: 10px;'>* Cena je orientační. Neobsahuje povrchovou úpravu (zinek/barva) a montáž.</p>
            </div>
            """, unsafe_allow_html=True)


elif aktualni_stranka == "Sjednat termín":
    st.markdown("<h2>Napište nám o svém projektu</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        jmeno = st.text_input("Vaše jméno a příjmení *")
        kontakt_volba = st.selectbox("Preferovaný způsob komunikace", ["Telefonicky", "E-mailem"])
        kontakt_udaj = st.text_input("Váš telefon nebo e-mail *")
    with c2:
        poznamka = st.text_area("Stručný popis toho, co poptáváte", height=130)
        
    if st.button("Odeslat nezávaznou poptávku"):
        if not jmeno or not kontakt_udaj:
            st.error("Vyplňte prosím své jméno a kontakt.")
        else:
            st.session_state.terminy.append({
                "datum": str(date.today()), "jmeno": jmeno, "typ_kontaktu": kontakt_volba,
                "kontakt": kontakt_udaj, "poznamka": poznamka, "vyreseno": False
            })
            uloz_json(SOUBOR_TERMINY, st.session_state.terminy)
            st.success("Vaše poptávka byla úspěšně odeslána! Brzy se ozveme.")
    st.markdown('</div>', unsafe_allow_html=True)


elif aktualni_stranka == "Administrace" and st.session_state.prihlasen:
    st.markdown("<h2>Správa poptávek</h2>", unsafe_allow_html=True)
    nevyresene = [t for t in st.session_state.terminy if not t.get("vyreseno", False)]
    
    if not nevyresene:
        st.success("Nemáte žádné nevyřízené poptávky.")
    else:
        for i, term in enumerate(nevyresene):
            with st.expander(f"🔴 Poptávka: {term['jmeno']} (Přijato: {term['datum']})"):
                st.write(f"**Kontakt:** {term['kontakt']} ({term.get('typ_kontaktu', '')})")
                st.write(f"**Text poptávky:** {term.get('poznamka', 'Bez poznámky')}")
                if st.button("Označit jako vyřízeno", key=f"vyresit_{i}"):
                    for idx, t in enumerate(st.session_state.terminy):
                        if t == term:
                            st.session_state.terminy[idx]["vyreseno"] = True
                            break
                    uloz_json(SOUBOR_TERMINY, st.session_state.terminy)
                    st.rerun()

elif aktualni_stranka == "Návštěvnost" and st.session_state.prihlasen:
    st.markdown("<h2>Statistiky webu</h2>", unsafe_allow_html=True)
    data_navstev = nacti_json(SOUBOR_NAVSTEVNOST, {})
    if not data_navstev:
        st.info("Zatím nejsou data.")
    else:
        graf_data = {den: (len(d) if isinstance(d, list) else d) for den, d in data_navstev.items()}
        st.bar_chart(graf_data)
