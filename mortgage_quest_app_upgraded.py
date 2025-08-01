
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Mortgage Quest — Interactive Game Mode Simulator", layout="wide")

# Sidebar navigation
menu = st.sidebar.radio("Navigate", ["🏠 Home", "📊 Data Trends", "💖 Simulations", "💡 Buy or Wait", "🔎 About"])

# Home Page
if menu == "🏠 Home":
    st.title("🏡 Mortgage Quest — Interactive Game Mode Simulator")
    st.markdown("A U.S. housing market simulator built for the NYU Fintech Capstone Project.")
    st.header("Welcome to Mortgage Quest")
    st.write("Explore macroeconomic stress, mortgage delinquency, and affordability dynamics interactively.")
    st.image("https://img.icons8.com/color/96/000000/home--v1.png", width=100)

# Data Trends Page
elif menu == "📊 Data Trends":
    st.header("Delinquency Trends")
    try:
        df = pd.read_csv("us_mortgage_data_fixed.csv")
        st.dataframe(df.head())
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        st.line_chart(df)
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Simulations Page
elif menu == "💖 Simulations":
    st.header("Stress Test Simulations")
    interest_rate = st.slider("Interest Rate (%)", 0.0, 10.0, 3.5)
    unemployment_rate = st.slider("Unemployment Rate (%)", 0.0, 20.0, 5.0)
    home_price_index = st.slider("Home Price Index", 100, 500, 250)
    st.write("Simulation Results:")
    st.write(f"With interest rate at {interest_rate}%, unemployment at {unemployment_rate}%, and home price index at {home_price_index}.")

# Buy or Wait Page
elif menu == "💡 Buy or Wait":
    st.header("📈 Buy or Wait?")
    st.markdown("This section evaluates if it’s a good time to buy a house based on your inputs.")
    affordability_index = st.slider("Affordability Index", 0, 100, 50)
    risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
    if affordability_index > 70 and risk_tolerance != "Low":
        st.success("✅ Buy Recommendation: Market conditions are favorable.")
    else:
        st.warning("⚠️ Wait Recommendation: It might be better to wait.")

# About Page
elif menu == "🔎 About":
    st.header("About the Project")
    st.markdown("""
    **Mortgage Quest** is a multi-modal fintech gaming platform that simulates U.S. homeownership decisions using real economic data.

    Built as part of the NYU Fintech Capstone, this project models real-time market indicators to suggest home-buying strategies.

    **Developed by BEFMNS**
    """)

# Footer
st.markdown("---")
st.markdown("🔧 Built using Streamlit | 📊 Data from FRED & NY Fed | 💼 For educational purposes only")
