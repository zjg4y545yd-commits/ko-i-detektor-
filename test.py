import streamlit as st
import json
import os
from datetime import date

# Nastavení stránky musí být první příkaz
st.set_page_config(page_title="Umělecké kovářství", layout="wide")

# --- FUNKCE PRO UKLÁDÁNÍ TERMÍNŮ ---
SOUBOR_TERMINY = "terminy.json"

def nacti_terminy():
    if os.path.exists(SOUBOR_TERMINY):
        with open(SOUBOR_TERMINY, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def uloz_terminy(data):
    with open(SOUBOR_TERMINY, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "terminy" not in st.session_state:
    st.session_state.terminy = nacti_terminy()

# Vložení vlastního CSS pro kovářský vzhled (tapeta a tmavý design)
st.markdown("""
<style>
/* Nastavení tapety na pozadí celého webu */
.stApp {
    background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAUVBMVEV3d3f///9wcHCJiYnGxsZ0dHT19fWZmZltbW1ra2vPz8+2trabm5v5+fl7e3uAgIDs7OyioqKurq7f39/W1ta6urqoqKiQkJDj4+PBwcHc3NwKRuvRAAAC3UlEQVR4nO3Yy3baMBgAYSSQESY2lwAlvP+D1jaXGoa03cGJZpas5O9I+m0mwR6bPPtxXS83v6Y/vY/t7Nj8n8nnts0xphKKOc3rf5vUq5wmBZViWj5ulnuTXVuWyFDM++9NmnmBIn2x/fzG5JjKFOlK+eupSb149cpeWT48MZkVTdKhfMCk7F3SFzcPJsfiSbqdsr8zadpir9dRi+PYZBNfvZ53KLUjk5MnZygu/5isPDnncnU12eVXr+VdSturydRtci03Z5O12+RWnJ1Nlg6dW2l6NvHojIpVb1J5dEblXW/i1BnXv6JMwpfXyag0700OXiej0qo3mWsyrtUEpUaTx7phrMlDmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZME6YJ04RpwjRhmjBNmCZ
