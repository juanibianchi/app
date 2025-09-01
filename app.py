import streamlit as st

# --- Función para formatear números grandes con puntos ---
def fmt_thousands(value, decimals=0):
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- Título ---
st.title("Calculadora de Costo por Km")

# --- Inputs de usuario (se quedan crudos, sin formateo) ---
fuel_price = st.number_input("Precio del combustible (ARS por litro)", value=1000.0, step=50.0)
fuel_efficiency = st.number_input("Eficiencia de combustible (km por litro)", value=12.0, step=0.1)
insurance_annual = st.number_input("Seguro anual (ARS)", value=1200000.0, step=10000.0)
km_per_year = st.number_input("Kilómetros recorridos por año", value=30000, step=1000)
tire_cost = st.number_input("Costo de un juego de cubiertas (ARS)", value=400000.0, step=10000.0)
tire_life = st.number_input("Duración estimada de las cubiertas (km)", value=40000, step=5000)
service_cost = st.number_input("Costo de un service (ARS)", value=150000.0, step=10000.0)
service_interval = st.number_input("Intervalo de service (km)", value=10000, step=1000)

# Nuevo input: kilómetros del viaje
viaje_km = st.number_input("Kilómetros del viaje (solo ida)", value=10, step=1)

# Margen de ganancia como slider
profit_margin = st.slider("Margen de ganancia (%)", min_value=0, max_value=100, value=30, step=1)

# --- Cálculo del costo por km ---
def calcular_costo_km():
    # Costo combustible por km
    fuel_cost_per_km = fuel_price / fuel_efficiency
    
    # Costo seguro por km
    insurance_per_km = insurance_annual / km_per_year
    
    # Costo cubiertas por km
    tire_per_km = tire_cost / tire_life
    
    # Costo service por km
    service_per_km = service_cost / service_interval
    
    # Total costo por km
    base_cost_per_km = fuel_cost_per_km + insurance_per_km + tire_per_km + service_per_km
    
    # Aplicar margen de ganancia
    return base_cost_per_km * (1 + profit_margin / 100)

# --- Botón para calcular ---
if st.button("Calcular"):
    costo_km = calcular_costo_km()
    
    # Redondeos solo para mostrar
    costo_total = costo_km * viaje_km * 2  # ida + vuelta
    costo_total_redondeado = round(costo_total)
    costo_km_redondeado = round(costo_km)

    st.success(
        f"**Costo total del viaje (ida y vuelta, {viaje_km} km):** "
        f"${fmt_thousands(costo_total_redondeado, 0)}\n\n"
        f"**Costo por km:** ${fmt_thousands(costo_km_redondeado, 0)}"
    )
