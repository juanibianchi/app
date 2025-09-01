# ===== Nuevo input: distancia del viaje =====
viaje_km = st.number_input(
    "Distancia del viaje (km)", 
    min_value=1, 
    value=10, 
    step=1
)

# ===== Botón Calcular =====
if st.button("Calcular"):
    # Parseo de los campos que ahora se ven con puntos de miles
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
