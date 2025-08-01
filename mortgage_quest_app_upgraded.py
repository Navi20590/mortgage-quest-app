import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import random

# Page Configuration
st.set_page_config(
    page_title="🏠 Mortgage Quest Elite",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'achievements': [],
        'points': 2450,
        'level': 12,
        'wallet_balance': 850.75,
        'current_streak': 7,
        'current_mode': 'dashboard'
    }

if 'properties' not in st.session_state:
    st.session_state.properties = []

if 'scenarios_run' not in st.session_state:
    st.session_state.scenarios_run = 0

if 'quests_completed' not in st.session_state:
    st.session_state.quests_completed = {}

# Life Stage Modes Configuration
LIFE_STAGE_MODES = {
    'first-timer': {
        'name': 'First Timer',
        'character': '🎯 First Timer Fred',
        'age_range': '22-28',
        'emoji': '🎯',
        'color': '#059669',
        'bg_color': '#ECFDF5',
        'description': 'Build credit, learn basics, save for first home',
        'features': ['Credit Score Building', 'Down Payment Savings', 'Market Education'],
        'current_quests': [
            {'name': 'Coffee Tracker Challenge', 'progress': 75, 'xp': 50, 'description': 'Track daily coffee expenses for 30 days'},
            {'name': 'Credit Score Boost', 'progress': 40, 'xp': 100, 'description': 'Improve credit score by 50 points'},
            {'name': 'Rent vs Buy Calculator', 'progress': 90, 'xp': 75, 'description': 'Complete 10 rent vs buy analyses'}
        ],
        'achievements': ['First Steps', 'Smart Saver', 'Credit Builder'],
        'mini_games': ['Credit Score Tetris', 'Budgeting Snake', 'Rent vs Buy Challenge']
    },
    'family-builder': {
        'name': 'Family Builder',
        'character': '👨‍👩‍👧‍👦 Family Planner',
        'age_range': '28-35',
        'emoji': '👨‍👩‍👧‍👦',
        'color': '#1E40AF',
        'bg_color': '#EFF6FF',
        'description': 'Family home planning and school district research',
        'features': ['School District Analysis', 'Family Budget Planning', 'Joint Savings Goals'],
        'current_quests': [
            {'name': 'School District Research', 'progress': 60, 'xp': 120, 'description': 'Research top 5 school districts in your area'},
            {'name': 'Family Emergency Fund', 'progress': 85, 'xp': 80, 'description': 'Build 6-month emergency fund'},
            {'name': 'Childcare Cost Planning', 'progress': 30, 'xp': 100, 'description': 'Calculate childcare costs for next 5 years'}
        ],
        'achievements': ['Nesting Expert', 'Team Player', 'Future Planner'],
        'mini_games': ['School District Memory Match', 'Family Budget Balancer', 'Nesting Tower Defense']
    },
    'trade-up-pro': {
        'name': 'Trade-Up Pro',
        'character': '🏠 Equity Optimizer',
        'age_range': '35-45',
        'emoji': '🏠',
        'color': '#D97706',
        'bg_color': '#FEF3E2',
        'description': 'Maximize equity through strategic improvements',
        'features': ['Market Timing', 'Equity Optimization', 'Advanced Strategies'],
        'current_quests': [
            {'name': 'Market Timing Mastery', 'progress': 45, 'xp': 200, 'description': 'Time 3 successful market transactions'},
            {'name': 'Equity Extraction Strategy', 'progress': 70, 'xp': 150, 'description': 'Develop optimal equity extraction plan'},
            {'name': 'Simultaneous Buy/Sell', 'progress': 20, 'xp': 300, 'description': 'Execute simultaneous buy/sell transaction'}
        ],
        'achievements': ['Portfolio Master', 'Timing Expert', 'Equity Genius'],
        'mini_games': ['Market Timing Flight Simulator', 'Equity Extraction Puzzle', 'Transaction Manager']
    },
    'smart-downsizer': {
        'name': 'Smart Downsizer',
        'character': '🏖️ Freedom Seeker',
        'age_range': '55+',
        'emoji': '🏖️',
        'color': '#7C3AED',
        'bg_color': '#F5F3FF',
        'description': 'Optimize retirement through strategic downsizing',
        'features': ['Geographic Arbitrage', 'Retirement Planning', 'Healthcare Integration'],
        'current_quests': [
            {'name': 'Geographic Arbitrage Analysis', 'progress': 80, 'xp': 180, 'description': 'Compare 10 retirement destinations'},
            {'name': 'Healthcare Cost Planning', 'progress': 55, 'xp': 120, 'description': 'Estimate healthcare costs for next 20 years'},
            {'name': 'Freedom Fund Building', 'progress': 90, 'xp': 250, 'description': 'Accumulate target retirement fund'}
        ],
        'achievements': ['Freedom Fighter', 'Smart Mover', 'Retirement Ready'],
        'mini_games': ['Geographic Arbitrage Explorer', 'Retirement Income Optimizer', 'Healthcare Cost Predictor']
    },
    'property-investor': {
        'name': 'Property Investor',
        'character': '🏛️ Property Mogul',
        'age_range': 'Any Age',
        'emoji': '🏛️',
        'color': '#DC2626',
        'bg_color': '#FEF2F2',
        'description': 'Build rental empire with advanced strategies',
        'features': ['BRRRR Method', 'Cash Flow Analysis', 'Portfolio Building'],
        'current_quests': [
            {'name': 'BRRRR Method Mastery', 'progress': 65, 'xp': 300, 'description': 'Complete full BRRRR cycle'},
            {'name': 'Cash Flow Optimization', 'progress': 40, 'xp': 200, 'description': 'Achieve positive cash flow on 3 properties'},
            {'name': 'Portfolio Diversification', 'progress': 75, 'xp': 250, 'description': 'Invest in 3 different property types'}
        ],
        'achievements': ['Landlord Legend', 'Cash Flow King', 'Portfolio Pro'],
        'mini_games': ['Cash Flow Calculator Pro', 'BRRRR Method Simulator', 'Portfolio Diversification Challenge']
    }
}

# Advanced CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Exo+2:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-blue: #1E40AF;
        --electric-blue: #3B82F6;
        --cyber-purple: #7C3AED;
        --neon-green: #059669;
        --emerald-green: #10B981;
        --sunset-orange: #EA580C;
        --golden-yellow: #D97706;
        --coral-pink: #DC2626;
        --hot-pink: #EC4899;
        --deep-space: #0F172A;
        --slate-gray: #334155;
        --glass-white: rgba(255, 255, 255, 0.95);
        --glass-blue: rgba(59, 130, 246, 0.1);
        --glass-purple: rgba(124, 58, 237, 0.1);
        --glass-green: rgba(16, 185, 129, 0.1);
        --hero-gradient: linear-gradient(135deg, #1E40AF 0%, #7C3AED 30%, #EC4899 60%, #DC2626 100%);
        --card-gradient: linear-gradient(145deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,0.95) 100%);
        --neon-glow: 0 0 20px rgba(59, 130, 246, 0.4), 0 0 40px rgba(124, 58, 237, 0.2);
        --shadow-premium: 0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(255, 255, 255, 0.05);
    }
    
    * {
        color: var(--deep-space) !important;
        font-family: 'Exo 2', sans-serif !important;
    }
    
    .main {
        background: linear-gradient(135deg, 
            #F8FAFC 0%, 
            #EEF2FF 15%, 
            #F0F9FF 30%, 
            #ECFDF5 45%, 
            #FEF3E2 60%, 
            #FDF2F8 75%, 
            #F5F3FF 90%, 
            #F1F5F9 100%);
        background-attachment: fixed;
        min-height: 100vh;
        position: relative;
    }
    
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(30, 64, 175, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(124, 58, 237, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(16, 185, 129, 0.03) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    .block-container {
        background: var(--card-gradient);
        border-radius: 35px;
        padding: 2.5rem;
        margin: 25px;
        box-shadow: var(--shadow-premium);
        border: 2px solid rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    
    .block-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1E40AF 0%, #7C3AED 25%, #EC4899 50%, #DC2626 75%, #059669 100%);
        border-radius: 35px 35px 0 0;
    }
    
    .hero-header {
        text-align: center;
        background: linear-gradient(135deg, #1E40AF 0%, #7C3AED 25%, #EC4899 50%, #DC2626 75%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace !important;
        font-size: clamp(2.5rem, 6vw, 4.5rem) !important;
        font-weight: 900 !important;
        margin: 1.5rem 0;
        letter-spacing: 0.1em;
        filter: drop-shadow(0 4px 8px rgba(30, 64, 175, 0.3));
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
        background: linear-gradient(90deg, transparent 0%, #7C3AED 50%, transparent 100%);
        border-radius: 2px;
    }
    
    .hero-subtitle {
        text-align: center;
        background: linear-gradient(135deg, #1E40AF 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        margin-bottom: 3rem;
        letter-spacing: 0.3em;
        text-transform: uppercase;
        font-family: 'Orbitron', monospace !important;
        filter: drop-shadow(0 2px 4px rgba(124, 58, 237, 0.2));
    }
    
    .mode-card {
        background: var(--card-gradient);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 20px 50px rgba(59, 130, 246, 0.2);
        border: 3px solid rgba(255, 255, 255, 0.4);
        transition: all 0.4s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .mode-card:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 35px 70px rgba(59, 130, 246, 0.35);
    }
    
    .mode-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.5s;
        opacity: 0;
    }
    
    .mode-card:hover::before {
        animation: shine 0.5s ease-in-out;
        opacity: 1;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .metric-card-3d {
        background: linear-gradient(145deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,0.95) 100%);
        border-radius: 25px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 
            0 20px 40px rgba(15, 23, 42, 0.08),
            0 8px 16px rgba(15, 23, 42, 0.04),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1.5px solid rgba(255, 255, 255, 0.6);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-3d::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #1E40AF 0%, #7C3AED 50%, #EC4899 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card-3d:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 
            0 35px 70px rgba(15, 23, 42, 0.15),
            0 15px 30px rgba(15, 23, 42, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }
    
    .metric-card-3d:hover::before {
        opacity: 1;
    }
    
    .metric-value-3d {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #1E40AF 0%, #7C3AED 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
        font-family: 'Orbitron', monospace !important;
        filter: drop-shadow(0 2px 4px rgba(30, 64, 175, 0.3));
        text-shadow: none;
    }
    
    .metric-label-3d {
        background: linear-gradient(135deg, #334155 0%, #1E40AF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-family: 'Orbitron', monospace !important;
    }
    
    .progress-bar-quest {
        height: 30px;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(248, 250, 252, 0.8) 0%, rgba(241, 245, 249, 0.9) 100%);
        overflow: hidden;
        position: relative;
        margin: 1rem 0;
        border: 2px solid rgba(30, 64, 175, 0.2);
        box-shadow: inset 0 2px 4px rgba(15, 23, 42, 0.06);
    }
    
    .progress-fill-quest {
        height: 100%;
        background: linear-gradient(135deg, #059669 0%, #10B981 30%, #1E40AF 70%, #7C3AED 100%);
        border-radius: 18px;
        transition: width 2s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 0 20px rgba(16, 185, 129, 0.4),
            inset 0 1px 2px rgba(255, 255, 255, 0.3);
    }
    
    .progress-fill-quest::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #1E40AF 0%, #7C3AED 50%, #EC4899 100%) !important;
        color: white !important;
        border: none !important;
        padding: 1.5rem 3rem !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        font-family: 'Orbitron', monospace !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 10px 30px rgba(30, 64, 175, 0.4),
            0 4px 15px rgba(124, 58, 237, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
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
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 
            0 20px 40px rgba(30, 64, 175, 0.5),
            0 8px 25px rgba(124, 58, 237, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        background: linear-gradient(135deg, #1D4ED8 0%, #6D28D9 50%, #DB2777 100%) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .quest-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,0.95) 100%);
        border-radius: 25px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1.5px solid rgba(30, 64, 175, 0.15);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 10px 25px rgba(15, 23, 42, 0.06),
            0 4px 10px rgba(15, 23, 42, 0.03);
    }
    
    .quest-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #059669 0%, #1E40AF 50%, #7C3AED 100%);
        transform: scaleX(0);
        transition: transform 0.3s ease;
        transform-origin: left;
    }
    
    .quest-card:hover {
        transform: translateX(15px) translateY(-5px);
        border-color: #1E40AF;
        box-shadow: 
            0 25px 50px rgba(30, 64, 175, 0.15),
            0 10px 25px rgba(15, 23, 42, 0.08);
    }
    
    .quest-card:hover::before {
        transform: scaleX(1);
    }
    
    .achievement-badge {
        background: linear-gradient(135deg, #D97706 0%, #DC2626 50%, #EC4899 100%);
        color: white !important;
        padding: 0.75rem 1.5rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        box-shadow: 
            0 8px 20px rgba(217, 119, 6, 0.3),
            0 3px 8px rgba(220, 38, 38, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .achievement-badge:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 
            0 12px 30px rgba(217, 119, 6, 0.4),
            0 5px 15px rgba(220, 38, 38, 0.3);
    }
    
    .mini-game-card {
        background: var(--card-gradient);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid rgba(59, 130, 246, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
        margin: 1rem 0;
    }
    
    .mini-game-card:hover {
        transform: scale(1.05);
        border-color: #3B82F6;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.2);
    }
    
    .wallet-feature {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(255,255,255,0.9) 100%);
        border: 2px solid #10B981;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .sidebar-profile {
        background: linear-gradient(145deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,0.95) 100%);
        border-radius: 25px;
        padding: 2.5rem;
        text-align: center;
        border: 1.5px solid rgba(30, 64, 175, 0.2);
        margin-bottom: 2rem;
        box-shadow: 
            0 15px 35px rgba(15, 23, 42, 0.08),
            0 5px 15px rgba(15, 23, 42, 0.04),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        position: relative;
        overflow: hidden;
    }
    
    .sidebar-profile::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1E40AF 0%, #7C3AED 50%, #EC4899 100%);
        border-radius: 25px 25px 0 0;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--cosmic-purple) !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    .mode-selector {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .icon-3d {
        font-size: 4rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 8px 16px rgba(30, 64, 175, 0.25)) drop-shadow(0 4px 8px rgba(124, 58, 237, 0.15));
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        display: inline-block;
        transform-style: preserve-3d;
    }
    
    .icon-3d:hover {
        transform: scale(1.15) rotateY(15deg) rotateX(5deg);
        filter: drop-shadow(0 12px 24px rgba(30, 64, 175, 0.35)) drop-shadow(0 6px 12px rgba(124, 58, 237, 0.25));
    }
    
    h1, h2, h3, h4, h5, h6 {
        background: linear-gradient(135deg, #1E40AF 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        filter: drop-shadow(0 2px 4px rgba(30, 64, 175, 0.2));
    } 92, 246, 0.5));
    }
</style>
""", unsafe_allow_html=True)

# Achievement System
ACHIEVEMENTS = {
    "first_visit": {"name": "🏠 Welcome Commander", "points": 50, "desc": "First mission completed", "icon": "🚀"},
    "mode_explorer": {"name": "🎯 Mode Explorer", "points": 100, "desc": "Visit all 5 life stage modes", "icon": "🗺️"},
    "quest_master": {"name": "⚔️ Quest Master", "points": 200, "desc": "Complete 10 quests", "icon": "👑"},
    "portfolio_starter": {"name": "📈 Portfolio Commander", "points": 75, "desc": "Add first property", "icon": "💎"},
    "streak_warrior": {"name": "🔥 Streak Warrior", "points": 150, "desc": "Maintain 30-day streak", "icon": "⚡"},
}

def track_achievement(action):
    awarded = False
    if action == "first_visit" and "first_visit" not in st.session_state.user_profile['achievements']:
        award_achievement("first_visit")
        awarded = True
    elif action == "mode_visit":
        visited_modes = st.session_state.get('visited_modes', set())
        if len(visited_modes) >= 5 and "mode_explorer" not in st.session_state.user_profile['achievements']:
            award_achievement("mode_explorer")
            awarded = True
    return awarded

def award_achievement(achievement_id):
    if achievement_id not in st.session_state.user_profile['achievements']:
        achievement = ACHIEVEMENTS[achievement_id]
        st.session_state.user_profile['achievements'].append(achievement_id)
        st.session_state.user_profile['points'] += achievement['points']
        new_level = (st.session_state.user_profile['points'] // 500) + 1
        if new_level > st.session_state.user_profile['level']:
            st.session_state.user_profile['level'] = new_level
            st.balloons()
            st.success(f"🎉 LEVEL UP! You've reached Level {new_level}!")
        st.success(f"🏆 Achievement Unlocked: {achievement['name']} (+{achievement['points']} XP)")

# Data Generation Functions
@st.cache_data(ttl=300)
def generate_market_data():
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='D')
    
    base_rate = 3.0
    rate_volatility = np.random.normal(0, 0.02, len(dates))
    rate_trend = base_rate + np.cumsum(rate_volatility)
    rate_trend = np.clip(rate_trend, 1.5, 9.0)
    
    unemployment_base = 4.0
    unemployment = unemployment_base + np.cumsum(np.random.normal(0, 0.1, len(dates)))
    unemployment = np.clip(unemployment, 2.5, 18.0)
    
    hpi_base = 250
    seasonal_effect = 10 * np.sin(2 * np.pi * dates.dayofyear / 365.25)
    hpi_trend = hpi_base + np.cumsum(np.random.normal(0.05, 0.8, len(dates))) + seasonal_effect
    hpi_trend = np.clip(hpi_trend, 180, 450)
    
    affordability = 100 - (rate_trend * 8) - (unemployment * 3) - ((hpi_trend - 250) * 0.1) + np.random.normal(0, 3, len(dates))
    affordability = np.clip(affordability, 15, 95)
    
    df = pd.DataFrame({
        'Date': dates,
        'Mortgage_Rate': rate_trend,
        'Unemployment_Rate': unemployment,
        'Home_Price_Index': hpi_trend,
        'Affordability_Index': affordability,
        'Market_Velocity': np.random.uniform(0.5, 2.5, len(dates))
    })
    
    return df

@st.cache_data
def calculate_metrics(df):
    latest = df.iloc[-1]
    prev_month = df.iloc[-30] if len(df) > 30 else df.iloc[0]
    
    return {
        'current_rate': latest['Mortgage_Rate'],
        'rate_change': latest['Mortgage_Rate'] - prev_month['Mortgage_Rate'],
        'unemployment': latest['Unemployment_Rate'],
        'hpi': latest['Home_Price_Index'],
        'affordability': latest['Affordability_Index'],
        'market_health': 'Elite' if latest['Affordability_Index'] > 70 else 'Advanced' if latest['Affordability_Index'] > 50 else 'Moderate' if latest['Affordability_Index'] > 30 else 'Challenging'
    }

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div class="sidebar-profile">
        <div class="icon-3d">🏠</div>
        <h1 style="background: linear-gradient(45deg, #3B82F6, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.8rem; margin: 0;">
            MORTGAGE QUEST
        </h1>
        <p style="color: #8B5CF6; font-size: 1rem; font-weight: 600; margin: 0.5rem 0;">Elite Gaming Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User Profile Display
    st.markdown(f"""
    <div class="sidebar-profile">
        <div class="icon-3d">👨‍🚀</div>
        <div style="color: #3B82F6; font-weight: 700; font-size: 1.2rem;">Level {st.session_state.user_profile['level']} Commander</div>
        <div style="color: #8B5CF6; font-weight: 600;">{st.session_state.user_profile['points']:,} XP</div>
        <div style="color: #10B981; font-weight: 600;">${st.session_state.user_profile['wallet_balance']:.2f} Wallet</div>
        <div style="color: #F59E0B; font-weight: 600;">{st.session_state.user_profile['current_streak']} Day Streak</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Menu
    menu_options = [
        "🎯 Mission Control Hub",
        "🎮 Life Stage Modes",
        "📊 Intelligence Center",
        "🧠 Strategy Simulator",
        "💎 Decision Matrix",
        "📈 Asset Portfolio",
        "ℹ️ Command Brief"
    ]
    
    selected_menu = st.radio("🚀 Navigation Console:", menu_options)
    
    # Quick Stats
    df = generate_market_data()
    metrics = calculate_metrics(df)
    
    st.markdown("### 🌌 Market Status")
    health_colors = {
        'Elite': '#059669',
        'Advanced': '#1E40AF',
        'Moderate': '#D97706',
        'Challenging': '#DC2626'
    }
    health_color = health_colors.get(metrics['market_health'], '#334155')
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {health_color}20 0%, rgba(255,255,255,0.9) 100%); 
                border: 2px solid {health_color}; border-radius: 15px; padding: 1.5rem; text-align: center;">
        <div style="color: {health_color}; font-weight: 700; font-size: 1.3rem;">{metrics['market_health']}</div>
        <div style="color: #1F2937; font-size: 1.1rem;">{metrics['affordability']:.0f}/100 Health</div>
    </div>
    """, unsafe_allow_html=True)

# Main Content Area
if selected_menu == "🎯 Mission Control Hub":
    track_achievement("first_visit")
    
    st.markdown('<h1 class="hero-header">🏠 MORTGAGE QUEST ELITE</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Multi-Modal Fintech Gaming Platform for Every Life Stage</p>', unsafe_allow_html=True)
    
    # Quick Stats Dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card-3d" style="background: linear-gradient(135deg, #1E40AF20 0%, rgba(255,255,255,0.98) 100%); border-color: #1E40AF;">
            <div class="icon-3d" style="color: #1E40AF;">👑</div>
            <div class="metric-label-3d">Player Level</div>
            <div class="metric-value-3d">{st.session_state.user_profile['level']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card-3d" style="background: linear-gradient(135deg, #05966920 0%, rgba(255,255,255,0.98) 100%); border-color: #059669;">
            <div class="icon-3d" style="color: #059669;">⭐</div>
            <div class="metric-label-3d">Total XP</div>
            <div class="metric-value-3d">{st.session_state.user_profile['points']:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card-3d" style="background: linear-gradient(135deg, #D9770620 0%, rgba(255,255,255,0.98) 100%); border-color: #D97706;">
            <div class="icon-3d" style="color: #D97706;">💰</div>
            <div class="metric-label-3d">Wallet Balance</div>
            <div class="metric-value-3d">${st.session_state.user_profile['wallet_balance']:.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card-3d" style="background: linear-gradient(135deg, #DC262620 0%, rgba(255,255,255,0.98) 100%); border-color: #DC2626;">
            <div class="icon-3d" style="color: #DC2626;">🔥</div>
            <div class="metric-label-3d">Daily Streak</div>
            <div class="metric-value-3d">{st.session_state.user_profile['current_streak']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Life Stage Mode Preview
    st.markdown("### 🎮 Life Stage Gaming Modes")
    st.markdown("Choose your financial journey and unlock personalized quests, mini-games, and rewards!")
    
    mode_cols = st.columns(3)
    mode_items = list(LIFE_STAGE_MODES.items())
    
    for i, (mode_key, mode_data) in enumerate(mode_items[:3]):
        with mode_cols[i % 3]:
            if st.button(f"{mode_data['emoji']} {mode_data['name']}", key=f"mode_btn_{mode_key}", use_container_width=True):
                st.session_state.user_profile['current_mode'] = mode_key
                st.rerun()
            
            st.markdown(f"""
            <div style="background: {mode_data['bg_color']}; border: 2px solid {mode_data['color']}; 
                        border-radius: 15px; padding: 1rem; margin: 0.5rem 0; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{mode_data['emoji']}</div>
                <div style="color: {mode_data['color']}; font-weight: 700; font-size: 1.1rem;">{mode_data['name']}</div>
                <div style="color: #1F2937; font-size: 0.9rem; margin: 0.5rem 0;">{mode_data['age_range']}</div>
                <div style="color: #1F2937; font-size: 0.8rem;">{mode_data['description']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Remaining modes in second row
    if len(mode_items) > 3:
        mode_cols2 = st.columns(3)
        for i, (mode_key, mode_data) in enumerate(mode_items[3:]):
            with mode_cols2[i]:
                if st.button(f"{mode_data['emoji']} {mode_data['name']}", key=f"mode_btn2_{mode_key}", use_container_width=True):
                    st.session_state.user_profile['current_mode'] = mode_key
                    st.rerun()
                
                st.markdown(f"""
                <div style="background: {mode_data['bg_color']}; border: 2px solid {mode_data['color']}; 
                            border-radius: 15px; padding: 1rem; margin: 0.5rem 0; text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{mode_data['emoji']}</div>
                    <div style="color: {mode_data['color']}; font-weight: 700; font-size: 1.1rem;">{mode_data['name']}</div>
                    <div style="color: #1F2937; font-size: 0.9rem; margin: 0.5rem 0;">{mode_data['age_range']}</div>
                    <div style="color: #1F2937; font-size: 0.8rem;">{mode_data['description']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Achievements
    st.markdown("### 🏆 Recent Achievements")
    
    achievement_cols = st.columns(2)
    for i, (ach_id, ach_data) in enumerate(list(ACHIEVEMENTS.items())[:4]):
        with achievement_cols[i % 2]:
            status = "✅" if ach_id in st.session_state.user_profile['achievements'] else "🔒"
            st.markdown(f"""
            <div class="achievement-badge" style="width: 100%; text-align: center; margin: 0.5rem 0;">
                {status} {ach_data['icon']} {ach_data['name']} (+{ach_data['points']} XP)
            </div>
            """, unsafe_allow_html=True)
    
    # Market Overview Chart
    st.markdown("### 📊 Live Market Intelligence")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Mortgage Rates', 'Unemployment Rate', 'Home Price Index', 'Affordability Index'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Add traces
    fig.add_trace(
        go.Scatter(x=df['Date'].tail(90), y=df['Mortgage_Rate'].tail(90), 
                  name='Mortgage Rate', line=dict(color='#3B82F6', width=3)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df['Date'].tail(90), y=df['Unemployment_Rate'].tail(90), 
                  name='Unemployment', line=dict(color='#EF4444', width=3)),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Scatter(x=df['Date'].tail(90), y=df['Home_Price_Index'].tail(90), 
                  name='HPI', line=dict(color='#8B5CF6', width=3)),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df['Date'].tail(90), y=df['Affordability_Index'].tail(90), 
                  name='Affordability', fill='tozeroy', line=dict(color='#10B981', width=3)),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, 
                     title_text="📈 90-Day Market Trends", 
                     plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    
    st.plotly_chart(fig, use_container_width=True)

elif selected_menu == "🎮 Life Stage Modes":
    st.markdown('<h1 class="hero-header">🎮 Life Stage Gaming Modes</h1>', unsafe_allow_html=True)
    
    # Mode Selection
    if st.session_state.user_profile['current_mode'] == 'dashboard':
        st.markdown("### Choose Your Financial Journey")
        
        for mode_key, mode_data in LIFE_STAGE_MODES.items():
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if st.button(f"Enter {mode_data['name']}", key=f"enter_{mode_key}", use_container_width=True):
                    st.session_state.user_profile['current_mode'] = mode_key
                    if 'visited_modes' not in st.session_state:
                        st.session_state.visited_modes = set()
                    st.session_state.visited_modes.add(mode_key)
                    track_achievement("mode_visit")
                    st.rerun()
            
            with col2:
                st.markdown(f"""
                <div class="mode-card" style="background: {mode_data['bg_color']}; border-color: {mode_data['color']};">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <div style="font-size: 3rem; margin-right: 1rem;">{mode_data['emoji']}</div>
                        <div>
                            <h3 style="color: {mode_data['color']}; margin: 0;">{mode_data['name']}</h3>
                            <p style="color: #1F2937; margin: 0; font-weight: 600;">{mode_data['character']}</p>
                            <span style="background: {mode_data['color']}; color: white; padding: 0.25rem 0.5rem; 
                                        border-radius: 10px; font-size: 0.8rem;">{mode_data['age_range']}</span>
                        </div>
                    </div>
                    <p style="color: #1F2937; margin-bottom: 1rem;">{mode_data['description']}</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                        {' '.join([f'<span style="background: rgba(59,130,246,0.1); color: #3B82F6; padding: 0.25rem 0.5rem; border-radius: 8px; font-size: 0.8rem;">{feature}</span>' for feature in mode_data['features']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # Display selected mode details
        current_mode = LIFE_STAGE_MODES[st.session_state.user_profile['current_mode']]
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {current_mode['emoji']} {current_mode['name']} Mode")
            st.markdown(f"**Character:** {current_mode['character']}")
        
        with col2:
            if st.button("← Back to Mode Selection", use_container_width=True):
                st.session_state.user_profile['current_mode'] = 'dashboard'
                st.rerun()
        
        st.markdown(f"""
        <div style="background: {current_mode['bg_color']}; border: 3px solid {current_mode['color']}; 
                    border-radius: 20px; padding: 2rem; margin: 1rem 0;">
            <h4 style="color: {current_mode['color']};">Mission Description</h4>
            <p style="color: #1F2937; font-size: 1.1rem; font-weight: 500;">{current_mode['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Active Quests
        st.markdown("### ⚔️ Active Quests")
        
        for i, quest in enumerate(current_mode['current_quests']):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class="quest-card">
                    <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 0.5rem;">
                        <h4 style="color: #1F2937; margin: 0; flex-grow: 1;">{quest['name']}</h4>
                        <span style="background: {current_mode['color']}; color: white; padding: 0.25rem 0.5rem; 
                                    border-radius: 10px; font-size: 0.8rem;">+{quest['xp']} XP</span>
                    </div>
                    <p style="color: #6B7280; margin: 0.5rem 0; font-size: 0.9rem;">{quest['description']}</p>
                    <div class="progress-bar-quest">
                        <div class="progress-fill-quest" style="width: {quest['progress']}%;"></div>
                    </div>
                    <p style="color: #1F2937; margin: 0; font-size: 0.8rem; font-weight: 600;">{quest['progress']}% Complete</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"Continue Quest", key=f"quest_{i}", use_container_width=True):
                    # Simulate quest progress
                    if quest['progress'] < 100:
                        progress_increase = random.randint(5, 25)
                        quest['progress'] = min(100, quest['progress'] + progress_increase)
                        st.session_state.user_profile['points'] += progress_increase
                        st.success(f"Quest progress: +{progress_increase}% (+{progress_increase} XP)")
                        st.rerun()
        
        # Mini Games
        st.markdown("### 🎮 Mini Games")
        
        game_cols = st.columns(3)
        for i, game in enumerate(current_mode['mini_games']):
            with game_cols[i % 3]:
                st.markdown(f"""
                <div class="mini-game-card">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                    <h4 style="color: #1F2937; margin: 0.5rem 0;">{game}</h4>
                    <button style="background: {current_mode['color']}; color: white; border: none; 
                                   padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">
                        Play Now
                    </button>
                </div>
                """, unsafe_allow_html=True)
        
        # Achievements for this mode
        st.markdown("### 🏆 Mode Achievements")
        
        ach_cols = st.columns(3)
        for i, achievement in enumerate(current_mode['achievements']):
            with ach_cols[i % 3]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #F59E0B20 0%, rgba(255,255,255,0.9) 100%); 
                            border: 2px solid #F59E0B; border-radius: 15px; padding: 1rem; text-align: center;">
                    <div style="font-size: 2rem;">🏆</div>
                    <div style="color: #F59E0B; font-weight: 700;">{achievement}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Stablecoin Wallet Integration
        st.markdown("### 💰 Stablecoin Wallet")
        
        wallet_cols = st.columns(4)
        wallet_features = [
            {"name": "Balance", "value": f"${st.session_state.user_profile['wallet_balance']:.2f}", "icon": "💰"},
            {"name": "Monthly Savings", "value": "$1,250", "icon": "📈"},
            {"name": "Investment Returns", "value": "+5.2%", "icon": "🎯"},
            {"name": "Streak Bonus", "value": f"{st.session_state.user_profile['current_streak']} days", "icon": "🔥"}
        ]
        
        for i, feature in enumerate(wallet_features):
            with wallet_cols[i]:
                st.markdown(f"""
                <div class="wallet-feature">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{feature['icon']}</div>
                    <div style="color: #6B7280; font-size: 0.9rem;">{feature['name']}</div>
                    <div style="color: #10B981; font-weight: 700; font-size: 1.2rem;">{feature['value']}</div>
                </div>
                """, unsafe_allow_html=True)

elif selected_menu == "📊 Intelligence Center":
    st.markdown('<h1 class="hero-header">📊 Intelligence Center</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">🔮 Advanced Market Analytics & Insights 🔮</p>', unsafe_allow_html=True)
    
    # Interactive Controls
    col1, col2, col3 = st.columns(3)
    with col1:
        date_range = st.date_input("📅 Time Range Scanner", 
                                 value=[df['Date'].min().date(), df['Date'].max().date()],
                                 min_value=df['Date'].min().date(),
                                 max_value=df['Date'].max().date())
    
    with col2:
        metrics_selection = st.multiselect("📊 Data Streams", 
                               ['Mortgage_Rate', 'Unemployment_Rate', 'Home_Price_Index', 'Affordability_Index'],
                               default=['Mortgage_Rate', 'Home_Price_Index'])
    
    with col3:
        viz_type = st.selectbox("📈 Visualization Mode", ['Line Analysis', 'Area Chart', 'Scatter Plot'])
    
    # Filter data based on date range
    if len(date_range) == 2:
        mask = (df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])
        filtered_df = df.loc[mask]
    else:
        filtered_df = df
    
    # Create dynamic visualization
    fig = go.Figure()
    colors = ['#3B82F6', '#8B5CF6', '#EF4444', '#10B981']
    
    for i, metric in enumerate(metrics_selection):
        if viz_type == 'Line Analysis':
            fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[metric], 
                                   mode='lines', name=metric.replace('_', ' '),
                                   line=dict(color=colors[i % len(colors)], width=4)))
        elif viz_type == 'Area Chart':
            fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[metric], 
                                   fill='tonexty', name=metric.replace('_', ' '),
                                   line=dict(color=colors[i % len(colors)]),
                                   fillcolor=f'{colors[i % len(colors)]}30'))
        else:
            fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[metric], 
                                   mode='markers', name=metric.replace('_', ' '),
                                   marker=dict(color=colors[i % len(colors)], size=8)))
    
    fig.update_layout(
        title="🌌 Advanced Market Intelligence Dashboard",
        height=600,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Market Insights
    st.markdown("### 🧠 AI Market Insights")
    
    insight_cols = st.columns(2)
    
    with insight_cols[0]:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3B82F620 0%, rgba(255,255,255,0.9) 100%); 
                    border: 2px solid #3B82F6; border-radius: 15px; padding: 1.5rem;">
            <h4 style="color: #3B82F6; margin: 0;">📈 Trend Analysis</h4>
            <p style="color: #1F2937;">Current market conditions show moderate stability with emerging opportunities in the next quarter.</p>
            <ul style="color: #1F2937;">
                <li>Mortgage rates stabilizing around current levels</li>
                <li>Unemployment showing gradual improvement</li>
                <li>Housing affordability maintaining steady trajectory</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with insight_cols[1]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #10B98120 0%, rgba(255,255,255,0.9) 100%); 
                    border: 2px solid #10B981; border-radius: 15px; padding: 1.5rem;">
            <h4 style="color: #10B981; margin: 0;">🎯 Strategic Recommendations</h4>
            <p style="color: #1F2937;">Based on current data analysis and market conditions:</p>
            <ul style="color: #1F2937;">
                <li><strong>First-Time Buyers:</strong> Favorable entry conditions</li>
                <li><strong>Investors:</strong> Monitor for rate opportunities</li>
                <li><strong>Upgraders:</strong> Consider market timing strategies</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif selected_menu == "🧠 Strategy Simulator":
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
    
    # Calculate battle outcomes
    market_stress = (interest_rate * 0.3 + unemployment * 0.4 + inflation * 0.2 + abs(gdp_growth) * 0.1)
    affordability_score = max(0, 100 - market_stress * 8 - (construction_cost - 100) * 0.5)
    investment_score = max(0, gdp_growth * 10 + (demand_index - 100) * 0.3 - market_stress * 5)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if market_stress < 6:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #10B98120 0%, rgba(255,255,255,0.9) 100%); 
                        border: 2px solid #10B981; border-radius: 15px; padding: 1.5rem; text-align: center;">
                <div style="font-size: 3rem;">✅</div>
                <h3 style="color: #10B981; margin: 0;">VICTORY CONDITIONS</h3>
                <h2 style="color: #1F2937; font-family: 'Orbitron', monospace;">Battle Score: {market_stress:.1f}/10</h2>
                <p style="color: #1F2937; font-weight: 600;">Optimal conditions detected!</p>
            </div>
            """, unsafe_allow_html=True)
        elif market_stress < 8:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #F59E0B20 0%, rgba(255,255,255,0.9) 100%); 
                        border: 2px solid #F59E0B; border-radius: 15px; padding: 1.5rem; text-align: center;">
                <div style="font-size: 3rem;">⚠️</div>
                <h3 style="color: #F59E0B; margin: 0;">CAUTION MODE</h3>
                <h2 style="color: #1F2937; font-family: 'Orbitron', monospace;">Battle Score: {market_stress:.1f}/10</h2>
                <p style="color: #1F2937; font-weight: 600;">Moderate resistance detected.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #EF444420 0%, rgba(255,255,255,0.9) 100%); 
                        border: 2px solid #EF4444; border-radius: 15px; padding: 1.5rem; text-align: center;">
                <div style="font-size: 3rem;">🚨</div>
                <h3 style="color: #EF4444; margin: 0;">DANGER ZONE</h3>
                <h2 style="color: #1F2937; font-family: 'Orbitron', monospace;">Battle Score: {market_stress:.1f}/10</h2>
                <p style="color: #1F2937; font-weight: 600;">High resistance encountered!</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card-3d">
            <div style="font-size: 3rem; color: #8B5CF6;">💎</div>
            <div class="metric-label-3d">Affordability Power</div>
            <div class="metric-value-3d">{affordability_score:.0f}/100</div>
            <div class="progress-bar-quest">
                <div class="progress-fill-quest" style="width:{affordability_score}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card-3d">
            <div style="font-size: 3rem; color: #3B82F6;">📈</div>
            <div class="metric-label-3d">Investment Force</div>
            <div class="metric-value-3d">{investment_score:.0f}/100</div>
            <div class="progress-bar-quest">
                <div class="progress-fill-quest" style="width:{max(0, min(100, investment_score))}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Battle Simulation
    if st.button("🔮 Execute Battle Simulation", type="primary"):
        st.session_state.scenarios_run += 1
        
        # Loading animation
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
                st.info("✅ Execute immediate advance operations")
            elif market_stress < 8:
                st.warning("🟡 Mixed battlefield signals - maintain vigilance")
                st.info("⚠️ Build defensive reserves and monitor for openings")
            else:
                st.error("🔴 Hostile territory ahead - high resistance expected")
                st.info("❌ Execute tactical withdrawal and strengthen position")
        
        with col2:
            st.markdown("**🎯 Tactical Recommendations:**")
            if affordability_score > 70:
                st.write("✅ Deploy fixed-rate mortgage strategies")
                st.write("✅ Consider aggressive expansion")
                st.write("✅ Optimal timing for major moves")
            elif affordability_score > 40:
                st.write("⚠️ Implement cautious advance strategy")
                st.write("⚠️ Focus on defensive positioning")
                st.write("⚠️ Wait for strategic opportunities")
            else:
                st.write("❌ Defensive posture recommended")
                st.write("❌ Focus on strengthening fundamentals")
                st.write("❌ Delay major operations")
        
        # Award XP for running simulation
        st.session_state.user_profile['points'] += 25
        st.success("🎯 Simulation Complete! +25 XP earned")

elif selected_menu == "💎 Decision Matrix":
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
        home_price_range = st.slider("🏠 Target Cost ($)", 100000, 800000, (250000, 400000), 10000)
        down_payment = st.slider("💵 Strike Force (%)", 3, 30, 20, 1)
        time_horizon = st.selectbox("⏰ Timeline", 
                                  ["🚀 Immediate (0-3 months)", "⚡ Rapid (3-12 months)", 
                                   "🎯 Strategic (1-2 years)", "🌌 Long-term (2+ years)"])
        risk_tolerance = st.selectbox("📊 Strategy", ["🛡️ Defensive", "⚖️ Balanced", "⚔️ Aggressive"])
    
    with col3:
        st.markdown("#### 🌍 Theater Operations")
        location_type = st.selectbox("📍 Battle Zone", 
                                   ["🌆 Urban Center", "🏘️ Suburban Base", "🌾 Rural Outpost", "🏖️ Coastal Fortress"])
        family_size = st.selectbox("👨‍👩‍👧‍👦 Squad Size", ["🧑 Solo", "👫 Duo", "👨‍👩‍👧‍👦 Small Squad", "👨‍👩‍👧‍👦‍👧‍👦 Large Unit"])
        job_stability = st.selectbox("💼 Security", ["🔒 Maximum", "✅ High", "⚠️ Moderate", "🚨 High Risk"])
        first_time_buyer = st.checkbox("🏠 First Mission Commander")
    
    if st.button("🧠 Generate AI Strategic Analysis", type="primary"):
        with st.spinner("🤖 AI analyzing commander profile..."):
            time.sleep(2)
        
        # Calculate strategic scores
        financial_readiness = min(100, (savings / (home_price_range[0] * down_payment / 100)) * 50 + 
                                (credit_score - 300) / 5.5 * 50)
        
        latest_data = df.iloc[-1]
        market_timing = max(0, 100 - latest_data['Mortgage_Rate'] * 10 - latest_data['Unemployment_Rate'] * 5)
        
        overall_score = (financial_readiness * 0.6 + market_timing * 0.4)
        
        # Display results
        st.markdown("---")
        st.markdown("### 🎯 Strategic Analysis Report")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card-3d">
                <div style="font-size: 3rem; color: #10B981;">💰</div>
                <div class="metric-label-3d">Financial Readiness</div>
                <div class="metric-value-3d">{financial_readiness:.0f}/100</div>
                <div class="progress-bar-quest">
                    <div class="progress-fill-quest" style="width:{financial_readiness}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card-3d">
                <div style="font-size: 3rem; color: #3B82F6;">⏰</div>
                <div class="metric-label-3d">Market Timing</div>
                <div class="metric-value-3d">{market_timing:.0f}/100</div>
                <div class="progress-bar-quest">
                    <div class="progress-fill-quest" style="width:{market_timing}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card-3d">
                <div style="font-size: 3rem; color: #8B5CF6;">🎯</div>
                <div class="metric-label-3d">Overall Score</div>
                <div class="metric-value-3d">{overall_score:.0f}/100</div>
                <div class="progress-bar-quest">
                    <div class="progress-fill-quest" style="width:{overall_score}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Strategic recommendations
        if overall_score >= 75:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #10B98120 0%, rgba(255,255,255,0.9) 100%); 
                        border: 2px solid #10B981; border-radius: 15px; padding: 2rem; text-align: center;">
                <div style="font-size: 4rem;">🚀</div>
                <h2 style="color: #10B981; margin: 0;">EXECUTE OPERATION</h2>
                <p style="color: #1F2937; font-weight: 600;"><strong>AI Recommendation:</strong> All systems optimal for immediate launch!</p>
                <p style="color: #1F2937;">Your readiness and market conditions are perfectly aligned for success.</p>
            </div>
            """, unsafe_allow_html=True)
        elif overall_score >= 50:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #F59E0B20 0%, rgba(255,255,255,0.9) 100%); 
                        border: 2px solid #F59E0B; border-radius: 15px; padding: 2rem; text-align: center;">
                <div style="font-size: 4rem;">⚖️</div>
                <h2 style="color: #F59E0B; margin: 0;">TACTICAL ADVANCE</h2>
                <p style="color: #1F2937; font-weight: 600;"><strong>AI Recommendation:</strong> Mission possible with strategic enhancements.</p>
                <p style="color: #1F2937;">Execute with careful planning and targeted improvements.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #EF444420 0%, rgba(255,255,255,0.9) 100%); 
                        border: 2px solid #EF4444; border-radius: 15px; padding: 2rem; text-align: center;">
                <div style="font-size: 4rem;">🛡️</div>
                <h2 style="color: #EF4444; margin: 0;">STRATEGIC RETREAT</h2>
                <p style="color: #1F2937; font-weight: 600;"><strong>AI Recommendation:</strong> Focus on strengthening your position.</p>
                <p style="color: #1F2937;">Use this time to optimize fundamentals for future victory.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Award XP for analysis
        st.session_state.user_profile['points'] += 50
        st.success("🎯 Strategic Analysis Complete! +50 XP earned")

elif selected_menu == "📈 Asset Portfolio":
    st.markdown('<h1 class="hero-header">📈 Asset Portfolio Command</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">🏰 Real Estate Empire Management System 🏰</p>', unsafe_allow_html=True)
    
    # Asset Management Console
    st.markdown("### 🏠 Asset Registry")
    
    with st.expander("➕ Register New Asset", expanded=len(st.session_state.properties) == 0):
        col1, col2, col3 = st.columns(3)
        with col1:
            prop_address = st.text_input("🏠 Asset Location")
            purchase_price = st.number_input("💰 Acquisition Cost ($)", 0, 2000000, 300000)
        with col2:
            purchase_date = st.date_input("📅 Acquisition Date")
            current_value = st.number_input("📈 Current Value ($)", 0, 2000000, 350000)
        with col3:
            property_type = st.selectbox("🏘️ Asset Type", 
                                       ["🏠 Single Family", "🏢 Condo", "🏘️ Townhouse", "🏭 Multi-Unit", "🏢 Commercial"])
            monthly_payment = st.number_input("💳 Monthly Cost ($)", 0, 10000, 1800)
        
        if st.button("➕ Deploy Asset") and prop_address:
            new_property = {
                'address': prop_address,
                'purchase_price': purchase_price,
                'current_value': current_value,
                'purchase_date': purchase_date,
                'property_type': property_type,
                'monthly_payment': monthly_payment,
                'id': len(st.session_state.properties)
            }
            st.session_state.properties.append(new_property)
            st.session_state.user_profile['points'] += 100
            if len(st.session_state.properties) == 1:
                award_achievement("portfolio_starter")
            st.success("🎉 Asset successfully deployed! +100 XP earned")
            st.rerun()
    
    # Portfolio Overview
    if st.session_state.properties:
        st.markdown("### 📊 Empire Overview")
        
        total_purchase = sum(p['purchase_price'] for p in st.session_state.properties)
        total_current = sum(p['current_value'] for p in st.session_state.properties)
        total_equity = total_current - total_purchase
        roi_percentage = ((total_equity / total_purchase) * 100) if total_purchase > 0 else 0
        monthly_costs = sum(p['monthly_payment'] for p in st.session_state.properties)
        
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            st.markdown(f"""
            <div class="metric-card-3d">
                <div style="font-size: 3rem; color: #3B82F6;">🏰</div>
                <div class="metric-label-3d">Total Assets</div>
                <div class="metric-value-3d">{len(st.session_state.properties)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_col2:
            st.markdown(f"""
            <div class="metric-card-3d">
                <div style="font-size: 3rem; color: #8B5CF6;">💰</div>
                <div class="metric-label-3d">Total Investment</div>
                <div class="metric-value-3d">${total_purchase:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_col3:
            st.markdown(f"""
            <div class="metric-card-3d">
                <div style="font-size: 3rem; color: #10B981;">📈</div>
                <div class="metric-label-3d">Current Value</div>
                <div class="metric-value-3d">${total_current:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_col4:
            color = "#10B981" if total_equity >= 0 else "#EF4444"
            st.markdown(f"""
            <div class="metric-card-3d">
                <div style="font-size: 3rem; color: {color};">💎</div>
                <div class="metric-label-3d">Total Equity</div>
                <div class="metric-value-3d">${total_equity:,.0f}</div>
                <div style="color: {color}; font-weight: 600;">{roi_percentage:+.1f}% ROI</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Property List
        st.markdown("### 🏠 Property Portfolio")
        
        for i, prop in enumerate(st.session_state.properties):
            with st.expander(f"{prop['property_type']} - {prop['address']}", expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Purchase Price", f"${prop['purchase_price']:,}")
                    st.metric("Purchase Date", prop['purchase_date'].strftime("%Y-%m-%d"))
                
                with col2:
                    st.metric("Current Value", f"${prop['current_value']:,}")
                    equity = prop['current_value'] - prop['purchase_price']
                    st.metric("Equity", f"${equity:,}")
                
                with col3:
                    roi = ((equity / prop['purchase_price']) * 100) if prop['purchase_price'] > 0 else 0
                    st.metric("ROI", f"{roi:.1f}%")
                    st.metric("Monthly Cost", f"${prop['monthly_payment']:,}")
                
                with col4:
                    days_owned = (datetime.now().date() - prop['purchase_date']).days
                    st.metric("Days Owned", f"{days_owned}")
                    
                    if st.button(f"🗑️ Remove Property", key=f"remove_{i}"):
                        st.session_state.properties.pop(i)
                        st.rerun()
        
        # Portfolio Performance Chart
        st.markdown("### 📊 Portfolio Performance")
        
        if len(st.session_state.properties) > 0:
            # Create portfolio composition pie chart
            property_types = {}
            property_values = {}
            
            for prop in st.session_state.properties:
                prop_type = prop['property_type']
                if prop_type in property_types:
                    property_types[prop_type] += 1
                    property_values[prop_type] += prop['current_value']
                else:
                    property_types[prop_type] = 1
                    property_values[prop_type] = prop['current_value']
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_pie = go.Figure(data=[go.Pie(
                    labels=list(property_types.keys()),
                    values=list(property_types.values()),
                    title="Portfolio Composition by Count"
                )])
                fig_pie.update_layout(height=400)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                fig_value = go.Figure(data=[go.Pie(
                    labels=list(property_values.keys()),
                    values=list(property_values.values()),
                    title="Portfolio Composition by Value"
                )])
                fig_value.update_layout(height=400)
                st.plotly_chart(fig_value, use_container_width=True)
    
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3B82F620 0%, rgba(255,255,255,0.9) 100%); 
                    border: 2px solid #3B82F6; border-radius: 15px; padding: 3rem; text-align: center;">
            <div style="font-size: 4rem;">🏠</div>
            <h3 style="color: #3B82F6;">Start Your Real Estate Empire</h3>
            <p style="color: #1F2937; font-size: 1.1rem;">Add your first property to begin tracking your portfolio performance and unlock achievement rewards!</p>
        </div>
        """, unsafe_allow_html=True)

elif selected_menu == "ℹ️ Command Brief":
    st.markdown('<h1 class="hero-header">ℹ️ Command Brief</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,249,250,0.8) 100%); 
                    border: 3px solid #3B82F6; border-radius: 20px; padding: 2rem;">
            <div style="font-size: 3rem; text-align: center; margin-bottom: 1rem;">🏠</div>
            <h2 style="color: #8B5CF6; margin: 0; text-align: center;">Mission Statement</h2>
            <p style="color: #1F2937; font-weight: 600; text-align: center;"><strong>Mortgage Quest Elite</strong> is the most advanced multi-modal fintech gaming platform, combining cutting-edge AI with immersive gaming experiences.</p>
            
            <h3 style="color: #3B82F6;">🚀 Core Gaming Systems:</h3>
            <ul style="color: #1F2937; font-weight: 500;">
                <li><strong>🎮 Life Stage Modes:</strong> 5 distinct gaming experiences for different life stages</li>
                <li><strong>⚔️ Quest System:</strong> Personalized challenges with XP rewards</li>
                <li><strong>🏆 Achievement Engine:</strong> Unlock badges and level progression</li>
                <li><strong>💰 Stablecoin Wallet:</strong> Real financial rewards and DeFi integration</li>
                <li><strong>🧠 AI Intelligence:</strong> Market analysis and strategic recommendations</li>
                <li><strong>📊 Portfolio Tracking:</strong> Real estate empire management</li>
            </ul>
            
            <h3 style="color: #10B981;">🎯 Life Stage Modes:</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
                <div style="background: #ECFDF5; padding: 1rem; border-radius: 10px; border: 2px solid #10B981;">
                    <strong>🎯 First Timer (22-28):</strong> Credit building, savings strategies, market education
                </div>
                <div style="background: #EFF6FF; padding: 1rem; border-radius: 10px; border: 2px solid #3B82F6;">
                    <strong>👨‍👩‍👧‍👦 Family Builder (28-35):</strong> School districts, family planning, joint goals
                </div>
                <div style="background: #FFFBEB; padding: 1rem; border-radius: 10px; border: 2px solid #F59E0B;">
                    <strong>🏠 Trade-Up Pro (35-45):</strong> Equity optimization, market timing, advanced strategies
                </div>
                <div style="background: #F5F3FF; padding: 1rem; border-radius: 10px; border: 2px solid #8B5CF6;">
                    <strong>🏖️ Smart Downsizer (55+):</strong> Retirement planning, geographic arbitrage
                </div>
            </div>
            <div style="text-align: center;">
                <div style="background: #FEF2F2; padding: 1rem; border-radius: 10px; border: 2px solid #EF4444; display: inline-block;">
                    <strong>🏛️ Property Investor (Any Age):</strong> BRRRR method, cash flow, portfolio building
                </div>
            </div>
            
            <h3 style="color: #EF4444;">🎓 Elite Development:</h3>
            <p style="color: #1F2937;">Created by <strong>BEFMNS Team</strong> for <strong>NYU Stern Fintech Program</strong> - bridging traditional banking with modern fintech innovation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,249,250,0.8) 100%); 
                    border: 3px solid #8B5CF6; border-radius: 20px; padding: 2rem;">
            <div style="font-size: 3rem; text-align: center;">🔧</div>
            <h3 style="color: #8B5CF6; text-align: center;">Tech Stack</h3>
            <div style="color: #1F2937; font-size: 0.9rem;">
                <p><strong>Frontend:</strong> Advanced Streamlit</p>
                <p><strong>Visualization:</strong> Plotly Interactive</p>
                <p><strong>Data Processing:</strong> Pandas & NumPy</p>
                <p><strong>AI Engine:</strong> Predictive Modeling</p>
                <p><strong>Design:</strong> Futuristic Gaming UI</p>
            </div>
            
            <div style="font-size: 3rem; text-align: center; margin: 1rem 0;">🎮</div>
            <h3 style="color: #8B5CF6; text-align: center;">Gaming Features</h3>
            <div style="color: #1F2937; font-size: 0.9rem;">
                <p>• Multi-Modal Life Stage System</p>
                <p>• Dynamic Quest Generation</p>
                <p>• Achievement & Badge System</p>
                <p>• Level Progression Mechanics</p>
                <p>• Stablecoin Wallet Integration</p>
                <p>• Real-time Market Data</p>
                <p>• AI-Powered Recommendations</p>
                <p>• Social Competition Elements</p>
            </div>
            
            <div style="font-size: 3rem; text-align: center; margin: 1rem 0;">🌟</div>
            <h3 style="color: #8B5CF6; text-align: center;">Innovation</h3>
            <div style="color: #1F2937; font-size: 0.9rem;">
                <p>• <strong>5-in-1 Platform:</strong> Multiple fintech products in one gaming experience</p>
                <p>• <strong>Life Stage Evolution:</strong> Seamless progression through financial journey</p>
                <p>• <strong>Real Economic Data:</strong> 10+ years of market intelligence</p>
                <p>• <strong>Gamified Learning:</strong> Mario-style progression with financial education</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # User Stats Summary
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #10B98120 0%, rgba(255,255,255,0.9) 100%); 
                    border: 2px solid #10B981; border-radius: 15px; padding: 1.5rem; margin-top: 1rem;">
            <h4 style="color: #10B981; text-align: center; margin: 0;">Your Commander Stats</h4>
            <div style="text-align: center; color: #1F2937; margin-top: 1rem;">
                <div><strong>Level:</strong> {st.session_state.user_profile['level']}</div>
                <div><strong>XP:</strong> {st.session_state.user_profile['points']:,}</div>
                <div><strong>Achievements:</strong> {len(st.session_state.user_profile['achievements'])}/{len(ACHIEVEMENTS)}</div>
                <div><strong>Properties:</strong> {len(st.session_state.properties)}</div>
                <div><strong>Wallet:</strong> ${st.session_state.user_profile['wallet_balance']:.2f}</div>
                <div><strong>Streak:</strong> {st.session_state.user_profile['current_streak']} days</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3B82F620 0%, #8B5CF620 50%, #10B98120 100%); 
                border: 3px solid #3B82F6; border-radius: 20px; padding: 2rem; text-align: center;">
        <div style="font-size: 4rem;">🚀</div>
        <h3 style="color: #8B5CF6;">Ready to Master Real Estate Gaming?</h3>
        <p style="color: #1F2937; font-weight: 600; font-size: 1.1rem;">Join the next generation of strategic real estate commanders with Mortgage Quest Elite</p>
        <div style="margin: 1rem 0;">
            <span style="background: #3B82F6; color: white; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.25rem; display: inline-block;">Multi-Modal Gaming</span>
            <span style="background: #8B5CF6; color: white; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.25rem; display: inline-block;">AI-Powered Intelligence</span>
            <span style="background: #10B981; color: white; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.25rem; display: inline-block;">Real Financial Rewards</span>
            <span style="background: #F59E0B; color: white; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.25rem; display: inline-block;">Life Stage Evolution</span>
        </div>
        <p style="color: #1F2937; margin-top: 2rem;"><strong>© 2024 BEFMNS Team | NYU Stern Fintech Program</strong></p>
        <p style="color: #6B7280; font-size: 0.9rem;">Bridging Traditional Banking with Modern Fintech Innovation</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(59,130,246,0.1) 0%, rgba(139,92,246,0.1) 100%); 
            border-radius: 15px; border: 2px solid rgba(59,130,246,0.3);">
    <p style="color: #6B7280; font-size: 0.9rem; margin: 0;">
        🚀 Powered by Real Economic Data • 🎮 Gamified Financial Learning • 💰 Stablecoin Integration • 🤝 Social Gaming Features
    </p>
    <p style="color: #8B5CF6; font-size: 0.8rem; margin: 0.5rem 0;">
        Next-Generation Fintech Gaming Platform for Strategic Real Estate Decision Making
    </p>
</div>
""", unsafe_allow_html=True)