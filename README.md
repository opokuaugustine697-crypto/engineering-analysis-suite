# Engineering Analysis Suite

A multi-page Streamlit application for petroleum/general engineering calculations and data analysis.

## Modules

1. **Pipe Flow Analyser**
   - Water, air, crude oil, and user-defined fluids
   - Velocity, Reynolds number, Darcy friction factor and pressure drop
   - Pressure-drop vs flow-rate plot
   - CSV export

2. **Heat Transfer Calculator**
   - Single-layer steady conduction using Fourier's law
   - Newton's law of cooling
   - Analytical cooling-time calculation
   - Interactive cooling curve

3. **Rock & Fluid Data Dashboard**
   - CSV upload
   - Summary statistics
   - Porosity filtering
   - Porosity histogram
   - Porosity-permeability crossplot
   - Filtered CSV export

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Engineering verification examples

### Pipe flow
For water with D = 0.10 m, L = 100 m, roughness = 4.5e-5 m and Q = 0.005 m³/s:
- Area ≈ 0.007854 m²
- Velocity ≈ 0.6366 m/s
- Re ≈ 63,408
- Haaland Darcy friction factor ≈ 0.02123
- Pressure drop ≈ 4.29 kPa

Small differences are expected if different water properties or a different turbulent friction-factor correlation are used.

### Flat-wall conduction
For k = 0.60 W/m·K, A = 10 m², T_hot = 100°C, T_cold = 25°C and L = 0.10 m:
Qdot = 0.60×10×(100−25)/0.10 = **4500 W**.

### Newton cooling
For T0 = 100°C, T∞ = 25°C, target = 40°C, h = 15 W/m²·K, A = 0.50 m², m = 2 kg, c = 900 J/kg·K:
t = −mc/(hA) ln[(Ttarget−T∞)/(T0−T∞)]
≈ **6.44 min**.

## AI usage documentation

Prompt 1 — "Build a modular Streamlit engineering app with separate pages for pipe flow, heat transfer and CSV data analysis. Put reusable engineering classes/functions in engineering.py."

Verified: page structure, imports, units and separation of calculations from UI.

Corrected: added input validation and explicit physical descriptions.

Prompt 2 — "Implement Darcy-Weisbach pressure drop using laminar f=64/Re and Haaland for turbulent flow."

Verified: hand calculation for the stated water example.

Corrected: handled zero-flow separately and rejected invalid diameter/roughness values.

Prompt 3 — "Implement Newton cooling and single-layer Fourier conduction with analytical verification."

Verified: formulas against analytical equations.

Corrected: restricted cooling to T0 > Ttarget > T∞ and added error handling.

## Deployment

Deploy this repository on Streamlit Community Cloud using `app.py` as the main file.

**GitHub repository URL:** _paste your URL here_

**Live Streamlit URL:** _paste your deployed URL here_
