import streamlit as st
import math

st.set_page_config(page_title="Calculadora de Costos por km", layout="centered")

st.title("🚚 Calculadora de costos por kilómetro")

st.markdown("Ajustá los parámetros y calculá el costo estimado por kilómetro para tu furgón.")

# --- INPUTS ---
fuel_efficiency = st.number_input(
    "Eficiencia de combustible (km por litro)",
    value=12.0,
    format="%.1f"
)

fuel_price = st.number_input(
    "Precio del combustible (ARS por litro)",
    value=1000.0,
    format="%.0f"
)

insurance_yearly = st.number_input(
    "Seguro anual (ARS)",
    value=1200000.0,
    format="%.0f"
)

maintenance_yearly = st.number_input(
    "Mantenimiento anual (ARS)",
    value=800000.0,
    format="%.0f"
)

tires_cost = st.number_input(
    "Costo de un juego de cubiertas (ARS)",
    value=600000.0,
    format="%.0f"
)

tires_life_km = st.number_input(
    "Duración estimada de las cubiertas (km)",
    value=40000.0,
    format="%.0f"
)

annual_km = st.number_input(
    "Kilómetros recorridos por año",
    value=30000.0,
    format="%.0f"
)

profit_margin = st.slider(
    "Margen de ganancia (%)",
    min_value=0,
    max_value=100,
    value=20,
    step=1
)

# --- CALCULOS ---
# Costo de combustible por km
fuel_cost_per_km = fuel_price / fuel_efficiency

# Costo de seguro por km
insurance_per_km = insurance_yearly / annual_km

# Costo de mantenimiento por km
maintenance_per_km = maintenance_yearly / annual_km

# Costo de cubiertas por km
tires_per_km = tires_cost / tires_life_km

# Total costo operativo por km
operational_cost_per_km = fuel_cost_per_km + insurance_per_km + maintenance_per_km + tires_per_km

# Aplicar margen de ganancia
final_cost_per_km = operational_cost_per_km * (1 + profit_margin / 100)

# --- RESULTADO ---
st.subheader("💰 Costo estimado por kilómetro")
st.success(f"ARS ${math.ceil(final_cost_per_km):,}".replace(",", "."))  # separador de miles con puntos

# --- DEBUG opcional ---
with st.expander("🔍 Ver desglose de costos"):
    st.write(f"Combustible: ARS {fuel_cost_per_km:.2f} por km")
    st.write(f"Seguro: ARS {insurance_per_km:.2f} por km")
    st.write(f"Mantenimiento: ARS {maintenance_per_km:.2f} por km")
    st.write(f"Cubiertas: ARS {tires_per_km:.2f} por km")
    st.write(f"**Total sin margen:** ARS {operational_cost_per_km:.2f} por km")
    st.write(f"**Total con margen:** ARS {final_cost_per_km:.2f} por km (redondeado a {math.ceil(final_cost_per_km)})")
