import streamlit as st
import math

st.set_page_config(page_title="Calculadora de costos logísticos", layout="centered")

st.title("🚚 Calculadora de costos logísticos")

st.header("Parámetros de entrada")

# --- Función para formatear con separador de miles ---
def format_input(label, value, step=1000.0, min_value=0.0):
    return st.number_input(
        label,
        min_value=min_value,
        value=value,
        step=step,
        format="%.0f"  # evita decimales
    )

fuel_efficiency = st.number_input("Eficiencia de combustible (km por litro)", min_value=1.0, value=12.0, step=0.5)
fuel_price = format_input("Precio del combustible (ARS por litro)", 1000.0, step=50.0)

insurance_annual = format_input("Seguro anual (ARS)", 1_200_000.0, step=50_000.0)
maintenance_annual = format_input("Mantenimiento anual (ARS)", 600_000.0, step=50_000.0)

tire_cost = format_input("Costo de las cubiertas (ARS)", 800_000.0, step=50_000.0)
tire_life_km = format_input("Duración estimada de las cubiertas (km)", 40_000.0, step=1000.0)

km_per_year = format_input("Kilómetros recorridos por año", 30_000.0, step=1000.0)

profit_margin = st.number_input("Margen de ganancia (%)", min_value=0.0, value=30.0, step=1.0)

# ---- Función de cálculo ----
def calcular_costo_km(
    fuel_efficiency,
    fuel_price,
    insurance_annual,
    maintenance_annual,
    tire_cost,
    tire_life_km,
    km_per_year,
    profit_margin
):
    fuel_cost_per_km = fuel_price / fuel_efficiency
    insurance_per_km = insurance_annual / km_per_year
    maintenance_per_km = maintenance_annual / km_per_year
    tire_per_km = tire_cost / tire_life_km

    total_cost_per_km = fuel_cost_per_km + insurance_per_km + maintenance_per_km + tire_per_km

    total_with_margin = total_cost_per_km * (1 + profit_margin / 100)

    return math.ceil(total_with_margin)

# ---- Botón Calcular ----
if st.button("Calcular"):
    costo = calcular_costo_km(
        fuel_efficiency,
        fuel_price,
        insurance_annual,
        maintenance_annual,
        tire_cost,
        tire_life_km,
        km_per_year,
        profit_margin
    )

    st.success(f"Costo total por km: ${costo:,.0f}".replace(",", "."))

    with st.expander("Ver desglose"):
        st.write(f"Combustible por km: ${fuel_price / fuel_efficiency:,.0f}".replace(",", "."))
        st.write(f"Seguro por km: ${insurance_annual / km_per_year:,.0f}".replace(",", "."))
        st.write(f"Mantenimiento por km: ${maintenance_annual / km_per_year:,.0f}".replace(",", "."))
        st.write(f"Cubiertas por km: ${tire_cost / tire_life_km:,.0f}".replace(",", "."))
