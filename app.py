import streamlit as st
import math
from functools import partial

st.set_page_config(page_title="Calculadora de Costos por km", layout="centered")

st.title("🚚 Calculadora de costos por kilómetro")
st.markdown("Ajustá los parámetros y calculá el costo estimado por kilómetro para tu furgón.")

# -------- Helpers de ARS --------
def format_ars(value: float, decimals: int = 0) -> str:
    """Devuelve '1.234.567' o '1.234.567,89' según decimals."""
    if value is None:
        return ""
    if decimals == 0:
        s = f"{int(round(value)):,}".replace(",", ".")
    else:
        s = f"{value:,.{decimals}f}"
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s

def parse_ars(text: str) -> float:
    """Convierte '1.234.567,89' o '1234567.89' a float."""
    if not text:
        return 0.0
    s = text.strip().replace(".", "").replace(" ", "")
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0

def _on_change_money(key: str):
    """Reformatea el input al salir del campo."""
    val = parse_ars(st.session_state.get(key, ""))
    st.session_state[key] = format_ars(val, 0)

# -------- Defaults en session_state --------
defaults = {
    "fuel_price_str": format_ars(1200, 0),        # ARS por litro
    "insurance_yearly_str": format_ars(1_200_000, 0),
    "maintenance_yearly_str": format_ars(800_000, 0),
    "tires_cost_str": format_ars(600_000, 0),
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# -------- Inputs --------
col1, col2 = st.columns(2)
with col1:
    fuel_efficiency = st.number_input(
        "Eficiencia de combustible (km por litro)",
        value=12.0, step=0.1, format="%.1f"
    )
    annual_km = st.number_input(
        "Kilómetros recorridos por año",
        value=30000.0, step=1000.0, format="%.0f"
    )
    tires_life_km = st.number_input(
        "Duración estimada de las cubiertas (km)",
        value=40000.0, step=1000.0, format="%.0f"
    )
with col2:
    st.text_input(
        "Precio del combustible (ARS por litro)",
        key="fuel_price_str",
        on_change=partial(_on_change_money, "fuel_price_str")
    )
    st.text_input(
        "Seguro anual (ARS)",
        key="insurance_yearly_str",
        on_change=partial(_on_change_money, "insurance_yearly_str")
    )
    st.text_input(
        "Mantenimiento anual (ARS)",
        key="maintenance_yearly_str",
        on_change=partial(_on_change_money, "maintenance_yearly_str")
    )
    st.text_input(
        "Costo de un juego de cubiertas (ARS)",
        key="tires_cost_str",
        on_change=partial(_on_change_money, "tires_cost_str")
    )

profit_margin = st.slider("Margen de ganancia (%)", 0, 100, 20, step=1)

st.markdown("---")

# -------- Calcular al presionar botón --------
if st.button("Calcular"):
    # Parseo de inputs monetarios
    fuel_price = parse_ars(st.session_state["fuel_price_str"])
    insurance_yearly = parse_ars(st.session_state["insurance_yearly_str"])
    maintenance_yearly = parse_ars(st.session_state["maintenance_yearly_str"])
    tires_cost = parse_ars(st.session_state["tires_cost_str"])

    # ---- Cálculos por km ----
    fuel_cost_per_km = fuel_price / max(fuel_efficiency, 0.0001)
    insurance_per_km = insurance_yearly / max(annual_km, 1.0)
    maintenance_per_km = maintenance_yearly / max(annual_km, 1.0)
    tires_per_km = tires_cost / max(tires_life_km, 1.0)

    operational_cost_per_km = fuel_cost_per_km + insurance_per_km + maintenance_per_km + tires_per_km
    final_cost_per_km = operational_cost_per_km * (1 + profit_margin / 100)

    # ---- Salida formateada ----
    st.subheader("💰 Costo estimado por kilómetro")
    st.success(f"ARS ${format_ars(math.ceil(final_cost_per_km), 0)}")

    with st.expander("🔍 Ver desglose de costos"):
        st.write(f"Combustible: ARS ${format_ars(fuel_cost_per_km, 2)} / km")
        st.write(f"Seguro: ARS ${format_ars(insurance_per_km, 2)} / km")
        st.write(f"Mantenimiento: ARS ${format_ars(maintenance_per_km, 2)} / km")
        st.write(f"Cubiertas: ARS ${format_ars(tires_per_km, 2)} / km")
        st.write(f"**Total sin margen:** ARS ${format_ars(operational_cost_per_km, 2)} / km")
        st.write(f"**Total con margen:** ARS ${format_ars(final_cost_per_km, 2)} / km (redondeado a {format_ars(math.ceil(final_cost_per_km), 0)})")
