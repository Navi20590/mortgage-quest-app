import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# Page Configuration
st.set_page_config(
    page_title="🏡 Mortgage Quest Pro",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .status-card {
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        margin: 1rem 0;
        border-left: 5px solid;
    }
    
    .success-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-left-color: #00d4aa;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-left-color: #ff9500;
    }
    
    .error-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        border-left-color: #ff4757;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 20px rgba(0, 0, 0, 0.3);
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea, #764ba2);
        height: 20px;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Generate Sample Data (for demo purposes)
@st.cache_data
def generate_sample_data():
    """Generate realistic mortgage market data for demonstration"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='M')
    np.random.seed(42)
    
    # Create realistic trend data
    base_rate = 3.0
    rate_trend = np.cumsum(np.random.normal(0, 0.1, len(dates))) + base_rate
    rate_trend = np.clip(rate_trend, 2.0, 8.0)
    
    unemployment = 4.0 + np.cumsum(np.random.normal(0, 0.2, len(dates)))
    unemployment = np.clip(unemployment, 3.0, 15.0)
    
    home_index = 250 + np.cumsum(np.random.normal(2, 5, len(dates)))
    home_index = np.clip(home_index, 200, 400)
    
    affordability = 100 - (rate_trend * 5) - (unemployment * 2) + np.random.normal(0, 5, len(dates))
    affordability = np.clip(affordability, 20, 100)
    
    df = pd.DataFrame({
        'Date': dates,
        'Mortgage_Rate': rate_trend,
        'Unemployment_Rate': unemployment,
        'Home_Price_Index': home_index,
        'Affordability_Index': affordability,
        'Market_Sentiment': np.random.choice(['Bullish', 'Neutral', 'Bearish'], len(dates), p=[0.3, 0.4, 0.3])
    })
    
    return df

# Enhanced sidebar navigation
with st.sidebar:
    st.markdown("## 🎮 Navigation Hub")
    menu = st.radio(
        "Choose Your Adventure:",
        ["🏠 Dashboard", "📊 Market Intelligence", "🎯 Scenario Simulator", "💡 Decision Engine", "📈 Portfolio Tracker", "ℹ️ About"],
        key="main_nav"
    )
    
    st.markdown("---")
    st.markdown("### 🔧 Quick Controls")
    
    # Real-time updates toggle
    real_time = st.checkbox("🔄 Real-time Updates", value=True)
    
    # Theme selector
    theme = st.selectbox("🎨 Theme", ["Professional", "Dark Mode", "Colorful"])

# Load data
df = generate_sample_data()
latest_data = df.iloc[-1]

# Dashboard Page
if menu == "🏠 Dashboard":
    st.markdown('<h1 class="main-header">🏡 Mortgage Quest Pro Dashboard</h1>', unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; color:#667eea;">📈 Mortgage Rate</h3>
            <h1 style="margin:0.5rem 0; color:#333;">{latest_data['Mortgage_Rate']:.2f}%</h1>
            <p style="margin:0; color:#666;">+0.15% from last month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; color:#764ba2;">📊 Unemployment</h3>
            <h1 style="margin:0.5rem 0; color:#333;">{latest_data['Unemployment_Rate']:.1f}%</h1>
            <p style="margin:0; color:#666;">-0.2% from last month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; color:#ff9a9e;">🏠 Price Index</h3>
            <h1 style="margin:0.5rem 0; color:#333;">{latest_data['Home_Price_Index']:.0f}</h1>
            <p style="margin:0; color:#666;">+2.1% from last month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; color:#a8edea;">💰 Affordability</h3>
            <h1 style="margin:0.5rem 0; color:#333;">{latest_data['Affordability_Index']:.0f}</h1>
            <p style="margin:0; color:#666;">Moderate Level</p>
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

# Market Intelligence Page
elif menu == "📊 Market Intelligence":
    st.markdown('<h1 class="main-header">📊 Market Intelligence Center</h1>', unsafe_allow_html=True)
    
    # Interactive filters
    col1, col2, col3 = st.columns(3)
    with col1:
        date_range = st.date_input("📅 Date Range", 
                                 value=[df['Date'].min().date(), df['Date'].max().date()],
                                 min_value=df['Date'].min().date(),
                                 max_value=df['Date'].max().date())
    
    with col2:
        metrics = st.multiselect("📈 Select Metrics", 
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
    
    for i, metric in enumerate(metrics):
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
                            color_continuous_scale='RdBu_r')
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        st.markdown("#### Distribution Analysis")
        selected_metric = st.selectbox("Select metric for distribution", metrics)
        if selected_metric:
            fig_hist = px.histogram(filtered_df, x=selected_metric, nbins=20, 
                                  title=f"{selected_metric} Distribution")
            st.plotly_chart(fig_hist, use_container_width=True)

# Scenario Simulator Page
elif menu == "🎯 Scenario Simulator":
    st.markdown('<h1 class="main-header">🎯 Advanced Scenario Simulator</h1>', unsafe_allow_html=True)
    
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
            <div class="status-card error-card">
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
            <div style="background:#e0e0e0; border-radius:10px; overflow:hidden;">
                <div class="progress-bar" style="width:{affordability_score}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Investment Score</h3>
            <h1>{investment_score:.0f}/100</h1>
            <div style="background:#e0e0e0; border-radius:10px; overflow:hidden;">
                <div class="progress-bar" style="width:{max(0, min(100, investment_score))}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Scenario recommendations
    st.markdown("### 🎯 Scenario-Based Recommendations")
    
    if st.button("🔮 Generate Detailed Analysis", type="primary"):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        st.markdown("#### 📋 Detailed Analysis Results")
        
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

# Decision Engine Page
elif menu == "💡 Decision Engine":
    st.markdown('<h1 class="main-header">💡 AI-Powered Decision Engine</h1>', unsafe_allow_html=True)
    
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
                <div style="background:#e0e0e0; border-radius:10px; overflow:hidden;">
                    <div class="progress-bar" style="width:{financial_readiness}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>⏰ Market Timing</h3>
                <h1>{market_timing:.0f}/100</h1>
                <div style="background:#e0e0e0; border-radius:10px; overflow:hidden;">
                    <div class="progress-bar" style="width:{market_timing}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎯 Overall Score</h3>
                <h1>{overall_score:.0f}/100</h1>
                <div style="background:#e0e0e0; border-radius:10px; overflow:hidden;">
                    <div class="progress-bar" style="width:{overall_score}%;"></div>
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
            <div class="status-card error-card">
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

# Portfolio Tracker Page
elif menu == "📈 Portfolio Tracker":
    st.markdown('<h1 class="main-header">📈 Real Estate Portfolio Tracker</h1>', unsafe_allow_html=True)
    
    # Portfolio input
    st.markdown("### 🏠 Your Properties")
    
    if 'properties' not in st.session_state:
        st.session_state.properties = []
    
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

# About Page
elif menu == "ℹ️ About":
    st.markdown('<h1 class="main-header">ℹ️ About Mortgage Quest Pro</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2>🎯 Mission Statement</h2>
            <p><strong>Mortgage Quest Pro</strong> is an advanced strategic simulation platform that empowers users to navigate the complex U.S. housing market with confidence and data-driven insights.</p>
            
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
        <p>Join thousands of users making smarter homeownership decisions with Mortgage Quest Pro</p>
        <p><strong>© 2024 BEFMNS Team | NYU Stern School of Business</strong></p>
    </div>
    """, unsafe_allow_html=True)
