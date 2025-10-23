import streamlit as st
import pandas as pd
import requests

SOFASCORE_LIVE_URL = "https://www.sofascore.com/api/v1/sport/football/events/live"
st.set_page_config(page_title="Live Football Bet Finder — Sofascore")
st.title("Live: Doble Oportunidad Local-Empate (SOFASCORE Real Time Data)")

def get_live_matches_sofa():
    try:
        response = requests.get(SOFASCORE_LIVE_URL)
        data = response.json()
        events = data.get("events", [])
        
        # Mostrar estructura RAW para diagnóstico
        st.write("Ejemplo de JSON Sofascore:")
        if events:
            st.write(events[0])  # Solo muestra el primer partido para no saturar el dashboard
        else:
            st.info("No hay partidos live en este momento.")

        partidos = []
        for ev in events:
            try:
                home_team = ev["homeTeam"]["name"]
                away_team = ev["awayTeam"]["name"]
                # Diagnóstico: muestra en la app los campos principales de cada partido
                st.write(f"{home_team} vs {away_team}")
                st.json(ev)
                # --- Filtrado básico, debe ser ajustado cuando veas los datos reales ---
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
                        })
            except Exception as e:
                st.warning(f"Error leyendo partido: {e}")
        return pd.DataFrame(partidos)
    except Exception as e:
        st.warning(f"Error al obtener datos de Sofascore: {e}")
        return pd.DataFrame(columns=["Partido", "Marcador HT", "Minuto", "Estado"])

st.write("Partidos donde el local va ganando al descanso. (Mira los datos en vivo y ajusta el filtrado según los campos, puedes copiar los nombres exactos desde la visualización para mejorar el filtro).")

if st.button("Refrescar datos"):
    partidos = get_live_matches_sofa()
else:
    partidos = get_live_matches_sofa()

if not partidos.empty:
    st.dataframe(partidos)
else:
    st.info("No hay partidos que cumplan el criterio en este momento.")

st.info("Puedes copiar aquí los campos relevantes del JSON para afinar el filtro.")
