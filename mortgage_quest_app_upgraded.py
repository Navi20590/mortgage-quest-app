
import streamlit as st
import pandas as pd
import plotly.express as px

# App configuration
st.set_page_config(page_title="Mortgage Quest Prototype", layout="wide")

st.title("🏡 Mortgage Quest — Interactive Game Mode Simulator")

# Load the dataset
df = pd.read_csv("us_mortgage_data_fixed.csv")

# Create top navigation
selected_tab = st.navigation(
    items=[
        {"label": "First Timer"},
        {"label": "Family Builder"},
        {"label": "Trade-Up Pro"},
        {"label": "Smart Downsizer"},
        {"label": "Property Investor"}
    ],
    position="top"
)
mode = selected_tab["label"]

# Filter date range with slider
st.sidebar.header("📆 Quarter Range Filter")
start_q, end_q = st.sidebar.select_slider(
    "Select Time Period:",
    options=df["Date"].tolist(),
    value=(df["Date"].iloc[0], df["Date"].iloc[-1])
)
filtered_df = df[df["Date"].between(start_q, end_q)]

# Show Key Metrics
st.subheader(f"🧠 Market Signals for {mode}")
latest_fed = filtered_df["Fed_Rate"].iloc[-1]
latest_delinq = filtered_df["Delinquency_90plus"].iloc[-1]

col1, col2 = st.columns(2)
col1.metric("Fed Rate (Latest)", f"{latest_fed:.2f}%")
col2.metric("90+ Day Delinquency", f"{latest_delinq:.2f}%")

# Game decision logic
st.markdown("### 🎯 Game AI Suggestion")
if latest_fed > 5 or latest_delinq > 4:
    st.error("🚨 Game says: **WAIT 🔴** — High market risk detected")
    st.markdown("💡 *Focus on saving and observing trends. Buying now may be risky.*")
else:
    st.success("✅ Game says: **BUY 🟢** — Favorable conditions")
    st.markdown("💡 *Explore mortgage offers and lock in lower rates if ready.*")

# Plotly chart
st.markdown("### 📈 Economic Trends Over Time")
fig = px.line(filtered_df, x="Date", y=["Fed_Rate", "Delinquency_90plus"],
              labels={"value": "Rate (%)", "variable": "Metric"},
              title="📊 Fed Rate vs. Delinquency Rate Trends")
st.plotly_chart(fig, use_container_width=True)

# Insight Summary
st.info(f"📌 Insight as of **{filtered_df['Date'].iloc[-1]}**: "
        f"Fed Rate is {'rising' if latest_fed > 4 else 'stable'}, "
        f"Delinquency is {'elevated' if latest_delinq > 4 else 'manageable'}.")
