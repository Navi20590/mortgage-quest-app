import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# Set up the page
st.set_page_config(page_title="Mortgage Quest — Game Mode Simulator", layout="wide")

# Custom CSS for font and styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
            background-color: #f9f9f9;
            color: #333333;
        }

        h1, h2, h3 {
            color: #2c3e50;
        }

        .stButton button {
            background-color: #5e60ce;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: bold;
        }

        .stSlider > div > div {
            background: linear-gradient(90deg, #60a5fa, #4f46e5);
        }

        .css-1v0mbdj, .css-1x8cf1d {
            background-color: #ffffff !important;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
menu = st.sidebar.radio("Navigate", ["🏠 Home", "📊 Data Trends", "💖 Simulations", "💡 Buy or Wait", "🔎 About"])

# Home Page
if menu == "🏠 Home":
    st.title("🏡 Mortgage Quest — Game Mode Simulator")
    st.markdown("A U.S. housing market simulator built for the NYU Fintech Capstone Project.")
    st.header("Welcome to Mortgage Quest")
    st.write("Explore macroeconomic stress, mortgage delinquency, and affordability dynamics interactively.")
    st.image("https://img.icons8.com/color/96/000000/home--v1.png", width=100)

# Data Trends Page
elif menu == "📊 Data Trends":
    st.header("Delinquency Trends")
    try:
        df = pd.read_csv("us_mortgage_data_fixed.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        st.dataframe(df.head())

        line_chart = alt.Chart(df.reset_index()).mark_line().encode(
            x='Date:T',
            y='Delinquency_90plus:Q',
            tooltip=['Date', 'Delinquency_90plus']
        ).properties(
            width=800,
            height=400
        )
        st.altair_chart(line_chart, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Simulations Page
elif menu == "💖 Simulations":
    st.header("Stress Test Simulations")
    interest_rate = st.slider("Interest Rate (%)", 0.0, 10.0, 3.5)
    unemployment_rate = st.slider("Unemployment Rate (%)", 0.0, 20.0, 5.0)
    home_price_index = st.slider("Home Price Index", 100, 500, 250)

    st.subheader("Simulation Results:")
    if interest_rate > 7 or unemployment_rate > 10:
        st.error("🚨 Market Stress Detected! High volatility and risk ahead.")
    elif interest_rate < 4 and unemployment_rate < 6:
        st.success("✅ Green Signal! Market stability supports homeownership.")
    else:
        st.warning("⚠️ Mixed Conditions. Stay alert and monitor closely.")

    st.metric("Interest Rate", f"{interest_rate}%")
    st.metric("Unemployment", f"{unemployment_rate}%")
    st.metric("Price Index", f"{home_price_index}")

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
st.markdown("<p style='text-align: center; color: gray'>🔧 Built using Streamlit | 📊 Data from FRED & NY Fed | 💼 For educational purposes only</p>", unsafe_allow_html=True)
