import streamlit as st
import pandas as pd
import requests

SOFASCORE_LIVE_URL = "https://www.sofascore.com/api/v1/sport/football/events/live"
st.set_page_config(page_title="Diagnóstico Sofascore Live")
st.title("Diagnóstico: mostrando TODOS los partidos en vivo desde Sofascore")

def get_all_live_sofa():
    response = requests.get(SOFASCORE_LIVE_URL)
    data = response.json()
    events = data.get("events", [])
    st.write("Datos RAW de partidos Sofascore:", events)  # 👈 Muestra el JSON completo
    partidos = []
    for ev in events:
        try:
            home_team = ev["homeTeam"]["name"]
            away_team = ev["awayTeam"]["name"]
            halftime_home = ev["homeScore"].get("period1", None)
            halftime_away = ev["awayScore"].get("period1", None)
            minuto = ev.get("time", {}).get("current", "--")
            estado = ev.get("status", {}).get("type", "")
            cuota1 = ev.get("markets", [{}])[0].get("outcomes", [{}])[0].get("odds", None)  # solo si existe este campo; puede ser None
            partidos.append({
                "Partido": f"{home_team} vs {away_team}",
                "Marcador HT": f"{halftime_home}-{halftime_away}",
                "Minuto": minuto,
                "Estado": estado,
                "Cuota 1": cuota1  # muestra la info si existe para debug
            })
        except Exception:
            pass
    return pd.DataFrame(partidos)

if st.button("Refrescar todos los partidos LIVE Sofascore"):
    df = get_all_live_sofa()
else:
    df = get_all_live_sofa()

if not df.empty:
    st.dataframe(df)
else:
    st.info("No hay partidos en vivo o no se recibieron datos.")

st.caption("Revisa los datos crudos y la tabla para ver todos los partidos live en Sofascore y cómo aparecen los campos.")
