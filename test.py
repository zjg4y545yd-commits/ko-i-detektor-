import streamlit as st

st.title("🐱 Kočičí detektor ti zmrde")

# 1. Zadáme jméno
jmeno = st.text_input("Jak se jmenuješ?")

# 2. Zadáme věk (výchozí hodnotu dáme schválně na 25, aby to rovnou prošlo)
vek = st.number_input("Kolik je ti let?", min_value=0, max_value=120, value=25)

if st.button("Vyhodnotit"):
    if vek > 20:
        st.success(f"Ahoj {jmeno}! Je ti víc než 20 ty stará vraždo, tak tady máš slíbenou kočku:")
        # Nový, stabilní odkaz na kočku z Unsplashe
        st.image("https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600", caption="Tvoje odměna ty sráči posranej! 🐱")
        st.image("https://images.unsplash.com/photo-1543852786-1cf6624b9987?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGNhdHxlbnwwfHwwfHx8MA%3D%3D", caption="Tvoje odměna ty sráči posranej! 🐱")
    else:
        st.warning(f"Ahoj {jmeno}, je ti jen {vek}. To je na kočku ještě málo, teď ti Rytmus napálí vypínačku ")
        st.image ("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8s0kQKci68L9t_hQ4sbMIKCo_hcka3XI6Of_2Z3YGyA&s=10")
        
# 3. Zadáme inteligenci
inteligence = st.number_input("Kolik máš IQ ty konino", min_value=0, max_value=200, value=25)
if st.button("test"):
    if inteligence > 20:
        st.success(f"Ahoj {jmeno}! Jsi chytřejší jak labrador, gratuluji!")
