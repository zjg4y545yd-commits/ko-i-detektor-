import streamlit as st

# Nastavení stránky musí být první příkaz
st.set_page_config(page_title="Umělecké kovářství", layout="wide")

# Vložení vlastního CSS pro kovářský vzhled (tapeta a tmavý design)
st.markdown("""
<style>
/* Nastavení tapety na pozadí celého webu */
.stApp {
    background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAUVBMVEV3d3f///9wcHCJiYnGxsZ0dHT19fWZmZltbW1ra2vPz8+2trabm5v5+fl7e3uAgIDs7OyioqKurq7f39/W1ta6urqoqKiQkJDj4+PBwcHc3NwKRuvRAAAC3UlEQVR4nO3Yy3baMBgAYSSQESY2lwAlvP+D1jaXGoa03cGJZpas5O9I+m0mwR6bPPtxXS83v6Y/vY/t7Nj8n8nnts0xphKKOc3rf5vUq5wmBZViWj5ulnuTXVuWyFDM++9NmnmBIn2x/fzG5JjKFOlK+eupSb149cpeWT48MZkVTdKhfMCk7F3SFzcPJsfiSbqdsr8zadpir9dRi+PYZBNfvZ53KLUjk5MnZygu/5isPDnncnU12eVXr+VdSturydRtci03Z5O12+RWnJ1Nlg6dW2l6NvHojIpVb1J5dEblXW/i1BnXv6JMwpfXyag0700OXiej0qo3mWsyrtUEpUaTx7phrMlDmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhg8mHJuM0YanpTA6a3BU6k3189SreqbTqTWpNRqV5b7LOr17HOxX3vUloX72OdyqfBhMHz6jYDCa1h+dWf530JsF9civvLiZbUW6Fi0m1ePVK3qX4dTUJB19RhlIbbiaNh2douE0uJmHm6Jlchs7NxD9R+rpP4rFJWImSj+HepEqloyx24cEkrNuyUXIdYBKqVcETOS1O4YlJ9zFY7PSJq3V4bhLqVORWSXk7Vrg3Cc1yUZxKWnysw19MOpV9mwsaQSnH7YMITbpO22nMsYByXm1qPv8zk67qWM9+fPWpevrw35iU3W+G/SY3Y3HcVQAAAABJRU5ErkJggg==");
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
tab1, tab2, tab3 = st.tabs(["Informace", "Fotogalerie", "Ceník a Kalkulačka"])

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
        # Zde nahradíte URL odkazy za cesty k vašim vlastním fotkám, např. "brana.jpg"
        st.image("https://images.unsplash.com/photo-1622359487565-d60321262d08?q=80&w=800&auto=format&fit=crop", caption="Detail kované brány")
    with col2:
        st.image("https://images.unsplash.com/photo-1533038590840-1cbea9766434?q=80&w=800&auto=format&fit=crop", caption="Kovářská práce v dílně")
        
    st.info("Administrátorská poznámka: Pro nahrávání nových fotografií přímo z aplikace lze do budoucna přidat modul 'st.file_uploader'. Nyní se fotografie nahrávají umístěním do složky programu.")

# ZÁLOŽKA 3: KALKULAČKA A CENÍK
with tab3:
    st.header("Orientační kalkulačka zakázky")
    st.write("Vyberte typ výrobku a zadejte požadovanou délku pro získání orientační ceny. Výpočet zohledňuje aktuální tržní cenu železa a náročnost ruční práce.")
    
    # Skryté proměnné na pozadí (zákazník je nevidí)
    aktualni_cena_zeleza_za_kg = 28.50  # Hodnota v CZK
    
    # Koeficienty pro různé typy výrobků
    # (kolik kg železa na 1 metr a základní cena práce na 1 metr)
    koeficienty = {
        "Kovaná brána": {"kg_na_metr": 55, "prace_na_metr": 6500},
        "Kovaný plot": {"kg_na_metr": 35, "prace_na_metr": 4200},
        "Kované dveře": {"kg_na_metr": 45, "prace_na_metr": 7000}
    }
    
    # Uživatelské vstupy
    vybrany_produkt = st.selectbox("Vyberte typ výrobku:", list(koeficienty.keys()))
    delka_v_metrech = st.number_input("Zadejte celkovou délku (v metrech):", min_value=0.5, value=2.0, step=0.5)
    
    # Výpočet po stisknutí tlačítka
    if st.button("Vypočítat orientační cenu"):
        data_produktu = koeficienty[vybrany_produkt]
        
        # Matematika na pozadí
        spotreba_zeleza_kg = data_produktu["kg_na_metr"] * delka_v_metrech
        cena_za_material = spotreba_zeleza_kg * aktualni_cena_zeleza_za_kg
        cena_za_praci = data_produktu["prace_na_metr"] * delka_v_metrech
        
        # Celková cena
        celkova_cena = cena_za_material + cena_za_praci
        
        # Zobrazení výsledku
        st.markdown("### Výsledek výpočtu")
        st.write(f"Zadaný rozměr: **{delka_v_metrech} m**")
        st.write(f"Typ konstrukce: **{vybrany_produkt}**")
        
        # Velký box s výslednou cenou
        st.metric(label="Odhadovaná celková cena", value=f"{celkova_cena:,.0f} CZK".replace(",", " "))
        
        st.caption("Uvedená cena je pouze orientační. Přesná kalkulace bude stanovena po osobním zaměření a dohodnutí konkrétních ozdobných detailů a povrchové úpravy. Cena železa použitá ve výpočtu je průběžně aktualizována.")
