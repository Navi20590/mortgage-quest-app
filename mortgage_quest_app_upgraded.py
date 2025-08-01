import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Mortgage Quest – Interactive Game Mode Simulator", layout="wide")

# Sidebar navigation
st.sidebar.title("🔍 Navigate")
page = st.sidebar.radio("", ["Home", "📊 Data Trends", "💖 Simulations", "💡 Buy or Wait", "🔎 About"])

# Load data safely
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("final_dataset.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Page: Home
if page == "Home":
    st.markdown("<h1>🏠 Mortgage Quest — Interactive Game Mode Simulator</h1>", unsafe_allow_html=True)
    st.write("A U.S. housing market simulator built for the NYU Fintech Capstone Project.")
    st.markdown("### Welcome to Mortgage Quest")
    st.write("Explore macroeconomic stress, mortgage delinquency, and affordability dynamics interactively.")
    st.image("https://cdn.pixabay.com/photo/2017/01/16/19/40/house-1989912_1280.png", use_column_width=True)

# Page: Data Trends
elif page == "📊 Data Trends":
    st.header("Delinquency Trends")
    df = load_data()
    if df is not None and "Quarter" in df.columns:
        fig = px.line(df, 
                      x="Quarter", 
                      y=["Mortgage", "Auto", "Student Loan", "Credit Card"],
                      labels={"value": "Delinquency Rate", "variable": "Loan Type"},
                      title="Delinquency Rates by Loan Type")
        st.plotly_chart(fig, use_container_width=True)

# Page: Simulations (Placeholder for now)
elif page == "💖 Simulations":
    st.header("Simulation Tools")
    st.info("Interactive simulation features coming soon!")

# Page: Buy or Wait (Placeholder)
elif page == "💡 Buy or Wait":
    st.header("Should You Buy Now or Wait?")
    st.warning("Decision tool under development. Stay tuned!")

# Page: About
elif page == "🔎 About":
    st.header("About This App")
    st.markdown("""
    **Mortgage Quest** is an interactive housing credit risk simulator developed for academic and research purposes.  
    Developed by **BEFMNS** as part of the NYU Fintech Capstone Project (2025).  
    Uses publicly available U.S. delinquency and credit data to simulate decision-making environments.
    """)
