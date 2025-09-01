import streamlit as st
import math

st.set_page_config(page_title="Calculadora de Costos por km", layout="centered")

st.title("🚚 Calculadora de costos por kilómetro")

st.markdown("Ajustá los parámetros y calculá el costo estimado por kilómetro para tu furgón.")

# --- INPUTS ---
fuel_efficiency = st.number_input("Eficiencia de combustible (km por litro)", value=12.0)
fuel_price = st.number_input("Precio del combustible (ARS por litro)", value=1000.0)
insurance_yearly = st.number_input("Seguro anual (ARS)", value=1200000.0)
maintenance_yearly = st.number_input("Mantenimiento anual (ARS)", value=800000.0)
tires_cost = st.number_input("Costo de un juego de cubiertas (ARS)", value=600000.0)
tires_life_km = st.number_input("Duración estimada de las cubiertas (km)", value=40000.0)
annual_km = st.number_input("Kilómetros recorridos por año", value=30000.0)
profit_margin = st.slider("Margen de ganancia (%)", min_value=0, max_value=100, value=20, step=1)

# --- CALCULO SOLO AL TOCAR BOTÓN ---
if st.button("Calcular"):
    # Costo de combustible por km
    fuel_cost_per_km = fuel_price / fuel_efficiency
    # Seguro por km
    insurance_per_km = insurance_yearly / annual_km
    # Mantenimiento por km
    maintenance_per_km = maintenance_yearly / annual_km
    # Cubiertas por km
    tires_per_km = tires_cost / tires_life_km

    # Total operativo
    operational_cost_per_km = fuel_cost_per_km + insurance_per_km + maintenance_per_km + tires_per_km
    final_cost_per_km = operational_cost_per_km * (1 + profit_margin / 100)

    # --- RESULTADO ---
    st.subheader("💰 Costo estimado por kilómetro")
    st.success(f"ARS ${math.ceil(final_cost_per_km):,}".replace(",", "."))  # separador de miles con puntos

    # --- DETALLE ---
    with st.expander("🔍 Ver desglose de costos"):
        st.write(f"Combustible: ARS {fuel_cost_per_km:,.2f}".replace(",", "."))
        st.write(f"Seguro: ARS {insurance_per_km:,.2f}".replace(",", "."))
        st.write(f"Mantenimiento: ARS {maintenance_per_km:,.2f}".replace(",", "."))
        st.write(f"Cubiertas: ARS {tires_per_km:,.2f}".replace(",", "."))
        st.write(f"**Total sin margen:** ARS {operational_cost_per_km:,.2f}".replace(",", "."))
        st.write(f"**Total con margen:** ARS {final_cost_per_km:,.2f}".replace(",", "."))
