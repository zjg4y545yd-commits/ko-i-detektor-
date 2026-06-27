import streamlit as st
import random
import json
import os
import pandas as pd
from datetime import date, datetime, timedelta
import yfinance as yf
import calendar

# 1. Nastavení stránky (musí být vždy na začátku)
st.set_page_config(layout="wide")
st.title("🐱 Kočičí detektor ti zmrde")

# --- ZÁZNAM NÁVŠTĚVNOSTI A SOUBORY ---
SOUBOR = "navstevnost.json"
UKOLY_SOUBOR = "ukoly.json"
KLIMATIZACE_SOUBOR = "klimatizace.json"
dnes = str(date.today())

def nacti_nebo_vytvor_data():
    if os.path.exists(SOUBOR):
        with open(SOUBOR, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "2026-06-12": 15,
            "2026-06-13": 42,
            "2026-06-14": 28,
            "2026-06-15": 73
        }

def nacti_ukoly():
    if os.path.exists(UKOLY_SOUBOR):
        with open(UKOLY_SOUBOR, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "Jaroslav": [{"text": "Popsat důkazy k žalobě Nováka", "termin": "18. 06. 2026", "hotovo": False}],
            "Petr": [],
            "Natálie": [{"text": "Odeslat datovky soudu v Brně", "termin": "20. 06. 2026", "hotovo": False}],
            "Pavla": []
        }

def uloz_ukoly():
    with open(UKOLY_SOUBOR, "w", encoding="utf-8") as f:
        json.dump(st.session_state.ukoly, f, ensure_ascii=False, indent=4)

def nacti_klimatizace():
    if os.path.exists(KLIMATIZACE_SOUBOR):
        with open(KLIMATIZACE_SOUBOR, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def uloz_klimatizace(data):
    with open(KLIMATIZACE_SOUBOR, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data_navstevnosti = nacti_nebo_vytvor_data()

# 2. Inicializace stavu
if "zapoteno" not in st.session_state:
    data_navstevnosti[dnes] = data_navstevnosti.get(dnes, 0) + 1
    with open(SOUBOR, "w", encoding="utf-8") as f:
        json.dump(data_navstevnosti, f)
    st.session_state.zapoteno = True

if "pravy_vyber" not in st.session_state: st.session_state.pravy_vyber = None
if "body" not in st.session_state: st.session_state.body = 0
if "pexeso_hotovo" not in st.session_state: st.session_state.pexeso_hotovo = False

if "ukoly" not in st.session_state:
    st.session_state.ukoly = nacti_ukoly()
if "klimatizace" not in st.session_state:
    st.session_state.klimatizace = nacti_klimatizace()

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
    if st.button("KLIMATIZACE", use_container_width=True, key="btn_klima"): st.session_state.pravy_vyber = "klima"
    if st.button("KLIMATIZACE EDITACE", use_container_width=True, key="btn_klima_edit"): st.session_state.pravy_vyber = "klima_edit"
    if st.button("KALKULAČKA", use_container_width=True, key="btn_kalk"): st.session_state.pravy_vyber = "kocka1"
    if st.button("FRANTIŠEK ŘEDITEL", use_container_width=True, key="btn_frantisek"): st.session_state.pravy_vyber = "kocka2"
    if st.button("PEXESO", use_container_width=True, key="btn_pexeso"): st.session_state.pravy_vyber = "pexeso"
    if st.button("NÁVŠTĚVNOST", use_container_width=True, key="btn_navstevnost"): st.session_state.pravy_vyber = "navstevnost"
    if st.button("PENÍZKY", use_container_width=True, key="btn_penizky"): st.session_state.pravy_vyber = "penizky"
    if st.button("AKCIE 2.0 🚀", use_container_width=True, key="btn_akcie2"): st.session_state.pravy_vyber = "akcie2"
    if st.button("PRO PRÁVNÍKY", use_container_width=True, key="btn_pravnici"): st.session_state.pravy_vyber = "pravnici"
    
    st.markdown("---")
    st.subheader(f"Tvoje body: {st.session_state.body}")
    if st.button("Resetovat body", key="btn_reset"):
        st.session_state.body = 0
        st.session_state.pexeso_hotovo = False
        for i in range(1, 5): st.session_state[f"q{i}_done"] = False
        st.rerun()

with left_col:
    # --- SEKCE: KLIMATIZACE (HLEDÁNÍ A PŘIDÁVÁNÍ) ---
    if st.session_state.pravy_vyber == "klima":
        st.header("❄️ Správa Klimatizací")
        st.write("Zadej ID štítku pro vyhledání nebo přidání klimatizace.")
        
        kod = st.text_input("ID štítku (např. 1, 2, ...):")
        
        if kod:
            if kod in st.session_state.klimatizace:
                info = st.session_state.klimatizace[kod]
                st.success(f"Nalezena jednotka: {info['model']}")
                
                try:
                    d_inst = datetime.strptime(info['datum_instalace'], '%Y-%m-%d').date()
                except ValueError:
                    d_inst = date.today()

                interval = info.get("interval_udrzby", 365)
                dalsi_servis = d_inst + timedelta(days=interval)
                zbyva = (dalsi_servis - date.today()).days
                
                stav = info.get("stav", "V provozu")
                st.info(f"**Aktuální stav:** {stav}")
                
                st.metric(f"Zbývá dní do údržby (Interval: {interval} dní)", f"{zbyva} dní")
                st.write(f"**Telefon zákazníka:** {info.get('telefon', '')}")
                st.write(f"**Poznámky/Filtry:** {info.get('pozn', '')}")
                st.write(f"**Údržba - chemie:** {info.get('udrzba_chemie', 'Neuvedeno')}")
                
                if zbyva <= 30:
                    st.warning("⚠️ Čas na servis! Je potřeba naplánovat údržbu.")
            else:
                st.info("Toto ID není v databázi. Vyplň údaje pro novou instalaci:")
                with st.form("nova_klima"):
                    model = st.text_input("Model zařízení")
                    tel = st.text_input("Telefon zákazníka")
                    pozn = st.text_area("Poznámky k instalaci / Filtry")
                    interval = st.number_input("Interval údržby (dny)", min_value=1, value=365)
                    chemie = st.text_input("Údržba - chemie (např. jaká chemie byla/bude použita)")

                    if st.form_submit_button("Uložit do databáze"):
                        st.session_state.klimatizace[kod] = {
                            "model": model, 
                            "telefon": tel, 
                            "pozn": pozn, 
                            "datum_instalace": str(date.today()),
                            "interval_udrzby": interval,
                            "udrzba_chemie": chemie,
                            "stav": "V provozu"
                        }
                        uloz_klimatizace(st.session_state.klimatizace)
                        st.success("Klimatizace uložena!")
                        st.rerun()

    # --- SEKCE: KLIMATIZACE EDITACE (PŘEHLED A ÚPRAVY) ---
    elif st.session_state.pravy_vyber == "klima_edit":
        st.header("🛠️ Editace a přehled klimatizací")
        st.write("Zde vidíš všechny zaregistrované klimatizace. Můžeš libovolně upravovat data, poznámky, intervaly údržby nebo mazat (zadej heslo '1234').")
        
        if not st.session_state.klimatizace:
            st.info("Zatím nejsou v databázi žádné klimatizace.")
        else:
            for kod, info in list(st.session_state.klimatizace.items()):
                with st.expander(f"🆔 ID: {kod} | {info['model']} | Stav: {info.get('stav', 'V provozu')}"):
                    with st.form(f"edit_form_{kod}"):
                        c1, c2 = st.columns(2)
                        
                        with c1:
                            # Ošetření pro stará data bez správného formátu data
                            try:
                                akt_datum = datetime.strptime(info.get('datum_instalace', str(date.today())), '%Y-%m-%d').date()
                            except ValueError:
                                akt_datum = date.today()

                            nove_datum = st.date_input("Datum instalace", value=akt_datum)
                            novy_tel = st.text_input("Telefon", value=info.get('telefon', ''))
                            novy_pozn = st.text_area("Poznámky", value=info.get('pozn', ''))
                        
                        with c2:
                            novy_interval = st.number_input("Interval údržby (ve dnech)", min_value=1, value=info.get('interval_udrzby', 365))
                            nova_chemie = st.text_input("Údržba - chemie", value=info.get('udrzba_chemie', ''))
                            
                            aktualni_stav = info.get("stav", "V provozu")
                            moznosti = ["V provozu", "V procesu", "Hotovo"]
                            novy_stav = st.selectbox("Upravit stav servisu:", moznosti, index=moznosti.index(aktualni_stav) if aktualni_stav in moznosti else 0)
                            
                            heslo = st.text_input("Heslo (pro uložení/smazání):", type="password")
                        
                        btn1, btn2, btn3 = st.columns([1, 1, 2])
                        ulozit = btn1.form_submit_button("Uložit změny")
                        smazat = btn2.form_submit_button("🗑️ Smazat")
                        
                        if ulozit:
                            if heslo == "1234":
                                # Aktualizace slovníku
                                st.session_state.klimatizace[kod]["datum_instalace"] = str(nove_datum)
                                st.session_state.klimatizace[kod]["telefon"] = novy_tel
                                st.session_state.klimatizace[kod]["pozn"] = novy_pozn
                                st.session_state.klimatizace[kod]["interval_udrzby"] = novy_interval
                                st.session_state.klimatizace[kod]["udrzba_chemie"] = nova_chemie
                                st.session_state.klimatizace[kod]["stav"] = novy_stav
                                
                                uloz_klimatizace(st.session_state.klimatizace)
                                st.success("Záznam úspěšně aktualizován!")
                                st.rerun()
                            else:
                                st.error("❌ Špatné heslo pro uložení!")
                        
                        if smazat:
                            if heslo == "1234":
                                del st.session_state.klimatizace[kod]
                                uloz_klimatizace(st.session_state.klimatizace)
                                st.warning(f"Záznam ID {kod} byl kompletně smazán.")
                                st.rerun()
                            else:
                                st.error("❌ Špatné heslo pro smazání!")

    # --- PŮVODNÍ ZÁLOŽKY ---
    elif st.session_state.pravy_vyber == "kocka1":
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

    elif st.session_state.pravy_vyber == "navstevnost":
        st.title("📈 Návštěvnost stránky")
        st.write("Tady vidíš, kolik zoufalců sem už dneska a v minulých dnech zabloudilo.")
        
        df = pd.DataFrame(list(data_navstevnosti.items()), columns=['Datum', 'Počet návštěv'])
        df.set_index('Datum', inplace=True)
        
        st.bar_chart(df)
        st.success(f"Dneska tě tu navštívilo už {data_navstevnosti.get(dnes, 0)} lidí!")

    elif st.session_state.pravy_vyber == "penizky":
        st.title("💸 Penízky (Základní přehled)")
        st.write("Tady máš klasický přehled trhu. Pro pokročilou analytiku a nákupní signály přepni na AKCIE 2.0 🚀.")
        
        akcie_seznam = {
            "Nu Holdings": "NU", "Duolingo": "DUOL", "Nvidia": "NVDA", "Microsoft": "MSFT",
            "Apple": "AAPL", "Amazon": "AMZN", "Meta": "META", "SoFi": "SOFI",
            "Novo Nordisk": "NVO", "PayPal": "PYPL", "ASML": "ASML", "Bitcoin": "BTC-USD"
        }
        
        polozky = list(akcie_seznam.items())
        
        for i in range(0, len(polozky), 2):
            cols = st.columns(2)
            
            def vykresli_akcii(col, nazev, ticker):
                with col:
                    st.subheader(f"{nazev} ({ticker})")
                    try:
                        ticker_data = yf.Ticker(ticker)
                        hist = ticker_data.history(period="3mo")
                        if not hist.empty:
                            cena_ted = hist['Close'].iloc[-1]
                            cena_vcera = hist['Close'].iloc[-2] if len(hist) > 1 else cena_ted
                            zmena_procenta = ((cena_ted - cena_vcera) / cena_vcera) * 100
                            st.metric(label="Aktuální cena", value=f"${cena_ted:.2f}", delta=f"{zmena_procenta:.2f} %")
                            st.line_chart(hist['Close'])
                        else:
                            st.warning("Data nejsou dostupná.")
                    except:
                        st.error("Chyba z burzy.")
            
            vykresli_akcii(cols[0], polozky[i][0], polozky[i][1])
            if i + 1 < len(polozky):
                vykresli_akcii(cols[1], polozky[i+1][0], polozky[i+1][1])
            st.markdown("---")

    elif st.session_state.pravy_vyber == "akcie2":
        st.title("🚀 AKCIE 2.0 - Terminál na tisk peněz")
        st.write("Tohle je tvůj osobní nástroj pro hledání extrémních slev na trhu a budování bohatství.")

        analyzy_db = {
            "AAPL": {
                "nazev": "Apple Inc.",
                "kvartal": "Apple ukázal silné tržby ze služeb (Services), které kompenzují mírně pomalejší prodeje iPhonů v Číně. Zisk na akcii (EPS) překonal očekávání trhu.",
                "analytici": "Většina analytiků drží doporučení BUY. Líbí se jim masivní zpětné odkupy akcií (100 mld. USD) a schopnost generovat hotovost.",
                "plany": "Nasazení 'Apple Intelligence' (AI přímo v iOS), nové super-výkonné čipy a příprava na skládací iPhony. Důraz na předplatné a uzavřený ekosystém.",
                "rizika": "Regulace v EU a USA (antimonopolní úřady), závislost na prodejích v Číně a riziko, že uživatelé budou protahovat cyklus výměny starých iPhonů za nové.",
                "plusy": ["Nejvěrnější zákazníci na světě", "Obrovská hromada hotovosti", "Rostoucí vysokomaržové služby"],
                "minusy": ["Vysoká závislost na iPhonu", "Prémiové ocenění (je to drahé)"]
            },
            "MSFT": {
                "nazev": "Microsoft",
                "kvartal": "Naprostá dominance. Cloud Azure roste tempem přes 30 % díky AI službám. Tržby i zisky drtí veškerá očekávání Wall Street.",
                "analytici": "Téměř všichni říkají STRONG BUY. Považují Microsoft za nejbezpečnější sázku na umělou inteligenci na světě.",
                "plany": "Zpeněžit Copilot (AI) ve Windows a Office 365, ovládnout herní průmysl přes Xbox/Activision a sebrat Google podíl ve vyhledávání.",
                "rizika": "Úřady jim dýchají na krk kvůli monopolu. OpenAI (jejich hlavní AI partner) by mohlo narazit na technologický strop nebo interní problémy.",
                "plusy": ["Naprostý monopol v korporátním softwaru", "Nejlepší integrace AI (Copilot)", "Diverzifikace (Cloud, PC, Hry)"],
                "minusy": ["Extrémně vysoká cena akcie (naceněno na dokonalost)"]
            },
            "META": {
                "nazev": "Meta Platforms (Facebook)",
                "kvartal": "Reklamní mašina šlape na 100 %. Tržby vyletěly nahoru díky AI cílení reklam. Firma navíc poprvé v historii začala vyplácet dividendu.",
                "analytici": "BUY. Wall Street miluje Zuckův 'Rok efektivity' (propouštění) a skutečnost, že z Instagramu a WhatsAppu ždímají maximum.",
                "plany": "Investice miliard do open-source AI (model Llama) a brýlí pro virtuální realitu. Chtějí ovládnout reklamní AI trh a metaverse.",
                "rizika": "Pálení desítek miliard dolarů v divizi Reality Labs (Metaverse), která je těžce ztrátová. Regulace sociálních sítí (TikTok konkurence).",
                "plusy": ["Nejlepší algoritmy na reklamu na světě", "Miliardy aktivních uživatelů", "Levnější valuace než u ostatních Big Tech"],
                "minusy": ["Zuckerbergova tvrdohlavost s Metaversem", "Náchylné na makroekonomiku (když firmy šetří, škrtají reklamu)"]
            },
            "AMZN": {
                "nazev": "Amazon",
                "kvartal": "Maloobchod se vrátil k ziskovosti díky optimalizaci doručování. Cloud AWS konečně po pauze opět akceleruje svůj růst.",
                "analytici": "STRONG BUY. Vidí obrovský potenciál ve zvyšování marží a v integraci AI do jejich cloudového byznysu.",
                "plany": "Automatizace skladů pomocí robotů, expanze zdravotnických služeb (Amazon Pharmacy) a vývoj vlastních AI čipů pro cloud AWS.",
                "rizika": "Ochlazení spotřebitelské poptávky kvůli inflaci, hrozba odborů mezi zaměstnanci skladů a útoky levné čínské konkurence (Temu, Shein).",
                "plusy": ["Dominance v cloudu (AWS) i e-commerce", "Nesmírně silný program Amazon Prime", "Zlepšující se ziskovost"],
                "minusy": ["Maloobchod má přirozeně strašně nízké marže"]
            },
            "NU": {
                "nazev": "Nu Holdings (Nubank)",
                "kvartal": "Raketový růst. Získávají miliony nových zákazníků měsíčně a čistý zisk roste exponenciálně.",
                "analytici": "BUY. Jde o nejlepší finanční technologii v Latinské Americe s podporou Warrena Buffetta.",
                "plany": "Masivní expanze z Brazílie do Mexika a Kolumbie. Nabízet více ziskové produkty (půjčky, kreditky) stávajícím uživatelům.",
                "rizika": "Měnové riziko (oslabení brazilského realu) a riziko nárůstu nesplácených půjček, pokud přijde v Latinské Americe ekonomická krize.",
                "plusy": ["Extrémní růst a škálovatelnost", "Nízké náklady na získání zákazníka", "Narušení starých zkostnatělých bank"],
                "minusy": ["Riziko rozvojových trhů", "Vysoké očekávání na další růst"]
            },
            "ASML": {
                "nazev": "ASML Holding",
                "kvartal": "Krátkodobý mírný pokles objednávek, ale výhled na rok 2025 je extrémně silný díky stavbě nových továren na čipy po celém světě.",
                "analytici": "STRONG BUY. ASML má absolutní monopol na výrobu strojů, bez kterých by žádné AI neexistovalo.",
                "plany": "Zavádění nové generace High-NA EUV litografie, která umožní vyrábět ještě menší a výkonnější čipy než 2nm.",
                "rizika": "Geopolitika! USA a Evropa jim zakazují prodávat ty nejlepší stroje do Číny, což zraňuje jejich tržby.",
                "plusy": ["Doslova světový technologický monopol", "Podpora megatrendu umělé inteligence"],
                "minusy": ["Politická a obchodní válka mezi USA a Čínou"]
            },
            "SOFI": {
                "nazev": "SoFi Technologies",
                "kvartal": "Konečně dosáhli čistého zisku (GAAP). Silně rostou depozita a počet uživatelů se zvyšuje navzdory špatným úrokovým sazbám.",
                "analytici": "HOLD / Lehký BUY. Banka pro mladé se sice lepší, ale valuace je pořád divoká a trh k ní přistupuje obezřetně.",
                "plany": "Stát se 'AWS pro fintech' pomocí platformy Galileo. Křížově prodávat víc produktů (hypotéky, investice) jednomu uživateli.",
                "rizika": "Riziko nesplácení studentských a osobních půjček. Vysoké úrokové sazby jim prodražují financování.",
                "plusy": ["Super moderní appka pro mladé", "Vlastní bankovní licence", "Rostoucí zisky"],
                "minusy": ["Pořád je to vysoce riziková a hodně 'shortovaná' akcie"]
            },
            "NVO": {
                "nazev": "Novo Nordisk",
                "kvartal": "Naprosté šílenství. Lidé vykupují léky na hubnutí (Wegovy) a cukrovku (Ozempic) tak rychle, že je nestíhají vyrábět. Zisky rostou raketově.",
                "analytici": "STRONG BUY, i když už je to drahé. Poptávka je tak velká, že převyšuje nabídku.",
                "plany": "Nákup nových továren pro zvýšení výroby a vývoj pilulkové formy (místo injekcí), což zdesetinásobí trh.",
                "rizika": "Konkurence od Eli Lilly (Zepbound) a velký politický tlak na snížení cen těchto léků pro pacienty.",
                "plusy": ["Produkt, který doslova mění svět a zdraví", "Gigantické marže", "Zákazník musí brát léky dlouhodobě"],
                "minusy": ["Cena akcie je už vyhnaná do nebes"]
            },
            "PYPL": {
                "nazev": "PayPal",
                "kvartal": "Tržby solidní, ale trh zklamal slabší výhled ziskové marže. Braintree (B2B platby) rostou, ale málo na nich vydělávají.",
                "analytici": "HOLD. Čekají, jestli nový CEO (Alex Chriss) dokáže firmu reálně nakopnout a zastavit pokles podílu na trhu.",
                "plany": "Nasazení AI do checkoutu, funkce 'Fastlane' pro placení bez hesel a lepší monetizace platformy Venmo.",
                "rizika": "Brutální konkurence ze všech stran (Apple Pay, Google Pay, Stripe, Adyen). Lidé od PayPalu odcházejí k modernějším řešením.",
                "plusy": ["Pořád je to obří dojná kráva na cash", "Valuace je extrémně levná", "Silný nový management"],
                "minusy": ["Ztrácí lesk a monopolní pozici v placení"]
            },
            "DUOL": {
                "nazev": "Duolingo",
                "kvartal": "Firma rozbila očekávání. Denní uživatelé a předplatitelé vyrostli meziročně o desítky procent.",
                "analytici": "BUY. Aplikace má extrémní retenční rate (lidé se vrací každý den, aby nepřišli o 'streak').",
                "plany": "Zpoplatnění 'Duolingo Max' (AI konverzace) a velká expanze výuky matematiky a hudby do jedné jediné appky.",
                "rizika": "Umělá inteligence. Pokud začnou lidé používat na překlady a učení přímo ChatGPT, appka ztratí smysl. Plus je aktuálně velmi drahá.",
                "plusy": ["Geniální gamifikace učení", "Silná značka (zelená sova)", "Nízké náklady na marketing (virální)"],
                "minusy": ["Akcie je oceněna velmi vysoko", "AI hrozba"]
            }
        }

        st.markdown("### 💼 Tvoje aktuální držení (Zlatá vejce)")
        moje_portfolio = ["MSFT", "META", "AMZN", "NU", "ASML", "SOFI", "NVO", "PYPL", "DUOL"]
        
        if st.button("🔄 Načíst a analyzovat mé portfolio"):
            with st.spinner("Stahuji data z Wall Street, drž si klobouk..."):
                portfolio_data = []
                for t in moje_portfolio:
                    try:
                        tkr = yf.Ticker(t)
                        hist = tkr.history(period="1y")
                        if not hist.empty:
                            last_price = hist['Close'].iloc[-1]
                            max_52 = hist['Close'].max()
                            sleva = ((last_price - max_52) / max_52) * 100
                            portfolio_data.append({
                                "Symbol": t,
                                "Aktuální cena ($)": round(last_price, 2),
                                "Roční High ($)": round(max_52, 2),
                                "Sleva od maxima (%)": round(sleva, 2)
                            })
                    except:
                        pass
                        
                if portfolio_data:
                    df_port = pd.DataFrame(portfolio_data)
                    def color_sleva(val):
                        if val < -20: return 'color: #00ff00; font-weight: bold;'
                        elif val < -10: return 'color: #73d055; font-weight: bold;'
                        elif val > -5: return 'color: #ff4b4b; font-weight: bold;'
                        else: return 'color: white;'

                    styled_port = df_port.style.map(color_sleva, subset=['Sleva od maxima (%)'])
                    st.dataframe(styled_port, use_container_width=True, hide_index=True)
                    st.caption("💡 Zelená čísla znamenají, že je akcie aktuálně ve slevě oproti svému ročnímu maximu. Červená znamená, že je vyhnaná strašně vysoko.")

        st.markdown("---")
        st.markdown("### 🎯 Radar na příležitosti (Zadej libovolný ticker)")
        
        col_input, col_btn = st.columns([3, 1])
        hledany = col_input.text_input("Napiš symbol akcie (např. AAPL, TSLA, PLTR, GOOGL):").upper()
        
        if hledany:
            with st.spinner(f"Počítám signály pro {hledany}..."):
                try:
                    tkr_hledany = yf.Ticker(hledany)
                    hist_hledany = tkr_hledany.history(period="1y")
                    info = tkr_hledany.info
                    
                    if not hist_hledany.empty:
                        cena_ted = hist_hledany['Close'].iloc[-1]
                        max_1y = hist_hledany['Close'].max()
                        min_1y = hist_hledany['Close'].min()
                        
                        sma50 = hist_hledany['Close'].tail(50).mean()
                        sma200 = hist_hledany['Close'].tail(200).mean()
                        propad_od_maxima = ((cena_ted - max_1y) / max_1y) * 100
                        
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Aktuální cena", f"${cena_ted:.2f}", f"{propad_od_maxima:.2f}% od ATH")
                        c2.metric("SMA 50 (Krátkodobý trend)", f"${sma50:.2f}")
                        c3.metric("SMA 200 (Dlouhodobý trend)", f"${sma200:.2f}")
                        c4.metric("Roční minimum", f"${min_1y:.2f}")
                        
                        if cena_ted < sma200 and propad_od_maxima < -20:
                            verdikt = "🔥 **STRONG BUY (Krvavá sleva!)**"
                            taktika = "Kupuj okamžitě nebo rozděl nákup na dvě části. První teď za Market cenu, druhou limitním příkazem na ročním minimu."
                            st.success(verdikt)
                        elif cena_ted < sma50:
                            verdikt = "🛒 **BUY (Dobrý vstupní bod)**"
                            taktika = f"Nastav si nákupní příkaz na ${min_1y + (cena_ted - min_1y)*0.4:.2f}. Bude to perfektní nástup."
                            st.info(verdikt)
                        elif cena_ted > sma50 and propad_od_maxima > -5:
                            verdikt = "🥵 **HOLD / PŘEDRAŽENO (Nekupuj)**"
                            taktika = f"Neskákej teď do rozjetého vlaku. Čekej, až to spadne zpátky ke klouzavému průměru kolem ${sma50:.2f}."
                            st.error(verdikt)
                        else:
                            verdikt = "⚖️ **NEUTRÁLNÍ ZÓNA**"
                            taktika = f"Kup první menší várku teď a zbytek dořeď, až to klesne k podpoře na ${sma200:.2f}."
                            st.warning(verdikt)
                        
                        st.write(f"**Jakou zadat objednávku:** {taktika}")
                        st.line_chart(hist_hledany['Close'])
                        
                        st.markdown(f"---")
                        st.markdown(f"### 🕵️ Hloubkový fundamentální a AI rozbor pro: **{hledany}**")
                        
                        if hledany in analyzy_db:
                            data = analyzy_db[hledany]
                            st.write(f"*(Data načtena z tvé prémiové databáze zlatých vajec)*")
                            
                            st.markdown(f"**📊 Poslední kvartální výsledky**")
                            st.info(data["kvartal"])
                            
                            st.markdown(f"**🎯 Co na to říkají analytici**")
                            st.info(data["analytici"])
                            
                            col_l, col_r = st.columns(2)
                            with col_l:
                                st.markdown(f"**🚀 Plány do budoucna a zlepšení byznysu**")
                                st.success(data["plany"])
                                st.markdown(f"**✅ Plusy**")
                                for p in data["plusy"]: st.markdown(f"- {p}")
                            with col_r:
                                st.markdown(f"**⚠️ Rizika a aktuální ohrožení**")
                                st.error(data["rizika"])
                                st.markdown(f"**❌ Mínusy**")
                                for m in data["minusy"]: st.markdown(f"- {m}")
                        
                        else:
                            st.write(f"*(Automatická Live AI analýza z Wall Street pro neznámý ticker)*")
                            
                            rev_growth = info.get("revenueGrowth", "N/A")
                            profit_margin = info.get("profitMargins", "N/A")
                            if rev_growth != "N/A": rev_growth = f"{rev_growth*100:.1f} %"
                            if profit_margin != "N/A": profit_margin = f"{profit_margin*100:.1f} %"
                            
                            rec = info.get("recommendationKey", "Neznámé").upper()
                            target = info.get("targetMeanPrice", "N/A")
                            short_biz = info.get("longBusinessSummary", "Žádný popis byznysu nebyl nalezen.")[:400] + "..."
                            pe_ratio = info.get("trailingPE", "N/A")
                            
                            st.markdown(f"**📊 Rychlá zpráva z Wall Street**")
                            st.info(f"Firma aktuálně reportuje růst tržeb **{rev_growth}** a její zisková marže se pohybuje kolem **{profit_margin}**. Aktuální poměr ceny k zisku (P/E) je **{pe_ratio}**.")
                            
                            st.markdown(f"**🎯 Co na to říkají analytici**")
                            st.info(f"Konsenzus analytiků na burze je **{rec}**. Průměrná cílová cena pro následujících 12 měsíců je stanovena na **${target}**.")
                            
                            col_l, col_r = st.columns(2)
                            with col_l:
                                st.markdown(f"**🚀 O čem je tento byznys**")
                                st.success(short_biz)
                                st.markdown(f"**✅ Silné stránky (Odhad Wall Street)**")
                                if profit_margin != "N/A" and info.get("profitMargins", 0) > 0.15: st.markdown("- Vysoká ziskovost a hrubá marže")
                                st.markdown("- Zavedená a obchodovaná společnost")
                                if rec in ["BUY", "STRONG_BUY"]: st.markdown("- Instituce a fondy akcii doporučují")
                            with col_r:
                                st.markdown(f"**⚠️ Rizika**")
                                st.error("Neznámá společnost mimo tvé hlavní portfolio. Makroekonomické vlivy, úrokové sazby a inflace mohou ovlivnit výkonnost.")
                                st.markdown(f"**❌ Slabé stránky (Odhad Wall Street)**")
                                if pe_ratio != "N/A" and isinstance(pe_ratio, (int, float)) and pe_ratio > 30: st.markdown("- Akcie je velmi drahá (Vysoké P/E)")
                                st.markdown("- Závislost na aktuálním tržním sentimentu")

                    else:
                        st.error("Nepodařilo se mi najít data pro tento ticker. Napsal jsi ho správně? (Např. AAPL, META)")
                except Exception as e:
                    st.error("Něco se pokazilo. Zkontroluj, jestli je ticker správně.")

    elif st.session_state.pravy_vyber == "pravnici":
        st.title("⚖️ Právnický koutek (Advokátní speciál)")
        st.write("Profesionální utility pro unavené advokáty a lidi, co se rádi soudí.")
        
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "⏱️ Kalkulačka lhůt", 
            "🔤 Překladač mluvy", 
            "📝 Předžalobní buchar", 
            "🎲 Justiční ruleta",
            "💸 Úroky z prodlení",
            "📋 Nástěnka úkolů",
            "📊 Přehled úkolů",
            "📅 Kalendář úkolů"
        ])
        
        with tab1:
            st.subheader("Výpočet procesních lhůt")
            datum_doruceni = st.date_input("Datum doručení písemnosti / rozsudku:", date.today())
            
            typ_lhuty = st.selectbox(
                "Vyber typ lhůty:",
                [
                    "Odvolání v civilním řízení (OSŘ) - 15 dní",
                    "Odpor proti platebnímu rozkazu - 15 dní",
                    "Kasační stížnost (NSS) - 2 týdny",
                    "Žaloba proti správnímu rozhodnutí - 2 měsíce"
                ]
            )
            
            if "15 dní" in typ_lhuty:
                konecna_lhuta = datum_doruceni + pd.Timedelta(days=15)
            elif "2 týdny" in typ_lhuty:
                konecna_lhuta = datum_doruceni + pd.Timedelta(days=14)
            elif "2 měsíce" in typ_lhuty:
                konecna_lhuta = datum_doruceni + pd.Timedelta(days=61)
                
            st.info(f"Materiál musí být odeslán nejpozději dne: **{konecna_lhuta.strftime('%d. %m. %Y')}**")
            
        with tab2:
            st.subheader("Pasivně-agresivní překladač do soudní mluvy")
            myslenka = st.selectbox(
                "Co chceš protistraně nebo soudci reálně vzkázat?",
                ["-", "Je to totální idiot a kompletně si vymýšlí", "Dluží mi prachy, nereaguje a dělá mrtvého brouka", "Ta jeho práce stojí za hovno, je to celé nakřivo", "Už mě neser, nebo tě poženu k soudu a zaplatíš i mýho právníka"]
            )
            preklady = {
                "Je to totální idiot a kompletně si vymýšlí": "👉 *Tvrzení protistrany vykazují zřejmé známky argumentační nouze...*",
                "Dluží mi prachy, nereaguje a dělá mrtvého brouka": "👉 *Žalovaný je dlouhodobě v prodlení se splněním svého peněžitého závazku...*",
                "Ta jeho práce stojí za hovno, je to celé nakřivo": "👉 *Předmět díla vykazuje zjevné statické, technické a estetické vady...*",
                "Už mě neser, nebo tě poženu k soudu a zaplatíš i mýho právníka": "👉 *V případě, že nedojde k okamžité nápravě, je můj klient nucen hájit svá práva...*"
            }
            if myslenka != "-": st.success(preklady[myslenka])

        with tab3:
            st.subheader("📝 Předžalobní výzva na jedno kliknutí")
            p_jmeno = st.text_input("Celé jméno / Název dlužníka:", "Jan Novák", key="pb_jmeno")
            p_adresa = st.text_input("Adresa / Sídlo dlužníka:", "Uliční 123, 110 00 Praha", key="pb_adresa")
            p_castka = st.number_input("Dlužná částka (Kč):", value=15000, key="pb_castka")
            p_duvod = st.text_input("Za co dluží:", "neuhrazené faktury za provedené služby", key="pb_duvod")
            
            if st.button("🚀 Vygenerovat Předžalobní výzvu", key="pb_generate"):
                text_vyzvy = f"**PŘEDŽALOBNÍ VÝZVA K PLNĚNÍ**\nŽalovaný: {p_jmeno}, adresa: {p_adresa}\nČástka: {p_castka:,.2f} Kč\nDůvod: {p_duvod}"
                st.text_area("Zkopíruj si text:", value=text_vyzvy, height=150)
                st.success("Buchar vygenerován!")
                
        with tab4:
            st.subheader("🎲 Věštírna: Jakou má dneska soudce náladu?")
            if st.button("🎰 Roztočit justiční ruletu", key="btn_ruleta"):
                st.warning("⚖️ **Soudce si zapomněl brýle:** Tvoje šance je přesně 50/50.")

        with tab5:
            st.subheader("💸 Kalkulačka zákonných úroků z prodlení")
            u_jistina = st.number_input("Dlužná jistina (Kč):", value=50000, step=1000, key="u_jistina")
            u_od = st.date_input("Počátek prodlení:", date(2025, 1, 1), key="u_od")
            u_do = st.date_input("Konec prodlení:", date.today(), key="u_do")
            sazba_anual = 0.1325 
            if u_od < u_do:
                dny_prodleni = (u_do - u_od).days
                vypocteny_urok = u_jistina * sazba_anual * (dny_prodleni / 365.0)
                celkem_s_urokem = u_jistina + vypocteny_urok
                st.info(f"Počet dní v prodlení: **{dny_prodleni} dní**")
                st.metric(label="Vypočtený zákonný úrok", value=f"{vypocteny_urok:,.2f} Kč")
            else:
                st.error("Chyba data.")

        with tab6:
            st.subheader("📋 Manažer lidských zdrojů (Úkolníček)")
            col_z_roleta, col_z_mezera = st.columns([1, 2])
            with col_z_roleta:
                vybrany_makac = st.selectbox("Vyber člověka:", ["Jaroslav", "Petr", "Natálie", "Pavla"])
            
            st.markdown(f"### Úkoly pro osobu: **{vybrany_makac}**")
            with st.form(key=f"form_ukol_{vybrany_makac}"):
                c1, c2, c3 = st.columns([2, 1, 1])
                novy_ukol_text = c1.text_input("Zadej nový úkol:")
                novy_ukol_termin = c2.date_input("Termín dodání (kalendář):", value=date.today())
                heslo = c3.text_input("Ověřovací heslo:", type="password")
                
                if st.form_submit_button("Přidat úkol"):
                    if heslo == "1234":
                        if novy_ukol_text.strip() != "":
                            st.session_state.ukoly[vybrany_makac].append({
                                "text": novy_ukol_text, 
                                "termin": novy_ukol_termin.strftime('%d. %m. %Y'), 
                                "hotovo": False
                            })
                            uloz_ukoly()
                            st.success(f"Úkol pro {vybrany_makac} byl přidán!")
                            st.rerun()
                        else:
                            st.warning("Musíš ten úkol nejdřív napsat.")
                    else:
                        st.error("❌ Špatné heslo! Úkol nebyl přidán.")
            
            st.markdown("---")
            if not st.session_state.ukoly[vybrany_makac]:
                st.info(f"Uf, {vybrany_makac} má prázdný stůl.")
            else:
                for idx, ukol in enumerate(st.session_state.ukoly[vybrany_makac]):
                    uc1, uc2, uc3 = st.columns([0.1, 0.7, 0.2])
                    je_hotovo = uc1.checkbox("", value=ukol["hotovo"], key=f"chk_{vybrany_makac}_{idx}")
                    if je_hotovo != ukol["hotovo"]:
                        st.session_state.ukoly[vybrany_makac][idx]["hotovo"] = je_hotovo
                        uloz_ukoly()
                        st.rerun()
                    if je_hotovo:
                        uc2.markdown(f"~~{ukol['text']}~~")
                        uc3.caption(f"~~🗓️ {ukol['termin']}~~ ✅")
                    else:
                        uc2.markdown(f"**{ukol['text']}**")
                        uc3.info(f"🗓️ {ukol['termin']}")

                st.markdown("---")
                del_col1, del_col2 = st.columns([2, 1])
                smazat_heslo = del_col2.text_input("Heslo pro smazání:", type="password", key=f"del_heslo_{vybrany_makac}")
                if del_col1.button(f"🗑️ Smazat hotové úkoly ({vybrany_makac})", key=f"btn_smazat_{vybrany_makac}", use_container_width=True):
                    if smazat_heslo == "1234":
                        st.session_state.ukoly[vybrany_makac] = [u for u in st.session_state.ukoly[vybrany_makac] if not u["hotovo"]]
                        uloz_ukoly()
                        st.rerun()
                    else:
                        st.error("❌ Špatné heslo!")

        with tab7:
            st.subheader("📊 Přehled všech úkolů pro tým")
            vsechny_ukoly_list = []
            for jmeno, ukoly_seznam in st.session_state.ukoly.items():
                for u in ukoly_seznam:
                    vsechny_ukoly_list.append({
                        "Osoba": jmeno, "Zadání úkolu": u["text"], "Termín plnění": u["termin"],
                        "Stav": "✅ Hotovo" if u["hotovo"] else "⏳ Čeká"
                    })
            if vsechny_ukoly_list:
                df_ukoly = pd.DataFrame(vsechny_ukoly_list)
                def obarvi_jmena(val):
                    barvy = {"Jaroslav": "color: #d62728; font-weight: bold;", "Petr": "color: #1f77b4; font-weight: bold;", "Natálie": "color: #2ca02c; font-weight: bold;", "Pavla": "color: #ff7f0e; font-weight: bold;"}
                    return barvy.get(val, "color: black;")
                styled_df = df_ukoly.style.map(obarvi_jmena, subset=["Osoba"])
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
            else:
                st.info("Aktuálně nejsou zadány žádné úkoly.")

        with tab8:
            st.subheader("📅 Měsíční kalendářní přehled úkolů")
            teky = date.today()
            c_rok, c_mes = st.columns(2)
            vybrany_rok = c_rok.selectbox("Vyber rok:", [2025, 2026, 2027], index=1, key="cal_year")
            mesice_cz = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen", "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]
            vybrany_mesic_nazev = c_mes.selectbox("Vyber měsíc:", mesice_cz, index=teky.month-1, key="cal_month")
            vybrany_mesic = mesice_cz.index(vybrany_mesic_nazev) + 1
            
            tasks_by_day = {}
            for jmeno, ukoly_seznam in st.session_state.ukoly.items():
                for u in ukoly_seznam:
                    try:
                        d_part, m_part, y_part = u["termin"].split(".")
                        d, m, y = int(d_part.strip()), int(m_part.strip()), int(y_part.strip())
                        if y == vybrany_rok and m == vybrany_mesic:
                            if d not in tasks_by_day: tasks_by_day[d] = []
                            tasks_by_day[d].append((jmeno, u["text"], u["hotovo"]))
                    except: pass
            
            cal = calendar.Calendar(firstweekday=0)
            weeks = cal.monthdayscalendar(vybrany_rok, vybrany_mesic)
            html = "<table style='width:100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ddd; font-family: sans-serif;'><tr style='background-color: #f0f2f6; text-align: center; font-weight: bold;'>"
            for day_name in ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]: html += f"<th style='padding: 10px; border: 1px solid #ddd; color: #333;'>{day_name}</th>"
            html += "</tr>"
            
            barvy = {"Jaroslav": "#d62728", "Petr": "#1f77b4", "Natálie": "#2ca02c", "Pavla": "#ff7f0e"}
            for week in weeks:
                html += "<tr style='height: 120px; vertical-align: top;'>"
                for day in week:
                    if day == 0: html += "<td style='background-color: #fafafa; border: 1px solid #ddd;'></td>"
                    else:
                        is_today = (teky.day == day and teky.month == vybrany_mesic and teky.year == vybrany_rok)
                        bg = "#fffdf0" if is_today else "#ffffff"
                        html += f"<td style='background-color: {bg}; border: 1px solid #ddd; padding: 6px; overflow: hidden;'>"
                        if is_today: html += f"<div style='font-weight: bold; color: #ff4b4b; margin-bottom: 5px; font-size: 13px;'>{day} (Dnes)</div>"
                        else: html += f"<div style='font-weight: bold; margin-bottom: 5px; color: #444; font-size: 13px;'>{day}</div>"
                        if day in tasks_by_day:
                            for jmeno, text, hotovo in tasks_by_day[day]:
                                barva = barvy.get(jmeno, "black")
                                decor = "line-through" if hotovo else "none"
                                opacity = "0.4" if hotovo else "1.0"
                                html += f"<div style='color: {barva}; font-size: 11px; text-decoration: {decor}; opacity: {opacity}; margin-bottom: 3px; padding: 2px 4px; border-left: 3px solid {barva}; background: rgba(0,0,0,0.01); line-height: 1.2; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;' title='{jmeno}: {text}'><b>{jmeno[0]}:</b> {text}</div>"
                        html += "</td>"
                html += "</tr>"
            html += "</table>"
            st.markdown(html, unsafe_allow_html=True)

    else:
        if st.session_state.get("pexeso_hotovo", False):
            st.error("DOMŮ je prázdné... všechno jsi vyřešil!")
        else:
            jmeno = st.text_input("Jak se jmenuješ?", key="in_jmeno")
            vek = st.number_input("Kolik je ti let?", 0, 120, 25, key="in_vek")
            if st.button("Vyhodnotit", key="btn_vyhodnotit"):
                if vek > 20:
                    st.success(f"Ahoj {jmeno}! Tady máš kočku:")
                    st.image("https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600")
                else:
                    st.warning("Na kočku jsi moc mladý, Rytmus ti dá vypínačku!")
            
            inteligence = st.number_input("Kolik máš IQ?", 0, 200, 25, key="in_iq")
            if st.button("test", key="btn_iq"):
                if inteligence > 160: st.success(f"Ahoj {jmeno}! Jsi chytřejší jak labrador, gratuluji!")
                else: st.warning(f"Ahoj {jmeno}, tvoje IQ je tak zasraně v hajzlu, že nemám slov")
