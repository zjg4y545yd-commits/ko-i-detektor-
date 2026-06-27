import streamlit as st
import random
import json
import os
import pandas as pd
from datetime import date, datetime, timedelta
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from pyzbar.pyzbar import decode
import cv2

# --- NASTAVENÍ ---
st.set_page_config(layout="wide")
st.title("🐱 Kočičí detektor a Servisní manažer")

KLIMATIZACE_SOUBOR = "klimatizace.json"

# --- FUNKCE ---
def nacti_klimatizace():
    if os.path.exists(KLIMATIZACE_SOUBOR):
        with open(KLIMATIZACE_SOUBOR, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def uloz_klimatizace(data):
    with open(KLIMATIZACE_SOUBOR, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Inicializace
if "klimatizace" not in st.session_state:
    st.session_state.klimatizace = nacti_klimatizace()

# Třída pro čtení čárových kódů
class BarcodeTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        decoded = decode(img)
        if decoded:
            # Uložíme kód do session_state, aby ho aplikace viděla
            st.session_state.naskenovany_kod = decoded[0].data.decode("utf-8")
        return img

# --- ZÁLOŽKA KLIMATIZACE ---
def sekce_klimatizace():
    st.header("❄️ Správa Klimatizací")
    
    # Kamera s transformátorem
    webrtc_streamer(key="barcode_scanner", video_transformer_factory=BarcodeTransformer)
    
    # Logika zobrazení výsledku
    kod = ""
    if "naskenovany_kod" in st.session_state:
        st.info(f"Naskenovaný kód: {st.session_state.naskenovany_kod}")
        kod = st.session_state.naskenovany_kod
        if st.button("Vymazat sken"):
            del st.session_state.naskenovany_kod
            st.rerun()
    else:
        kod = st.text_input("Nebo zadej kód ručně:")
    
    if kod:
        if kod in st.session_state.klimatizace:
            info = st.session_state.klimatizace[kod]
            st.success(f"Nalezena jednotka: {info['model']}")
            
            d_inst = datetime.strptime(info['datum_instalace'], '%Y-%m-%d').date()
            zbyva = 365 - (date.today() - d_inst).days
            
            st.metric("Zbývá dní do čištění", f"{zbyva} dní")
            st.write(f"**Telefon:** {info['telefon']}")
            st.write(f"**Poznámka:** {info['pozn']}")
            
            if zbyva <= 30:
                st.warning("⚠️ Čas na servis!")
        else:
            st.write("Jednotka není v databázi. Přidej ji:")
            with st.form("nova_klima"):
                model = st.text_input("Typ klimatizace")
                tel = st.text_input("Telefon zákazníka")
                pozn = st.text_area("Poznámky")
                if st.form_submit_button("Uložit"):
                    st.session_state.klimatizace[kod] = {
                        "model": model, "telefon": tel, "pozn": pozn, "datum_instalace": str(date.today())
                    }
                    uloz_klimatizace(st.session_state.klimatizace)
                    st.success("Uloženo!")
                    st.rerun()

# --- MENU ---
left_col, right_col = st.columns([3, 1])
with right_col:
    if st.button("KLIMATIZACE"): st.session_state.sekce = "klima"
with left_col:
    if st.session_state.get("sekce") == "klima":
        sekce_klimatizace()
