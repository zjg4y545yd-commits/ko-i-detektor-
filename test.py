import streamlit as st
import json
import os
from datetime import date, datetime
import uuid
import base64

# Nastavení stránky
st.set_page_config(page_title="Umělecké kovářství", layout="wide")

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
    """Načte obrázek a převede ho do formátu pro CSS pozadí."""
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
seznam_stranek = ["Informace", "Fotogalerie", "Ceník a Kalkulačka", "Termíny"]
if st.session_state.prihlasen:
    seznam_stranek.extend(["Administrace", "Návštěvnost"])

# Nahrazení tabs za dynamické menu
aktualni_stranka = st.radio("Navigace", seznam_stranek, horizontal=True, label_visibility="collapsed")

# --- CSS STYLING A DYNAMICKÉ POZADÍ ---
obrazek_pozadi_base64 = nacti_obrazek_base64("pozadi.png")

# Pokud jsme v Galerii nebo Administraci, dáme plné barvy bez obrázku
if aktualni_stranka in ["Fotogalerie", "Administrace"] or not obrazek_pozadi_base64:
    css_pozadi = """
    .stApp { background-color: #2e3033 !important; }
    .main .block-container { background-color: #1a1b1c !important; }
    """
else:
    # Pro ostatní stránky nastavíme obrázek a poloprůhledný kontejner pro čitelnost textu
    css_pozadi = f"""
    .stApp {{
        background-image: url("data:image/png;base64,{obrazek_pozadi_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .main .block-container {{
        background-color: rgba(26, 27, 28, 0.85) !important; /* Poloprůhledná černá pro čitelnost */
        backdrop-filter: blur(5px); /* Lehké rozmazání pozadí za textem */
    }}
    """

# Přidání zbytku tvých stylů (nadpisy, tlačítka atd.)
st.markdown(f"""
<style>
{css_pozadi}
.main .block-container {{ padding: 3rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.6); color: #f5f5f5 !important; margin-top: 1rem; }}
h1, h2, h3 {{ color: #ff6600 !important; font-family: 'Georgia', serif; }}
p, label, .stMarkdown, [data-testid="stMarkdownContainer"] {{ color: #ffffff !important; font-size: 1.1rem; }}
.stButton>button {{ background-color: #3a1c00 !important; color: #d4af37 !important; border: 1px solid #d4af37 !important; transition: 0.3s; }}
.stButton>button:hover {{ background-color: #d4af37 !important; color: #111111 !important; }}
/* Stylizace radio buttonů, aby vypadaly jako navigační lišta */
div[role="radiogroup"] {{ flex-wrap: wrap; gap: 15px; margin-bottom: 20px; padding: 10px; background-color: rgba(0,0,0,0.5); border-radius: 8px; }}
[data-testid="stExpander"] details, [data-testid="stExpander"] {{ background-color: #26282b !important; border: 1px solid #444 !important; border-radius: 8px; }}
[data-testid="stExpander"] summary {{ background-color: #33363a !important; color: #ff6600 !important; }}
</style>
""", unsafe_allow_html=True)


# --- HLAVIČKA A PŘIHLAŠOVÁNÍ ---
col_nadpis, col_login = st.columns([3, 1])
with col_nadpis:
    # Nahrazení textového nadpisu za obrázek pozadi2.jpg
    if os.path.exists("pozadi2.jpg"):
        st.image("pozadi2.jpg", width=400)
    else:
        st.title("Umělecké kovářství") # Záloha, kdyby se obrázek nenahrál správně

with col_login:
    if not st.session_state.prihlasen:
        with st.expander("👤 Přihlášení pro správce"):
            jmeno_prihlaseni = st.text_input("Jméno", key="in_jmeno")
            heslo_prihlaseni = st.text_input("Heslo", type="password", key="in_heslo")
            if st.button("Přihlásit"):
                if jmeno_prihlaseni == "1" and heslo_prihlaseni == "1":
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


# --- ZOBRAZENÍ OBSAHU PODLE VYBRANÉ STRÁNKY ---

if aktualni_stranka == "Informace":
    st.header("O naší dílně")
    st.write("""
    Vítejte na stránkách našeho uměleckého kovářství. Specializujeme se na ruční výrobu a umělecké zpracování kovů s hlavním zaměřením na zakázkovou výrobu kovaných plotů a vjezdových bran.
    
    Každý kus, který opustí naši dílnu, je výsledkem poctivé řemeslné práce, kde se tradiční kovářské postupy setkávají s přesností a důrazem na detail. Ať už hledáte robustní ochranu vašeho pozemku nebo elegantní vstupní prvek, navrhneme a vyrobíme řešení přesně na míru vašim představám a architekce vašeho domu.
    
    Naše práce se vyznačuje vysokou odolností, kvalitní povrchovou úpravou a nadčasovým designem, který vydrží generace.
    """)
    
    st.subheader("Naše hlavní služby")
    st.markdown("""
    * Kované brány (křídlové i posuvné)
    * Kované ploty a výplně
    * Vstupní dveře s kovanými prvky
    * Restaurování historických kovářských děl
    """)


elif aktualni_stranka == "Fotogalerie":
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


elif aktualni_stranka == "Ceník a Kalkulačka":
    st.header("Orientační kalkulačka zakázky")
    st
