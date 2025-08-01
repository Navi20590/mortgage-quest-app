import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# Page setup
st.set_page_config(page_title="🏡 Mortgage Quest Simulator", layout="wide")

# Custom CSS for smoother feel
st.markdown("""
<style>
    .main { background-color: #F4F6F9; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3, h4 { color: #4B4B8C; }
    .metric-label, .stSlider label { font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
menu = st.sidebar.radio("🎮 Navigate Your Quest", ["🏠 Home", "📊 Market Trends", "🎯 Simulation Arena", "💡 Buy or Wait", "ℹ️ About"])

# Load Data
def load_data():
    try:
        df = pd.read_csv("us_mortgage_data_fixed.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        st.warning("Data not found. Please upload or check the dataset.")
        return pd.DataFrame()

# Home Page
if menu == "🏠 Home":
    st.title("🏡 Mortgage Quest: The Game Mode Simulator")
    st.markdown("Welcome, market explorer! Step into your virtual world of U.S. housing dynamics.")
    st.image("https://img.icons8.com/color/96/000000/home--v1.png", width=100)
    st.markdown("Navigate through economic chaos, test survival under market stress, and find out: Should you buy that house?")

# Data Trends Page
elif menu == "📊 Market Trends":
    st.header("📊 Market Trend Radar")
    df = load_data()
    if not df.empty:
        selected_metric = st.selectbox("Select Metric", df.columns[1:])
        chart = alt.Chart(df).mark_line(point=True).encode(
            x='Date:T',
            y=alt.Y(f'{selected_metric}:Q', title=selected_metric.replace("_", " ")),
            tooltip=['Date', selected_metric]
        ).properties(width=900, height=400)
        st.altair_chart(chart, use_container_width=True)
        st.dataframe(df.tail(5))

# Simulation Arena
elif menu == "🎯 Simulation Arena":
    st.header("🎮 Simulate Market Shock")
    col1, col2, col3 = st.columns(3)
    with col1:
        interest_rate = st.slider("🏦 Interest Rate (%)", 0.0, 10.0, 3.5)
    with col2:
        unemployment = st.slider("📉 Unemployment Rate (%)", 0.0, 20.0, 5.0)
    with col3:
        home_index = st.slider("🏠 Home Price Index", 100, 500, 250)

    st.markdown("---")
    st.subheader("🔍 Simulation Outcome")
    if interest_rate > 7 or unemployment > 10:
        st.error("🚨 Market Stress Alert: Conditions resemble a financial crisis. High caution advised.")
    elif interest_rate < 4 and unemployment < 6:
        st.success("✅ Stable Market: This could be a sweet spot for mortgage seekers.")
    else:
        st.warning("⚠️ Moderate Risk: Consider risk mitigation.")

    st.metric("Simulated Interest Rate", f"{interest_rate}%")
    st.metric("Simulated Unemployment", f"{unemployment}%")
    st.metric("Simulated Price Index", f"{home_index}")

# Buy or Wait Page
elif menu == "💡 Buy or Wait":
    st.header("💡 Buy or Wait Decision Engine")
    affordability = st.slider("💰 Affordability Index", 0, 100, 50)
    risk = st.selectbox("📊 Your Risk Appetite", ["Low", "Medium", "High"])
    
    st.markdown("---")
    st.subheader("🏁 Your Personalized Verdict")
    if affordability > 70 and risk != "Low":
        st.success("🏠 Buy Now: Market conditions align with your preferences.")
    else:
        st.warning("⏳ Wait It Out: Monitor trends before making a move.")

# About Page
elif menu == "ℹ️ About":
    st.header("🔎 About Mortgage Quest")
    st.markdown("""
    **Mortgage Quest** is a strategic simulation tool that lets users interact with U.S. mortgage trends,
    test economic stress scenarios, and make data-driven homeownership decisions.

    Developed for the NYU Stern Fintech Capstone by **BEFMNS**, this app blends real-world macroeconomics with gamified decision logic.
    """)

    st.markdown("---")
    st.markdown("🔧 Built with Streamlit | 📊 Data from FRED & NY Fed | 🚀 Simulation powered by Pandas & Altair")
