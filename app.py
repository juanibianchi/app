import streamlit as st
import math

# ---- Configuración de página ----
st.set_page_config(page_title="Calculadora de costos logísticos", layout="centered")

# ---- Función para formatear números ----
def format_number(n):
    return f"{int(n):,}".replace(",", ".")

# ---- Entradas ----
st.title("🚚 Calculadora de costos logísticos")

st.header("Parámetros de entrada")

fuel_efficiency = st.number_input("Eficiencia de combustible (km por litro)", min_value=1.0, value=12.0, step=0.5)
fuel_price = st.number_input("Precio del combustible (ARS por litro)", min_value=0.0, value=1000.0, step=50.0)

insurance_annual = st.number_input("Seguro anual (ARS)", min_value=0.0, value=1_200_000.0, step=50_000.0)
maintenance_annual = st.number_input("Mantenimiento anual (ARS)", min_value=0.0, value=600_000.0, step=50_000.0)

tire_cost = st.number_input("Costo de las cubiertas (ARS)", min_value=0.0, value=800_000.0, step=50_000.0)
tire_life_km = st.number_input("Duración estimada de las cubiertas (km)", min_value=1.0, value=40_000.0, step=1000.0)

km_per_year = st.number_input("Kilómetros recorridos por año", min_value=1.0, value=30_000.0, step=1000.0)

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

    # aplicar margen
    total_with_margin = total_cost_per_km * (1 + profit_margin / 100)

    return math.ceil(total_with_margin)  # redondear para arriba

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

    st.success(f"Costo total por km: ${format_number(costo)} ARS")

    with st.expander("Ver desglose"):
        st.write(f"Combustible por km: ${format_number(round(fuel_price / fuel_efficiency))}")
        st.write(f"Seguro por km: ${format_number(round(insurance_annual / km_per_year))}")
        st.write(f"Mantenimiento por km: ${format_number(round(maintenance_annual / km_per_year))}")
        st.write(f"Cubiertas por km: ${format_number(round(tire_cost / tire_life_km))}")
