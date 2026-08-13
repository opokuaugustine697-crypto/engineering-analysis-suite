"""Module A: pipe-flow calculator."""

import io
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from engineering import Fluid, Pipe

st.set_page_config(page_title="Pipe Flow Analyser", page_icon="🛢️", layout="wide")
st.title("🛢️ Module A — Pipe Flow Analyser")

FLUIDS = {
    "Water": Fluid("Water", 998.0, 1.002e-3),
    "Air": Fluid("Air", 1.184, 1.85e-5),
    "Crude oil": Fluid("Crude oil", 850.0, 5.00e-2),
}

with st.sidebar:
    st.header("Fluid")
    fluid_choice = st.selectbox("Select fluid", list(FLUIDS) + ["User-defined"])

    if fluid_choice == "User-defined":
        density = st.number_input(
            "Density, ρ (kg/m³)",
            min_value=0.0001,
            value=900.0,
            help="Mass of fluid per unit volume.",
        )
        viscosity = st.number_input(
            "Dynamic viscosity, μ (Pa·s)",
            min_value=1e-8,
            value=0.01,
            format="%.6g",
            help="Resistance of the fluid to shear flow.",
        )
        fluid = Fluid("User-defined", density, viscosity)
    else:
        fluid = FLUIDS[fluid_choice]
        st.caption(
            f"Auto-populated: ρ = {fluid.density:g} kg/m³, μ = {fluid.viscosity:g} Pa·s"
        )

    st.header("Pipe geometry")
    diameter = st.number_input(
        "Internal diameter, D (m)",
        min_value=0.0001,
        value=0.10,
        help="Inside diameter available for flow.",
    )
    length = st.number_input(
        "Pipe length, L (m)",
        min_value=0.0,
        value=100.0,
        help="Length over which frictional pressure loss is calculated.",
    )
    roughness = st.number_input(
        "Absolute roughness, ε (m)",
        min_value=0.0,
        value=4.5e-5,
        format="%.6g",
        help="Average internal wall roughness height.",
    )
    flow_rate = st.number_input(
        "Volumetric flow rate, Q (m³/s)",
        min_value=0.0,
        value=0.005,
        format="%.6g",
        help="Volume of fluid passing through the pipe per second.",
    )
    max_flow = st.number_input(
        "Plot range maximum Q (m³/s)",
        min_value=0.0001,
        value=max(flow_rate * 2, 0.01),
        format="%.6g",
    )

try:
    pipe = Pipe(diameter, length, roughness)
    velocity = pipe.velocity(flow_rate)
    reynolds = pipe.reynolds_number(flow_rate, fluid)
    friction = pipe.friction_factor(flow_rate, fluid)
    dp = pipe.pressure_drop(flow_rate, fluid)

    st.caption(
        "Model: Darcy-Weisbach. Laminar: f = 64/Re. Turbulent: Haaland approximation."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Velocity", f"{velocity:.3f} m/s")
    c2.metric("Reynolds number", f"{reynolds:,.0f}")
    c3.metric("Darcy friction factor", f"{friction:.5f}")
    c4.metric("Pressure drop", f"{dp/1000:.3f} kPa")

    q_values = np.linspace(max_flow / 1000, max_flow, 100)
    dp_values = [pipe.pressure_drop(q, fluid) / 1000 for q in q_values]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=q_values,
            y=dp_values,
            mode="lines",
            name="Pressure drop",
        )
    )
    fig.add_vline(x=flow_rate, line_dash="dash", annotation_text="Selected Q")
    fig.update_layout(
        title="Pressure Drop vs Flow Rate",
        xaxis_title="Flow rate Q (m³/s)",
        yaxis_title="Pressure drop ΔP (kPa)",
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

    results = pd.DataFrame(
        {
            "Fluid": [fluid.name],
            "Density_kg_m3": [fluid.density],
            "Viscosity_Pa_s": [fluid.viscosity],
            "Diameter_m": [diameter],
            "Length_m": [length],
            "Roughness_m": [roughness],
            "FlowRate_m3_s": [flow_rate],
            "Velocity_m_s": [velocity],
            "Reynolds": [reynolds],
            "DarcyFrictionFactor": [friction],
            "PressureDrop_Pa": [dp],
            "PressureDrop_kPa": [dp / 1000],
        }
    )

    csv_bytes = results.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download current pipe-flow result as CSV",
        data=csv_bytes,
        file_name="pipe_flow_result.csv",
        mime="text/csv",
    )
except ValueError as exc:
    st.error(f"Input error: {exc}")
except Exception as exc:
    st.error(f"Unexpected calculation error: {exc}")
