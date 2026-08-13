"""Module C: uploaded rock/fluid data dashboard."""

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Rock & Fluid Dashboard", page_icon="🪨", layout="wide")
st.title("🪨 Module C — Rock & Fluid Data Dashboard")

uploaded = st.file_uploader(
    "Upload a CSV containing rock or fluid measurements",
    type=["csv"],
    help="For the example charts, use columns named Porosity and Permeability if available.",
)

if uploaded is None:
    st.info("Upload a CSV file to begin.")
    st.stop()

try:
    data = pd.read_csv(uploaded)
except Exception as exc:
    st.error(f"Could not read the CSV file: {exc}")
    st.stop()

if data.empty:
    st.warning("The uploaded CSV contains no rows.")
    st.stop()

st.subheader("Data preview")
st.dataframe(data, use_container_width=True)

numeric = data.select_dtypes(include="number").columns.tolist()
st.subheader("Summary statistics")
if numeric:
    st.dataframe(data[numeric].describe().T, use_container_width=True)
else:
    st.warning("No numeric columns were found.")
    st.stop()

st.sidebar.header("Filters")
filtered = data.copy()

porosity_col = next((c for c in data.columns if c.lower() == "porosity"), None)
if porosity_col is not None:
    min_porosity = st.sidebar.slider(
        "Minimum porosity (%)",
        min_value=float(data[porosity_col].min()),
        max_value=float(data[porosity_col].max()),
        value=float(data[porosity_col].min()),
    )
    filtered = filtered[filtered[porosity_col] >= min_porosity]
else:
    st.sidebar.info("No 'Porosity' column found; porosity filter and charts are disabled.")

st.metric("Rows after filtering", len(filtered))

if porosity_col is not None:
    fig1 = px.histogram(
        filtered,
        x=porosity_col,
        nbins=20,
        title="Porosity Distribution",
        labels={porosity_col: "Porosity (%)"},
    )
    st.plotly_chart(fig1, use_container_width=True)

    permeability_col = next(
        (c for c in data.columns if c.lower() == "permeability"), None
    )
    if permeability_col is not None:
        fig2 = px.scatter(
            filtered,
            x=porosity_col,
            y=permeability_col,
            title="Porosity–Permeability Crossplot",
            labels={
                porosity_col: "Porosity (%)",
                permeability_col: "Permeability",
            },
            hover_data=filtered.columns,
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info(
            "Add a numeric column named 'Permeability' to enable the crossplot."
        )

st.subheader("Filtered data")
st.dataframe(filtered, use_container_width=True)

st.download_button(
    "⬇️ Download filtered data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_engineering_data.csv",
    mime="text/csv",
)
