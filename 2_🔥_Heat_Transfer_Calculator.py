"""Module B: conduction and Newton cooling calculator."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from engineering import conduction_heat_rate, cooling_temperature, cooling_time

st.set_page_config(page_title="Heat Transfer Calculator", page_icon="🔥", layout="wide")
st.title("🔥 Module B — Heat Transfer Calculator")

tab1, tab2 = st.tabs(["Steady-state conduction", "Newton cooling"])

with tab1:
    st.subheader("1. Steady-state conduction through a flat wall")
    st.write(
        "Fourier's law for a single homogeneous wall is "
        "Q̇ = kA(T_hot − T_cold)/L. This assumes one-dimensional steady conduction."
    )

    with st.sidebar:
        st.header("Conduction inputs")
        k = st.number_input(
            "Thermal conductivity, k (W/m·K)",
            min_value=1e-9,
            value=0.60,
            help="How readily the wall material conducts heat.",
            key="k",
        )
        area = st.number_input(
            "Wall area, A (m²)",
            min_value=1e-9,
            value=10.0,
            help="Surface area perpendicular to heat flow.",
            key="area",
        )
        hot = st.number_input(
            "Hot-side temperature, T_hot (°C)",
            value=100.0,
            help="Temperature at the warmer wall face.",
            key="hot",
        )
        cold = st.number_input(
            "Cold-side temperature, T_cold (°C)",
            value=25.0,
            help="Temperature at the cooler wall face.",
            key="cold",
        )
        thickness = st.number_input(
            "Wall thickness, L (m)",
            min_value=1e-9,
            value=0.10,
            help="Distance heat travels through the wall.",
            key="thickness",
        )

    try:
        qdot = conduction_heat_rate(k, area, hot, cold, thickness)
        st.metric("Heat-transfer rate", f"{qdot:,.2f} W")
        st.metric("Heat flux", f"{qdot/area:,.2f} W/m²")
        st.success(
            "Positive heat rate means heat is flowing from the hotter side toward the colder side."
        )
    except ValueError as exc:
        st.error(str(exc))

with tab2:
    st.subheader("2. Newton's Law of Cooling")
    st.write(
        "For a lumped object, T(t) = T∞ + (T₀ − T∞) exp[−hAt/(mc)]. "
        "This gives the time required to reach a selected target temperature."
    )

    with st.sidebar:
        st.header("Cooling inputs")
        t0 = st.number_input(
            "Initial object temperature, T₀ (°C)",
            value=100.0,
            help="Object temperature at time zero.",
            key="t0",
        )
        target = st.slider(
            "Target object temperature, T_target (°C)",
            min_value=0.0,
            max_value=99.0,
            value=40.0,
            help="Temperature at which you want to know the cooling time.",
            key="target",
        )
        tinf = st.number_input(
            "Ambient temperature, T∞ (°C)",
            value=25.0,
            help="Surrounding fluid/room temperature assumed constant.",
            key="tinf",
        )
        h = st.number_input(
            "Convection coefficient, h (W/m²·K)",
            min_value=1e-9,
            value=15.0,
            help="Strength of convective heat transfer between the object and surroundings.",
            key="h",
        )
        area_c = st.number_input(
            "Object surface area, A (m²)",
            min_value=1e-9,
            value=0.50,
            help="Surface area exchanging heat with the surroundings.",
            key="area_c",
        )
        mass = st.number_input(
            "Object mass, m (kg)",
            min_value=1e-9,
            value=2.0,
            help="Mass of the cooling object.",
            key="mass",
        )
        cp = st.number_input(
            "Specific heat capacity, c (J/kg·K)",
            min_value=1e-9,
            value=900.0,
            help="Energy required to raise one kilogram by one kelvin.",
            key="cp",
        )

    try:
        if t0 <= tinf or target <= tinf or target >= t0:
            raise ValueError(
                "For cooling, use T₀ > T_target > T∞. Adjust the temperature inputs."
            )

        time_s = cooling_time(t0, target, tinf, h, area_c, mass, cp)
        st.metric("Time to target", f"{time_s/60:.2f} min")

        times = np.linspace(0, max(time_s * 1.5, 60), 150)
        temps = [
            cooling_temperature(t, t0, tinf, h, area_c, mass, cp)
            for t in times
        ]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times/60, y=temps, mode="lines", name="T(t)"))
        fig.add_hline(y=target, line_dash="dash", annotation_text="Target")
        fig.add_hline(y=tinf, line_dash="dot", annotation_text="Ambient")
        fig.update_layout(
            title="Newton Cooling Curve",
            xaxis_title="Time (min)",
            yaxis_title="Object temperature (°C)",
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "The curve updates whenever the sidebar inputs or target-temperature slider changes."
        )
    except ValueError as exc:
        st.error(str(exc))
