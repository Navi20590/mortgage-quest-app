import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="Mortgage Quest", layout="wide")

# Title
st.title("🏡 Mortgage Quest — Interactive Game Mode Simulator")
st.markdown("A U.S. housing market simulator built for the NYU Fintech Capstone Project.")

# Tabs for navigation
tabs = st.tabs(["🏠 Home", "📊 Data Trends", "🧪 Simulations", "💡 Buy or Wait", "ℹ️ About"])

# ----- HOME -----
with tabs[0]:
    st.subheader("Welcome to Mortgage Quest")
    st.markdown("Explore macroeconomic stress, mortgage delinquency, and affordability dynamics interactively.")
   st.image("https://cdn.pixabay.com/photo/2017/01/16/19/40/house-1989912_1280.png", use_container_width=True)

# ----- DATA TRENDS -----
with tabs[1]:
    st.subheader("U.S. Mortgage Delinquency & Macro Trends")
    uploaded_file = "us_mortgage_data_fixed.csv"

    try:
        df = pd.read_csv(uploaded_file)
        df['Date'] = pd.to_datetime(df['Date'])

        selected_column = st.selectbox("Choose a metric to visualize", df.columns[1:])
        fig = px.line(df, x='Date', y=selected_column, title=f"{selected_column} Over Time")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")

# ----- SIMULATIONS -----
with tabs[2]:
    st.subheader("Macroeconomic Shock Simulator")

    rate_hike = st.slider("📈 Fed Rate (%)", 0.0, 10.0, 5.0)
    unemployment = st.slider("💼 Unemployment Rate (%)", 0.0, 20.0, 6.5)
    rent_index = st.slider("🏠 Rent Index (Base 100)", 80, 200, 120)

    risk_score = (rate_hike * 0.4) + (unemployment * 0.4) + ((rent_index - 100) * 0.2)
    st.metric("📉 Simulated Risk Score", round(risk_score, 2))

    if risk_score >= 15:
        st.error("⚠️ High Risk: Mortgage instability likely.")
    elif risk_score >= 8:
        st.warning("⚠️ Moderate Risk: Monitor closely.")
    else:
        st.success("✅ Low Risk: Market appears stable.")

# ----- BUY OR WAIT -----
with tabs[3]:
    st.subheader("📌 Should You Buy or Wait?")

    income = st.number_input("Your Monthly Income (₹)", value=75000)
    emi = st.number_input("Expected Monthly EMI (₹)", value=25000)
    inflation = st.slider("Expected Inflation (%)", 0.0, 10.0, 4.5)

    affordability = (income - emi) / income * 100 - inflation
    st.metric("📊 Affordability Index", round(affordability, 2))

    if affordability > 25:
        st.success("👍 Buy — Market looks affordable for you.")
    else:
        st.warning("⏳ Wait — Reassess affordability or lower EMI burden.")

# ----- ABOUT -----
with tabs[4]:
    st.subheader("About the Project")
    st.markdown("""
    - **Mortgage Quest** is a fintech simulation tool designed to help users understand how macroeconomic factors like interest rates, rent, and employment affect mortgage performance and homebuying decisions.
    - It allows interactive visualizations and real-time scenario analysis using real U.S. housing & delinquency datasets (2020–2025).
    
    ---
    📌 Developed by **BEFMNS**  
    🏫 NYU Stern MS Fintech | Capstone Project 2025
    """)
