import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import json
import math

# ============================================================================
# ENTERPRISE-LEVEL PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="🏡 Mortgage Quest Elite | AI-Powered Real Estate Intelligence",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.mortgagequest.ai/help',
        'Report a bug': "https://www.mortgagequest.ai/bug-report",
        'About': "# Mortgage Quest Elite\nThe most advanced AI-powered real estate platform"
    }
)

# ============================================================================
# PREMIUM ENTERPRISE CSS STYLING
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --danger-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --dark-gradient: linear-gradient(135deg, #2c3e50 0%, #4a6741 100%);
        --glass-bg: rgba(255, 255, 255, 0.25);
        --glass-border: rgba(255, 255, 255, 0.18);
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 400;
        line-height: 1.6;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
        min-height: 100vh;
        position: relative;
    }
    
    .main::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        pointer-events: none;
    }
    
    .block-container {
        padding: 2rem 1rem;
        background: var(--glass-bg);
        border-radius: 25px;
        margin: 20px;
        box-shadow: 
            0 8px 32px 0 rgba(31, 38, 135, 0.37),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header {
        text-align: center;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: clamp(2.5rem, 5vw, 4rem);
        font-weight: 800;
        margin: 2rem 0;
        letter-spacing: -0.02em;
        position: relative;
    }
    
    .hero-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.25rem;
        font-weight: 300;
        margin-bottom: 3rem;
        letter-spacing: 0.01em;
    }
    
    .premium-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px 0 rgba(31, 38, 135, 0.37),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .premium-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .premium-card:hover::before {
        left: 100%;
    }
    
    .premium-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 60px 0 rgba(31, 38, 135, 0.5),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
    }
    
    .metric-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 
            0 8px 32px 0 rgba(31, 38, 135, 0.37),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 15px 45px 0 rgba(31, 38, 135, 0.5),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 600;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-change {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        font-weight: 400;
    }
    
    .status-card {
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        transition: all 0.3s ease;
    }
    
    .status-card:hover {
        transform: translateY(-5px);
    }
    
    .success-card {
        background: var(--success-gradient);
        color: white;
        box-shadow: 0 15px 35px rgba(79, 172, 254, 0.3);
    }
    
    .warning-card {
        background: var(--warning-gradient);
        color: white;
        box-shadow: 0 15px 35px rgba(67, 233, 123, 0.3);
    }
    
    .danger-card {
        background: var(--danger-gradient);
        color: white;
        box-shadow: 0 15px 35px rgba(250, 112, 154, 0.3);
    }
    
    .info-card {
        background: var(--primary-gradient);
        color: white;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    }
    
    .sidebar .sidebar-content {
        background: var(--dark-gradient);
        border-radius: 0 25px 25px 0;
    }
    
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    .progress-bar {
        height: 25px;
        border-radius: 15px;
        background: var(--glass-bg);
        overflow: hidden;
        position: relative;
        margin: 1rem 0;
        border: 1px solid var(--glass-border);
    }
    
    .progress-fill {
        height: 100%;
        background: var(--primary-gradient);
        border-radius: 15px;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background-image: linear-gradient(
            -45deg,
            rgba(255, 255, 255, 0.2) 25%,
            transparent 25%,
            transparent 50%,
            rgba(255, 255, 255, 0.2) 50%,
            rgba(255, 255, 255, 0.2) 75%,
            transparent 75%,
            transparent
        );
        background-size: 50px 50px;
        animation: move 2s linear infinite;
    }
    
    @keyframes move {
        0% { background-position: 0 0; }
        100% { background-position: 50px 50px; }
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 
            0 25px 50px 0 rgba(31, 38, 135, 0.5),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .nav-item {
        margin: 0.5rem 0;
        padding: 1rem;
        border-radius: 15px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
    }
    
    .floating-action {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: var(--secondary-gradient);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 30px rgba(240, 147, 251, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .floating-action:hover {
        transform: scale(1.1) rotate(15deg);
        box-shadow: 0 15px 40px rgba(240, 147, 251, 0.6);
    }
    
    .notification-badge {
        position: absolute;
        top: -5px;
        right: -5px;
        background: #ff4757;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    .glassmorphism-input .stSelectbox > div > div {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 15px;
    }
    
    .glassmorphism-input .stSlider > div > div {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-radius: 15px;
    }
    
    .data-table {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        border: 1px solid var(--glass-border);
        overflow: hidden;
    }
    
    .loading-spinner {
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top: 4px solid #667eea;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .pulse-animation {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .slide-in-animation {
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .block-container {
            margin: 10px;
            padding: 1rem;
        }
        
        .hero-header {
            font-size: 2rem;
        }
        
        .feature-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .metric-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# ENTERPRISE DATA GENERATION & CACHING
# ============================================================================
@st.cache_data(ttl=300)  # Cache for 5 minutes
def generate_enterprise_data():
    """Generate comprehensive, realistic mortgage market data"""
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='D')
    
    # Advanced economic indicators
    base_rate = 3.0
    rate_volatility = np.random.normal(0, 0.02, len(dates))
    rate_trend = base_rate + np.cumsum(rate_volatility)
    rate_trend = np.clip(rate_trend, 1.5, 9.0)
    
    # Correlated unemployment data
    unemployment_base = 4.0
    unemployment_shock = np.where(dates > pd.Timestamp('2022-01-01'), 
                                 np.random.normal(0, 0.5, sum(dates > pd.Timestamp('2022-01-01'))), 0)
    unemployment = unemployment_base + np.cumsum(np.concatenate([
        np.random.normal(0, 0.1, sum(dates <= pd.Timestamp('2022-01-01'))),
        unemployment_shock
    ]))
    unemployment = np.clip(unemployment, 2.5, 18.0)
    
    # Housing price index with realistic trends
    hpi_base = 250
    seasonal_effect = 10 * np.sin(2 * np.pi * dates.dayofyear / 365.25)
    market_cycles = 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 1460)  # 4-year cycle
    hpi_trend = hpi_base + np.cumsum(np.random.normal(0.05, 0.8, len(dates))) + seasonal_effect + market_cycles
    hpi_trend = np.clip(hpi_trend, 180, 450)
    
    # Advanced affordability calculations
    affordability = 100 - (rate_trend * 8) - (unemployment * 3) - ((hpi_trend - 250) * 0.1) + np.random.normal(0, 3, len(dates))
    affordability = np.clip(affordability, 15, 95)
    
    # Market sentiment with regime changes
    sentiment_prob = 1 / (1 + np.exp(-(affordability - 50) / 10))  # Sigmoid function
    sentiment = np.random.choice(['Bullish', 'Neutral', 'Bearish'], len(dates), 
                                p=[0.6, 0.3, 0.1] if np.random.random() > 0.5 else [0.2, 0.3, 0.5])
    
    # Additional enterprise metrics
    construction_permits = 1200 + 200 * np.sin(2 * np.pi * dates.dayofyear / 365.25) + np.cumsum(np.random.normal(0, 20, len(dates)))
    construction_permits = np.clip(construction_permits, 800, 2000)
    
    inventory_levels = 4.5 + np.cumsum(np.random.normal(0, 0.1, len(dates)))
    inventory_levels = np.clip(inventory_levels, 1.5, 8.0)
    
    price_per_sqft = 150 + (hpi_trend - 250) * 0.5 + np.random.normal(0, 5, len(dates))
    price_per_sqft = np.clip(price_per_sqft, 100, 300)
    
    df = pd.DataFrame({
        'Date': dates,
        'Mortgage_Rate': rate_trend,
        'Unemployment_Rate': unemployment,
        'Home_Price_Index': hpi_trend,
        'Affordability_Index': affordability,
        'Market_Sentiment': sentiment,
        'Construction_Permits': construction_permits,
        'Inventory_Months': inventory_levels,
        'Price_Per_SqFt': price_per_sqft,
        'Market_Velocity': np.random.uniform(0.5, 2.5, len(dates)),
        'Investment_Grade': np.random.choice(['A+', 'A', 'A-', 'B+', 'B', 'B-'], len(dates))
    })
    
    return df

@st.cache_data
def calculate_market_metrics(df):
    """Calculate advanced market analytics"""
    latest = df.iloc[-1]
    prev_month = df.iloc[-30]
    prev_year = df.iloc[-365] if len(df) > 365 else df.iloc[0]
    
    metrics = {
        'current_rate': latest['Mortgage_Rate'],
        'rate_change_month': latest['Mortgage_Rate'] - prev_month['Mortgage_Rate'],
        'rate_change_year': latest['Mortgage_Rate'] - prev_year['Mortgage_Rate'],
        'unemployment': latest['Unemployment_Rate'],
        'unemployment_change': latest['Unemployment_Rate'] - prev_month['Unemployment_Rate'],
        'hpi': latest['Home_Price_Index'],
        'hpi_change': ((latest['Home_Price_Index'] - prev_year['Home_Price_Index']) / prev_year['Home_Price_Index']) * 100,
        'affordability': latest['Affordability_Index'],
        'market_health': 'Excellent' if latest['Affordability_Index'] > 70 else 'Good' if latest['Affordability_Index'] > 50 else 'Fair' if latest['Affordability_Index'] > 30 else 'Poor',
        'trend_direction': 'Rising' if latest['Mortgage_Rate'] > prev_month['Mortgage_Rate'] else 'Falling',
        'volatility': df['Mortgage_Rate'].tail(30).std(),
        'momentum': np.mean(df['Mortgage_Rate'].tail(7)) - np.mean(df['Mortgage_Rate'].tail(30))
    }
    
    return metrics

# ============================================================================
# ADVANCED SIDEBAR NAVIGATION WITH ANALYTICS
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="background: linear-gradient(45deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.5rem; font-weight: 800;">
            🏡 MORTGAGE QUEST ELITE
        </h1>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">AI-Powered Real Estate Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation with modern icons
    menu_options = {
        "🎯 Command Center": "command",
        "📊 Market Intelligence": "intelligence", 
        "🧠 AI Scenario Lab": "scenarios",
        "💎 Decision Engine": "decisions",
        "📈 Portfolio Suite": "portfolio",
        "🔬 Analytics Hub": "analytics",
        "⚙️ System Config": "config",
        "ℹ️ Enterprise Info": "about"
    }
    
    menu = st.radio("Navigate:", list(menu_options.keys()), key="main_nav")
    selected_page = menu_options[menu]
    
    st.markdown("---")
    
    # Real-time system status
    st.markdown("### ⚡ System Status")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background: rgba(0,255,0,0.2); padding: 0.5rem; border-radius: 10px; text-align: center;">
            <div style="color: #00ff00; font-size: 0.8rem;">🟢 LIVE</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(0,255,255,0.2); padding: 0.5rem; border-radius: 10px; text-align: center;">
            <div style="color: #00ffff; font-size: 0.8rem;">⚡ FAST</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick controls
    st.markdown("### 🎮 Quick Controls")
    real_time_updates = st.toggle("🔄 Real-time Data", value=True)
    advanced_mode = st.toggle("🔬 Expert Mode", value=False)
    notifications = st.toggle("🔔 Alerts", value=True)
    
    # Market health indicator
    df = generate_enterprise_data()
    metrics = calculate_market_metrics(df)
    
    st.markdown("### 🏥 Market Health")
    health_color = "#4facfe" if metrics['market_health'] == 'Excellent' else "#43e97b" if metrics['market_health'] == 'Good' else "#feca57" if metrics['market_health'] == 'Fair' else "#ff6b6b"
    
    st.markdown(f"""
    <div style="background: {health_color}20; border: 1px solid {health_color}40; padding: 1rem; border-radius: 15px; text-align: center;">
        <div style="color: {health_color}; font-weight: 600;">{metrics['market_health']}</div>
        <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem;">{metrics['affordability']:.0f}/100</div>
    </div>
    """, unsafe_allow_html=True)

# Load enterprise data
df = generate_enterprise_data()
metrics = calculate_market_metrics(df)
latest_data = df.iloc[-1]

# ============================================================================
# COMMAND CENTER - ENTERPRISE DASHBOARD
# ============================================================================
if selected_page == "command":
    st.markdown('<h1 class="hero-header slide-in-animation">🎯 Mission Control Center</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Real-time market intelligence at your fingertips</p>', unsafe_allow_html=True)
    
    # Live market alerts
    if notifications:
        alert_col1, alert_col2, alert_col3 = st.columns(3)
        
        with alert_col1:
            if abs(metrics['rate_change_month']) > 0.25:
                st.markdown(f"""
                <div class="status-card danger-card pulse-animation">
                    <h4>🚨 Rate Alert</h4>
                    <p>Significant rate movement detected</p>
                    <strong>{metrics['rate_change_month']:+.2f}% this month</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with alert_col2:
            if metrics['volatility'] > 0.5:
                st.markdown(f"""
                <div class="status-card warning-card pulse-animation">
                    <h4>⚠️ Volatility Warning</h4>
                    <p>High market volatility</p>
                    <strong>{metrics['volatility']:.2f}% std dev</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with alert_col3:
            if latest_data['Affordability_Index'] < 40:
                st.markdown(f"""
                <div class="status-card info-card pulse-animation">
                    <h4>📊 Affordability Alert</h4>
                    <p>Low affordability conditions</p>
                    <strong>{latest_data['Affordability_Index']:.0f}/100</strong>
                </div>
                """, unsafe_allow_html=True)
    
    # Premium KPI Dashboard
    st.markdown("### 📊 Executive KPI Dashboard")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    
    with kpi_col1:
        st.markdown(f"""
        <div class="metric-card slide-in-animation">
            <div class="metric-label">🏦 Mortgage Rate</div>
            <div class="metric-value">{metrics['current_rate']:.2f}%</div>
            <div class="metric-change">{metrics['rate_change_month']:+.2f}% MTD</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {min(100, metrics['current_rate']*10)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col2:
        st.markdown(f"""
        <div class="metric-card slide-in-animation">
            <div class="metric-label">📉 Unemployment</div>
            <div class="metric-value">{metrics['unemployment']:.1f}%</div>
            <div class="metric-change">{metrics['unemployment_change']:+.1f}% MTD</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {min(100, metrics['unemployment']*5)}%;
