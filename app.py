import streamlit as st

# ===== Helpers =====
def fmt_thousands(value, decimals=0):
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def parse_local_number(value_str):
    return float(value_str.replace(".", "").replace(",", "."))

# ===== Cálculo =====
def calcular_costo_km(fuel_efficiency, fuel_price, insurance_annual,
                      maintenance_annual, tire_cost, tire_life_km,
                      km_per_year, profit_margin):
    fuel_cost_per_km = fuel_price / max(fuel_efficiency, 1e-9)
    insurance_per_km = insurance_annual / max(km_per_year, 1.0)
    maintenance_per_km = maintenance_annual / max(km_per_year, 1.0)
    tires_per_km = tire_cost / max(tire_life_km, 1.0)

    total_cost_per_km = fuel_cost_per_km + insurance_per_km + maintenance_per_km + tires_per_km
    return total_cost_per_km * (1 + profit_margin / 100.0)

# ===== Interfaz =====
st.title("Calculadora de costo por kilómetro")

fuel_efficiency = st.number_input("Eficiencia de combustible (km por litro)", min_value=1, value=12, step=1)
fuel_price_str = st.text_input("Precio del combustible (ARS por litro)", value="1.200")
insurance_yearly_str = st.text_input("Seguro anual (ARS)", value="1.200.000")
maintenance_yearly_str = st.text_input("Mantenimiento anual (ARS)", value="600.000")
tires_cost_str = st.text_input("Costo de un juego de cubiertas (ARS)", value="800.000")
tires_life_km_str = st.text_input("Duración estimada de las cubiertas (km)", value="40.000")
annual_km_str = st.text_input("Kilómetros recorridos por año", value="30.000")

# ===== Nuevo input: distancia del viaje =====
viaje_km = st.number_input("Distancia del viaje (km)", min_value=1, value=10, step=1)

profit_margin = st.slider("Margen de ganancia (%)", min_value=0, max_value=100, value=30, step=1)

if st.button("Calcular"):
    fuel_price = parse_local_number(fuel_price_str)
    insurance_annual = parse_local_number(insurance_yearly_str)
    maintenance_annual = parse_local_number(maintenance_yearly_str)
    tire_cost = parse_local_number(tires_cost_str)
    tire_life_km = parse_local_number(tires_life_km_str)
    km_per_year = parse_local_number(annual_km_str)

    costo_km = calcular_costo_km(
        fuel_efficiency,
        fuel_price,
        insurance_annual,
        maintenance_annual,
        tire_cost,
        tire_life_km,
        km_per_year,
        float(profit_margin)
    )

    costo_total = costo_km * viaje_km * 2  # ida + vuelta

    st.success(f"Costo total del viaje (ida y vuelta, {viaje_km} km): ${fmt_thousands(costo_total, 0)}")

    with st.expander("Ver desglose (por km)"):
        st.write(f"Combustible por km: ${fmt_thousands(fuel_price / max(fuel_efficiency, 1e-9), 2)}")
        st.write(f"Seguro por km: ${fmt_thousands(insurance_annual / max(km_per_year, 1.0), 2)}")
        st.write(f"Mantenimiento por km: ${fmt_thousands(maintenance_annual / max(km_per_year, 1.0), 2)}")
        st.write(f"Cubiertas por km: ${fmt_thousands(tire_cost / max(tire_life_km, 1.0), 2)}")
