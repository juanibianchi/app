import streamlit as st
import math

# ==============================
# Funciones de cálculo
# ==============================

def calcular_costo_km_total(
    fuel_price,            # precio por litro
    fuel_efficiency_km_l,  # km recorridos por litro
    seguro_anual, km_anuales,
    costo_cubiertas, km_cubiertas,
    costo_service, km_service,
    profit_margin=0.3      # 30% por defecto
):
    # --- Combustible ---
    combustible_km = fuel_price / fuel_efficiency_km_l

    # --- Seguro ---
    seguro_km = seguro_anual / km_anuales

    # --- Mantenimiento ---
    cubiertas_km = costo_cubiertas / km_cubiertas
    service_km = costo_service / km_service
    mantenimiento_km = cubiertas_km + service_km

    # --- Costo operativo ---
    costo_operativo = combustible_km + seguro_km + mantenimiento_km

    # --- Precio con margen ---
    total_km = costo_operativo * (1 + profit_margin)

    return {
        "combustible_km": round(combustible_km, 2),
        "seguro_km": round(seguro_km, 2),
        "mantenimiento_km": round(mantenimiento_km, 2),
        "costo_operativo_km": round(costo_operativo, 2),
        "total_km": round(total_km, 2),
    }


def calcular_costo_viaje(distancia_km, costos_km):
    """ Calcula el costo de un viaje ida y vuelta, redondeado hacia arriba. """
    distancia_total = distancia_km * 2  # ida y vuelta
    costo_viaje = distancia_total * costos_km["total_km"]
    return math.ceil(costo_viaje)  # redondeo SIEMPRE hacia arriba


# ==============================
# Interfaz Streamlit
# ==============================

st.set_page_config(page_title="Simulador de Costos Logísticos", page_icon="🚚")

st.title("🚚 Simulador de costos logísticos")
st.write("Ingresá los datos de tu vehículo (podés modificarlos si querés) y simulá el costo de un envío en CABA.")

# --- Entradas ---
st.header("Parámetros del vehículo")

fuel_price = st.number_input("Precio por litro de combustible (ARS)", value=1200.0, step=10.0)
fuel_efficiency = st.number_input("Eficiencia de combustible (km por litro)", value=12.0, step=0.5)
seguro_anual = st.number_input("Seguro anual (ARS)", value=1200000.0, step=10000.0)
km_anuales = st.number_input("Km recorridos por año", value=80000.0, step=1000.0)
costo_cubiertas = st.number_input("Costo de un juego de cubiertas (ARS)", value=400000.0, step=10000.0)
km_cubiertas = st.number_input("Duración de cubiertas (km)", value=40000.0, step=1000.0)
costo_service = st.number_input("Costo de un service (ARS)", value=80000.0, step=5000.0)
km_service = st.number_input("Intervalo de service (km)", value=10000.0, step=500.0)
profit_margin = st.slider("Margen de ganancia (%)", 0, 100, 30) / 100

st.header("Distancia del viaje")
distancia = st.number_input("Distancia (solo ida, en km)", value=15.0, step=1.0)

# --- Calcular ---
if st.button("Calcular"):
    costos = calcular_costo_km_total(
        fuel_price, fuel_efficiency,
        seguro_anual, km_anuales,
        costo_cubiertas, km_cubiertas,
        costo_service, km_service,
        profit_margin
    )
    costo_viaje = calcular_costo_viaje(distancia, costos)

    st.subheader("Resultados por km")
    st.write(f"- Combustible: ${costos['combustible_km']} / km")
    st.write(f"- Seguro: ${costos['seguro_km']} / km")
    st.write(f"- Mantenimiento: ${costos['mantenimiento_km']} / km")
    st.write(f"- Costo operativo total: ${costos['costo_operativo_km']} / km")
    st.write(f"- Precio final (con margen): ${costos['total_km']} / km")

    st.subheader("Costo total del viaje")
    st.success(f"Un viaje ida y vuelta de {distancia} km cuesta aproximadamente: **${costo_viaje}**")