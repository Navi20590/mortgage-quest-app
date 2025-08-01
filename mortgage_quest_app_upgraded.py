import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(
    page_title="Mortgage Quest — Interactive Game Mode Simulator",
    layout="wide"
)

# Title
st.title("🏠 Mortgage Quest — Interactive Game Mode Simulator")
st.markdown("A U.S. housing market simulator built for the NYU Fintech Capstone Project.")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("us_mortgage_data_fixed.csv")  # Make sure this file is in your repo
    return df

df = load_data()

# Tabs
tabs = st.tabs(["🏠 Home", "📊 Data Trends", "🧮 Simulations", "💡 Buy or Wait", "ℹ️ About"])

# --- Home Tab ---
with tabs[0]:
    st.subheader("Welcome to Mortgage Quest")
    st.write("Explore macroeconomic stress, mortgage delinquency, and affordability dynamics interactively.")
    st.image("https://images.unsplash.com/photo-1560185127-6ed189bf02bb")  # Optional: aesthetic

# --- Data Trends Tab ---
with tabs[1]:
    st.subheader("📊 Mortgage & Delinquency Trends")
    st.write("Visualizing trends from 2020 to 2025")
    
    selected_metric = st.selectbox("Select Metric", df.columns[1:])
    fig = px.line(df, x="Date", y=selected_metric, title=f"{selected_metric} Over Time")
    st.plotly_chart(fig, use_container_width=True)

# --- Simulations Tab ---
with tabs[2]:
    st.subheader("🧮 Economic Stress Simulation")
    fed_rate = st.slider("Simulated Fed Rate (%)", 0.0, 10.0, 5.0)
    income = st.slider("Median Income ($)", 20000, 120000, 60000)
    rent = st.slider("Median Rent ($)", 500, 4000, 1500)

    affordability_index = income / rent
    st.metric("Affordability Index", round(affordability_index, 2))

# --- Buy or Wait Tab ---
with tabs[3]:
    st.subheader("💡 Should You BUY or WAIT?")
    if affordability_index > 3:
        st.success("📈 Market seems affordable → Recommended: **BUY**")
    elif affordability_index > 2:
        st.warning("⚖️ Borderline case → Recommended: **WAIT and Watch**")
    else:
        st.error("📉 Market is tight → Recommended: **WAIT**")

# --- About Tab ---
with tabs[4]:
    st.subheader("ℹ️ About This Project")
    st.markdown("""
    **Mortgage Quest** is a fintech simulation tool designed for the NYU Stern Fintech Capstone.  
    It uses real U.S. economic data to model how consumers might decide between **buying** or **waiting** in the housing market.

    **Developed by:** BEFMNS  
    **Year:** 2025  
    """)
