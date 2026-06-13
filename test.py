import streamlit as st

# 1. Nastavení stránky
st.set_page_config(layout="wide")
st.title("🐱 Kočičí detektor ti zmrde")

# 2. Inicializace stavu
if "pravy_vyber" not in st.session_state:
    st.session_state.pravy_vyber = None
if "body" not in st.session_state:
    st.session_state.body = 0

# Funkce pro přičítání bodů v kvízu
def pricti_body(key, hodnota):
    if st.session_state[key] == hodnota and not st.session_state.get(f"{key}_done", False):
        st.session_state.body += 10
        st.session_state[f"{key}_done"] = True

# Funkce pro trest (Rytmus)
def dej_vypinac():
    st.warning("Špatně sráči! Rytmus ti právě najebal uspávací bombičku")
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8s0kQKci68L9t_hQ4sbMIKCo_hcka3XI6Of_2Z3YGyA&s=10")

# 3. Rozdělení stránky
left_col, right_col = st.columns([3, 1])

# Pravý panel
with right_col:
    st.subheader("Další menu")
    if st.button("DOMŮ", use_container_width=True, key="btn_domu"):
        st.session_state.pravy_vyber = None
    if st.button("KALKULAČKA", use_container_width=True, key="btn_kalk"):
        st.session_state.pravy_vyber = "kocka1"
    if st.button("FRANTIŠEK ŘEDITEL", use_container_width=True, key="btn_frantisek"):
        st.session_state.pravy_vyber = "kocka2"
    
    st.markdown("---")
    st.subheader(f"Tvoje body: {st.session_state.body}")
    if st.button("Resetovat body", key="btn_reset"):
        st.session_state.body = 0
        st.session_state.q1_done = False
        st.session_state.q2_done = False
        st.session_state.q3_done = False
        st.session_state.q4_done = False
        st.rerun()

# Levý panel
with left_col:
    if st.session_state.pravy_vyber == "kocka1":
        st.header("🐱 Kočičí kalkulačka")
        st.video("https://www.youtube.com/watch?v=fWcKji80qns", autoplay=True)
        
        if "vysledek" not in st.session_state:
            st.session_state.vysledek = 0

        c1 = st.number_input("První číslo", value=0, key="c1_input")
        c2 = st.number_input("Druhé číslo", value=0, key="c2_input")

        col1, col2, col3, col4 = st.columns(4)
        if col1.button("➕", key="plus"): st.session_state.vysledek = c1 + c2
        if col2.button("➖", key="minus"): st.session_state.vysledek = c1 - c2
        if col3.button("✖️", key="krat"): st.session_state.vysledek = c1 * c2
        if col4.button("➗", key="deleno"):
            if c2 != 0: st.session_state.vysledek = c1 / c2
            else: st.error("Dělení nulou, ty kočičáku!")

        st.subheader(f"Výsledek: {st.session_state.vysledek}")
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJ4ZzR6NHJ4ZzR6NHJ4ZzR6NHJ4ZzR6NHJ4ZzR6NHJ4ZzR6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/JIX9t2j0ZTN9S/giphy.gif", width=300)

    elif st.session_state.pravy_vyber == "kocka2":
        st.title("TEST PROKRASTINACE")
        st.header("František ředitel, ministr zeměkoule")
        
        # Otázka 1
        q1 = st.selectbox("Kolik stály ugurty ?", ["-", "8,90 ty pisooo", "7,90 ty pisooo"], key="q1", on_change=pricti_body, args=("q1", "7,90 ty pisooo"))
        if q1 != "-" and q1 != "7,90 ty pisooo": dej_vypinac()
        
        if st.session_state.get("q1_done"):
            st.success("Nádherné, jde vidět, že žiješ kvalitně")
            
            # Otázka 2
            q2 = st.selectbox("Kdo je Františkova holka?", ["-", "Zatím nemá", "Maruška"], key="q2", on_change=pricti_body, args=("q2", "Maruška"))
            if q2 != "-" and q2 != "Maruška": dej_vypinac()
            
            if st.session_state.get("q2_done"):
                st.success("Super kamaráde! Alespoň tady můžeš zářit, když v životě smrdíš!")
                
                # Otázka 3
                q3 = st.selectbox("Co má František nejraději?", ["-", "Grilovačky", "Grilovánky"], key="q3", on_change=pricti_body, args=("q3", "Grilovánky"))
                if q3 != "-" and q3 != "Grilovánky": dej_vypinac()
                
                if st.session_state.get("q3_done"):
                    st.success("Máš naprostou pravdu, patříš mezi top 1%!")
                    
                    # Otázka 4
                    q4 = st.selectbox("Co vše musíme dát do rajčatového salátu", ["-", "sůl,ocet,cukr", "ocet,sůl,cukr krystal"], key="q4", on_change=pricti_body, args=("q4", "sůl,ocet,cukr"))
                    if q4 != "-" and q4 != "sůl,ocet,cukr": dej_vypinac()
                    
                    if st.session_state.get("q4_done"):
                        st.success("Správně, konečně tě internet naučil něco kloudného!")
                        st.balloons()
    else:
        # Původní aplikace
        jmeno = st.text_input("Jak se jmenuješ?", key="input_jmeno")
        vek = st.number_input("Kolik je ti let?", min_value=0, max_value=120, value=25, key="input_vek")

        if st.button("Vyhodnotit", key="btn_vyhodnotit"):
            if vek > 20:
                st.success(f"Ahoj {jmeno}! Je ti víc než 20 ty stará vraždo, tak tady máš slíbenou kočku:")
                st.image("https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600", caption="Tvoje odměna ty sráči posranej! 🐱")
                st.image("https://images.unsplash.com/photo-1543852786-1cf6624b9987?w=800&auto=format&fit=crop&q=60", caption="Tvoje odměna ty sráči posranej! 🐱")
            else:
                st.warning(f"Ahoj {jmeno}, je ti jen {vek}. To je na kočku ještě málo, teď ti Rytmus napálí vypínačku ")
                st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8s0kQKci68L9t_hQ4sbMIKCo_hcka3XI6Of_2Z3YGyA&s=10")
        
        inteligence = st.number_input("Kolik máš IQ ty konino min:0  max:200 ", min_value=0, max_value=200, value=25, key="input_iq")
        if st.button("test", key="btn_iq"):
            if inteligence > 160:
                st.success(f"Ahoj {jmeno}! Jsi chytřejší jak labrador, gratuluji!")
            else:
                st.warning(f"Ahoj {jmeno}, tvoje IQ je tak zasraně v hajzlu, že nemám slov")
                st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQqRavdWAv8MxitBXG9GazogltUp6RJ2djHAhAqxeJfA&s=10")

        nalada = st.selectbox("Jakou máš dnes náladu?", ["-", "Skvělou", "Pod psa"], key="nalada_sel")
        if nalada == "Skvělou":
            st.balloons()
            st.write("jupí ty sketo!")
        elif nalada == "Pod psa":
            st.write("S tvým kscihtem se ani nedivím:).")
