# streamlit_app.py
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="DCF Assumptions Sandbox", layout="centered")

DISCOUNT_RATE = 0.10
LINE_COLOR = "#AF1A1D"  # RGB (175, 26, 29)


# ---------- Inputs ----------
st.subheader("Cash flow inputs")

col1, col2 = st.columns(2)

with col1:
    cf1 = st.number_input("Cash flow year 1", value=150.0, step=1.0, format="%.2f")
    cf2 = st.number_input("Cash flow year 2", value=156.0, step=1.0, format="%.2f")
    cf3 = st.number_input("Cash flow year 3", value=162.0, step=1.0, format="%.2f")

with col2:
    cf4 = st.number_input("Cash flow year 4", value=169.0, step=1.0, format="%.2f")
    cf5 = st.number_input("Cash flow year 5", value=176.0, step=1.0, format="%.2f")

cash_flows = [cf1, cf2, cf3, cf4, cf5]
years = [1, 2, 3, 4, 5]

# ---------- Data ----------
df = pd.DataFrame(
    {
        "Year": years,
        "Cash flow": cash_flows,
    }
)

# ---------- Chart ----------
st.subheader("Cash flow profile")

line = (
    alt.Chart(df)
    .mark_line(point=True, strokeWidth=3, color=LINE_COLOR)
    .encode(
        x=alt.X("Year:O", title="Year", axis=alt.Axis(labelAngle=0)),  
        y=alt.Y("Cash flow:Q", title="Cash flow"),
        tooltip=[
            alt.Tooltip("Year:O", title="Year"),
            alt.Tooltip("Cash flow:Q", title="Cash flow", format=",.2f"),
        ],
    )
)

st.altair_chart(line, use_container_width=True)

# ---------- Valuation ----------
present_values = [
    cf / ((1 + DISCOUNT_RATE) ** (year - 1))
    for cf, year in zip(cash_flows, years)
]

valuation = sum(present_values)

st.subheader("Valuation")
st.metric("Valuation", f"{valuation:,.2f}")
