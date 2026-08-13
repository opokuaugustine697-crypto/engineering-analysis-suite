"""Home page for the Engineering Analysis Suite."""

import streamlit as st

st.set_page_config(
    page_title="Engineering Analysis Suite",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ Engineering Analysis Suite")
st.subheader("Petroleum & General Engineering Calculators")

st.markdown(
    """
This multi-page Streamlit application contains three engineering modules:

- **A — Pipe Flow Analyser:** Darcy-Weisbach pipe-flow calculations, pressure-drop plots, and CSV export.
- **B — Heat Transfer Calculator:** Fourier conduction and Newton cooling with an analytical cooling curve.
- **C — Rock & Fluid Data Dashboard:** CSV upload, filtering, statistics, charts, and filtered-data export.

Use the navigation menu on the left to open a module.

### Calculation conventions
- SI units are used internally.
- Pipe pressure drop is calculated with the **Darcy-Weisbach equation**.
- Turbulent friction factor uses the **Haaland explicit approximation**; laminar flow uses `f = 64/Re`.
- Cooling uses the **lumped-capacitance Newton cooling solution**, so the Biot-number assumption should be reasonable for the physical object being modelled.
"""
)

st.info(
    "Educational engineering tool: always check assumptions, units, and results against a hand calculation before using them for design decisions."
)
