import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# Set wide layout
st.set_page_config(layout="wide")

# Navigation
selected_tab = st.sidebar.radio(
    "Navigate",
    ["Home", "📊 Data Trends", "🧪 Simulations", "💡 Buy or Wait", "ℹ️ About"]
)

# Home tab
if selected_tab == "Home":
    st.title("🏠 Mortgage Quest — Interactive Game Mode Simulator")
    st.markdown("Explore macroeconomic stress, mortgage delinquency, and affordability dynamics interactively.")
    st.image(
        "https://cdn.pixabay.com/photo/2017/01/16/19/40/house-1989912_1280.png",
        use_container_width=True
    )

# Data Trends tab
elif selected_tab == "📊 Data Trends":
    st.header("📈 U.S. Mortgage Delinquency Trends (2020–2025)")
    
    df = pd.read_csv("us_mortgage_data_fixed.csv")
    df['Date'] = pd.to_datetime(df['Date'])

    fig = px.line(df, x="Date", y=["Mortgage", "Auto", "Student Loan", "Credit Card"],
                  labels={"value": "Delinquency Rate", "variable": "Loan Type"},
                  title="Delinquency Rates by Loan Type")
    st.plotly_chart(fig, use_container_width=True)

# Simulations tab
elif selected_tab == "🧪 Simulations":
    st.header("🧪 Macro Simulation Engine")

    fed_rate = st.slider("📉 Fed Interest Rate (%)", 0.0, 10.0, 3.5, step=0.25)
    income = st.slider("👩‍💼 Median Household Income ($)", 20000, 120000, 60000, step=5000)
    rent = st.slider("🏘️ Average Monthly Rent ($)", 500, 4000, 1800, step=100)

    stress_score = (fed_rate * 2) + (4000 - rent) / 200 + (100000 - income) / 10000
    st.metric("Simulated Stress Score", round(stress_score, 2))

# Buy or Wait tab
elif selected_tab == "💡 Buy or Wait":
    st.header("💡 Affordability Signal Engine")

    income_input = st.number_input("👩‍💼 Monthly Income ($)", min_value=1000, value=5000, step=100)
    rent_input = st.number_input("🏘️ Monthly Housing Cost ($)", min_value=500, value=1800, step=50)

    ratio = rent_input / income_input

    if ratio < 0.3:
        st.success("✅ It's a good time to BUY!")
    elif 0.3 <= ratio <= 0.4:
        st.info("🤔 Consider WAITING or evaluating further.")
    else:
        st.warning("🚫 Better to WAIT. Affordability is stressed.")

# About tab
elif selected_tab == "ℹ️ About":
    st.header("ℹ️ About This App")
    st.markdown("""
    **Mortgage Quest** is a U.S. housing market simulator built for the NYU Fintech Capstone Project.  
    It lets users explore delinquency rates, simulate macro stress scenarios, and test housing affordability using real datasets.  
    \nBuilt with Streamlit using Python, Plotly, and open-source mortgage datasets (2020–2025).
    \n\n👨‍💻 Developed by **BEFMNS**
    """)
