import streamlit as st
import json
import os
from datetime import date, datetime
import uuid
import base64

# Nastavení stránky na široký profil
st.set_page_config(page_title="Umělecké kovářství Štěpán Palla", layout="wide", initial_sidebar_state="collapsed")

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

# --- NAVIGACE ---
seznam_stranek = ["Domů (Informace)", "Ukázky práce", "Kalkulačka zakázky", "Sjednat termín"]
if st.session_state.prihlasen:
    seznam_stranek.extend(["Administrace", "Návštěvnost"])

aktualni_stranka = st.radio("Navigace", seznam_stranek, horizontal=True, label_visibility="collapsed")

# --- CSS STYLING A DYNAMICKÉ POZADÍ (PROFI VZHLED) ---
obrazek_pozadi_base64 = nacti_obrazek_base64("pozadi.png")

if aktualni_stranka in ["Ukázky práce", "Administrace"] or not obrazek_pozadi_base64:
    css_pozadi = """
    .stApp { background-color: #1a1a1c !important; }
    .main .block-container { background-color: #121212 !important; }
    """
else:
    css_pozadi = f"""
    .stApp {{
        background-image: url("data:image/png;base64,{obrazek_pozadi_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .main .block-container {{
        background-color: rgba(18, 18, 18, 0.90) !important;
        backdrop-filter: blur(8px);
    }}
    """

st.markdown(f"""
<style>
{css_pozadi}
/* Celkový kontejner */
.main .block-container {{ 
    padding: 2.5rem 4rem; 
    border-radius: 16px; 
    box-shadow: 0 10px 30px rgba(0,0,0,0.8); 
    color: #eaeaea !important; 
    margin-top: 1.5rem; 
    border: 1px solid #333;
}}

/* Nadpisy */
h1, h2, h3 {{ color: #d4af37 !important; font-family: 'Cinzel', 'Georgia', serif; letter-spacing: 1px; }}
h1 {{ border-bottom: 2px solid #d4af37; padding-bottom: 10px; margin-bottom: 20px; }}

/* Texty */
p, li {{ font-size: 1.15rem; line-height: 1.6; color: #cccccc !important; }}

/* Navigační menu z Radio buttonů */
div[role="radiogroup"] {{ 
    display: flex; justify-content: center; gap: 10px; 
    background: linear-gradient(145deg, #1f1f22, #2a2a2d); 
    padding: 15px; border-radius: 12px; border: 1px solid #444; 
    box-shadow: 0 4px 15px rgba(0,0,0,0.5); 
    margin-bottom: 30px;
}}
div[role="radiogroup"] label {{ cursor: pointer; padding: 5px 10px; transition: 0.3s; }}
div[role="radiogroup"] label:hover {{ color: #d4af37 !important; }}

/* Tlačítka (Zlatý/Měděný vzhled) */
.stButton>button {{ 
    background: linear-gradient(135deg, #b87333 0%, #d4af37 100%) !important; 
    color: #111 !important; 
    font-weight: 800 !important; 
    font-size: 1.1rem !important; 
    border: none !important; 
    border-radius: 8px !important; 
    padding: 0.6rem 2.5rem !important; 
    box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2) !important; 
    transition: all 0.3s ease !important;
}}
.stButton>button:hover {{ 
    transform: translateY(-3px); 
    box-shadow: 0 8px 25px rgba(212, 175, 55, 0.5) !important; 
    color: #000 !important;
}}

/* Expander (Přihlášení a administrace) */
[data-testid="stExpander"] {{ background-color: #1e1e20 !important; border: 1px solid #444 !important; border-radius: 10px; }}
[data-testid="stExpander"] summary {{ color: #d4af37 !important; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)


# --- HLAVIČKA A LOGO ---
col_logo, col_login = st.columns([4, 1])
with col_logo:
    # Kontrola pro jpg i png formát loga
    if os.path.exists("pozadi2.png"):
        st.image("pozadi2.png", width=450)
    elif os.path.exists("pozadi2.jpg"):
        st.image("pozadi2.jpg", width=450)
    else:
        st.title("Umělecké kovářství Štěpán Palla")

with col_login:
    if not st.session_state.prihlasen:
        with st.expander("⚙️ Správa"):
            jmeno = st.text_input("Jméno")
            heslo = st.text_input("Heslo", type="password")
            if st.button("Vstoupit"):
                if jmeno == "1" and heslo == "1":
                    st.session_state.prihlasen = True
                    st.rerun()
                else:
                    st.error("Přístup odepřen.")
    else:
        st.success("Administrátor")
        if st.button("Odhlásit"):
            st.session_state.prihlasen = False
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)


# --- STRÁNKY ---

if aktualni_stranka == "Domů (Informace)":
    st.markdown("## Poctivé kovářské řemeslo na míru")
    
    col_text, col_vyhody = st.columns([1.2, 1])
    
    with col_text:
        st.write("""
        Vítejte v naší dílně. Specializujeme se na ruční umělecké zpracování kovů. 
        Naším hlavním zaměřením je **zakázková výroba kovaných plotů, vjezdových bran a mříží**.
        
        Každý kus, který opustí kovadlinu, je výsledkem tradičních postupů, 
        kde se surová síla ohně potkává s absolutní přesností a citem pro detail.
        Navrhneme řešení, které dokonale podtrhne architekturu vašeho domu a vydrží generace.
        """)
        st.markdown("### Naše služby")
        st.markdown("🔸 **Kované vjezdové brány** (křídlové i posuvné automatické)<br>🔸 **Kované ploty a výplně zídek**<br>🔸 **Mříže, zábradlí a ocelové prvky**", unsafe_allow_html=True)

    with col_vyhody:
        st.markdown("### Proč si vybrat nás?")
        st.info("🛡️ **Maximální odolnost**\n\nPoužíváme kvalitní žárové zinkování a kovářské barvy, které chrání kov před rzí na desítky let.")
        st.info("🔨 **100% Ruční práce**\n\nŽádné sériové odlitky. Každý spoj a ornament je tvořen ručně.")
        st.info("📐 **Návrh na míru**\n\nZaměření a konzultace přímo na místě instalace.")


elif aktualni_stranka == "Ukázky práce":
    st.markdown("## Nahlédněte pod pokličku naší práce")
    
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
            cols = st.columns(3) # Změněno na 3 sloupce pro hezčí mřížku
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
    st.markdown("## Získejte okamžitý odhad ceny")
    st.write("Vyberte, co potřebujete vyrobit. Výpočet v reálném čase zohledňuje aktuální ceny hutních materiálů a časovou náročnost ruční kovářské práce.")
    
    col_kalk, col_vysledek = st.columns([1, 1])
    
    koeficienty = {
        "Kovaná brána (vjezdová)": {"kg_na_metr": 55, "prace_na_metr": 6500},
        "Kovaný plot (plotové dílce)": {"kg_na_metr": 35, "prace_na_metr": 4200},
        "Kované dveře / mříže": {"kg_na_metr": 45, "prace_na_metr": 7000}
    }
    
    with col_kalk:
        vybrany_produkt = st.selectbox("Typ konstrukce:", list(koeficienty.keys()))
        delka_v_metrech = st.number_input("Celková šířka/délka v metrech:", min_value=0.5, value=3.0, step=0.5)
        pocitat = st.button("Vypočítat cenu")
        
    with col_vysledek:
        if pocitat:
            aktualni_cena_zeleza_za_kg = 28.50 
            data = koeficienty[vybrany_produkt]
            cena = (data["kg_na_metr"] * delka_v_metrech * aktualni_cena_zeleza_za_kg) + (data["prace_na_metr"] * delka_v_metrech)
            
            st.markdown(f"""
            <div style='background-color: #2a2a2d; padding: 20px; border-radius: 10px; border-left: 5px solid #d4af37;'>
                <h4 style='margin-top: 0; color: white;'>Předběžná kalkulace</h4>
                <p style='margin-bottom: 5px;'>Produkt: <b>{vybrany_produkt}</b></p>
                <p style='margin-bottom: 15px;'>Rozměr: <b>{delka_v_metrech} m</b></p>
                <h2 style='color: #d4af37; margin: 0;'>{cena:,.0f} Kč</h2>
                <p style='font-size: 0.9rem; color: #888; margin-top: 10px;'>* Cena je orientační. Neobsahuje povrchovou úpravu (zinek/barva) a montáž.</p>
            </div>
            """, unsafe_allow_html=True)


elif aktualni_stranka == "Sjednat termín":
    st.markdown("## Napište nám o svém projektu")
    st.write("Zanechte nám na sebe kontakt a my se vám co nejdříve ozveme pro probrání detailů nebo zaměření.")
    
    with st.container():
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


elif aktualni_stranka == "Administrace" and st.session_state.prihlasen:
    st.markdown("## 📅 Správa poptávek")
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
    st.markdown("## 📊 Statistiky webu")
    data_navstev = nacti_json(SOUBOR_NAVSTEVNOST, {})
    if not data_navstev:
        st.info("Zatím nejsou data.")
    else:
        graf_data = {den: (len(d) if isinstance(d, list) else d) for den, d in data_navstev.items()}
        st.bar_chart(graf_data)
