import streamlit as st
import math

st.set_page_config(page_title="Calculadora de costos logísticos", layout="centered")

# ===== Helpers de formateo (AR) =====
def fmt_thousands(n: float, decimals: int = 0) -> str:
    """1.234.567 o 1.234.567,89"""
    if n is None:
        return ""
    if decimals == 0:
        s = f"{int(round(n)):,}".replace(",", ".")
    else:
        s = f"{n:,.{decimals}f}"
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s

def parse_local_number(text: str) -> float:
    """'1.234.567,89' -> 1234567.89"""
    if not text:
        return 0.0
    s = text.strip().replace(".", "").replace(" ", "")
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0

# ===== Título =====
st.title("🚚 Calculadora de costos logísticos")

st.header("Parámetros de entrada")

# === Entradas (idénticas a tu 1ª versión donde corresponde) ===
# Mantengo number_input donde necesitás decimales / controles.
fuel_efficiency = st.number_input(
    "Eficiencia de combustible (km por litro)",
    min_value=1.0, value=12.0, step=0.1, format="%.1f"
)

# Para que se vean con puntos de miles, uso text_input + formateo propio:
col1, col2 = st.columns(2)

with col1:
    fuel_price_str = st.text_input(
        "Precio del combustible (ARS por litro)",
        value=fmt_thousands(1200, 0)  # se muestra "1.200"
    )
    insurance_yearly_str = st.text_input(
        "Seguro anual (ARS)",
        value=fmt_thousands(1_200_000, 0)  # "1.200.000"
    )
    maintenance_yearly_str = st.text_input(
        "Mantenimiento anual (ARS)",
        value=fmt_thousands(800_000, 0)
    )

with col2:
    tires_cost_str = st.text_input(
        "Costo de un juego de cubiertas (ARS)",
        value=fmt_thousands(600_000, 0)
    )
    tires_life_km_str = st.text_input(
        "Duración estimada de las cubiertas (km)",
        value=fmt_thousands(40_000, 0)
    )
    annual_km_str = st.text_input(
        "Kilómetros recorridos por año",
        value=fmt_thousands(30_000, 0)
    )

# Mantengo el SLIDER como en tu primera versión (default 30%)
profit_margin = st.slider("Margen de ganancia (%)", min_value=0, max_value=100, value=30, step=1)

st.markdown("---")

# ===== Cálculo (misma lógica de tu 1ª versión) =====
def calcular_costo_km(
    fuel_efficiency: float,
    fuel_price: float,
    insurance_annual: float,
    maintenance_annual: float,
    tire_cost: float,
    tire_life_km: float,
    km_per_year: float,
    profit_margin_pct: float
) -> float:
    fuel_cost_per_km = fuel_price / max(fuel_efficiency, 1e-9)
    insurance_per_km = insurance_annual / max(km_per_year, 1.0)
    maintenance_per_km = maintenance_annual / max(km_per_year, 1.0)
    tires_per_km = tire_cost / max(tire_life_km, 1.0)
    operational_cost_per_km = fuel_cost_per_km + insurance_per_km + maintenance_per_km + tires_per_km
    final_cost_per_km = operational_cost_per_km * (1 + profit_margin_pct / 100.0)
    return math.ceil(final_cost_per_km)  # redondeo hacia arriba, sin decimales

# ===== Botón Calcular =====
if st.button("Calcular"):
    # Parseo de los campos que ahora se ven con puntos de miles
    fuel_price = parse_local_number(fuel_price_str)
    insurance_annual = parse_local_number(insurance_yearly_str)
    maintenance_annual = parse_local_number(maintenance_yearly_str)
    tire_cost = parse_local_number(tires_cost_str)
    tire_life_km = parse_local_number(tires_life_km_str)
    km_per_year = parse_local_number(annual_km_str)

    costo = calcular_costo_km(
        fuel_efficiency,
        fuel_price,
        insurance_annual,
        maintenance_annual,
        tire_cost,
        tire_life_km,
        km_per_year,
        float(profit_margin)
    )

    st.success(f"Costo total por km: ${fmt_thousands(costo, 0)}")

    with st.expander("Ver desglose"):
        st.write(f"Combustible por km: ${fmt_thousands(fuel_price / max(fuel_efficiency, 1e-9), 2)}")
        st.write(f"Seguro por km: ${fmt_thousands(insurance_annual / max(km_per_year, 1.0), 2)}")
        st.write(f"Mantenimiento por km: ${fmt_thousands(maintenance_annual / max(km_per_year, 1.0), 2)}")
        st.write(f"Cubiertas por km: ${fmt_thousands(tire_cost / max(tire_life_km, 1.0), 2)}")
