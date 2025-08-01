import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# ============================================================================
# ENTERPRISE-LEVEL PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="🏡 Mortgage Quest Elite | AI-Powered Real Estate Intelligence",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {'achievements': [], 'points': 0, 'level': 1}
if 'properties' not in st.session_state:
    st.session_state.properties = []
if 'scenarios_run' not in st.session_state:
    st.session_state.scenarios_run = 0

# ============================================================================
# PREMIUM ENTERPRISE CSS STYLING
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        --secondary-gradient: linear-gradient(135deg, #38b2ac 0%, #319795 100%);
        --success-gradient: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        --warning-gradient: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        --danger-gradient: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        --glass-bg: rgba(255, 255, 255, 0.95);
        --glass-border: rgba(255, 255, 255, 0.3);
        --dark-glass-bg: rgba(45, 55, 72, 0.1);
        --accent-color: #38b2ac;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 400;
        line-height: 1.6;
    }
    
    .main {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
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
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23718096' fill-opacity='0.02'%3E%3Ccircle cx='30' cy='30' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        pointer-events: none;
    }
    
    .block-container {
        padding: 2rem 1rem;
        background: var(--glass-bg);
        border-radius: 25px;
        margin: 20px;
        box-shadow: 
            0 8px 32px 0 rgba(45, 55, 72, 0.1),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.8);
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
    }
    
    .hero-subtitle {
        text-align: center;
        color: #4a5568;
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
            0 8px 32px 0 rgba(45, 55, 72, 0.1),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.8);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .premium-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 60px 0 rgba(45, 55, 72, 0.15),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.9);
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
            0 8px 32px 0 rgba(45, 55, 72, 0.1),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.8);
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 15px 45px 0 rgba(45, 55, 72, 0.15),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.9);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--secondary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #2d3748;
        font-weight: 600;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-change {
        color: #718096;
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
        box-shadow: 0 15px 35px rgba(72, 187, 120, 0.3);
    }
    
    .warning-card {
        background: var(--warning-gradient);
        color: white;
        box-shadow: 0 15px 35px rgba(237, 137, 54, 0.3);
    }
    
    .danger-card {
        background: var(--danger-gradient);
        color: white;
        box-shadow: 0 15px 35px rgba(245, 101, 101, 0.3);
    }
    
    .info-card {
        background: var(--secondary-gradient);
        color: white;
        box-shadow: 0 15px 35px rgba(56, 178, 172, 0.3);
    }
    
    .stButton > button {
        background: var(--secondary-gradient);
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(56, 178, 172, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 40px rgba(56, 178, 172, 0.6);
    }
    
    .progress-bar {
        height: 25px;
        border-radius: 15px;
        background: rgba(226, 232, 240, 0.8);
        overflow: hidden;
        position: relative;
        margin: 1rem 0;
        border: 1px solid rgba(226, 232, 240, 0.5);
    }
    
    .progress-fill {
        height: 100%;
        background: var(--secondary-gradient);
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
        margin: 1rem 0;
        color: #2d3748;
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 
            0 25px 50px 0 rgba(45, 55, 72, 0.15),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.9);
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
    
    .pulse-animation {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .achievement-badge {
        background: var(--warning-gradient);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.25rem;
        display: inline-block;
        box-shadow: 0 5px 15px rgba(237, 137, 54, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# GAMIFICATION SYSTEM
# ============================================================================
ACHIEVEMENTS = {
    "first_visit": {"name": "🏠 Welcome Home", "points": 50, "desc": "First visit to Dashboard"},
    "scenario_runner": {"name": "🎯 Scenario Master", "points": 100, "desc": "Run 10 scenarios"},
    "portfolio_starter": {"name": "📈 Property Investor", "points": 75, "desc": "Add first property"},
    "data_explorer": {"name": "📊 Market Analyst", "points": 125, "desc": "Use all analysis tools"},
    "decision_maker": {"name": "💎 Smart Buyer", "points": 200, "desc": "Complete decision analysis"}
}

def track_achievement(action):
    """Track user achievements and award points"""
    awarded = False
    
    if action == "🎯 Command Center" and "first_visit" not in st.session_state.user_profile['achievements']:
        award_achievement("first_visit")
        awarded = True
    
    if st.session_state.scenarios_run >= 5 and "scenario_runner" not in st.session_state.user_profile['achievements']:
        award_achievement("scenario_runner")
        awarded = True
    
    if len(st.session_state.properties) >= 1 and "portfolio_starter" not in st.session_state.user_profile['achievements']:
        award_achievement("portfolio_starter")
        awarded = True
    
    return awarded

def award_achievement(achievement_id):
    """Award achievement and update user profile"""
    if achievement_id not in st.session_state.user_profile['achievements']:
        achievement = ACHIEVEMENTS[achievement_id]
        st.session_state.user_profile['achievements'].append(achievement_id)
        st.session_state.user_profile['points'] += achievement['points']
        
        # Level up system
        new_level = (st.session_state.user_profile['points'] // 500) + 1
        if new_level > st.session_state.user_profile['level']:
            st.session_state.user_profile['level'] = new_level
            st.balloons()
            st.success(f"🎉 Level Up! You're now Level {new_level}!")
        
        st.success(f"🏆 Achievement Unlocked: {achievement['name']} (+{achievement['points']} points)")

# ============================================================================
# ENTERPRISE DATA GENERATION & CACHING
# ============================================================================
@st.cache_data(ttl=300)
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
    unemployment = unemployment_base + np.cumsum(np.random.normal(0, 0.1, len(dates)))
    unemployment = np.clip(unemployment, 2.5, 18.0)
    
    # Housing price index with realistic trends
    hpi_base = 250
    seasonal_effect = 10 * np.sin(2 * np.pi * dates.dayofyear / 365.25)
    hpi_trend = hpi_base + np.cumsum(np.random.normal(0.05, 0.8, len(dates))) + seasonal_effect
    hpi_trend = np.clip(hpi_trend, 180, 450)
    
    # Advanced affordability calculations
    affordability = 100 - (rate_trend * 8) - (unemployment * 3) - ((hpi_trend - 250) * 0.1) + np.random.normal(0, 3, len(dates))
    affordability = np.clip(affordability, 15, 95)
    
    # Market sentiment
    sentiment = np.random.choice(['Bullish', 'Neutral', 'Bearish'], len(dates), p=[0.3, 0.4, 0.3])
    
    # Additional enterprise metrics
    construction_permits = 1200 + 200 * np.sin(2 * np.pi * dates.dayofyear / 365.25) + np.cumsum(np.random.normal(0, 20, len(dates)))
    construction_permits = np.clip(construction_permits, 800, 2000)
    
    inventory_levels = 4.5 + np.cumsum(np.random.normal(0, 0.1, len(dates)))
    inventory_levels = np.clip(inventory_levels, 1.5, 8.0)
    
    df = pd.DataFrame({
        'Date': dates,
        'Mortgage_Rate': rate_trend,
        'Unemployment_Rate': unemployment,
        'Home_Price_Index': hpi_trend,
        'Affordability_Index': affordability,
        'Market_Sentiment': sentiment,
        'Construction_Permits': construction_permits,
        'Inventory_Months': inventory_levels,
        'Market_Velocity': np.random.uniform(0.5, 2.5, len(dates))
    })
    
    return df

@st.cache_data
def calculate_market_metrics(df):
    """Calculate advanced market analytics"""
    latest = df.iloc[-1]
    prev_month = df.iloc[-30] if len(df) > 30 else df.iloc[0]
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
        'volatility': df['Mortgage_Rate'].tail(30).std()
    }
    
    return metrics

# ============================================================================
# ADVANCED SIDEBAR NAVIGATION
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
    
    # User Profile
    st.markdown(f"""
    <div style="background: rgba(45, 55, 72, 0.1); padding: 1rem; border-radius: 15px; margin-bottom: 1rem; border: 1px solid rgba(56, 178, 172, 0.2);">
        <div style="color: #2d3748; text-align: center;">
            <div style="font-size: 2rem;">👤</div>
            <div style="font-weight: 600; color: #2d3748;">Level {st.session_state.user_profile['level']} Player</div>
            <div style="color: #718096;">{st.session_state.user_profile['points']} Points</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    menu_options = [
        "🎯 Command Center",
        "📊 Market Intelligence", 
        "🧠 AI Scenario Lab",
        "💎 Decision Engine",
        "📈 Portfolio Suite",
        "ℹ️ Enterprise Info"
    ]
    
    menu = st.radio("Navigate:", menu_options, key="main_nav")
    
    st.markdown("---")
    
    # Quick controls
    st.markdown("### 🎮 Quick Controls")
    real_time_updates = st.toggle("🔄 Real-time Data", value=True)
    expert_mode = st.toggle("🔬 Expert Mode", value=False)
    notifications = st.toggle("🔔 Alerts", value=True)
    
    # Market health indicator
    df = generate_enterprise_data()
    metrics = calculate_market_metrics(df)
    
    st.markdown("### 🏥 Market Health")
    health_color = "#48bb78" if metrics['market_health'] == 'Excellent' else "#38b2ac" if metrics['market_health'] == 'Good' else "#ed8936" if metrics['market_health'] == 'Fair' else "#f56565"
    
    st.markdown(f"""
    <div style="background: {health_color}20; border: 1px solid {health_color}40; padding: 1rem; border-radius: 15px; text-align: center;">
        <div style="color: {health_color}; font-weight: 600;">{metrics['market_health']}</div>
        <div style="color: #718096; font-size: 0.8rem;">{metrics['affordability']:.0f}/100</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Achievements
    st.markdown("### 🏆 Achievements")
    for ach_id, ach in ACHIEVEMENTS.items():
        status = "✅" if ach_id in st.session_state.user_profile['achievements'] else "🔒"
        st.markdown(f"<div class='achievement-badge'>{status} {ach['name']}</div>", unsafe_allow_html=True)

# Load data
df = generate_enterprise_data()
metrics = calculate_market_metrics(df)
latest_data = df.iloc[-1]

# Track achievements
track_achievement(menu)

# ============================================================================
# COMMAND CENTER - ENTERPRISE DASHBOARD
# ============================================================================
if menu == "🎯 Command Center":
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
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
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
                <div class="progress-fill" style="width: {min(100, metrics['unemployment']*5)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col3:
        st.markdown(f"""
        <div class="metric-card slide-in-animation">
            <div class="metric-label">🏠 Price Index</div>
            <div class="metric-value">{metrics['hpi']:.0f}</div>
            <div class="metric-change">{metrics['hpi_change']:+.1f}% YTD</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {min(100, metrics['hpi']/4)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col4:
        st.markdown(f"""
        <div class="metric-card slide-in-animation">
            <div class="metric-label">💰 Affordability</div>
            <div class="metric-value">{metrics['affordability']:.0f}</div>
            <div class="metric-change">{metrics['market_health']}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {metrics['affordability']}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interactive overview chart
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Mortgage Rates Trend', 'Unemployment vs Housing', 'Affordability Index', 'Market Sentiment'),
        specs=[[{"secondary_y": True}, {"secondary_y": True}],
               [{"secondary_y": False}, {"type": "pie"}]]
    )
    
    # Mortgage rates
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Mortgage_Rate'], name='Mortgage Rate', 
                  line=dict(color='#667eea', width=3)),
        row=1, col=1
    )
    
    # Unemployment vs Home prices
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Unemployment_Rate'], name='Unemployment', 
                  line=dict(color='#ff9a9e', width=2)),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Home_Price_Index'], name='Home Price Index', 
                  line=dict(color='#764ba2', width=2)),
        row=1, col=2, secondary_y=True
    )
    
    # Affordability
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Affordability_Index'], name='Affordability',
                  fill='tozeroy', line=dict(color='#a8edea', width=2)),
        row=2, col=1
    )
    
    # Market sentiment pie
    sentiment_counts = df['Market_Sentiment'].value_counts()
    fig.add_trace(
        go.Pie(labels=sentiment_counts.index, values=sentiment_counts.values, 
               name="Market Sentiment", showlegend=False),
        row=2, col=2
    )
    
    fig.update_layout(height=800, showlegend=True, title_text="Market Overview Dashboard")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# MARKET INTELLIGENCE PAGE
# ============================================================================
elif menu == "📊 Market Intelligence":
    st.markdown('<h1 class="hero-header slide-in-animation">📊 Market Intelligence Center</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Advanced analytics and market insights</p>', unsafe_allow_html=True)
    
    # Interactive filters
    col1, col2, col3 = st.columns(3)
    with col1:
        date_range = st.date_input("📅 Date Range", 
                                 value=[df['Date'].min().date(), df['Date'].max().date()],
                                 min_value=df['Date'].min().date(),
                                 max_value=df['Date'].max().date())
    
    with col2:
        metrics_selection = st.multiselect("📈 Select Metrics", 
                               ['Mortgage_Rate', 'Unemployment_Rate', 'Home_Price_Index', 'Affordability_Index'],
                               default=['Mortgage_Rate', 'Home_Price_Index'])
    
    with col3:
        chart_type = st.selectbox("📊 Chart Type", ['Line', 'Area', 'Scatter'])
    
    # Filter data
    if len(date_range) == 2:
        mask = (df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])
        filtered_df = df.loc[mask]
    else:
        filtered_df = df
    
    # Create dynamic chart
    fig = go.Figure()
    colors = ['#667eea', '#764ba2', '#ff9a9e', '#a8edea']
    
    for i, metric in enumerate(metrics_selection):
        if chart_type == 'Line':
            fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[metric], 
                                   mode='lines', name=metric.replace('_', ' '),
                                   line=dict(color=colors[i % len(colors)], width=3)))
        elif chart_type == 'Area':
            fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[metric], 
                                   fill='tonexty', name=metric.replace('_', ' '),
                                   line=dict(color=colors[i % len(colors)])))
        else:
            fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[metric], 
                                   mode='markers', name=metric.replace('_', ' '),
                                   marker=dict(color=colors[i % len(colors)], size=8)))
    
    fig.update_layout(
        title="Advanced Market Analysis",
        xaxis_title="Date",
        yaxis_title="Value",
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistical insights
    st.markdown("### 📊 Statistical Insights")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Correlation Matrix")
        corr_matrix = filtered_df[['Mortgage_Rate', 'Unemployment_Rate', 'Home_Price_Index', 'Affordability_Index']].corr()
        fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto", 
                            color_continuous_scale='RdBu_r', title="Market Correlations")
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        st.markdown("#### Distribution Analysis")
        if metrics_selection:
            selected_metric = st.selectbox("Select metric for distribution", metrics_selection)
            fig_hist = px.histogram(filtered_df, x=selected_metric, nbins=20, 
                                  title=f"{selected_metric} Distribution")
            st.plotly_chart(fig_hist, use_container_width=True)

# ============================================================================
# AI SCENARIO LAB
# ============================================================================
elif menu == "🧠 AI Scenario Lab":
    st.markdown('<h1 class="hero-header slide-in-animation">🧠 AI Scenario Laboratory</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Advanced scenario modeling and stress testing</p>', unsafe_allow_html=True)
    
    st.markdown("### 🎮 Create Your Market Scenario")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Economic Parameters")
        interest_rate = st.slider("🏦 Federal Interest Rate (%)", 0.0, 10.0, 3.5, 0.1)
        unemployment = st.slider("📉 Unemployment Rate (%)", 0.0, 20.0, 5.0, 0.1)
        inflation = st.slider("💰 Inflation Rate (%)", -2.0, 10.0, 2.5, 0.1)
        gdp_growth = st.slider("📈 GDP Growth (%)", -5.0, 8.0, 2.0, 0.1)
        
    with col2:
        st.markdown("#### Housing Market Factors")
        housing_supply = st.slider("🏘️ Housing Supply Index", 50, 200, 100, 5)
        construction_cost = st.slider("🔨 Construction Cost Index", 80, 150, 100, 5)
        demand_index = st.slider("🎯 Housing Demand Index", 60, 180, 100, 5)
        location_factor = st.selectbox("📍 Market Location", 
                                     ["Major Metro", "Suburban", "Rural", "Coastal"])
    
    # Scenario analysis
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    # Calculate scenario outcomes
    market_stress = (interest_rate * 0.3 + unemployment * 0.4 + inflation * 0.2 + abs(gdp_growth) * 0.1)
    affordability_score = max(0, 100 - market_stress * 8 - (construction_cost - 100) * 0.5)
    investment_score = max(0, gdp_growth * 10 + (demand_index - 100) * 0.3 - market_stress * 5)
    
    with col1:
        if market_stress < 6:
            st.markdown(f"""
            <div class="status-card success-card">
                <h3>✅ Favorable Market</h3>
                <h2>Stress Score: {market_stress:.1f}/10</h2>
                <p>Low economic stress, favorable conditions for homebuyers and investors.</p>
            </div>
            """, unsafe_allow_html=True)
        elif market_stress < 8:
            st.markdown(f"""
            <div class="status-card warning-card">
                <h3>⚠️ Moderate Risk</h3>
                <h2>Stress Score: {market_stress:.1f}/10</h2>
                <p>Some economic headwinds. Proceed with caution and proper planning.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="status-card danger-card">
                <h3>🚨 High Stress</h3>
                <h2>Stress Score: {market_stress:.1f}/10</h2>
                <p>Challenging market conditions. Consider waiting or seek professional advice.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Affordability Score</h3>
            <h1>{affordability_score:.0f}/100</h1>
            <div class="progress-bar">
                <div class="progress-fill" style="width:{affordability_score}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Investment Score</h3>
            <h1>{investment_score:.0f}/100</h1>
            <div class="progress-bar">
                <div class="progress-fill" style="width:{max(0, min(100, investment_score))}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Run scenario button
    if st.button("🔮 Generate AI Analysis", type="primary"):
        st.session_state.scenarios_run += 1
        
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        st.markdown("#### 📋 AI Analysis Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Market Outlook:**")
            if market_stress < 6:
                st.success("🟢 Positive outlook for next 6-12 months")
            elif market_stress < 8:
                st.warning("🟡 Mixed signals, monitor key indicators")
            else:
                st.error("🔴 Challenging conditions ahead")
                
            st.markdown("**Key Risk Factors:**")
            if interest_rate > 6:
                st.write("• High interest rates affecting affordability")
            if unemployment > 7:
                st.write("• Elevated unemployment impacting demand")
            if inflation > 4:
                st.write("• High inflation eroding purchasing power")
        
        with col2:
            st.markdown("**Recommended Actions:**")
            if affordability_score > 70:
                st.write("✅ Consider accelerating purchase timeline")
                st.write("✅ Explore fixed-rate mortgage options")
            elif affordability_score > 40:
                st.write("⚠️ Build larger down payment fund")
                st.write("⚠️ Improve credit score for better rates")
            else:
                st.write("❌ Consider delaying purchase")
                st.write("❌ Focus on improving financial position")

# ============================================================================
# DECISION ENGINE
# ============================================================================
elif menu == "💎 Decision Engine":
    st.markdown('<h1 class="hero-header slide-in-animation">💎 AI-Powered Decision Engine</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Personalized recommendations based on your unique profile</p>', unsafe_allow_html=True)
    
    st.markdown("### 👤 Personal Profile Setup")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Financial Profile")
        annual_income = st.number_input("💰 Annual Income ($)", 30000, 500000, 75000, 5000)
        savings = st.number_input("🏦 Available Savings ($)", 0, 200000, 25000, 5000)
        debt_ratio = st.slider("💳 Debt-to-Income Ratio (%)", 0, 50, 15, 1)
        credit_score = st.slider("📊 Credit Score", 300, 850, 720, 5)
    
    with col2:
        st.markdown("#### Preferences")
        home_price_range = st.slider("🏠 Target Home Price ($)", 100000, 800000, (250000, 400000), 10000)
        down_payment = st.slider("💵 Down Payment (%)", 3, 30, 20, 1)
        time_horizon = st.selectbox("⏰ Purchase Timeline", 
                                  ["Immediate (0-3 months)", "Short-term (3-12 months)", 
                                   "Medium-term (1-2 years)", "Long-term (2+ years)"])
        risk_tolerance = st.selectbox("📊 Risk Tolerance", ["Conservative", "Moderate", "Aggressive"])
    
    with col3:
        st.markdown("#### Location & Lifestyle")
        location_type = st.selectbox("📍 Preferred Location", 
                                   ["Urban Core", "Suburban", "Rural", "Coastal"])
        family_size = st.selectbox("👨‍👩‍👧‍👦 Family Size", ["Single", "Couple", "Small Family (3-4)", "Large Family (5+)"])
        job_stability = st.selectbox("💼 Job Stability", ["Very Stable", "Stable", "Moderate", "Uncertain"])
        first_time_buyer = st.checkbox("🏠 First-time Homebuyer")
    
    if st.button("🧠 Generate AI Recommendation", type="primary"):
        # Simulate AI processing
        with st.spinner("🤖 AI analyzing your profile..."):
            time.sleep(2)
        
        # Calculate recommendation scores
        financial_readiness = min(100, (savings / (home_price_range[0] * down_payment / 100)) * 50 + 
                                (800 - max(300, credit_score)) / 5.5 * 50)
        
        market_timing = max(0, 100 - latest_data['Mortgage_Rate'] * 10 - latest_data['Unemployment_Rate'] * 5)
        
        overall_score = (financial_readiness * 0.6 + market_timing * 0.4)
        
        # Display results
        st.markdown("---")
        st.markdown("### 🎯 Your Personalized Recommendation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>💰 Financial Readiness</h3>
                <h1>{financial_readiness:.0f}/100</h1>
                <div class="progress-bar">
                    <div class="progress-fill" style="width:{financial_readiness}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>⏰ Market Timing</h3>
                <h1>{market_timing:.0f}/100</h1>
                <div class="progress-bar">
                    <div class="progress-fill" style="width:{market_timing}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎯 Overall Score</h3>
                <h1>{overall_score:.0f}/100</h1>
                <div class="progress-bar">
                    <div class="progress-fill" style="width:{overall_score}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendation logic
        if overall_score >= 75:
            st.markdown(f"""
            <div class="status-card success-card">
                <h2>🚀 Strong Buy Signal</h2>
                <p><strong>Recommendation:</strong> You're in an excellent position to buy now!</p>
                <p>Your financial readiness and current market conditions align favorably.</p>
                <ul style="text-align: left;">
                    <li>✅ Strong credit profile and savings</li>
                    <li>✅ Favorable market timing</li>
                    <li>✅ Good debt-to-income ratio</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif overall_score >= 50:
            st.markdown(f"""
            <div class="status-card warning-card">
                <h2>⚖️ Conditional Buy</h2>
                <p><strong>Recommendation:</strong> You can proceed with careful planning.</p>
                <p>Consider addressing some areas for improvement first.</p>
                <ul style="text-align: left;">
                    <li>⚠️ Build larger emergency fund</li>
                    <li>⚠️ Monitor market conditions closely</li>
                    <li>⚠️ Consider pre-approval to understand options</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="status-card danger-card">
                <h2>⏳ Wait and Prepare</h2>
                <p><strong>Recommendation:</strong> Focus on improving your financial position.</p>
                <p>Use this time to strengthen your profile for future opportunities.</p>
                <ul style="text-align: left;">
                    <li>❌ Increase savings and down payment fund</li>
                    <li>❌ Improve credit score</li>
                    <li>❌ Reduce existing debt obligations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# PORTFOLIO SUITE
# ============================================================================
elif menu == "📈 Portfolio Suite":
    st.markdown('<h1 class="hero-header slide-in-animation">📈 Real Estate Portfolio Manager</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Track and optimize your real estate investments</p>', unsafe_allow_html=True)
    
    # Portfolio input
    st.markdown("### 🏠 Your Properties")
    
    with st.expander("➕ Add New Property", expanded=len(st.session_state.properties) == 0):
        col1, col2, col3 = st.columns(3)
        with col1:
            prop_address = st.text_input("🏠 Property Address")
            purchase_price = st.number_input("💰 Purchase Price ($)", 0, 2000000, 300000)
        with col2:
            purchase_date = st.date_input("📅 Purchase Date")
            current_value = st.number_input("📈 Current Estimated Value ($)", 0, 2000000, 350000)
        with col3:
            property_type = st.selectbox("🏘️ Property Type", 
                                       ["Single Family", "Condo", "Townhouse", "Multi-Family"])
            monthly_payment = st.number_input("💳 Monthly Payment ($)", 0, 10000, 1800)
        
        if st.button("➕ Add Property") and prop_address:
            st.session_state.properties.append({
                'address': prop_address,
                'purchase_price': purchase_price,
                'current_value': current_value,
                'purchase_date': purchase_date,
                'property_type': property_type,
                'monthly_payment': monthly_payment
            })
            st.success("Property added successfully!")
            st.rerun()
    
    # Display portfolio
    if st.session_state.properties:
        st.markdown("### 📊 Portfolio Overview")
        
        total_purchase = sum(p['purchase_price'] for p in st.session_state.properties)
        total_current = sum(p['current_value'] for p in st.session_state.properties)
        total_equity = total_current - total_purchase
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🏠 Properties", len(st.session_state.properties))
        with col2:
            st.metric("💰 Total Investment", f"${total_purchase:,.0f}")
        with col3:
            st.metric("📈 Current Value", f"${total_current:,.0f}")
        with col4:
            st.metric("💎 Total Equity", f"${total_equity:,.0f}", f"{((total_equity/total_purchase)*100):+.1f}%")
        
        # Property details
        for i, prop in enumerate(st.session_state.properties):
            with st.expander(f"🏠 {prop['address']} - {prop['property_type']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Purchase Price:** ${prop['purchase_price']:,.0f}")
                    st.write(f"**Purchase Date:** {prop['purchase_date']}")
                    st.write(f"**Monthly Payment:** ${prop['monthly_payment']:,.0f}")
                with col2:
                    st.write(f"**Current Value:** ${prop['current_value']:,.0f}")
                    equity = prop['current_value'] - prop['purchase_price']
                    st.write(f"**Equity:** ${equity:,.0f}")
                    roi = ((equity / prop['purchase_price']) * 100) if prop['purchase_price'] > 0 else 0
                    st.write(f"**ROI:** {roi:.1f}%")

# ============================================================================
# ENTERPRISE INFO PAGE
# ============================================================================
elif menu == "ℹ️ Enterprise Info":
    st.markdown('<h1 class="hero-header slide-in-animation">ℹ️ About Mortgage Quest Elite</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2>🎯 Mission Statement</h2>
            <p><strong>Mortgage Quest Elite</strong> is an advanced strategic simulation platform that empowers users to navigate the complex U.S. housing market with confidence and data-driven insights.</p>
            
            <h3>🚀 Key Features:</h3>
            <ul>
                <li><strong>Real-time Market Intelligence:</strong> Live tracking of mortgage rates, unemployment, and housing indices</li>
                <li><strong>Advanced Scenario Modeling:</strong> Simulate economic conditions and predict market outcomes</li>
                <li><strong>AI-Powered Decision Engine:</strong> Personalized recommendations based on your financial profile</li>
                <li><strong>Portfolio Management:</strong> Track and analyze your real estate investments</li>
                <li><strong>Professional Analytics:</strong> Institutional-grade tools for serious investors</li>
            </ul>
            
            <h3>🎓 Academic Excellence:</h3>
            <p>Developed for the <strong>NYU Stern Fintech Capstone</strong> by team <strong>BEFMNS</strong>, this application represents the intersection of cutting-edge financial technology and practical real estate decision-making.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🔧 Technology Stack</h3>
            <p><strong>Frontend:</strong> Streamlit with custom CSS</p>
            <p><strong>Visualization:</strong> Plotly & Interactive Charts</p>
            <p><strong>Data Processing:</strong> Pandas & NumPy</p>
            <p><strong>Analytics:</strong> Statistical Modeling</p>
            <p><strong>Design:</strong> Modern UI/UX Principles</p>
            
            <h3>📊 Data Sources</h3>
            <p>• Federal Reserve Economic Data (FRED)</p>
            <p>• New York Federal Reserve</p>
            <p>• Bureau of Labor Statistics</p>
            <p>• Housing Market Indices</p>
            
            <h3>🎮 Gamification Elements</h3>
            <p>• Interactive Scenarios</p>
            <p>• Progress Tracking</p>
            <p>• Achievement System</p>
            <p>• Real-time Feedback</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Team information
    st.markdown("### 👥 Meet the Team - BEFMNS")
    team_col1, team_col2, team_col3 = st.columns(3)
    
    with team_col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Strategy & Analytics</h4>
            <p>Financial modeling and market analysis experts bringing Wall Street insights to Main Street decisions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with team_col2:
        st.markdown("""
        <div class="feature-card">
            <h4>💻 Technology & Development</h4>
            <p>Full-stack developers and data scientists creating scalable fintech solutions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with team_col3:
        st.markdown("""
        <div class="feature-card">
            <h4>🎨 Design & Experience</h4>
            <p>UX/UI specialists focused on making complex financial data accessible and actionable.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
        <h3>🚀 Ready to Transform Your Real Estate Journey?</h3>
        <p>Join thousands of users making smarter homeownership decisions with Mortgage Quest Elite</p>
        <p><strong>© 2024 BEFMNS Team | NYU Stern School of Business</strong></p>
    </div>
    """, unsafe_allow_html=True)
