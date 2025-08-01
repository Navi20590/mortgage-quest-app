'current_rate': latest['Mortgage_Rate'],
        'rate_change_month': latest['Mortgage_Rate'] - prev_month['Mortgage_Rate'],
        'unemployment': latest['Unemployment_Rate'],
        'unemployment_change': latest['Unemployment_Rate'] - prev_month['Unemployment_Rate'],
        'hpi': latest['Home_Price_Index'],
        'hpi_change': ((latest['Home_Price_Index'] - prev_year['Home_Price_Index']) / prev_year['Home_Price_Index']) * 100,
        'affordability': latest['Affordability_Index'],
        'market_health': 'Elite' if latest['Affordability_Index'] > 70 else 'Advanced' if latest['Affordability_Index'] > 50 else 'Moderate' if latest['Affordability_Index'] > 30 else 'Challenging',
        'volatility': df['Mortgage_Rate'].tail(30).std()
    }
    
    return metrics

# ============================================================================
# FUTURISTIC SIDEBAR NAVIGATION
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <div class="icon-3d">🎮</div>
        <h1 style="background: linear-gradient(45deg, #00D4FF, #9D4EDD); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.8rem; font-weight: 900; font-family: 'Orbitron', monospace; margin: 0;">
            MORTGAGE QUEST
        </h1>
        <p style="color: #9D4EDD; font-size: 1rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.2em; font-family: 'Orbitron', monospace; margin: 0.5rem 0;">Futuristic Gaming Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User Profile Card
    st.markdown(f"""
    <div class="game-card-3d" style="margin-bottom: 2rem; text-align: center;">
        <div class="icon-3d">👨‍🚀</div>
        <div style="color: #00D4FF; font-weight: 700; font-size: 1.2rem; text-transform: uppercase; font-family: 'Orbitron', monospace;">Level {st.session_state.user_profile['level']} Commander</div>
        <div style="color: #9D4EDD; font-weight: 600; font-size: 1.1rem;">{st.session_state.user_profile['points']} XP</div>
        <div class="progress-bar-3d">
            <div class="progress-fill-3d" style="width: {min(100, (st.session_state.user_profile['points'] % 500) * 100 / 500)}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Menu
    menu_options = [
        "🎯 Mission Control Hub",
        "📊 Intelligence Center", 
        "🧠 Strategy Simulator",
        "💎 Decision Matrix",
        "📈 Asset Portfolio",
        "ℹ️ Command Brief"
    ]
    
    menu = st.radio("🚀 Navigation Console:", menu_options, key="main_nav")
    
    st.markdown("---")
    
    # Gaming Controls
    st.markdown("### 🎮 System Controls")
    real_time_updates = st.toggle("⚡ Real-time Data", value=True)
    advanced_mode = st.toggle("🔬 Advanced Mode", value=False) 
    battle_alerts = st.toggle("🚨 Battle Alerts", value=True)
    
    # Market Status Indicator
    df = generate_futuristic_data()
    metrics = calculate_advanced_metrics(df)
    
    st.markdown("### 🌌 Market Status")
    health_color = "#39FF14" if metrics['market_health'] == 'Elite' else "#00D4FF" if metrics['market_health'] == 'Advanced' else "#FFD60A" if metrics['market_health'] == 'Moderate' else "#FF6B9D"
    
    st.markdown(f"""
    <div class="game-card-3d" style="text-align: center; background: linear-gradient(135deg, {health_color}20 0%, rgba(255,255,255,0.9) 100%); border: 2px solid {health_color};">
        <div style="color: {health_color}; font-weight: 700; font-size: 1.3rem; text-transform: uppercase; font-family: 'Orbitron', monospace;">{metrics['market_health']}</div>
        <div style="color: #0A0E27; font-size: 1.1rem; font-weight: 600;">{metrics['affordability']:.0f}/100 Health</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Achievement Badges
    st.markdown("### 🏆 Achievement Gallery")
    for ach_id, ach in ACHIEVEMENTS.items():
        status = "✅" if ach_id in st.session_state.user_profile['achievements'] else "🔒"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFD60A20 0%, rgba(255,255,255,0.9) 100%); 
                    border: 2px solid #FFD60A; border-radius: 15px; padding: 1rem; margin: 0.5rem 0; 
                    text-align: center;">
            <div style="font-size: 1.5rem;">{status} {ach['icon']}</div>
            <div style="color: #0A0E27; font-weight: 600; font-size: 0.9rem;">{ach['name']}</div>
        </div>
        """, unsafe_allow_html=True)

# Load data
df = generate_futuristic_data()
metrics = calculate_advanced_metrics(df)
latest_data = df.iloc[-1]

# Track achievements
track_achievement(menu)

# ============================================================================
# MISSION CONTROL HUB - MAIN DASHBOARD
# ============================================================================
if menu == "🎯 Mission Control Hub":
    st.markdown('<h1 class="hero-header">🎯 Mission Control Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">⚡ Advanced Real Estate Gaming Intelligence ⚡</p>', unsafe_allow_html=True)
    
    # Live Battle Alerts
    if battle_alerts:
        alert_col1, alert_col2, alert_col3 = st.columns(3)
        
        with alert_col1:
            if abs(metrics['rate_change_month']) > 0.25:
                st.markdown(f"""
                <div class="game-card-3d" style="background: linear-gradient(135deg, #FF6B9D20 0%, rgba(255,255,255,0.9) 100%); border: 2px solid #FF6B9D;">
                    <div class="icon-3d">🚨</div>
                    <h4 style="color: #FF6B9D; margin: 0;">RATE ALERT</h4>
                    <p style="color: #0A0E27; font-weight: 600;">Critical rate movement detected</p>
                    <strong style="color: #FF6B9D; font-size: 1.2rem;">{metrics['rate_change_month']:+.2f}% This Month</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with alert_col2:
            if metrics['volatility'] > 0.5:
                st.markdown(f"""
                <div class="game-card-3d" style="background: linear-gradient(135deg, #FFD60A20 0%, rgba(255,255,255,0.9) 100%); border: 2px solid #FFD60A;">
                    <div class="icon-3d">⚠️</div>
                    <h4 style="color: #FFD60A; margin: 0;">VOLATILITY WARNING</h4>
                    <p style="color: #0A0E27; font-weight: 600;">High market turbulence</p>
                    <strong style="color: #FFD60A; font-size: 1.2rem;">{metrics['volatility']:.2f}% Deviation</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with alert_col3:
            if latest_data['Affordability_Index'] < 40:
                st.markdown(f"""
                <div class="game-card-3d" style="background: linear-gradient(135deg, #00D4FF20 0%, rgba(255,255,255,0.9) 100%); border: 2px solid #00D4FF;">
                    <div class="icon-3d">📊</div>
                    <h4 style="color: #00D4FF; margin: 0;">AFFORDABILITY ALERT</h4>
                    <p style="color: #0A0E27; font-weight: 600;">Low affordability conditions</p>
                    <strong style="color: #00D4FF; font-size: 1.2rem;">{latest_data['Affordability_Index']:.0f}/100 Status</strong>
                </div>
                """, unsafe_allow_html=True)
    
    # Premium KPI Battle Station
    st.markdown("### 📊 Executive Battle Dashboard")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.markdown(f"""
        <div class="metric-card-3d">
            <div class="icon-3d">🏦</div>
            <div class="metric-label-3d">Mortgage Rate</div>
            <div class="metric-value-3d">{metrics['current_rate']:.2f}%</div>
            <div class="metric-change-3d">{metrics['rate_change_month']:+.2f}% MTD</div>
            <div class="progress-bar-3d">
                <div class="progress-fill-3d" style="width: {min(100, metrics['current_rate']*10)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col2:
        st.markdown(f"""
        <div class="metric-card-3d">
            <div class="icon-3d">📉</div>
            <div class="metric-label-3d">Unemployment</div>
            <div class="metric-value-3d">{metrics['unemployment']:.1f}%</div>
            <div class="metric-change-3d">{metrics['unemployment_change']:+.1f}% MTD</div>
            <div class="progress-bar-3d">
                <div class="progress-fill-3d" style="width: {min(100, metrics['unemployment']*5)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col3:
        st.markdown(f"""
        <div class="metric-card-3d">
            <div class="icon-3d">🏠</div>
            <div class="metric-label-3d">Price Index</div>
            <div class="metric-value-3d">{metrics['hpi']:.0f}</div>
            <div class="metric-change-3d">{metrics['hpi_change']:+.1f}% YTD</div>
            <div class="progress-bar-3d">
                <div class="progress-fill-3d" style="width: {min(100, metrics['hpi']/4)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col4:
        st.markdown(f"""
        <div class="metric-card-3d">
            <div class="icon-3d">💎</div>
            <div class="metric-label-3d">Affordability</div>
            <div class="metric-value-3d">{metrics['affordability']:.0f}</div>
            <div class="metric-change-3d">{metrics['market_health']}</div>
            <div class="progress-bar-3d">
                <div class="progress-fill-3d" style="width: {metrics['affordability']}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interactive Battle Chart
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('🚀 Mortgage Rates Command', '⚔️ Economic Battle Zone', '💎 Affordability Status', '🌌 Market Sentiment'),
        specs=[[{"secondary_y": True}, {"secondary_y": True}],
               [{"secondary_y": False}, {"type": "pie"}]]
    )
    
    # Mortgage rates with futuristic styling
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Mortgage_Rate'], name='Mortgage Rate', 
                  line=dict(color='#00D4FF', width=4),
                  hovertemplate='<b>Rate:</b> %{y:.2f}%<br><b>Date:</b> %{x}<extra></extra>'),
        row=1, col=1
    )
    
    # Unemployment vs Home prices
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Unemployment_Rate'], name='Unemployment', 
                  line=dict(color='#FF6B9D', width=3)),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Home_Price_Index'], name='Home Price Index', 
                  line=dict(color='#9D4EDD', width=3)),
        row=1, col=2, secondary_y=True
    )
    
    # Affordability with futuristic fill
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Affordability_Index'], name='Affordability',
                  fill='tozeroy', line=dict(color='#39FF14', width=3),
                  fillcolor='rgba(57, 255, 20, 0.3)'),
        row=2, col=1
    )
    
    # Market sentiment pie with futuristic colors
    sentiment_counts = df['Market_Sentiment'].value_counts()
    fig.add_trace(
        go.Pie(labels=sentiment_counts.index, values=sentiment_counts.values, 
               name="Market Sentiment", showlegend=False,
               marker=dict(colors=['#00D4FF', '#FFD60A', '#FF6B9D'])),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800, 
        showlegend=True, 
        title_text="🌌 Advanced Market Intelligence Dashboard",
        title_font=dict(size=24, family="Orbitron, monospace", color="#9D4EDD"),
        plot_bgcolor='rgba(248, 249, 250, 0.1)',
        paper_bgcolor='rgba(248, 249, 250, 0.1)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# INTELLIGENCE CENTER
# ============================================================================
elif menu == "📊 Intelligence Center":
    st.markdown('<h1 class="hero-header">📊 Intelligence Center</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">🔮 Advanced Market Analytics & Insights 🔮</p>', unsafe_allow_html=True)
    
    # Interactive Control Panel
    col1, col2, col3 = st.columns(3)
    with col1:
        date_range = st.date_input("🗓️ Time Range Scanner", 
                                 value=[df['Date'].min().date(), df['Date'].max().date()],
                                 min_value=df['Date'].min().date(),
                                 max_value=df['Date'].max().date())
    
    with col2:
        metrics_selection = st.multiselect("🎯 Data Streams", 
                               ['Mortgage_Rate', 'Unemployment_Rate', 'Home_Price_Index', 'Affordability_Index'],
                               default=['Mortgage_Rate', 'Home_Price_Index'])
    
    with col3:
        viz_type = st.selectbox("📈 Visualization Mode", ['Line Command', 'Area Scan', 'Scatter Analysis'])
    
    # Filter data
    if len(date_range) == 2:
        mask = (df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])
        filtered_df = df.loc[mask]
    else:
        filtered_df = df
    
    # Create dynamic futuristic chart
    fig = go.Figure()
    colors = ['#00D4FF', '#9D4EDD', '#FF6B9D', '#39FF14']
    
    for i, metric in enumerate(metrics_selection):
        if viz_type == 'Line Command':
            fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[metric], 
                                   mode='lines', name=metric.replace('_', ' '),
                                   line=dict(color=colors[i % len(colors)], width=4)))
        elif viz_type == 'Area Scan':
            fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[metric], 
                                   fill='tonexty', name=metric.replace('_', ' '),
                                   line=dict(color=colors[i % len(colors)]),
                                   fillcolor=f'{colors[i % len(colors)]}30'))
        else:
            fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[metric], 
                                   mode='markers', name=metric.replace('_', ' '),
                                   marker=dict(color=colors[i % len(colors)], size=10, 
                                             line=dict(width=2, color='#FFFFFF'))))
    
    fig.update_layout(
        title="🌌 Advanced Intelligence Analysis",
        title_font=dict(size=20, family="Orbitron, monospace", color="#9D4EDD"),
        xaxis_title="Timeline",
        yaxis_title="Values",
        height=600,
        hovermode='x unified',
        plot_bgcolor='rgba(248, 249, 250, 0.1)',
        paper_bgcolor='rgba(248, 249, 250, 0.1)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Advanced Analytics
    st.markdown("### 🔬 Advanced Intelligence Reports")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌐 Correlation Matrix")
        corr_matrix = filtered_df[['Mortgage_Rate', 'Unemployment_Rate', 'Home_Price_Index', 'Affordability_Index']].corr()
        fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto", 
                            color_continuous_scale=['#FF6B9D', '#FFFFFF', '#00D4FF'],
                            title="Market Correlation Intelligence")
        fig_corr.update_layout(
            title_font=dict(size=16, family="Orbitron, monospace", color="#9D4EDD")
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Distribution Scanner")
        if metrics_selection:
            selected_metric = st.selectbox("Select Intelligence Stream", metrics_selection)
            fig_hist = px.histogram(filtered_df, x=selected_metric, nbins=25, 
                                  title=f"{selected_metric} Distribution Analysis",
                                  color_discrete_sequence=['#00D4FF'])
            fig_hist.update_layout(
                title_font=dict(size=16, family="Orbitron, monospace", color="#9D4EDD"),
                plot_bgcolor='rgba(248, 249, 250, 0.1)',
                paper_bgcolor='rgba(248, 249, 250, 0.1)'
            )
            st.plotly_chart(fig_hist, use_container_width=True)

# ============================================================================
# STRATEGY SIMULATOR
# ============================================================================
elif menu == "🧠 Strategy Simulator":
    st.markdown('<h1 class="hero-header">🧠 Strategy Simulator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">⚔️ Advanced Battle Scenario Modeling ⚔️</p>', unsafe_allow_html=True)
    
    st.markdown("### 🎮 Battle Configuration Console")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🌌 Economic Parameters")
        interest_rate = st.slider("🏦 Federal Battle Rate (%)", 0.0, 10.0, 3.5, 0.1)
        unemployment = st.slider("📉 Unemployment Level (%)", 0.0, 20.0, 5.0, 0.1)
        inflation = st.slider("💰 Inflation Force (%)", -2.0, 10.0, 2.5, 0.1)
        gdp_growth = st.slider("📈 GDP Power (%)", -5.0, 8.0, 2.0, 0.1)
        
    with col2:
        st.markdown("#### 🏠 Housing Battle Factors")
        housing_supply = st.slider("🏘️ Supply Index", 50, 200, 100, 5)
        construction_cost = st.slider("🔨 Build Cost Index", 80, 150, 100, 5)
        demand_index = st.slider("🎯 Demand Force", 60, 180, 100, 5)
        location_factor = st.selectbox("📍 Battle Zone", 
                                     ["🌆 Major Metro", "🏘️ Suburban", "🌾 Rural", "🏖️ Coastal"])
    
    # Battle Analysis
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    # Calculate battle outcomes
    market_stress = (interest_rate * 0.3 + unemployment * 0.4 + inflation * 0.2 + abs(gdp_growth) * 0.1)
    affordability_score = max(0, 100 - market_stress * 8 - (construction_cost - 100) * 0.5)
    investment_score = max(0, gdp_growth * 10 + (demand_index - 100) * 0.3 - market_stress * 5)
    
    with col1:
        if market_stress < 6:
            st.markdown(f"""
            <div class="game-card-3d" style="background: linear-gradient(135deg, #39FF1420 0%, rgba(255,255,255,0.9) 100%); border: 2px solid #39FF14;">
                <div class="icon-3d">✅</div>
                <h3 style="color: #39FF14; margin: 0;">VICTORY CONDITIONS</h3>
                <h2 style="color: #0A0E27; font-family: 'Orbitron', monospace;">Battle Score: {market_stress:.1f}/10</h2>
                <p style="color: #0A0E27; font-weight: 600;">Optimal market conditions detected. Execute advance strategy!</p>
            </div>
            """, unsafe_allow_html=True)
        elif market_stress < 8:
            st.markdown(f"""
            <div class="game-card-3d" style="background: linear-gradient(135deg, #FFD60A20 0%, rgba(255,255,255,0.9) 100%); border: 2px solid #FFD60A;">
                <div class="icon-3d">⚠️</div>
                <h3 style="color: #FFD60A; margin: 0;">CAUTION MODE</h3>
                <h2 style="color: #0A0E27; font-family: 'Orbitron', monospace;">Battle Score: {market_stress:.1f}/10</h2>
                <p style="color: #0A0E27; font-weight: 600;">Moderate resistance detected. Proceed with tactical planning.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="game-card-3d" style="background: linear-gradient(135deg, #FF6B9D20 0%, rgba(255,255,255,0.9) 100%); border: 2px solid #FF6B9D;">
                <div class="icon-3d">🚨</div>
                <h3 style="color: #FF6B9D; margin: 0;">DANGER ZONE</h3>
                <h2 style="color: #0A0E27; font-family: 'Orbitron', monospace;">Battle Score: {market_stress:.1f}/10</h2>
                <p style="color: #0A0E27; font-weight: 600;">High resistance encountered. Strategic retreat recommended.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card-3d">
            <div class="icon-3d">💎</div>
            <div class="metric-label-3d">Affordability Power</div>
            <div class="metric-value-3d">{affordability_score:.0f}/100</div>
            <div class="progress-bar-3d">
                <div class="progress-fill-3d" style="width:{affordability_score}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card-3d">
            <div class="icon-3d">📈</div>
            <div class="metric-label-3d">Investment Force</div>
            <div class="metric-value-3d">{investment_score:.0f}/100</div>
            <div class="progress-bar-3d">
                <div class="progress-fill-3d" style="width:{max(0, min(100, investment_score))}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Battle Simulation
    if st.button("🔮 Execute Battle Simulation", type="primary"):
        st.session_state.scenarios_run += 1
        
        # Epic loading animation
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            if i < 25:
                status_text.text('🔍 Scanning market conditions...')
            elif i < 50:
                status_text.text('⚔️ Running battle simulations...')
            elif i < 75:
                status_text.text('🧠 Analyzing strategic outcomes...')
            else:
                status_text.text('🎯 Finalizing battle report...')
            time.sleep(0.02)
        
        status_text.text('✅ Battle simulation complete!')
        
        st.markdown("#### 📋 Strategic Battle Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔮 Market Intelligence:**")
            if market_stress < 6:
                st.success("🟢 Favorable battle conditions for next 6-12 months")
                st.info("🎯 Recommended: Aggressive expansion strategy")
            elif market_stress < 8:
                st.warning("🟡 Mixed battlefield signals - maintain vigilance")
                st.info("⚠️ Recommended: Defensive positioning with selective strikes")
            else:
                st.error("🔴 Hostile territory ahead - high resistance expected")
                st.info("🛡️ Recommended: Strategic retreat and fortification")
                
            st.markdown("**⚔️ Key Battle Factors:**")
            if interest_rate > 6:
                st.write("• 🏦 High rate resistance affecting advance capabilities")
            if unemployment > 7:
                st.write("• 📉 Economic weakness impacting demand forces")
            if inflation > 4:
                st.write("• 💰 Inflation pressure eroding purchasing power")
        
        with col2:
            st.markdown("**🎯 Tactical Recommendations:**")
            if affordability_score > 70:
                st.write("✅ 🚀 Execute immediate advance operations")
                st.write("✅ 🎯 Deploy fixed-rate mortgage strategies")
                st.write("✅ 💎 Maximize acquisition opportunities")
            elif affordability_score > 40:
                st.write("⚠️ 🛡️ Build defensive reserves")
                st.write("⚠️ 📈 Strengthen credit battle rating")
                st.write("⚠️ 🔍 Monitor for strategic openings")
            else:
                st.write("❌ 🏃 Execute tactical withdrawal")
                st.write("❌ 💪 Focus on strengthening battle position")
                st.write("❌ ⏰ Wait for favorable conditions")
        
        # Achievement check
        track_achievement("scenario_run")

# ============================================================================
# DECISION MATRIX
# ============================================================================
elif menu == "💎 Decision Matrix":
    st.markdown('<h1 class="hero-header">💎 Decision Matrix</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">🧠 AI-Powered Strategic Intelligence Engine 🧠</p>', unsafe_allow_html=True)
    
    st.markdown("### 👨‍🚀 Commander Profile Setup")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 💰 Financial Arsenal")
        annual_income = st.number_input("💵 Annual Income ($)", 30000, 500000, 75000, 5000)
        savings = st.number_input("🏦 War Chest ($)", 0, 200000, 25000, 5000)
        debt_ratio = st.slider("💳 Debt Burden (%)", 0, 50, 15, 1)
        credit_score = st.slider("📊 Battle Rating", 300, 850, 720, 5)
    
    with col2:
        st.markdown("#### 🎯 Mission Parameters")
        home_import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# ============================================================================
# FUTURISTIC GAMING PLATFORM CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="🎮 Mortgage Quest - Futuristic Gaming Platform",
    page_icon="🎮",
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
# FUTURISTIC 3D GAME STYLING
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Exo+2:wght@300;400;500;600;700&display=swap');
    
    :root {
        /* Futuristic Color Palette */
        --primary-blue: #00D4FF;
        --electric-cyan: #0FF0FC;
        --neon-green: #39FF14;
        --cosmic-purple: #9D4EDD;
        --golden-yellow: #FFD60A;
        --coral-pink: #FF6B9D;
        --silver-white: #F8F9FA;
        --deep-space: #0A0E27;
        --space-blue: #1A1F3A;
        --glass-white: rgba(248, 249, 250, 0.95);
        --glass-dark: rgba(26, 31, 58, 0.9);
        
        /* Gradients */
        --hero-gradient: linear-gradient(135deg, var(--primary-blue) 0%, var(--cosmic-purple) 100%);
        --success-gradient: linear-gradient(135deg, var(--neon-green) 0%, var(--electric-cyan) 100%);
        --warning-gradient: linear-gradient(135deg, var(--golden-yellow) 0%, var(--coral-pink) 100%);
        --danger-gradient: linear-gradient(135deg, var(--coral-pink) 0%, var(--cosmic-purple) 100%);
        --card-gradient: linear-gradient(145deg, var(--glass-white) 0%, rgba(255,255,255,0.8) 100%);
    }
    
    * {
        color: var(--deep-space) !important;
        font-family: 'Exo 2', 'Segoe UI', sans-serif !important;
    }
    
    .main {
        background: linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 50%, #E8F5E8 100%);
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
        background: 
            radial-gradient(circle at 20% 20%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(157, 78, 221, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 60% 40%, rgba(57, 255, 20, 0.05) 0%, transparent 50%);
        pointer-events: none;
        animation: float 8s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(2deg); }
    }
    
    .block-container {
        padding: 2rem 1rem;
        background: var(--card-gradient);
        border-radius: 30px;
        margin: 20px;
        box-shadow: 
            0 20px 60px rgba(0, 212, 255, 0.15),
            0 10px 30px rgba(157, 78, 221, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .block-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        animation: shimmer 4s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* FUTURISTIC HEADERS */
    .hero-header {
        text-align: center;
        background: var(--hero-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Orbitron', monospace !important;
        font-size: clamp(2.5rem, 6vw, 5rem) !important;
        font-weight: 900 !important;
        margin: 2rem 0;
        letter-spacing: 0.1em;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
        animation: glow-pulse 3s ease-in-out infinite alternate;
        position: relative;
    }
    
    .hero-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 200px;
        height: 4px;
        background: var(--hero-gradient);
        border-radius: 2px;
        animation: expand 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow-pulse {
        from { text-shadow: 0 0 20px rgba(0, 212, 255, 0.3); }
        to { text-shadow: 0 0 40px rgba(0, 212, 255, 0.8), 0 0 60px rgba(157, 78, 221, 0.4); }
    }
    
    @keyframes expand {
        from { width: 100px; }
        to { width: 300px; }
    }
    
    .hero-subtitle {
        text-align: center;
        color: var(--cosmic-purple) !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        margin-bottom: 3rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        font-family: 'Orbitron', monospace !important;
    }
    
    /* 3D GAMING CARDS */
    .game-card-3d {
        background: var(--card-gradient);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 
            0 25px 50px rgba(0, 212, 255, 0.2),
            0 15px 35px rgba(157, 78, 221, 0.1),
            inset 0 2px 0 rgba(255, 255, 255, 0.8),
            inset 0 -2px 0 rgba(0, 0, 0, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.4);
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    
    .game-card-3d::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: var(--hero-gradient);
        border-radius: 27px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .game-card-3d:hover {
        transform: translateY(-15px) rotateX(5deg) rotateY(2deg) scale(1.02);
        box-shadow: 
            0 35px 70px rgba(0, 212, 255, 0.3),
            0 25px 50px rgba(157, 78, 221, 0.2),
            inset 0 2px 0 rgba(255, 255, 255, 0.9);
    }
    
    .game-card-3d:hover::before {
        opacity: 1;
    }
    
    /* 3D ICONS */
    .icon-3d {
        display: inline-block;
        font-size: 3rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 10px 20px rgba(0, 212, 255, 0.3));
        transition: all 0.3s ease;
        animation: float-icon 4s ease-in-out infinite;
    }
    
    .icon-3d:hover {
        transform: scale(1.2) rotateY(20deg);
        filter: drop-shadow(0 15px 30px rgba(157, 78, 221, 0.5));
    }
    
    @keyframes float-icon {
        0%, 100% { transform: translateY(0px) rotateY(0deg); }
        50% { transform: translateY(-10px) rotateY(5deg); }
    }
    
    /* METRIC CARDS WITH 3D EFFECT */
    .metric-card-3d {
        background: var(--card-gradient);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 
            0 20px 40px rgba(0, 212, 255, 0.15),
            0 10px 25px rgba(157, 78, 221, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        margin: 1rem 0;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .metric-card-3d:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 
            0 30px 60px rgba(0, 212, 255, 0.25),
            0 20px 40px rgba(157, 78, 221, 0.15),
            inset 0 2px 0 rgba(255, 255, 255, 0.9);
    }
    
    .metric-value-3d {
        font-size: 3rem !important;
        font-weight: 900 !important;
        background: var(--hero-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 1rem 0;
        font-family: 'Orbitron', monospace !important;
        text-shadow: 0 5px 15px rgba(0, 212, 255, 0.3);
        animation: number-glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes number-glow {
        from { filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.3)); }
        to { filter: drop-shadow(0 0 25px rgba(0, 212, 255, 0.8)); }
    }
    
    .metric-label-3d {
        color: var(--cosmic-purple) !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-family: 'Orbitron', monospace !important;
    }
    
    .metric-change-3d {
        color: var(--primary-blue) !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    /* 3D PROGRESS BARS */
    .progress-bar-3d {
        height: 35px;
        border-radius: 20px;
        background: rgba(248, 249, 250, 0.3);
        overflow: hidden;
        position: relative;
        margin: 1.5rem 0;
        border: 2px solid rgba(0, 212, 255, 0.3);
        box-shadow: 
            inset 0 5px 15px rgba(0, 0, 0, 0.1),
            0 5px 15px rgba(0, 212, 255, 0.2);
    }
    
    .progress-fill-3d {
        height: 100%;
        background: var(--success-gradient);
        border-radius: 18px;
        transition: width 1.5s cubic-bezier(0.23, 1, 0.320, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(57, 255, 20, 0.5);
    }
    
    .progress-fill-3d::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(255, 255, 255, 0.4) 50%, 
            transparent 100%);
        animation: progress-shine 2s infinite;
    }
    
    @keyframes progress-shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(200%); }
    }
    
    /* FUTURISTIC BUTTONS */
    .stButton > button {
        background: var(--hero-gradient) !important;
        color: white !important;
        border: none !important;
        padding: 1.2rem 3rem !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        font-family: 'Orbitron', monospace !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1) !important;
        box-shadow: 
            0 15px 35px rgba(0, 212, 255, 0.4),
            0 5px 15px rgba(157, 78, 221, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 
            0 25px 50px rgba(0, 212, 255, 0.6),
            0 15px 30px rgba(157, 78, 221, 0.4),
            inset 0 2px 0 rgba(255, 255, 255, 0.5) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* SIDEBAR GAMING STYLE */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--glass-white) 0%, rgba(248, 249, 250, 0.95) 100%) !important;
        border-right: 3px solid var(--primary-blue) !important;
        box-shadow: 5px 0 25px rgba(0, 212, 255, 0.2) !important;
    }
    
    /* NAVIGATION ITEMS */
    .stRadio > div > label {
        background: var(--card-gradient) !important;
        margin: 0.8rem 0 !important;
        padding: 1.2rem !important;
        border-radius: 20px !important;
        border: 2px solid rgba(0, 212, 255, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1) !important;
        cursor: pointer !important;
        color: var(--deep-space) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 10px 25px rgba(0, 212, 255, 0.1) !important;
    }
    
    .stRadio > div > label:hover {
        border: 2px solid var(--primary-blue) !important;
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(157, 78, 221, 0.05) 100%) !important;
        transform: translateX(10px) scale(1.02) !important;
        box-shadow: 0 15px 35px rgba(0, 212, 255, 0.3) !important;
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: var(--hero-gradient) !important;
        border: 2px solid var(--primary-blue) !important;
        color: white !important;
        transform: translateX(15px) scale(1.05) !important;
        box-shadow: 0 20px 40px rgba(0, 212, 255, 0.4) !important;
    }
    
    /* INPUT FIELD STYLING */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: var(--card-gradient) !important;
        border: 2px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 15px !important;
        color: var(--deep-space) !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border: 2px solid var(--primary-blue) !important;
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.4) !important;
    }
    
    /* LABELS */
    .stTextInput > label, .stNumberInput > label, .stSelectbox > label,
    .stSlider > label, .stDateInput > label {
        color: var(--cosmic-purple) !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-family: 'Orbitron', monospace !important;
    }
    
    /* METRICS STYLING */
    .stMetric > div {
        background: var(--card-gradient) !important;
        padding: 2rem !important;
        border-radius: 20px !important;
        border: 2px solid rgba(0, 212, 255, 0.2) !important;
        box-shadow: 0 15px 35px rgba(0, 212, 255, 0.15) !important;
    }
    
    .stMetric label {
        color: var(--cosmic-purple) !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        font-family: 'Orbitron', monospace !important;
    }
    
    .stMetric [data-testid="metric-value"] {
        color: var(--primary-blue) !important;
        font-weight: 900 !important;
        font-size: 2.5rem !important;
        font-family: 'Orbitron', monospace !important;
    }
    
    /* ALERT MESSAGES */
    .stAlert {
        background: var(--card-gradient) !important;
        border: 2px solid var(--primary-blue) !important;
        border-radius: 20px !important;
        color: var(--deep-space) !important;
        padding: 1.5rem !important;
        font-weight: 600 !important;
    }
    
    .stSuccess {
        border-color: var(--neon-green) !important;
        background: linear-gradient(135deg, rgba(57, 255, 20, 0.1) 0%, var(--card-gradient) 100%) !important;
    }
    
    .stWarning {
        border-color: var(--golden-yellow) !important;
        background: linear-gradient(135deg, rgba(255, 214, 10, 0.1) 0%, var(--card-gradient) 100%) !important;
    }
    
    .stError {
        border-color: var(--coral-pink) !important;
        background: linear-gradient(135deg, rgba(255, 107, 157, 0.1) 0%, var(--card-gradient) 100%) !important;
    }
    
    /* HEADERS STYLING */
    h1, h2, h3, h4, h5, h6 {
        color: var(--cosmic-purple) !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }
    
    /* PARAGRAPH TEXT */
    p, div, span, li {
        color: var(--deep-space) !important;
        font-weight: 500 !important;
        line-height: 1.7 !important;
        font-size: 1rem !important;
    }
    
    /* STRONG TEXT */
    strong, b {
        color: var(--primary-blue) !important;
        font-weight: 800 !important;
    }
    
    /* LINKS */
    a {
        color: var(--primary-blue) !important;
        font-weight: 600 !important;
        text-decoration: none !important;
    }
    
    a:hover {
        color: var(--cosmic-purple) !important;
    }
    
    /* LIST ITEMS */
    li {
        color: var(--deep-space) !important;
        font-weight: 500 !important;
        margin: 0.5rem 0 !important;
    }
    
    /* MOBILE RESPONSIVENESS */
    @media (max-width: 768px) {
        .block-container {
            margin: 10px;
            padding: 1.5rem;
        }
        
        .hero-header {
            font-size: 2rem !important;
        }
        
        .game-card-3d {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .metric-value-3d {
            font-size: 2rem !important;
        }
        
        .icon-3d {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# GAMIFICATION SYSTEM
# ============================================================================
ACHIEVEMENTS = {
    "first_visit": {"name": "🏠 Welcome Pilot", "points": 50, "desc": "First mission completed", "icon": "🚀"},
    "scenario_runner": {"name": "🎯 Scenario Master", "points": 100, "desc": "Run 5 battle simulations", "icon": "⚔️"},
    "portfolio_starter": {"name": "📈 Property Commander", "points": 75, "desc": "Add first asset to portfolio", "icon": "💎"},
    "data_explorer": {"name": "📊 Data Wizard", "points": 125, "desc": "Master all analysis tools", "icon": "🔮"},
    "decision_maker": {"name": "💡 Strategic Genius", "points": 200, "desc": "Complete advanced analysis", "icon": "🧠"}
}

def track_achievement(action):
    """Track user achievements and award points"""
    awarded = False
    
    if action == "🎯 Mission Control Hub" and "first_visit" not in st.session_state.user_profile['achievements']:
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
            st.success(f"🎉 LEVEL UP! You've reached Level {new_level}!")
        
        st.success(f"🏆 Achievement Unlocked: {achievement['name']} (+{achievement['points']} XP)")

# ============================================================================
# ENTERPRISE DATA GENERATION
# ============================================================================
@st.cache_data(ttl=300)
def generate_futuristic_data():
    """Generate comprehensive market data for the gaming platform"""
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
    
    df = pd.DataFrame({
        'Date': dates,
        'Mortgage_Rate': rate_trend,
        'Unemployment_Rate': unemployment,
        'Home_Price_Index': hpi_trend,
        'Affordability_Index': affordability,
        'Market_Sentiment': sentiment,
        'Market_Velocity': np.random.uniform(0.5, 2.5, len(dates))
    })
    
    return df

@st.cache_data
def calculate_advanced_metrics(df):
    """Calculate advanced market analytics"""
    latest = df.iloc[-1]
    prev_month = df.iloc[-30] if len(df) > 30 else df.iloc[0]
    prev_year = df.iloc[-365] if len(df) > 365 else df.iloc[0]
    
    metrics = {
        'current_rate': latest['Mortgage_Rate'],
        'rate_change_month': latest['Mortgage_Rate'] - prev_month['Mortgage_Rate'],
        'unemployment': latest['Unemployment_Rate'],
        'unemployment_change': latest['Unemployment_Rate'] - prev_month['Unemployment_Rate'],
        'hpi': latest['Home_Price_Index'],
        'hpi_change': ((latest['Home_Price_Index'] - prev_year['Home_Price_Index']) / prev_year['Home_Price_Index']) * 100,
        'affordability': latest['Affordability_Index'],
        'market_health': 'Elite' if latest['Affordability_Index'] > 70 else 'Advanced' if latest['Affordability_Index'] > 50 else 'Moderate' if latest['Affordability_Index'] > 30 else 'Challenging',
        'volatility': df['Mortgage_Rate'].tail(30).std()
    }
    
    return metrics
