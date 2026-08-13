# AI Usage Record

This project used AI as a coding assistant, but each generated calculation was checked against the governing engineering equation and a hand-calculated test case.

## Prompt 1
Build a modular Streamlit engineering app with separate pages for pipe flow, heat transfer and CSV data analysis. Put reusable engineering classes/functions in engineering.py.

**Verified:** page structure, imports, units and separation of calculations from UI.

**Corrected:** added input validation, physical descriptions and clear unit labels.

## Prompt 2
Implement Darcy-Weisbach pressure drop using laminar f=64/Re and Haaland for turbulent flow.

**Verified:** water example using D=0.10 m, L=100 m, roughness=4.5e-5 m and Q=0.005 m³/s.

**Corrected:** added zero-flow handling and validation for positive diameter and fluid properties.

## Prompt 3
Implement Newton cooling and single-layer Fourier conduction with analytical verification.

**Verified:** formulas and numerical examples against the analytical solutions.

**Corrected:** added physical constraints for a valid cooling case and protected the UI from invalid input crashes.
