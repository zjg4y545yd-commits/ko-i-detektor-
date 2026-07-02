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
SOUBOR_GALERIE = "galerie.json"  # Nový soubor pro trvalou persistenci fotografií

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
if "galerie" not in st.session_state:
    st.session_state.galerie = nacti_json(SOUBOR_GALERIE, [])
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

# --- CSS STYLING (Prémiový kovářský vizuál) ---
st.markdown("""
<style>
/* Import prémiového uměleckého písma Cinzel z Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800;900&family=Inter:wght@400;500;600&display=swap');

/* Základní barvy a pozadí */
[data-testid="stAppViewContainer"] {
    background-color: #110f16 !important; /* Temné grafitové pozadí */
    color: #e2e8f0;
}
[data-testid="stSidebar"] {
    background-color: #171520 !important; /* Sladěné tmavé menu */
    border-right: 1px solid #2a2538;
}
[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* Skrytí horního panelu u postranního menu */
[data-testid="stSidebarNav"] { display: none; }

/* Typografie - Nadpisy mají umělecký font kovaného bronzu */
h1, h2, h3, h4 {
    font-family: 'Cinzel', serif !important;
    color: #c5a059 !important; /* Sjednoceno na barvu kovaného bronzu */
    letter-spacing: 1px;
}
p, span, div, label {
    font-family: 'Inter', sans-serif;
}

/* Kontejner pro logo v levém rohu */
.sidebar-logo-container {
    text-align: center;
    padding: 15px 0 25px 0;
    border-bottom: 1px solid #2a2538;
    margin-bottom: 20px;
}
.sidebar-logo-img {
    max-width: 90%;
    height: auto;
    display: block;
    margin: 0 auto;
    filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.5));
}

/* Záložní text pro logo */
.sidebar-logo-text {
    font-family: 'Cinzel', serif !important;
    font-size: 1.1rem;
    font-weight: 700;
    color: #c5a059;
    padding: 10px 0 20px 0;
    border-bottom: 1px solid #2a2538;
    margin-bottom: 20px;
    text-transform: uppercase;
    text-align: center;
}

/* --- ÚPRAVA POLOŽEK V MENU --- */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span[data-baseweb="radio"] {
    display: none;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    padding: 12px 15px;
    border-radius: 8px;
    margin-bottom: 6px;
    cursor: pointer;
    background-color: transparent;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
}
/* Aktivní/Hover efekt v menu s nádechem bronzu */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background-color: rgba(197, 160, 89, 0.08);
    border-left: 3px solid #c5a059;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div {
    font-size: 0.95rem;
    font-weight: 500;
    margin-left: 5px;
    color: #cbd5e1;
}

.menu-section-title {
    font-size: 0.75rem;
    color: #71717a;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 10px;
    padding-left: 5px;
    letter-spacing: 1px;
}

/* Hlavní poutač (Hero Banner) - Styl hluboké kovářské noci */
.hero-banner {
    background: linear-gradient(135deg, #1c1924 0%, #121017 100%);
    border: 1px solid #36304a;
    border-radius: 16px;
    padding: 3.5rem 2rem;
    text-align: center;
    margin-bottom: 2.5rem;
    box-shadow: 0 15px 35px rgba(0,0,0,0.6);
}
.hero-banner h1 {
    font-size: 3rem;
    font-weight: 900;
    margin-bottom: 15px;
    color: #c5a059 !important;
    border: none;
}
.hero-banner p {
    font-size: 1.15rem;
    color: #94a3b8;
    max-width: 750px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Obsahové bloky s efektem sálajícího tepla (Hover zář) */
.content-card {
    background-color: #16141d;
    border: 1px solid #2a2538;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.content-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(197, 160, 89, 0.12);
    border-color: #453d5a;
}

/* Rámečky pro obrázky v galerii */
.stImage img {
    border-radius: 8px !important;
    border: 1px solid #2a2538 !important;
    transition: transform 0.3s ease;
}
.stImage img:hover {
    transform: scale(1.02);
}

/* Nová prémiová kovářská tlačítka (Barva kovaného bronzu/mosazi) */
.stButton>button {
    background-color: #c5a059 !important;
    color: #110f16 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(197, 160, 89, 0.2) !important;
}
.stButton>button:hover {
    background-color: #e5c17b !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 15px rgba(197, 160, 89, 0.3) !important;
}

/* --- FIX: OPRAVDOVÝ MINI OBDÉLNÍČEK V PRAVÉM ROHU DOLE --- */
div[data-testid="stPopover"] {
    position: fixed !important;
    bottom: 15px !important;
    right: 15px !important;
    z-index: 999999 !important;
    width: auto !important; /* Blokuje roztažení přes celou obrazovku */
    display: inline-block !important;
}
div[data-testid="stPopover"] > button {
    background-color: rgba(23, 21, 32, 0.8) !important; 
    color: #c5a059 !important;
    border-radius: 4px !important;
    width: 45px !important; /* Fixní malá šířka obdélníku */
    height: 28px !important; /* Fixní nízká výška */
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: 1px solid rgba(197, 160, 89, 0.4) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.6) !important;
    transition: all 0.3s ease !important;
    opacity: 0.6;
}
div[data-testid="stPopover"] > button:hover {
    background-color: #c5a059 !important;
    border-color: #e5c17b !important;
    opacity: 1;
    transform: scale(1.05);
}
div[data-testid="stPopover"] > button:hover > div > div > p {
    color: #110f16 !important;
}
div[data-testid="stPopover"] > button > div > div > p {
    color: #c5a059 !important;
    font-size: 11px !important;
    font-weight: bold;
    margin: 0;
    transition: color 0.3s ease !important;
}
div[data-testid="stPopover"] > button svg {
    display: none; /* Odstraní šipku Streamlitu, aby zbyl čistý obdélník */
}
</style>
""", unsafe_allow_html=True)

# --- LEVÉ POSTSTRANNÍ MENU (SIDEBAR) ---
with st.sidebar:
    
    foto_logo = nacti_obrazek_base64("podpis.png")
    if foto_logo:
        st.markdown(f"""
        <div class="sidebar-logo-container">
            <img src="data:image/png;base64,{foto_logo}" class="sidebar-logo-img" alt="Podpis Štěpán Pala">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='sidebar-logo-text'>Štěpán Palla</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='menu-section-title'>Navigace</div>", unsafe_allow_html=True)
    
    seznam_stranek = ["🏠 Domů (Informace)", "🔨 Ukázky práce", "🧮 Kalkulačka zakázky", "✉️ Sjednat termín"]
    
    if st.session_state.prihlasen:
        st.markdown("<div class='menu-section-title'>Správa webu</div>", unsafe_allow_html=True)
        seznam_stranek.extend(["⚙️ Administrace", "📊 Návštěvnost"])

    vybrana_polozka = st.radio("Menu", seznam_stranek, label_visibility="collapsed")
    aktualni_stranka = vybrana_polozka.split(" ", 1)[1]

# --- PLOVOUCÍ PŘIHLÁŠENÍ (STRIKTNÍ OBDÉLNÍČEK VPRAVO DOLE) ---
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
        st.success("Přihlášen: Admin")
        if st.button("Odhlásit", use_container_width=True):
            st.session_state.prihlasen = False
            st.rerun()

# --- HLAVNÍ OBSAHOVÉ STRÁNKY ---

if aktualni_stranka == "Domů (Informace)":
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
            <h3 style='margin-top:0;'>Naše služby</h3>
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
            <h3 style='margin-top:0;'>Proč si vybrat nás?</h3>
            <p style='color:#a09eb5;'>🛡️ <b>Maximální odolnost:</b> Používáme kvalitní žárové zinkování a barvy proti rzi.</p>
            <p style='color:#a09eb5;'>🔨 <b>100% Ruční práce:</b> Žádné sériové odlitky. Každý spoj tvořen ručně.</p>
            <p style='color:#a09eb5;'>📐 <b>Návrh na míru:</b> Zaměření a konzultace přímo na místě instalace.</p>
        </div>
        """, unsafe_allow_html=True)

elif aktualni_stranka == "Ukázky práce":
    st.markdown("<h2>Ukázky naší práce</h2>", unsafe_allow_html=True)
    
    if st.session_state.prihlasen:
        with st.expander("📸 Přidat nové fotografie"):
            uploaded_file = st.file_uploader("Vyberte obrázek (JPG, PNG)", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                if st.button("Nahrát na web"):
                    # Převod nahraného obrázku na Base64 string pro trvalé uložení v JSONu
                    bytes_data = uploaded_file.getvalue()
                    base64_foto = base64.b64encode(bytes_data).decode("utf-8")
                    
                    st.session_state.galerie.append({
                        "id": str(uuid.uuid4())[:8],
                        "nazev": uploaded_file.name,
                        "data": base64_foto
                    })
                    uloz_json(SOUBOR_GALERIE, st.session_state.galerie)
                    st.success("Fotografie byla trvale uložena do databáze!")
                    st.rerun()

    # Načítání a vykreslování fotek z trvalého JSONu místo nestabilní složky
    if not st.session_state.galerie:
        st.info("Galerie se momentálně připravuje. Brzy zde uvidíte naše realizace.")
    else:
        cols = st.columns(3)
        for i, fotka in enumerate(st.session_state.galerie):
            with cols[i % 3]:
                try:
                    raw_bytes = base64.b64decode(fotka["data"])
                    st.image(raw_bytes, use_container_width=True)
                except Exception:
                    st.error("Chyba při načítání souboru.")
                    
                if st.session_state.prihlasen:
                    if st.button("🗑️ Smazat", key=f"del_{fotka['id']}"):
                        st.session_state.galerie.pop(i)
                        uloz_json(SOUBOR_GALERIE, st.session_state.galerie)
                        st.rerun()

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
            <div class="content-card" style='border-left: 5px solid #c5a059;'>
                <h4 style='margin-top: 0;'>Předběžná kalkulace</h4>
                <p style='margin-bottom: 5px; color:#a09eb5;'>Produkt: <b>{vybrany_produkt}</b></p>
                <p style='margin-bottom: 15px; color:#a09eb5;'>Rozměr: <b>{delka_v_metrech} m</b></p>
                <h2 style='color: #ffffff; margin: 0;'>{cena:,.0f} Kč</h2>
                <p style='font-size: 0.85rem; color: #71717a; margin-top: 10px;'>* Cena je orientační. Neobsahuje povrchovou úpravu (zinek/barva) a montáž.</p>
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
