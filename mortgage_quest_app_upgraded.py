    # Achievement Badges (continued)
    padding: 1rem; margin: 0.5rem 0; border-radius: 15px; border: 2px solid rgba(0, 212, 255, 0.3);">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 1.5rem;">{ach['icon']}</span>
            <div>
                <div style="color: #00D4FF; font-weight: 700; font-family: 'Orbitron', monospace;">{ach['name']} {status}</div>
                <div style="color: #0A0E27; font-size: 0.9rem;">{ach['desc']} (+{ach['points']} XP)</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT SECTIONS
# ============================================================================

# Load data for main content
df = generate_futuristic_data()
metrics = calculate_advanced_metrics(df)

# Mission Control Hub
if menu == "🎯 Mission Control Hub":
    track_achievement("🎯 Mission Control Hub")
    
    st.markdown('<h1 class="hero-header">Mission Control Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Command Center for Market Operations</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card-3d">
            <div class="metric-label-3d">Market Health</div>
            <div class="metric-value-3d">{metrics['market_health']}</div>
            <div class="metric-change-3d">Affordability: {metrics['affordability']:.1f}/100</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card-3d">
            <div class="metric-label-3d">Mortgage Rate</div>
            <div class="metric-value-3d">{metrics['current_rate']:.2f}%</div>
            <div class="metric-change-3d">{'↑' if metrics['rate_change_month'] > 0 else '↓'} {abs(metrics['rate_change_month']):.2f}% (30d)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card-3d">
            <div class="metric-label-3d">Price Index</div>
            <div class="metric-value-3d">{metrics['hpi']:.0f}</div>
            <div class="metric-change-3d">{'↑' if metrics['hpi_change'] > 0 else '↓'} {abs(metrics['hpi_change']):.1f}% (1y)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Market Overview Chart
    fig = make_subplots(rows=2, cols=1, 
                       subplot_titles=("Market Trends", "Affordability Index"),
                       vertical_spacing=0.15)
    
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Home_Price_Index'], 
                  name='HPI', line=dict(color='#00D4FF')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Mortgage_Rate'], 
                  name='Rates', line=dict(color='#9D4EDD')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Affordability_Index'], 
                  name='Affordability', line=dict(color='#39FF14')),
        row=2, col=1
    )
    
    fig.update_layout(
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(248,249,250,0.95)',
        font=dict(family='Orbitron', color='#0A0E27'),
        showlegend=True,
        margin=dict(t=100)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Intelligence Center
elif menu == "📊 Intelligence Center":
    st.markdown('<h1 class="hero-header">Intelligence Center</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Advanced Market Analytics</p>', unsafe_allow_html=True)
    
    # Interactive Filters
    col1, col2 = st.columns([1, 3])
    with col1:
        time_range = st.selectbox("Time Range", ["1Y", "2Y", "5Y"], key="intel_time")
        metric = st.selectbox("Metric", ["Home_Price_Index", "Mortgage_Rate", "Affordability_Index"], key="intel_metric")
    
    # Filter data based on selection
    days = {"1Y": 365, "2Y": 730, "5Y": 1825}
    filtered_df = df.tail(days[time_range])
    
    # Detailed Analysis Chart
    fig = px.line(filtered_df, x='Date', y=metric,
                 title=f"{metric.replace('_', ' ')} Analysis",
                 color_discrete_sequence=['#00D4FF'])
    
    fig.update_layout(
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(248,249,250,0.95)',
        font=dict(family='Orbitron', color='#0A0E27')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistical Summary
    stats = filtered_df[metric].describe()
    st.markdown(f"""
    <div class="game-card-3d">
        <h3>Statistical Analysis</h3>
        <ul>
            <li>Mean: {stats['mean']:.2f}</li>
            <li>Std Dev: {stats['std']:.2f}</li>
            <li>Min: {stats['min']:.2f}</li>
            <li>Max: {stats['max']:.2f}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Strategy Simulator
elif menu == "🧠 Strategy Simulator":
    st.markdown('<h1 class="hero-header">Strategy Simulator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Battle-Test Your Mortgage Strategies</p>', unsafe_allow_html=True)
    
    with st.form("simulator_form"):
        col1, col2 = st.columns(2)
        with col1:
            loan_amount = st.number_input("Loan Amount ($)", 100000, 1000000, 300000, step=50000)
            interest_rate = st.number_input("Interest Rate (%)", 1.0, 10.0, metrics['current_rate'], step=0.25)
        with col2:
            loan_term = st.selectbox("Loan Term (Years)", [15, 20, 30])
            down_payment = st.number_input("Down Payment ($)", 0, loan_amount, int(loan_amount * 0.2))
        
        submitted = st.form_submit_button("Run Simulation")
        
        if submitted:
            st.session_state.scenarios_run += 1
            track_achievement("scenario_runner")
            
            # Mortgage calculations
            monthly_rate = interest_rate / 1200
            num_payments = loan_term * 12
            monthly_payment = loan_amount * monthly_rate * (1 + monthly_rate)**num_payments / ((1 + monthly_rate)**num_payments - 1)
            total_cost = monthly_payment * num_payments
            
            st.markdown(f"""
            <div class="game-card-3d">
                <h3>Simulation Results</h3>
                <ul>
                    <li>Monthly Payment: ${monthly_payment:,.2f}</li>
                    <li>Total Cost: ${total_cost:,.2f}</li>
                    <li>Total Interest: ${(total_cost - loan_amount):,.2f}</li>
                    <li>Monthly Income Needed: ${(monthly_payment * 3):,.2f}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Amortization Schedule
            schedule = []
            balance = loan_amount
            for i in range(num_payments):
                interest = balance * monthly_rate
                principal = monthly_payment - interest
                balance -= principal
                schedule.append([i+1, monthly_payment, principal, interest, max(0, balance)])
            
            schedule_df = pd.DataFrame(schedule, 
                                     columns=['Month', 'Payment', 'Principal', 'Interest', 'Balance'])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=schedule_df['Month'], y=schedule_df['Balance'],
                                   name='Balance', line=dict(color='#00D4FF')))
            fig.add_trace(go.Scatter(x=schedule_df['Month'], y=schedule_df['Interest'],
                                   name='Interest', line=dict(color='#9D4EDD')))
            
            fig.update_layout(
                title="Amortization Schedule",
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(248,249,250,0.95)',
                font=dict(family='Orbitron', color='#0A0E27')
            )
            
            st.plotly_chart(fig, use_container_width=True)

# Decision Matrix
elif menu == "💎 Decision Matrix":
    st.markdown('<h1 class="hero-header">Decision Matrix</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Strategic Property Analysis</p>', unsafe_allow_html=True)
    
    with st.form("decision_form"):
        col1, col2 = st.columns(2)
        with col1:
            property_value = st.number_input("Property Value ($)", 100000, 2000000, 400000)
            rental_income = st.number_input("Monthly Rental Income ($)", 0, 10000, 2000)
        with col2:
            maintenance_cost = st.number_input("Annual Maintenance ($)", 0, 50000, 5000)
            property_tax = st.number_input("Annual Property Tax ($)", 0, 20000, 4000)
        
        submitted = st.form_submit_button("Analyze Investment")
        
        if submitted:
            # ROI Calculations
            annual_net_income = (rental_income * 12) - maintenance_cost - property_tax
            roi = (annual_net_income / property_value) * 100
            
            st.markdown(f"""
            <div class="game-card-3d">
                <h3>Investment Analysis</h3>
                <ul>
                    <li>Annual Net Income: ${annual_net_income:,.2f}</li>
                    <li>ROI: {roi:.2f}%</li>
                    <li>Cap Rate: {(annual_net_income / property_value * 100):.2f}%</li>
                    <li>Break-even Years: {property_value / annual_net_income:.1f}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Risk Assessment
            risk_score = (metrics['current_rate'] * 10 + metrics['unemployment'] * 5 - metrics['affordability'] / 2) / 100
            risk_level = "Low" if risk_score < 0.3 else "Medium" if risk_score < 0.6 else "High"
            
            st.markdown(f"""
            <div class="game-card-3d">
                <h3>Risk Assessment</h3>
                <div>Risk Level: <span style="color: {'#39FF14' if risk_level == 'Low' else '#FFD60A' if risk_level == 'Medium' else '#FF6B9D'}">{risk_level}</span></div>
                <div>Risk Score: {risk_score:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

# Asset Portfolio
elif menu == "📈 Asset Portfolio":
    st.markdown('<h1 class="hero-header">Asset Portfolio</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Manage Your Property Empire</p>', unsafe_allow_html=True)
    
    with st.form("portfolio_form"):
        property_name = st.text_input("Property Name")
        purchase_price = st.number_input("Purchase Price ($)", 100000, 2000000, 400000)
        current_value = st.number_input("Current Value ($)", 100000, 2000000, 400000)
        
        if st.form_submit_button("Add Property"):
            st.session_state.properties.append({
                'name': property_name,
                'purchase_price': purchase_price,
                'current_value': current_value,
                'appreciation': ((current_value - purchase_price) / purchase_price) * 100
            })
            track_achievement("portfolio_starter")
            st.success(f"Property {property_name} added to portfolio!")
    
    if st.session_state.properties:
        portfolio_df = pd.DataFrame(st.session_state.properties)
        total_value = portfolio_df['current_value'].sum()
        total_appreciation = portfolio_df['appreciation'].mean()
        
        st.markdown(f"""
        <div class="game-card-3d">
            <h3>Portfolio Summary</h3>
            <ul>
                <li>Total Properties: {len(st.session_state.properties)}</li>
                <li>Total Value: ${total_value:,.2f}</li>
                <li>Average Appreciation: {total_appreciation:.2f}%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(portfolio_df.style.format({
            'purchase_price': '${:,.2f}',
            'current_value': '${:,.2f}',
            'appreciation': '{:.2f}%'
        }))

# Command Brief
elif menu == "ℹ️ Command Brief":
    st.markdown('<h1 class="hero-header">Command Brief</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Mission Guidelines & Intelligence</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="game-card-3d">
        <h3>Welcome to Mortgage Quest</h3>
        <p>Your mission is to navigate the complex housing market using advanced analytics and strategic simulations. Complete missions to earn XP, unlock achievements, and level up your Commander status.</p>
        <h4>Key Objectives:</h4>
        <ul>
            <li>Analyze market trends in the Intelligence Center</li>
            <li>Test strategies in the Strategy Simulator</li>
            <li>Build your empire in the Asset Portfolio</li>
            <li>Make informed decisions using the Decision Matrix</li>
        </ul>
        <h4>System Features:</h4>
        <ul>
            <li>Real-time market data updates</li>
            <li>Advanced visualization systems</li>
            <li>Gamified progression system</li>
            <li>Strategic analysis tools</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Real-time Updates
if real_time_updates and battle_alerts:
    if metrics['volatility'] > 0.5:
        st.warning("⚠️ High market volatility detected! Proceed with caution.")
    if metrics['affordability'] < 40:
        st.error("🚨 Challenging market conditions! Review strategies carefully.")

# Advanced Mode Features
if advanced_mode:
    st.markdown("""
    <div class="game-card-3d">
        <h3>Advanced Analytics Mode</h3>
        <p>Enhanced data processing and predictive modeling activated. Contact Mission Control for custom analysis requests.</p>
    </div>
    """, unsafe_allow_html=True)
