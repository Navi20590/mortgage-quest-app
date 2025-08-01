import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Mortgage Quest – Interactive Game Mode Simulator", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("us_mortgage_data_fixed.csv")

df = load_data()

# Sidebar
st.sidebar.title("Navigate")
selection = st.sidebar.radio("Go to", ["🏠 Home", "📊 Data Trends", "💖 Simulations", "💡 Buy or Wait", "🔍 About"])

# Home Page
if selection == "🏠 Home":
    st.title("🏡 Mortgage Quest — Interactive Game Mode Simulator")
    st.markdown("A U.S. housing market simulator built for the NYU Fintech Capstone Project.")
    st.subheader("Welcome to Mortgage Quest")
    st.markdown("Explore macroeconomic stress, mortgage delinquency, and affordability dynamics interactively.")
    st.image("https://img.icons8.com/?size=512&id=81297&format=png", width=80)

# Data Trends Page
elif selection == "📊 Data Trends":
    st.title("Delinquency Trends")

    if "Date" in df.columns and "Delinquency_90plus" in df.columns and "Fed_Rate" in df.columns:
        st.dataframe(df[["Date", "Fed_Rate", "Delinquency_90plus"]].head())

        # Line Chart
        fig, ax = plt.subplots()
        ax.plot(pd.to_datetime(df["Date"]), df["Delinquency_90plus"], label="Delinquency_90plus")
        ax.plot(pd.to_datetime(df["Date"]), df["Fed_Rate"], label="Fed_Rate")
        ax.set_title("Delinquency vs Fed Rate Over Time")
        ax.set_ylabel("Rate (%)")
        ax.legend()
        st.pyplot(fig)

        # Explore Low Delinquency Quarters
        st.subheader("📉 Explore Low Delinquency Quarters (Below 2%)")
        low_delinquency_df = df[df["Delinquency_90plus"] < 2]

        if not low_delinquency_df.empty:
            selected_quarter = st.selectbox("Select a quarter", low_delinquency_df["Date"].tolist())
            st.write("**Details for selected quarter:**")
            st.dataframe(low_delinquency_df[low_delinquency_df["Date"] == selected_quarter])

            with st.expander("See all quarters with Delinquency < 2%"):
                st.dataframe(low_delinquency_df)
        else:
            st.warning("No quarters found with Delinquency_90plus less than 2%.")
    else:
        st.error("Error loading data: Required columns not found.")

# Simulations Page
elif selection == "💖 Simulations":
    st.title("Simulate Mortgage Scenarios")
    st.markdown("Coming soon: Choose your role, apply macroeconomic shocks, and see impacts on mortgage outcomes.")

# Buy or Wait Logic
elif selection == "💡 Buy or Wait":
    st.title("Buy or Wait Signal")
    latest = df.tail(1)
    fed = latest["Fed_Rate"].values[0]
    delq = latest["Delinquency_90plus"].values[0]

    if fed < 3 and delq < 2:
        signal = "BUY 🟢"
        comment = "Favorable macro conditions and low mortgage stress suggest it's a good time to buy."
    else:
        signal = "WAIT 🔴"
        comment = "High rates or stress detected. Better to wait and monitor trends."

    st.metric("Signal", signal)
    st.markdown(f"**Reasoning:** {comment}")

# About Page
elif selection == "🔍 About":
    st.title("About")
    st.markdown("""
    **Mortgage Quest** is an NYU Stern Fintech capstone simulation project built to model U.S. mortgage market behavior
    using delinquency, interest rate, and affordability data.
    
    Developed by **BEFMNS Team**.
    """)
