import streamlit as st
import pandas as pd
import requests
from functools import reduce

SOFASCORE_LIVE_URL = "https://www.sofascore.com/api/v1/sport/football/events/live"
st.set_page_config(page_title="Combinada Live Football — SOLO Sofascore")
st.title("Combinada automática Local-Empate (1X) — Solo con datos Sofascore")

def get_live_matches_sofa():
    response = requests.get(SOFASCORE_LIVE_URL)
    data = response.json()
    events = data.get("events", [])
    partidos = []
    for ev in events:
        try:
            home_team = ev["homeTeam"]["name"]
            away_team = ev["awayTeam"]["name"]
            halftime_home = ev["homeScore"].get("period1", None)
            halftime_away = ev["awayScore"].get("period1", None)
            minuto = ev.get("time", {}).get("current", "--")
            estado = ev.get("status", {}).get("type", "")
            if halftime_home is not None and halftime_away is not None:
                if halftime_home > halftime_away:
                    partidos.append({
                        "Partido": f"{home_team} vs {away_team}",
                        "Marcador HT": f"{halftime_home}-{halftime_away}",
                        "Minuto": minuto,
                        "Estado": estado,
                        "Cuota 1": None,
                        "Cuota X": None,
                        "Cuota Doble Oportunidad 1X": None
                    })
        except Exception:
            pass
    return pd.DataFrame(partidos).head(3)

def calcular_cuota_1x(cuota_1, cuota_x):
    try:
        if cuota_1 and cuota_x:
            return round(1 / (1/cuota_1 + 1/cuota_x), 2)
        return None
    except Exception:
        return None

if st.button("Refrescar partidos Sofascore"):
    partidos = get_live_matches_sofa()
else:
    partidos = get_live_matches_sofa()

if not partidos.empty:
    st.write("Ingresa la cuota 'Local gana' (1) y 'Empate' (X) para cada partido, tomadas de Sofascore o tu casa de apuestas favorita:")
    for i, row in partidos.iterrows():
        cuota_1 = st.number_input(f"Cuota LOCAL gana (1) — {row['Partido']}", min_value=1.01, max_value=20.0, value=1.90, step=0.01, key=f"cuota1_{i}")
        cuota_x = st.number_input(f"Cuota EMPATE (X) — {row['Partido']}", min_value=1.01, max_value=20.0, value=3.20, step=0.01, key=f"cuotax_{i}")
        partidos.at[i, "Cuota 1"] = cuota_1
        partidos.at[i, "Cuota X"] = cuota_x
        partidos.at[i, "Cuota Doble Oportunidad 1X"] = calcular_cuota_1x(cuota_1, cuota_x)
    st.dataframe(partidos[["Partido","Marcador HT","Minuto","Cuota 1","Cuota X","Cuota Doble Oportunidad 1X"]])

    cuotas_combinadas = partidos["Cuota Doble Oportunidad 1X"].tolist()
    if all(cuotas_combinadas) and len(cuotas_combinadas) == 3:
        valor_combinada = reduce(lambda x, y: x*y, cuotas_combinadas)
        st.success(f"**Valor total de la combinada Local-Empate (1X): {valor_combinada:.2f}**")
    else:
        st.info("Ingresa ambas cuotas para calcular la doble oportunidad y el valor de la combinada.")
else:
    st.info("No hay partidos que cumplan el criterio en este momento.")

st.caption("La cuota doble oportunidad (1X) se estima usando las cuotas simples 'Local gana' y 'Empate'. Puedes copiar estos datos desde Sofascore o tu casa de apuestas favorita.")
