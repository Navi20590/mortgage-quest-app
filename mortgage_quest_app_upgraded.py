import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import scipy.stats as stats

# Page setup
st.set_page_config(page_title="Mortgage Quest", layout="wide")
st.title("🏡 Mortgage Quest — Interactive Game Mode Simulator")
st.markdown("A U.S. housing market simulator built for the NYU Fintech Capstone Project.")

# Sidebar Navigation
selected_tab = st.sidebar.radio("Navigate", ["Home", "📊 Data Trends", "🧡 Simulations", "🔋 Buy or Wait", "🔑 About"])

# HOME TAB
if selected_tab == "Home":
    st.header("Welcome to Mortgage Quest")
    st.markdown("Explore macroeconomic stress, mortgage delinquency, and affordability dynamics interactively.")
    st.image("https://cdn.pixabay.com/photo/2017/01/16/19/40/house-1989912_1280.png", use_container_width=True)

# DATA TRENDS TAB
elif selected_tab == "📊 Data Trends":
    st.header("Delinquency Trends")
    try:
        df = pd.read_csv("final_dataset.csv")
        df["Date"] = pd.to_datetime(df["Date"])

        # Reshape for plotly
        df_melted = df.melt(id_vars="Date", 
                            value_vars=["Mortgage", "Auto", "Student Loan", "Credit Card"], 
                            var_name="Loan Type", 
                            value_name="Delinquency Rate")

        fig = px.line(df_melted, x="Date", y="Delinquency Rate", color="Loan Type", 
                      title="Delinquency Rates by Loan Type")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")

# SIMULATIONS TAB
elif selected_tab == "🧡 Simulations":
    st.header("Stress Test Simulator")
    st.markdown("Adjust macro parameters to simulate default risk.")

    interest_rate = st.slider("Interest Rate (%)", 0.0, 15.0, 5.0)
    unemployment = st.slider("Unemployment Rate (%)", 0.0, 20.0, 6.5)
    inflation = st.slider("Inflation Rate (%)", 0.0, 10.0, 3.0)

    # Simple risk score calculation
    score = (interest_rate * 0.4) + (unemployment * 0.4) + (inflation * 0.2)

    st.metric(label="Risk Score", value=round(score, 2))

    if score > 12:
        st.warning("⚠️ High Risk: Lending may be discouraged in this environment.")
    elif score > 7:
        st.info("Moderate Risk: Proceed with caution.")
    else:
        st.success("Low Risk: Favorable conditions for lending.")

# BUY OR WAIT TAB
elif selected_tab == "🔋 Buy or Wait":
    st.header("Affordability Advisor")
    st.markdown("Estimate if it's better to buy now or wait.")

    home_price = st.number_input("Current Home Price ($)", min_value=50000, max_value=2000000, value=350000)
    down_payment_pct = st.slider("Down Payment (%)", 5, 50, 20)
    rate = st.slider("Mortgage Rate (%)", 2.0, 10.0, 6.5)
    years = st.selectbox("Loan Term (Years)", [15, 20, 25, 30], index=3)

    loan_amount = home_price * (1 - down_payment_pct / 100)
    monthly_rate = rate / 100 / 12
    n_payments = years * 12
    monthly_payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate)**(-n_payments))

    st.metric(label="Estimated Monthly Payment", value=f"${monthly_payment:,.2f}")

# ABOUT TAB
elif selected_tab == "🔑 About":
    st.header("About This App")
    st.markdown("""
    **Mortgage Quest** is a capstone simulation project built to demonstrate interactive modeling of U.S. mortgage market risk and borrower affordability dynamics.

    - Developed by **BEFMNS** Team
    - Built with Streamlit, Plotly, and Python
    - Created as part of the **NYU Stern MS in Fintech** program (2025)
    """)
