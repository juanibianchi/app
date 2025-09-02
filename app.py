import streamlit as st
import math
import requests
from bs4 import BeautifulSoup

st.title("Calculadora de costos de envío")

# Función para obtener precio de nafta desde Surtidores.com.ar
def fetch_fuel_price():
    try:
        resp = requests.get("https://www.surtidores.com.ar/precios/")
        soup = BeautifulSoup(resp.text, "html.parser")
        # Busca "Nafta Super" o similar y extrae el siguiente valor
        cell = soup.find("td", string=lambda s: "Super" in s)
        if cell:
            price_str = cell.find_next_sibling("td").text
            price = float(price_str.replace("$", "").replace(".", "").strip())
            return price
    except Exception:
        pass
    return None

# Intentar obtener precio real
default_price = fetch_fuel_price()
if default_price is None:
    default_price = 1334.0  # valor de respaldo (septiembre 2025)

fuel_price = st.number_input(
    "Precio del combustible por litro (ARS)",
    min_value=0.0,
    value=default_price,
    step=1.0,
    format="%.0f"
)

fuel_efficiency = st.number_input("Rendimiento del vehículo (km por litro)", min_value=1.0, value=12.0, step=0.1)
tire_cost = st.number_input("Costo total de cubiertas (ARS)", min_value=0.0, value=1200000.0, step=1000.0, format="%.0f")
tire_life = st.number_input("Duración esperada de cubiertas (km)", min_value=1.0, value=60000, step=1000)
service_cost = st.number_input("Costo de cada service (ARS)", min_value=0.0, value=200000.0, step=1000.0, format="%.0f")
service_interval = st.number_input("Intervalo entre services (km)", min_value=1.0, value=10000, step=500)
insurance_cost = st.number_input("Seguro anual (ARS)", min_value=0.0, value=1200000.0, step=1000.0, format="%.0f")
annual_km = st.number_input("Km recorridos por año", min_value=1, value=60000, step=1000, format="%.0f")
margin = st.slider("Margen de ganancia (%)", min_value=0, max_value=100, value=30, step=1)
trip_km = st.number_input("Kilómetros del viaje (sólo ida)", min_value=1, value=10, step=1, format="%.0f")

# Cálculos
fuel_cost_per_km = fuel_price / fuel_efficiency
tire_cost_per_km = tire_cost / tire_life
service_cost_per_km = service_cost / service_interval
insurance_cost_per_km = insurance_cost / annual_km

cost_per_km = fuel_cost_per_km + tire_cost_per_km + service_cost_per_km + insurance_cost_per_km
cost_per_km_with_margin = cost_per_km * (1 + margin / 100)

# Costo total ida y vuelta
total_trip_cost = cost_per_km_with_margin * trip_km * 2

# Mostrar resultados formateados
st.subheader("Resultado")
st.write(f"Costo total del viaje (ida y vuelta, {trip_km} km): ${math.ceil(total_trip_cost):,}".replace(",", "."))
st.write(f"**Costo por km:** ${math.ceil(cost_per_km_with_margin):,}".replace(",", "."))
