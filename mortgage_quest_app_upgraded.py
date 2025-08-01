import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Mortgage Quest — Interactive Game Mode Simulator", layout="wide")

# Sidebar navigation
menu = st.sidebar.radio("Navigate", ["🏠 Home", "📊 Data Trends", "💖 Simulations", "💡 Buy or Wait", "🔎 About"])

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("us_mortgage_data_fixed.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# 🏠 Home Page
if menu == "🏠 Home":
    st.title("🏡 Mortgage Quest — Interactive Game Mode Simulator")
    st.markdown("A U.S. housing market simulator built for the NYU Fintech Capstone Project.")
    st.subheader("Welcome to Mortgage Quest")
    st.write("Explore macroeconomic stress, mortgage delinquency, and affordability dynamics interactively.")
    st.image("https://img.icons8.com/color/96/000000/home--v1.png", width=100)

# 📊 Data Trends
elif menu == "📊 Data Trends":
    st.header("📉 Delinquency & Rate Trends")
    st.dataframe(df[['Date', 'Fed_Rate', 'Delinquency_90plus']].head())

    # Plotting
    chart_data = df.set_index('Date')[['Delinquency_90plus', 'Fed_Rate']]
    st.line_chart(chart_data)

    # Low delinquency filter
    st.subheader("🔍 Explore Quarters with Delinquency < 2%")
    low_delinquency = df[df['Delinquency_90plus'] < 2]
    if not low_delinquency.empty:
        selected_quarter = st.selectbox("Select Quarter", low_delinquency['Date'].dt.strftime("%Y-%q"))
        st.write(low_delinquency[low_delinquency['Date'].dt.strftime("%Y-%q") == selected_quarter])
    else:
        st.info("No quarters found with delinquency below 2%.")

# 💖 Simulations Page
elif menu == "💖 Simulations":
    st.header("🎯 Run a Stress Test Simulation")
    st.markdown("Adjust macroeconomic sliders to simulate market stress")

    # User Inputs
    col1, col2, col3 = st.columns(3)
    with col1:
        interest_rate = st.slider("📈 Interest Rate (%)", 0.0, 10.0, 4.5)
    with col2:
        unemployment_rate = st.slider("📉 Unemployment Rate (%)", 0.0, 20.0, 6.0)
    with col3:
        hpi = st.slider("🏡 Home Price Index", 100, 500, 250)

    st.subheader("🧠 AI Stress Signal Recommendation")
    if interest_rate < 3 and unemployment_rate < 5 and hpi < 300:
        st.success("✅ Status: BUY — Market shows resilience and affordability.")
    elif interest_rate > 6 or unemployment_rate > 10:
        st.error("⛔ Status: WAIT — High risk due to economic stress.")
    else:
        st.warning("⚠️ Status: NEUTRAL — Watch the market closely.")

# 💡 Buy or Wait Logic
elif menu == "💡 Buy or Wait":
    st.header("📊 Should You Buy Now?")
    affordability = st.slider("Affordability Index", 0, 100, 50)
    risk = st.selectbox("Your Risk Tolerance", ["Low", "Medium", "High"])

    st.markdown("#### Recommendation")
    if affordability >= 70 and risk in ["Medium", "High"]:
        st.success("👍 Suggestion: BUY — Market conditions look favorable.")
    elif affordability < 40 and risk == "Low":
        st.error("👎 Suggestion: WAIT — Risk may outweigh benefits.")
    else:
        st.warning("⏳ Suggestion: Review all indicators before deciding.")

# 🔎 About
elif menu == "🔎 About":
    st.header("📘 About the Project")
    st.markdown("""
    **Mortgage Quest** is a multi-modal fintech gaming platform that simulates U.S. homeownership decisions using real economic data.

    🧠 Combines macroeconomic indicators, credit risk, and affordability analysis  
    💡 Helps users decide when to buy or wait using visual & interactive logic  
    🚀 Built using Streamlit, pandas, matplotlib  
    🧪 Developed by **BEFMNS** for NYU Fintech Capstone  
    """)

# Footer
st.markdown("---")
st.caption("🔧 Built using Streamlit | 📊 Data from FRED & NY Fed | 🧪 For educational purposes only")
