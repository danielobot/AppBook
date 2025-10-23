import streamlit as st
import pandas as pd
import requests
from functools import reduce

# API Keys y URLs
ODDS_API_KEY = "4d8a3575f4d3a137e72adcb1af3bdaa5"
ODDS_API_URL = f"https://api.the-odds-api.com/v4/sports/soccer_brazil_campeonato/events?apiKey={ODDS_API_KEY}"
SOFASCORE_LIVE_URL = "https://www.sofascore.com/api/v1/sport/football/events/live"

st.set_page_config(page_title="Live Bets Cruzado: Sofascore + Odds API")
st.title("Live Bets: Partidos recomendados + Cuotas Doble Oportunidad (1X) [Automático]")

# Obtiene partidos en vivo desde Sofascore (local va ganando al descanso)
def get_live_matches_sofa():
    try:
        response = requests.get(SOFASCORE_LIVE_URL)
        data = response.json()
        events = data.get("events", [])
        partidos = []
        for ev in events:
            home_team = ev["homeTeam"]["name"]
            away_team = ev["awayTeam"]["name"]
            halftime_home = ev["homeScore"].get("period1", None)
            halftime_away = ev["awayScore"].get("period1", None)
            minuto = ev.get("time", {}).get("current", "--")
            estado = ev.get("status", {}).get("type", "")
            if halftime_home is not None and halftime_away is not None:
                if halftime_home > halftime_away:
                    partidos.append({
                        "home_team": home_team,
                        "away_team": away_team,
                        "Partido": f"{home_team} vs {away_team}",
                        "Marcador HT": f"{halftime_home}-{halftime_away}",
                        "Minuto": minuto,
                        "Estado": estado,
                    })
        return pd.DataFrame(partidos).head(3)
    except Exception as e:
        st.warning(f"Error al obtener datos de Sofascore: {e}")
        return pd.DataFrame(columns=["Partido", "Marcador HT", "Minuto", "Estado"])

# Obtiene cuotas 1X (double chance: home or draw) desde Odds API
def get_odds_events():
    response = requests.get(ODDS_API_URL)
    events = response.json()
    odds_data = []
    for ev in events:
        home_team = ev.get('home_team')
        away_team = ev.get('away_team')
        cuota_1X = None
        for bookmaker in ev.get('bookmakers', []):
            for market in bookmaker.get('markets', []):
                if market['key'] == 'double_chance':
                    for outcome in market.get('outcomes', []):
                        if outcome['name'] == 'Home or Draw':
                            cuota_1X = outcome['price']
                            odds_data.append({
                                "home_team": home_team,
                                "away_team": away_team,
                                "Partido": f"{home_team} vs {away_team}",
                                "Cuota Local-Empate (1X)": cuota_1X,
                                "Casa de apuestas": bookmaker['title'],
                            })
    return pd.DataFrame(odds_data)

if st.button("Refrescar recomendaciones"):
    partidos_sofa = get_live_matches_sofa()
    cuotas_odds = get_odds_events()
else:
    partidos_sofa = get_live_matches_sofa()
    cuotas_odds = get_odds_events()

# Cruce de partidos
if not partidos_sofa.empty and not cuotas_odds.empty:
    # Join cruzado por ambos equipos (mayúsculas/minúsculas uniformizadas)
    partidos_sofa['home_team'] = partidos_sofa['home_team'].str.lower()
    partidos_sofa['away_team'] = partidos_sofa['away_team'].str.lower()
    cuotas_odds['home_team'] = cuotas_odds['home_team'].str.lower()
    cuotas_odds['away_team'] = cuotas_odds['away_team'].str.lower()
    combinadas = pd.merge(partidos_sofa, cuotas_odds, on=['home_team', 'away_team'])
    st.dataframe(combinadas[["Partido_x", "Marcador HT", "Minuto", "Cuota Local-Empate (1X)", "Casa de apuestas"]])
    
    # Totalizador de combinada 1X (solo si hay 3 partidos y todas las cuotas disponibles)
    cuotas = combinadas["Cuota Local-Empate (1X)"].tolist()
    if cuotas and len(cuotas) == 3:
        valor_combinada = reduce(lambda x, y: x*y, cuotas)
        st.success(f"**Valor total de la combinada 1X:** {valor_combinada:.2f}")
    else:
        st.info("Se requieren 3 partidos y cuotas activas para calcular la combinada.")
else:
    st.info("No hay partidos que cumplan el criterio en Sofascore o cuotas disponibles en Odds API.")

st.caption("Puedes modificar los endpoints o agregar más ligas según tu preferencia. El sistema cruza partidos live (local ganando al descanso) con las cuotas reales del mercado 1X.")
