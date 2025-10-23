import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Buscador Live Partidos Doble Oportunidad")

st.title("Buscador de Partidos LIVE - Doble Oportunidad Local-Empate")

# Función simulada para obtener partidos en vivo (deberías conectar una API real)
def get_live_matches():
    # Simulación: deberías reemplazar por requests a una API real como Overlyzer, 365Scores o SportRadar
    data = [
        {'Partido': 'Universidad de Chile vs Lanus', 'Local': 'U. de Chile', 'Marcador HT': '1-0', 'Estado': 'En juego', 'Cuota Doble 1X': 1.48},
        {'Partido': 'Juventus vs Inter', 'Local': 'Juventus', 'Marcador HT': '2-1', 'Estado': 'En juego', 'Cuota Doble 1X': 1.34},
        {'Partido': 'River vs Boca', 'Local': 'River', 'Marcador HT': '1-0', 'Estado': 'En juego', 'Cuota Doble 1X': 1.57},
        {'Partido': 'Benfica vs Sporting', 'Local': 'Benfica', 'Marcador HT': '0-1', 'Estado': 'En juego', 'Cuota Doble 1X': 1.9},
    ]
    matches = pd.DataFrame(data)
    # Filtrar solo donde el local va ganando al descanso
    filtered = matches[matches['Marcador HT'].str.match(r'^[1-9]-0|^[1-9]-[1-9]')].head(3)
    return filtered

st.write("Filtrando partidos donde el local va ganando al descanso y recomendando apuesta doble 'Local-Empate' (1X):")

partidos = get_live_matches()
st.dataframe(partidos)

st.info("Selecciona una combinada de los partidos recomendados y realiza tu apuesta manualmente en la casa correspondiente.")

# Se recomienda agregar la conexión a una API deportiva para datos reales y actualizar cada minuto.

