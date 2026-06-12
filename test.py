import streamlit as st

# 1. Nastavení stránky
st.set_page_config(layout="wide")
st.title("🐱 Kočičí detektor ti zmrde")

# 2. Inicializace stavu
if "pravy_vyber" not in st.session_state:
    st.session_state.pravy_vyber = None

# 3. Rozdělení stránky
left_col, right_col = st.columns([3, 1])

# Pravý panel (Menu)
with right_col:
    st.subheader("Další menu")
    if st.button("DOMŮ", use_container_width=True):
        st.session_state.pravy_vyber = None
    if st.button("KOČKA 1", use_container_width=True):
        st.session_state.pravy_vyber = "kocka1"
    if st.button("KOČKA 2", use_container_width=True):
        st.session_state.pravy_vyber = "kocka2"

# Levý panel (Hlavní obsah)
with left_col:
    if st.session_state.pravy_vyber == "kocka1":
        st.header("🐱 Kočičí kalkulačka a párty")
        # Video se spustí automaticky
        st.video("https://www.youtube.com/watch?v=fWcKji80qns", autoplay=True)
        
        if "vysledek" not in st.session_state:
            st.session_state.vysledek = 0

        cislo1 = st.number_input("První číslo", value=0, key="c1")
        cislo2 = st.number_input("Druhé číslo", value=0, key="c2")

        col1, col2, col3, col4 = st.columns(4)
        if col1.button("➕"): st.session_state.vysledek = cislo1 + cislo2
        if col2.button("➖"): st.session_state.vysledek = cislo1 - cislo2
        if col3.button("✖️"): st.session_state.vysledek = cislo1 * cislo2
        if col4.button("➗"):
            if cislo2 != 0: st.session_state.vysledek = cislo1 / cislo2
            else: st.error("Dělení nulou, ty kočičáku!")

        st.write("---")
        st.subheader(f"Výsledek: {st.session_state.vysledek}")
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJ4ZzR6NHJ4ZzR6NHJ4ZzR6NHJ4ZzR6NHJ4ZzR6NHJ4ZzR6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/JIX9t2j0ZTN9S/giphy.gif", width=300)

    elif st.session_state.pravy_vyber == "kocka2":
        st.header("Záložka: KOČKA 2")
        st.write("Tady je obsah pro druhou kočku.")
    
    else:
        # Původní aplikace
        jmeno = st.text_input("Jak se jmenuješ?")
        vek = st.number_input("Kolik je ti let?", min_value=0, max_value=120, value=25)

        if st.button("Vyhodnotit"):
            if vek > 20:
                st.success(f"Ahoj {jmeno}! Je ti víc než 20 ty stará vraždo, tak tady máš slíbenou kočku:")
                st.image("https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600", caption="Tvoje odměna ty sráči posranej! 🐱")
                st.image("https://images.unsplash.com/photo-1543852786-1cf6624b9987?w=800&auto=format&fit=crop&q=60", caption="Tvoje odměna ty sráči posranej! 🐱")
            else:
                st.warning(f"Ahoj {jmeno}, je ti jen {vek}. To je na kočku ještě málo, teď ti Rytmus napálí vypínačku ")
                st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8s0kQKci68L9t_hQ4sbMIKCo_hcka3XI6Of_2Z3YGyA&s=10")
        
        inteligence = st.number_input("Kolik máš IQ ty konino", min_value=0, max_value=200, value=25)
        if st.button("test"):
            if inteligence > 20:
                st.success(f"Ahoj {jmeno}! Jsi chytřejší jak labrador, gratuluji!")
            else:
                st.warning(f"Ahoj {jmeno}, tvoje IQ je tak zasraně v hajzlu, že nemám slov")
                st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQqRavdWAv8MxitBXG9GazogltUp6RJ2djHAhAqxeJfA&s=10")

        nalada = st.selectbox("Jakou máš dnes náladu?", ["Skvělou", "Pod psa"])
        if nalada == "Skvělou":
            st.balloons()
            st.write("jupí ty sketo!")
        elif nalada == "Pod psa":
            st.write("S tvým ksichtem se ani nedivím:).")
