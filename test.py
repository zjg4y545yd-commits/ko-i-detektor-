import streamlit as st
import random
import json
import os
import pandas as pd
from datetime import date, datetime
import yfinance as yf

# 1. Nastavení stránky (musí být vždy na začátku)
st.set_page_config(layout="wide")
st.title("🐱 Kočičí detektor ti zmrde")

# --- ZÁZNAM NÁVŠTĚVNOSTI ---
SOUBOR = "navstevnost.json"
UKOLY_SOUBOR = "ukoly.json"
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

# --- FUNKCE PRO PERSISTENCI ÚKOLŮ ---
def nacti_ukoly():
    if os.path.exists(UKOLY_SOUBOR):
        with open(UKOLY_SOUBOR, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Výchozí data, pokud soubor ještě neexistuje
        return {
            "Jaroslav": [{"text": "Popsat důkazy k žalobě Nováka", "termin": "Dnes", "hotovo": False}],
            "Petr": [],
            "Natálie": [{"text": "Odeslat datovky soudu v Brně", "termin": "Zítra", "hotovo": False}],
            "Pavla": []
        }

def uloz_ukoly():
    with open(UKOLY_SOUBOR, "w", encoding="utf-8") as f:
        json.dump(st.session_state.ukoly, f, ensure_ascii=False, indent=4)

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

# Načtení úkolů ze souboru, aby přežily refresh stránky
if "ukoly" not in st.session_state:
    st.session_state.ukoly = nacti_ukoly()

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
    if st.button("NÁVŠTĚVNOST", use_container_width=True, key="btn_navstevnost"): st.session_state.pravy_vyber = "navstevnost"
    if st.button("PENÍZKY", use_container_width=True, key="btn_penizky"): st.session_state.pravy_vyber = "penizky"
    if st.button("PRO PRÁVNÍKY", use_container_width=True, key="btn_pravnici"): st.session_state.pravy_vyber = "pravnici"
    
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

    # --- NÁVŠTĚVNOST ---
    elif st.session_state.pravy_vyber == "navstevnost":
        st.title("📈 Návštěvnost stránky")
        st.write("Tady vidíš, kolik zoufalců sem už dneska a v minulých dnech zabloudilo.")
        
        df = pd.DataFrame(list(data_navstevnosti.items()), columns=['Datum', 'Počet návštěv'])
        df.set_index('Datum', inplace=True)
        
        st.bar_chart(df)
        st.success(f"Dneska tě tu navštívilo už {data_navstevnosti.get(dnes, 0)} lidí!")

    # --- PENÍZKY (AKCIE) ---
    elif st.session_state.pravy_vyber == "penizky":
        st.title("💸 Penízky (Akcie & Krypto)")
        st.write("Tady máš přehled trhu s inteligentními nákupními a prodejními cíli.")
        
        akcie_seznam = {
            "Nu Holdings": "NU",
            "Duolingo": "DUOL",
            "Nvidia": "NVDA",
            "Microsoft": "MSFT",
            "Apple": "AAPL",
            "Amazon": "AMZN",
            "Meta": "META",
            "SoFi Technologies": "SOFI",
            "Novo Nordisk": "NVO",
            "PayPal": "PYPL",
            "ASML Holding": "ASML",
            "Bitcoin": "BTC-USD"
        }
        
        doporuceni = {
            "Nu Holdings": "🟢 STRONG BUY (Tohle je jasná volba, sype to!)",
            "Duolingo": "🟢 BUY (Ta zelená sova tě jinak zabije, kup to)",
            "Nvidia": "🟢 STRONG BUY (AI boom, kupuj dokud to roste!)",
            "Microsoft": "🟢 BUY (Wall Street to miluje, stabilní jistota)",
            "Apple": "🟡 HOLD / Lehký BUY (Čeká se na další hračky od Tima Cooka)",
            "Amazon": "🟢 BUY (Jeff potřebuje další raketu, podpoř ho)",
            "Meta": "🟢 BUY (Zuck tě sice sleduje, ale peníze z toho jsou)",
            "SoFi Technologies": "🟢 BUY (Fintech pro mladé, tohle má velkou budoucnost)",
            "Novo Nordisk": "🟢 STRONG BUY (Ozempic vládne světu, lidstvo bude líné a tlusté pořád)",
            "PayPal": "🟡 HOLD (Stará klasika, uvidíme, jestli chytí druhý dech)",
            "ASML Holding": "🟢 STRONG BUY (Bez jejich mašin nikdo na světě nevyrobí pořádný čip)",
            "Bitcoin": "🟢 BUY (Čekáme na návrat k historickým maximům, ne?)"
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
                            
                            max_3m = hist['Close'].max()
                            min_3m = hist['Close'].min()
                            
                            nakup_pod = min_3m * 1.03
                            prodej_nad = max_3m * 0.97
                            
                            if cena_ted <= min_3m * 1.07:
                                teplomer = "🛒 VE SLEVĚ (Blízko 3měsíčního minima)"
                            elif cena_ted >= max_3m * 0.95:
                                teplomer = "🥵 DRAHÉ (Blízko 3měsíčního maxima)"
                            else:
                                teplomer = "⚖️ NEUTRÁLNÍ (Zlatá střední cesta)"
                            
                            st.metric(label="Aktuální cena", value=f"${cena_ted:.2f}", delta=f"{zmena_procenta:.2f} %")
                            st.write(f"🟢 **Kdy koupit (pod):** ${nakup_pod:.2f} | 🔴 **Kdy prodat (nad):** ${prodej_nad:.2f}")
                            st.markdown(f"**Teploměr trhu:** {teplomer}")
                            st.markdown(f"**Názor analytiků:** {doporuceni[nazev]}")
                            st.line_chart(hist['Close'])
                        else:
                            st.warning("Data nejsou momentálně dostupná.")
                    except Exception as e:
                        st.error("Nepodařilo se načíst data z burzy.")
            
            nazev1, ticker1 = polozky[i]
            vykresli_akcii(cols[0], nazev1, ticker1)
            
            if i + 1 < len(polozky):
                nazev2, ticker2 = polozky[i+1]
                vykresli_akcii(cols[1], nazev2, ticker2)
            
            st.markdown("---")

    # --- PRO PRÁVNÍKY ---
    elif st.session_state.pravy_vyber == "pravnici":
        st.title("⚖️ Právnický koutek (Advokátní speciál)")
        st.write("Profesionální utility pro unavené advokáty a lidi, co se rádi soudí.")
        
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "⏱️ Kalkulačka lhůt", 
            "🔤 Překladač mluvy", 
            "📝 Předžalobní buchar", 
            "🎲 Justiční ruleta",
            "💸 Úroky z prodlení",
            "📋 Nástěnka úkolů",
            "📊 Přehled úkolů"
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
            st.caption("⚠️ **Upozornění pro koncipienty:** Pokud konec lhůty připadne na sobotu, neděli nebo svátek, posledním dnem lhůty je nejbližší příští pracovní den podle § 57 odst. 2 OSŘ. Neodkládejte to na poslední chvíli, vy lamy.")
            
        with tab2:
            st.subheader("Pasivně-agresivní překladač do soudní mluvy")
            
            myslenka = st.selectbox(
                "Co chceš protistraně nebo soudci reálně vzkázat?",
                [
                    "-",
                    "Je to totální idiot a kompletně si vymýšlí",
                    "Dluží mi prachy, nereaguje a dělá mrtvého brouka",
                    "Ta jeho práce stojí za hovno, je to celé nakřivo",
                    "Už mě neser, nebo tě poženu k soudu a zaplatíš i mýho právníka"
                ]
            )
            
            preklady = {
                "Je to totální idiot a kompletně si vymýšlí": 
                    "👉 *Tvrzení protistrany vykazují zřejmé známky argumentační nouze, jsou zcela účelová a v příkrém rozporu se skutečným stavem věci, což žalobce v následujících bodech prokáže listinnými důkazy.*",
                "Dluží mi prachy, nereaguje a dělá mrtvého brouka": 
                    "👉 *Žalovaný je dlouhodobě v prodlení se splněním svého peněžitého závazku. Na opakované mimosoudní předžalobní výzvy k plnění doručené do jeho datové schránky doposud nijak nereagoval.*",
                "Ta jeho práce stojí za hovno, je to celé nakřivo": 
                    "👉 *Předmět díla vykazuje zjevné statické, technické a estetické vady neodpovídající schválené projektové dokumentaci, platným technologickým postupům ani závazným normám ČSN.*",
                "Už mě neser, nebo tě poženu k soudu a zaplatíš i mýho právníka": 
                    "👉 *V případě, že ze strany žalovaného nedojde k okamžité nápravě tohoto protiprávního stavu, je můj klient nucen hájit svá legitimní práva soudní cestou, což pro žalovaného bude znamenat povinnost uhradit rovněž plné náklady nalézacího řízení.*"
            }
            
            if myslenka != "-":
                st.success(preklady[myslenka])

        with tab3:
            st.subheader("📝 Předžalobní výzva na jedno kliknutí")
            
            p_jmeno = st.text_input("Celé jméno / Název dlužníka:", "Jan Novák", key="pb_jmeno")
            p_adresa = st.text_input("Adresa / Sídlo dlužníka:", "Uliční 123, 110 00 Praha", key="pb_adresa")
            p_castka = st.number_input("Dlužná částka (Kč):", value=15000, key="pb_castka")
            p_duvod = st.text_input("Za co dluží (např. nezaplacená faktura, zpackaná práce):", "neuhrazené faktury za provedené služby", key="pb_duvod")
            
            if st.button("🚀 Vygenerovat Předžalobní výzvu", key="pb_generate"):
                text_vyzvy = f"""
                **PŘEDŽALOBNÍ VÝZVA K PLNĚNÍ**
                ve smyslu § 142a zákona č. 99/1963 Sb., občanský soudní řád (OSŘ)
                
                **VÝZVA TELNÍ:**
                **Žalovaný (Dlužník):** {p_jmeno}, nar. / IČO, bytem/se sídlem {p_adresa}
                
                Vážený pane / Vážená paní,
                
                tímto Vás formálně vyzývám k dobrovolnému splnění Vašeho dluhu ve výši **{p_castka:,.2f} Kč**, který vznikl z titulu: *{p_duvod}*.
                
                Uvedenou částku zašlete nejpozději do **7 dnů** od doručení této výzvy na účet věřitele.
                
                Pokud dluh v této lhůtě neuhradíte, berte na vědomí, že záležitost bude neprodleně předána věcně a místně příslušnému soudu k zahájení nalézacího řízení. V takovém případě budete povinen/povinna uhradit nejen jistinu dluhu a zákonný úrok z prodlení, ale rovněž veškeré náklady soudního řízení a právního zastoupení, které mohou mnohonásobně převýšit samotný původní dluh.
                
                Tato výzva představuje splnění zákonné podmínky pro přiznání náhrady nákladů řízení ve smyslu § 142a OSŘ.
                
                V Praze, dne {date.today().strftime('%d. %m. %Y')}
                """
                st.text_area("Zkopíruj si text:", value=text_vyzvy, height=350)
                st.success("Buchar vygenerován! Zkopíruj to, hoď do datovky a dlužník se posere.")
                
        with tab4:
            st.subheader("🎲 Věštírna: Jakou má dneska soudce náladu?")
            
            if st.button("🎰 Roztočit justiční ruletu", key="btn_ruleta"):
                vysledky = [
                    "⚖️ **Soudce má zítra dovolenou:** Všechno se naslepo odročuje. Můžeš jít domů, smůla.",
                    "⚖️ **Soudce se ráno pohádal se starou:** Dneska prohraješ i to, že je obloha modrá. Rychle stáhni žalobu a utíkej.",
                    "⚖️ **Těžká kocovina z plesu právníků:** Rozsudek bude mít 3 odstavce a nebude dávat smysl. Vyhrává ten, kdo u pultíku mluvil tišeji.",
                    "⚖️ **Dobrá nálada, sluníčko svítí:** Suverénně vyhraješ! ...Ale protistrana se odvolá a potáhne se to další 3 roky.",
                    "⚖️ **Soudce si zapomněl brýle:** Spoléhá jen na to, co mu nakecá zapisovatelka. Tvoje šance je přesně 50/50.",
                    "⚖️ **Zaujatost level 1000:** Protistrana má hezčího koncipienta. Tady končíš, sráči."
                ]
                st.warning(random.choice(vysledky))
                st.image("https://media.giphy.com/media/3o7TKSd0EA9zH0kS5q/giphy.gif", width=300)

        with tab5:
            st.subheader("💸 Kalkulačka zákonných úroků z prodlení")
            
            u_jistina = st.number_input("Dlužná jistina (Kč):", value=50000, step=1000, key="u_jistina")
            u_od = st.date_input("Počátek prodlení (první den po splatnosti):", date(2025, 1, 1), key="u_od")
            u_do = st.date_input("Konec prodlení (případně dnešní den):", date.today(), key="u_do")
            
            sazba_anual = 0.1325 
            
            if u_od < u_do:
                dny_prodleni = (u_do - u_od).days
                vypocteny_urok = u_jistina * sazba_anual * (dny_prodleni / 365.0)
                celkem_s_urokem = u_jistina + vypocteny_urok
                
                st.info(f"Počet dní v prodlení: **{dny_prodleni} dní**")
                st.metric(label="Vypočtený zákonný úrok", value=f"{vypocteny_urok:,.2f} Kč")
                st.metric(label="Celková pohledávka s úrokem", value=f"{celkem_s_urokem:,.2f} Kč")
            else:
                st.error("Chyba: Počátek prodlení musí být dříve než konec prodlení.")

        with tab6:
            st.subheader("📋 Manažer lidských zdrojů (Úkolníček)")
            st.write("Vyber si oběť a přiřaď jí práci. Ať se v té kanceláři neflákají.")
            
            col_z_roleta, col_z_mezera = st.columns([1, 2])
            with col_z_roleta:
                vybrany_makac = st.selectbox("Vyber člověka:", ["Jaroslav", "Petr", "Natálie", "Pavla"])
            
            st.markdown(f"### Úkoly pro osobu: **{vybrany_makac}**")
            
            # Formulář pro přidání úkolu
            with st.form(key=f"form_ukol_{vybrany_makac}"):
                c1, c2 = st.columns([3, 1])
                novy_ukol_text = c1.text_input("Zadej nový úkol:")
                novy_ukol_termin = c2.selectbox("Termín dodání:", ["Dnes", "Zítra", "Tento týden", "Příští týden"])
                
                if st.form_submit_button("Přidat úkol"):
                    if novy_ukol_text.strip() != "":
                        st.session_state.ukoly[vybrany_makac].append({
                            "text": novy_ukol_text, 
                            "termin": novy_ukol_termin, 
                            "hotovo": False
                        })
                        uloz_ukoly()  # Zápis do souboru
                        st.success(f"Úkol pro {vybrany_makac} byl přidán!")
                        st.rerun()
                    else:
                        st.warning("Musíš ten úkol nejdřív napsat, prázdný formulář jim práci nepřidá.")
            
            st.markdown("---")
            
            # Správa a zobrazení úkolů pro vybraného makače (přesunuto správně do tab6)
            if not st.session_state.ukoly[vybrany_makac]:
                st.info(f"Uf, {vybrany_makac} má prázdný stůl. Asi čas mu hodit další spis.")
            else:
                for idx, ukol in enumerate(st.session_state.ukoly[vybrany_makac]):
                    uc1, uc2, uc3 = st.columns([0.1, 0.7, 0.2])
                    
                    # Checkbox pro odškrtnutí
                    je_hotovo = uc1.checkbox("", value=ukol["hotovo"], key=f"chk_{vybrany_makac}_{idx}")
                    
                    # Logika uložení stavu
                    if je_hotovo != ukol["hotovo"]:
                        st.session_state.ukoly[vybrany_makac][idx]["hotovo"] = je_hotovo
                        uloz_ukoly()  # Zápis do souboru při odškrtnutí
                        st.rerun()
                    
                    # Zobrazení textu a termínu
                    if je_hotovo:
                        uc2.markdown(f"~~{ukol['text']}~~")
                        uc3.caption(f"~~🗓️ {ukol['termin']}~~ ✅")
                    else:
                        uc2.markdown(f"**{ukol['text']}**")
                        
                        # Barevný indikátor u termínu
                        if ukol["termin"] == "Dnes":
                            uc3.error(f"🗓️ {ukol['termin']}")
                        elif ukol["termin"] == "Zítra":
                            uc3.warning(f"🗓️ {ukol['termin']}")
                        else:
                            uc3.info(f"🗓️ {ukol['termin']}")

                # Tlačítko na vyčištění hotových úkolů
                st.markdown("")
                if st.button(f"🗑️ Smazat hotové úkoly ({vybrany_makac})", key=f"btn_smazat_{vybrany_makac}"):
                    puvodni_pocet = len(st.session_state.ukoly[vybrany_makac])
                    st.session_state.ukoly[vybrany_makac] = [u for u in st.session_state.ukoly[vybrany_makac] if not u["hotovo"]]
                    uloz_ukoly()  # Zápis do souboru po promazání
                    
                    if puvodni_pocet > len(st.session_state.ukoly[vybrany_makac]):
                        st.rerun()
                    else:
                        st.warning("Nejsou tu žádné hotové úkoly ke smazání.")

        with tab7:
            st.subheader("📊 Přehled všech úkolů pro tým")
            st.write("Kompletní tabulka rozdělených úkolů napříč celou advokátní kanceláří.")
            
            # Transformace slovníku úkolů na plochý list pro Pandas DataFrame
            vsechny_ukoly_list = []
            for jmeno, ukoly_seznam in st.session_state.ukoly.items():
                for u in ukoly_seznam:
                    vsechny_ukoly_list.append({
                        "Osoba": jmeno,
                        "Zadání úkolu": u["text"],
                        "Termín plnění": u["termin"],
                        "Stav": "✅ Hotovo" if u["hotovo"] else "⏳ Čeká"
                    })
            
            if vsechny_ukoly_list:
                df_ukoly = pd.DataFrame(vsechny_ukoly_list)
                
                # Funkce pro stylování barev jmen v tabulce podle tvého původního klíče
                def obarvi_jmena(val):
                    barvy = {
                        "Jaroslav": "color: #1f77b4; font-weight: bold;", # Modrá
                        "Petr": "color: #d62728; font-weight: bold;",     # Červená
                        "Natálie": "color: #2ca02c; font-weight: bold;",  # Zelená
                        "Pavla": "color: #ff7f0e; font-weight: bold;"     # Oranžová
                    }
                    return barvy.get(val, "color: black;")
                
                # Aplikace stylů na sloupec "Osoba"
                styled_df = df_ukoly.style.map(obarvi_jmena, subset=["Osoba"])
                
                # Vykreslení krásné grafické tabulky roztažené na šířku
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
            else:
                st.info("Aktuálně nejsou v celém týmu zadány žádné úkoly. Všichni mají čistý stůl!")

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
