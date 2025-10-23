import streamlit as st
import pandas as pd
import requests

SOFASCORE_LIVE_URL = "https://www.sofascore.com/api/v1/sport/football/events/live"

st.set_page_config(page_title="Live Football Bet Finder — Sofascore")
st.title("Live: Doble Oportunidad Local-Empate (SOFASCORE Real Time Data)")

def get_live_matches_sofa():
    try:
      def get_live_matches_sofa():
    response = requests.get("https://www.sofascore.com/api/v1/sport/football/events/live")
    data = response.json()
    events = data.get("events", [])
    
    # Ver la estructura RAW de los datos
    st.write("Eventos Sofascore raw:", events)
    
    partidos = []
    for ev in events:
        try:
            home_team = ev["homeTeam"]["name"]
            away_team = ev["awayTeam"]["name"]
            # Mostramos toda la info relevante de cada partido
            st.write(f"{home_team} vs {away_team}", ev)
        except Exception as e:
            st.warning(f"Error leyendo partido: {e}")
    return pd.DataFrame(partidos)

        for ev in events:
            home_team = ev["homeTeam"]["name"]
            away_team = ev["awayTeam"]["name"]
            # Datos actuales y halftime (puede cambiar según estructura Sofascore)
            halftime_home = ev["homeScore"].get("period1", None)
            halftime_away = ev["awayScore"].get("period1", None)
            minuto = ev.get("time", {}).get("current", "--")
            estado = ev.get("status", {}).get("type", "")
            if halftime_home is not None and halftime_away is not None:
                # Solo si es mitad de partido y local va ganando
                if halftime_home > halftime_away:
                    partidos.append({
                        "Partido": f"{home_team} vs {away_team}",
                        "Marcador HT": f"{halftime_home}-{halftime_away}",
                        "Minuto": minuto,
                        "Estado": estado,
                    })
        return pd.DataFrame(partidos).head(3)
    except Exception as e:
        st.warning(f"Error al obtener datos de Sofascore: {e}")
        return pd.DataFrame(columns=["Partido", "Marcador HT", "Minuto", "Estado"])

# Actualización automática con simple recarga
if st.button("Refrescar datos"):
    partidos = get_live_matches_sofa()
else:
    partidos = get_live_matches_sofa()

st.dataframe(partidos)
st.info("Partidos donde el local va ganando al descanso. Recomendación: combinada doble oportunidad Local-Empate (1X).")


