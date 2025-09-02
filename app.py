import streamlit as st
import math
import requests
from bs4 import BeautifulSoup

# ---------- Helpers ----------
def fmt_number(num: float) -> str:
    """Formatea un número con separador de miles (1.200.000)."""
    return f"{int(num):,}".replace(",", ".")

def parse_number(text: str) -> float:
    """Convierte texto con puntos de miles a número float."""
    return float(text.replace(".", "").replace(",", "."))

def number_input_with_format(label, default):
    """Crea un text_input que muestra números con separador de miles y mantiene el valor numérico."""
    key = label.replace(" ", "_")
    text_val = st.text_input(label, value=st.session_state.get(key, fmt_number(default)))
    try:
        num_val = parse_number(text_val)
        # Re-formatear en session_state para que quede lindo
        st.session_state[key] = fmt_number(num_val)
    except ValueError:
        num_val = default
    return num_val


import re
import requests
try:
    from bs4 import BeautifulSoup
    _HAS_BS4 = True
except Exception:
    _HAS_BS4 = False

def get_default_fuel_price() -> float:
    """
    Devuelve el precio por defecto del litro de nafta (ARS) para CABA,
    scrapeando 2–3 fuentes públicas. Si no logra extraer un valor
    plausible, retorna 1000.0 como fallback seguro.
    """
    # Fuentes a intentar (podés ajustar/ordenar)
    SOURCES = [
        "https://www.ambito.com/contenidos/nafta.html",
        "https://www.iprofesional.com/tag/combustibles",   # notas con precios
        "https://www.cronista.com/tags/combustibles/"      # idem
    ]

    # Palabras clave alrededor de las cuales buscar números
    KEYWORDS = ("nafta super", "súper", "super", "nafta", "gasolina", "combustible")

    # Rango plausible de ARS por litro (ajustable)
    MIN_PLAUSIBLE = 200.0
    MAX_PLAUSIBLE = 10000.0

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/123.0 Safari/537.36"
    }

    def _to_float(num_str: str) -> float | None:
        # normaliza formatos "1.200,50" -> "1200.50", "1200" -> "1200"
        s = num_str.replace("\xa0", " ").replace(".", "").replace(",", ".")
        m = re.search(r"(\d+(?:\.\d+)?)", s)
        return float(m.group(1)) if m else None

    def _plausible(x: float) -> bool:
        return MIN_PLAUSIBLE <= x <= MAX_PLAUSIBLE

    for url in SOURCES:
        try:
            r = requests.get(url, headers=HEADERS, timeout=6)
            if r.status_code != 200 or not r.text:
                continue
            html = r.text

            # 1) Intento con BeautifulSoup si está disponible
            if _HAS_BS4:
                soup = BeautifulSoup(html, "html.parser")
                # Busca nodos que contengan alguna keyword
                nodes = soup.find_all(string=re.compile("|".join(KEYWORDS), re.I))
                for node in nodes:
                    # Tomamos el texto del nodo + un poco de contexto
                    ctx = " ".join([
                        node.parent.get_text(" ", strip=True) if hasattr(node, "parent") else str(node)
                    ])
                    # números tipo $ 1.234,56 o 1234,56 o 1234
                    m = re.search(r"\$?\s*([0-9][0-9\.\,]{2,})", ctx)
                    if m:
                        val = _to_float(m.group(1))
                        if val and _plausible(val):
                            return round(val, 2)

            # 2) Fallback: regex directo sobre el HTML completo con keyword cerca
            for m in re.finditer(
                r"(nafta|súper|super|gasolina|combustible)[^$0-9]{0,60}\$?\s*([0-9][0-9\.\,]{2,})",
                html,
                flags=re.I,
            ):
                val = _to_float(m.group(2))
                if val and _plausible(val):
                    return round(val, 2)

            # 3) Último intento: cualquier número con $ en la página (menos robusto)
            for m in re.finditer(r"\$\s*([0-9][0-9\.\,]{2,})", html):
                val = _to_float(m.group(1))
                if val and _plausible(val):
                    return round(val, 2)

        except Exception:
            # Si una fuente falla, seguimos con la próxima
            continue

    # Fallback definitivo si nada funcionó
    return 1000.0

default_fuel_price = get_default_fuel_price()

# ---------- Inputs ----------
st.title("Calculadora de costos logísticos")

viaje_km = st.number_input("Kilómetros del viaje (solo ida)", min_value=1, value=10)

fuel_price = st.number_input(
    "Precio del combustible por litro (ARS)",
    min_value=0.0,
    value=default_fuel_price,
    step=10.0,
    format="%.2f")
fuel_efficiency = st.number_input("Eficiencia de combustible (km por litro)", min_value=1.0, value=12.0, step=0.1, format="%.1f")

# ---- Inputs grandes con separador de miles ----
seguro_anual = number_input_with_format("Seguro anual (ARS)", 1200000)
service_cost = number_input_with_format("Costo del service (ARS)", 150000)
service_km = st.number_input("Frecuencia del service (km)", min_value=1000, value=10000, step=500)

cubiertas_cost = number_input_with_format("Costo de un juego de cubiertas (ARS)", 400000)
cubiertas_km = st.number_input("Duración estimada de las cubiertas (km)", min_value=1000, value=40000, step=1000)

km_anuales = st.number_input("Kilómetros recorridos por año", min_value=1000, value=30000, step=1000)

profit_margin = st.slider("Margen de ganancia (%)", min_value=0, max_value=100, value=30)

# ---------- Cálculo ----------
if st.button("Calcular"):
    insurance_per_km = seguro_anual / km_anuales
    service_per_km = service_cost / service_km
    tires_per_km = cubiertas_cost / cubiertas_km

    fuel_per_km = fuel_price / fuel_efficiency

    cost_per_km = insurance_per_km + service_per_km + tires_per_km + fuel_per_km
    cost_per_km_with_margin = cost_per_km * (1 + profit_margin / 100)

    total_trip_cost = cost_per_km_with_margin * viaje_km * 2

    st.success(
        f"Costo total del viaje (ida y vuelta, {viaje_km} km): ${fmt_number(math.ceil(total_trip_cost))}\n\n"
        f"Costo por km: ${fmt_number(math.ceil(cost_per_km_with_margin))}"
    )
