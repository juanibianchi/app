import streamlit as st
import math

st.title("Calculadora de Costo por Km")

st.header("Parámetros del vehículo y costos")

# Inputs con formato de miles
fuel_efficiency = st.number_input("Eficiencia de combustible (km por litro)", value=12)
fuel_price = st.number_input("Precio del combustible (ARS por litro)", value=1000, format="%.0f")
insurance_yearly = st.number_input("Seguro anual (ARS)", value=1200000, format="%.0f")
maintenance_yearly = st.number_input("Mantenimiento anual (ARS)", value=800000, format="%.0f")
tires_cost = st.number_input("Costo de un juego de cubiertas (ARS)", value=600000, format="%.0f")
tires_life_km = st.number_input("Duración estimada de las cubiertas (km)", value=40000)
margin = st.slider("Margen de ganancia (%)", 0, 100, 20)

st.header("Cálculo")

distance_km = st.number_input("Distancia (km, solo ida)", value=10.0)

# ---- Cálculo ----
total_distance = distance_km * 2  # ida y vuelta
liters_consumed = total_distance / fuel_efficiency
fuel_cost = liters_consumed * fuel_price

insurance_per_km = insurance_yearly / 20000  # suponiendo 20k km al año
maintenance_per_km = maintenance_yearly / 20000
tires_per_km = tires_cost / tires_life_km

otros_por_km = insurance_per_km + maintenance_per_km + tires_per_km
otros_cost = otros_por_km * total_distance

base_cost = fuel_cost + otros_cost
final_cost = math.ceil(base_cost * (1 + margin / 100))

st.subheader("Resultado")
st.write(f"Costo estimado: **ARS {final_cost:,.0f}**")
