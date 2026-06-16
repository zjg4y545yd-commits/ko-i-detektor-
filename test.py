import streamlit as st
import random

# 1. Nastavení stránky
st.set_page_config(layout="wide")
st.title("🐱 Kočičí detektor ti zmrde")

# 2. Inicializace stavu
if "pravy_vyber" not in st.session_state: st.session_state.pravy_vyber = None
if "body" not in st.session_state: st.session_state.body = 0
if "pexeso_hotovo" not in st.session_state: st.session_state.pexeso_hotovo = False

# Funkce pro body a trest
def pricti_body(key, hodnota):
    if st.session_state[key] == hodnota and not st.session_state.get(f"{key}_done", False):
        st.session_state.body += 10
        st.session_state[f"{key}_done"] = True

def dej_vypinac():
    st.warning("Špatně sráči! Rytmus ti právě najebal uspávací bombičku")
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8s0kQKci68L9t_hQ4sbMIKCo_hcka3XI6Of_2Z3YGyA&s=10")

# 3. Rozdělení stránky
left_col, right_col = st.columns([3, 1])

with right_col:
    st.subheader("Další menu")
    if st.button("DOMŮ", use_container_width=True, key="btn_domu"): st.session_state.pravy_vyber = None
    if st.button("KALKULAČKA", use_container_width=True, key="btn_kalk"): st.session_state.pravy_vyber = "kocka1"
    if st.button("FRANTIŠEK ŘEDITEL", use_container_width=True, key="btn_frantisek"): st.session_state.pravy_vyber = "kocka2"
    if st.button("PEXESO", use_container_width=True, key="btn_pexeso"): st.session_state.pravy_vyber = "pexeso"
    
    st.markdown("---")
    st.subheader(f"Tvoje body: {st.session_state.body}")
    if st.button("Resetovat body", key="btn_reset"):
        st.session_state.body = 0
        st.session_state.pexeso_hotovo = False
        for i in range(1, 5): st.session_state[f"q{i}_done"] = False
        st.rerun()

with left_col:
    # --- KALKULAČKA ---
    if st.session_state.pravy_vyber == "kocka1":
        st.header("🐱 Kočičí kalkulačka")
        st.video("https://www.youtube.com/watch?v=fWcKji80qns", autoplay=True)
        if "vysledek" not in st.session_state: st.session_state.vysledek = 0
        c1 = st.number_input("První číslo", value=0, key="c1_input")
        c2 = st.number_input("Druhé číslo", value=0, key="c2_input")
        col1, col2, col3, col4 = st.columns(4)
        if col1.button("➕", key="plus"): st.session_state.vysledek = c1 + c2
        if col2.button("➖", key="minus"): st.session_state.vysledek = c1 - c2
        if col3.button("✖️", key="krat"): st.session_state.vysledek = c1 * c2
        if col4.button("➗", key="deleno"): st.session_state.vysledek = c1/c2 if c2!=0 else "Chyba!"
        st.subheader(f"Výsledek: {st.session_state.vysledek}")
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJ4ZzR6NHJ4ZzR6NHJ4ZzR6NHJ4ZzR6NHJ4ZzR6NHJ4ZzR6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/JIX9t2j0ZTN9S/giphy.gif", width=300)

    # --- KVÍZ ---
    elif st.session_state.pravy_vyber == "kocka2":
        st.title("TEST PROKRASTINACE")
        q1 = st.selectbox("Kolik stály ugurty ?", ["-", "8,90 ty pisooo", "7,90 ty pisooo"], key="q1", on_change=pricti_body, args=("q1", "7,90 ty pisooo"))
        if q1 not in ["-", "7,90 ty pisooo"]: dej_vypinac()
        if st.session_state.get("q1_done"):
            st.success("Nádherné!")
            q2 = st.selectbox("Kdo je Františkova holka?", ["-", "Zatím nemá", "Maruška"], key="q2", on_change=pricti_body, args=("q2", "Maruška"))
            if q2 not in ["-", "Maruška"]: dej_vypinac()
            if st.session_state.get("q2_done"):
                st.success("Super!")
                q3 = st.selectbox("Co má František nejraději?", ["-", "Grilovačky", "Grilovánky"], key="q3", on_change=pricti_body, args=("q3", "Grilovánky"))
                if q3 not in ["-", "Grilovánky"]: dej_vypinac()
                if st.session_state.get("q3_done"):
                    st.success("Správně!")
                    q4 = st.selectbox("Co vše musíme dát do salátu", ["-", "sůl,ocet,cukr", "ocet,sůl,cukr krystal"], key="q4", on_change=pricti_body, args=("q4", "sůl,ocet,cukr"))
                    if q4 not in ["-", "sůl,ocet,cukr"]: dej_vypinac()

    # --- PEXESO ---
    elif st.session_state.pravy_vyber == "pexeso":
        st.title("🧩 Pexeso (František edition)")
        if "karty" not in st.session_state or len(st.session_state.karty) != 8:
            st.session_state.karty = ["🍎", "🍎", "🐱", "🐱", "🐶", "🐶", "🐭", "🐭"]
            random.shuffle(st.session_state.karty)
            st.session_state.odkryto = [False] * 8
            st.session_state.vybrane = []
        
        if st.button("Reset Pexeso"): 
            st.session_state.pexeso_hotovo = False
            del st.session_state.karty
            st.rerun()

        if st.session_state.pexeso_hotovo:
            st.balloons()
            st.success("GRATULUJI! Vyřešil jsi pexeso pro malé žebráky, vyhráváš mixér!")
        else:
            for row in range(0, 8, 4):
                cols = st.columns(4)
                for i in range(4):
                    idx = row + i
                    label = st.session_state.karty[idx] if st.session_state.odkryto[idx] else "❓"
                    if cols[i].button(label, key=f"p_{idx}"):
                        if not st.session_state.odkryto[idx]:
                            if len(st.session_state.vybrane) == 2:
                                st.session_state.odkryto[st.session_state.vybrane[0]] = False
                                st.session_state.odkryto[st.session_state.vybrane[1]] = False
                                st.session_state.vybrane = []
                            st.session_state.odkryto[idx] = True
                            st.session_state.vybrane.append(idx)
                            if len(st.session_state.vybrane) == 2:
                                idx1, idx2 = st.session_state.vybrane
                                if st.session_state.karty[idx1] == st.session_state.karty[idx2]: 
                                    st.session_state.vybrane = []
                                    if all(st.session_state.odkryto):
                                        st.session_state.pexeso_hotovo = True
                                        st.session_state.body = 40
                                        st.rerun()
                            st.rerun()

    # --- DOMŮ ---
    else:
        if st.session_state.get("pexeso_hotovo", False):
            st.error("DOMŮ je prázdné... všechno jsi vyřešil, tak tady nic není!")
        else:
            jmeno = st.text_input("Jak se jmenuješ?", key="in_jmeno")
            vek = st.number_input("Kolik je ti let?", 0, 120, 25, key="in_vek")
            if st.button("Vyhodnotit", key="btn_vyhodnotit"):
                if vek > 20:
                    st.success(f"Ahoj {jmeno}! Tady máš kočku:")
                    st.image("https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600", caption="Tvoje odměna!")
                else:
                    st.warning("Na kočku jsi moc mladý, Rytmus ti dá vypínačku!")
                    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8s0kQKci68L9t_hQ4sbMIKCo_hcka3XI6Of_2Z3YGyA&s=10")
            
            inteligence = st.number_input("Kolik máš IQ?", 0, 200, 25, key="in_iq")
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
