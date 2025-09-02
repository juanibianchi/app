import streamlit as st
import math
import requests
import re
import googlemaps

# -----------------------
# CONFIG GOOGLE MAPS API
# -----------------------
gmaps = googlemaps.Client(key=st.secrets["GOOGLE_MAPS_API_KEY"])

# ---------- Helpers ----------

# -----------------------
# FUNCIÓN PARA DISTANCIA
# -----------------------
def calcular_distancia(origen, destino):
    try:
        result = gmaps.distance_matrix(origen, destino, mode="driving", region="ar")
        distancia_metros = result["rows"][0]["elements"][0]["distance"]["value"]
        return distancia_metros / 1000  # en km
    except Exception:
        return None

def fmt_number(num: float) -> str:
    """Formatea un número con separador de miles (1.200.000)."""
    return f"{int(num):,}".replace(",", ".")

def parse_number(text: str) -> float:
    """Convierte texto con puntos de miles a número float."""
    return float(text.replace(".", "").replace(",", "."))

def number_input_with_format(label, default):
    """Crea un text_input que muestra números con separador de miles y mantiene el valor numérico."""
    key = label.replace(" ", "_")
    text_val = st.text_input(label, value=st.session_state.get(key, fmt_number(default)))
    try:
        num_val = parse_number(text_val)
        # Re-formatear en session_state para que quede lindo
        st.session_state[key] = fmt_number(num_val)
    except ValueError:
        num_val = default
    return num_val


def get_default_fuel_price():
    """
    Extrae el precio actual de nafta Súper en CABA desde surtidores.com.ar.
    Si no lo consigue, devuelve 1334.0 como fallback.
    """
    url = "https://surtidores.com.ar/precios/"
    headers = {"User-Agent": "Mozilla/5.0"}
    fallback = 1334.0
    try:
        r = requests.get(url, headers=headers, timeout=6)
        if r.status_code != 200 or not r.text:
            return fallback
        html = r.text
        # Busca "Super" en la cabecera de septiembre 2025
        m = re.search(r"Super\s+2025\s+Septiembre\s+(\d+)", html)
        if m:
            precio = float(m.group(1))
            return precio
        # Otra forma genérica: "Super" seguido de número en la tabla
        m2 = re.search(r"Super\s+([0-9]{3,4})", html)
        if m2:
            return float(m2.group(1))
    except Exception:
        pass
    return fallback
        

default_fuel_price = get_default_fuel_price()

# ---------- Inputs ----------
st.title("Calculadora de costos logísticos")

# -----------------------
# INPUTS DE DISTANCIA
# -----------------------
st.subheader("Distancia del viaje")

# Opción 1: Ingresar km directamente
km_manual = st.number_input("Kilómetros del viaje (solo ida)", value=10.0, step=1.0)

# Opción 2: Ingresar dirección
direccion_destino = st.text_input("Ingresá una dirección en CABA (opcional):")
deposito = "Baez 626, Palermo, CABA, Argentina"  # origen fijo

km_viaje = km_manual  # default: lo que ingresa el usuario
if direccion_destino:
    km_calculado = calcular_distancia(deposito, direccion_destino)
    if km_calculado:
        km_viaje = km_calculado
        st.success(f"Distancia estimada desde el depósito hasta '{direccion_destino}': {km_viaje:.1f} km")
    else:
        st.error("No se pudo calcular la distancia, se usará el valor manual.")

fuel_price = st.number_input(
    "Precio del combustible por litro (ARS)",
    min_value=0.0,
    value=default_fuel_price,
    step=10.0,
    format="%.2f")
fuel_efficiency = st.number_input("Eficiencia de combustible (km por litro)", min_value=1.0, value=12.0, step=0.1, format="%.1f")

# ---- Inputs grandes con separador de miles ----
seguro_anual = number_input_with_format("Seguro anual (ARS)", 1200000)
service_cost = number_input_with_format("Costo del service (ARS)", 150000)
service_km = st.number_input("Frecuencia del service (km)", min_value=1000, value=10000, step=500)

cubiertas_cost = number_input_with_format("Costo de un juego de cubiertas (ARS)", 400000)
cubiertas_km = st.number_input("Duración estimada de las cubiertas (km)", min_value=1000, value=40000, step=1000)

km_anuales = st.number_input("Kilómetros recorridos por año", min_value=1000, value=30000, step=1000)

profit_margin = st.slider("Margen de ganancia (%)", min_value=0, max_value=100, value=30)

# ---------- Cálculo ----------
if st.button("Calcular"):
    insurance_per_km = seguro_anual / km_anuales
    service_per_km = service_cost / service_km
    tires_per_km = cubiertas_cost / cubiertas_km

    fuel_per_km = fuel_price / fuel_efficiency

    cost_per_km = insurance_per_km + service_per_km + tires_per_km + fuel_per_km
    cost_per_km_with_margin = cost_per_km * (1 + profit_margin / 100)

    total_trip_cost = cost_per_km_with_margin * km_viaje * 2

    st.success(
        f"Costo total del viaje (ida y vuelta, {km_viaje} km): ${fmt_number(math.ceil(total_trip_cost))}\n\n"
        f"Costo por km: ${fmt_number(math.ceil(cost_per_km_with_margin))}"
    )
