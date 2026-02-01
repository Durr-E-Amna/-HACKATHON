# -*- coding: utf-8 -*-
"""
🏆 AWARD-WINNING STREAMLIT DASHBOARD 🏆
Pakistan Air Quality Forecasting System
Professional Dashboard with Enhanced UI/UX
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import joblib
import datetime
from datetime import timedelta
import warnings
warnings.filterwarnings('ignore')

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="🌫️ Pakistan Air Quality AI",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/air-quality',
        'Report a bug': "https://github.com/yourusername/air-quality/issues",
        'About': "# Pakistan Air Quality Forecasting\nPowered by Machine Learning"
    }
)

# ==================== PREMIUM CSS STYLES ====================
st.markdown("""
<style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');
    
    /* ====== ROOT VARIABLES ====== */
    :root {
        --primary-dark: #0F172A;
        --primary-blue: #3B82F6;
        --primary-purple: #8B5CF6;
        --success-green: #10B981;
        --warning-orange: #F59E0B;
        --danger-red: #EF4444;
        --text-dark: #1E293B;
        --text-medium: #475569;
        --text-light: #94A3B8;
        --bg-light: #F8FAFC;
        --bg-white: #FFFFFF;
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
        --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.16);
        --shadow-xl: 0 12px 48px rgba(0, 0, 0, 0.20);
    }
    
    /* ====== GLOBAL RESET ====== */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        line-height: 1.6;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* ====== MAIN CONTAINER ====== */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
        padding: 0;
    }
    
    .block-container {
        padding: 2rem 2rem 3rem 2rem;
        max-width: 1400px;
    }
    
    /* ====== TYPOGRAPHY - ENHANCED VISIBILITY ====== */
    h1, .hero-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 900;
        font-size: 3.75rem;
        line-height: 1.1;
        letter-spacing: -0.03em;
        color: #FFFFFF;
        margin: 0;
        text-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    
    h2, .section-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 2.25rem;
        line-height: 1.2;
        letter-spacing: -0.02em;
        color: #0F172A;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 4px solid transparent;
        border-image: linear-gradient(90deg, #3B82F6, #8B5CF6, #EC4899) 1;
        position: relative;
        padding-left: 1.5rem;
    }
    
    h3 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.75rem;
        line-height: 1.3;
        color: #1E293B;
        letter-spacing: -0.01em;
    }
    
    h4 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.5rem;
        line-height: 1.4;
        color: #334155;
        letter-spacing: -0.005em;
    }
    
    p, li, span:not(.metric-value):not(.hero-title):not(.hero-subtitle) {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 1.0625rem;
        line-height: 1.75;
        color: #334155;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 1.5rem;
        line-height: 1.6;
        color: #FFFFFF;
        margin-top: 1rem;
        letter-spacing: 0.01em;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* ====== HERO HEADER - ENHANCED ====== */
    .hero-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #8B5CF6 100%);
        padding: 4rem 3rem;
        border-radius: 32px;
        margin-bottom: 3rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 24px 72px rgba(0, 0, 0, 0.35);
        border: 4px solid rgba(255, 255, 255, 0.25);
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.25);
        padding: 1rem 2.5rem;
        border-radius: 50px;
        margin-top: 1.5rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.25rem;
        letter-spacing: 0.05em;
        color: #FFFFFF;
        backdrop-filter: blur(12px);
        border: 3px solid rgba(255, 255, 255, 0.4);
        position: relative;
        z-index: 2;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
    }
    
    /* ====== GLASSMORPHISM CARDS - ENHANCED ====== */
    .glass-card {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(24px);
        border-radius: 28px;
        padding: 2.5rem;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
        border: 2px solid rgba(255, 255, 255, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 2rem;
    }
    
    .glass-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.18);
    }
    
    /* ====== PREMIUM METRICS - ENHANCED VISIBILITY ====== */
    .premium-metric {
        background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.10);
        border: 3px solid #E2E8F0;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }
    
    .premium-metric::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 8px;
        background: linear-gradient(90deg, #3B82F6, #8B5CF6, #EC4899, #F59E0B, #3B82F6);
        background-size: 300% 100%;
        animation: gradient-flow 4s linear infinite;
    }
    
    @keyframes gradient-flow {
        0% { background-position: 0% 0%; }
        100% { background-position: 300% 0%; }
    }
    
    .premium-metric:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 18px 48px rgba(0, 0, 0, 0.16);
        border-color: #3B82F6;
    }
    
    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-weight: 900;
        font-size: 3rem;
        line-height: 1;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #1E3A8A, #3B82F6, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 1rem 0;
        display: block;
    }
    
    .metric-label {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 0.9375rem;
        line-height: 1.4;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }
    
    .metric-icon {
        font-size: 3.5rem;
        margin-bottom: 0.75rem;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
    }
    
    /* ====== CITY STATUS CARDS - ENHANCED ====== */
    .city-status-card {
        background: white;
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border-left: 8px solid;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.10);
    }
    
    .city-status-card:hover {
        transform: translateX(12px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .city-status-card.good { 
        border-left-color: #10B981; 
        background: linear-gradient(135deg, #FFFFFF 0%, #ECFDF5 100%); 
    }
    .city-status-card.moderate { 
        border-left-color: #F59E0B; 
        background: linear-gradient(135deg, #FFFFFF 0%, #FFFBEB 100%); 
    }
    .city-status-card.unhealthy { 
        border-left-color: #F97316; 
        background: linear-gradient(135deg, #FFFFFF 0%, #FFF7ED 100%); 
    }
    .city-status-card.very-unhealthy { 
        border-left-color: #EF4444; 
        background: linear-gradient(135deg, #FFFFFF 0%, #FEF2F2 100%); 
    }
    
    .city-status-card h3 {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 1.75rem;
        line-height: 1.3;
        margin: 0;
    }
    
    /* ====== SIDEBAR - DRAMATICALLY IMPROVED ====== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        padding: 2.5rem 1.5rem;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        font-family: 'Poppins', sans-serif;
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    
    [data-testid="stSidebar"] label {
        font-family: 'Inter', sans-serif;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.0625rem !important;
        letter-spacing: 0.03em;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stCheckbox label {
        color: #FFFFFF !important;
        font-size: 1.0625rem !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar Select Box */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 14px !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        backdrop-filter: blur(12px);
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div:hover {
        background: rgba(255, 255, 255, 0.22) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Sidebar Slider */
    [data-testid="stSidebar"] .stSlider > div > div > div {
        color: #FFFFFF !important;
    }
    
    [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {
        background: rgba(255, 255, 255, 0.15);
        padding: 1.5rem;
        border-radius: 14px;
        backdrop-filter: blur(12px);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Sidebar Checkbox */
    [data-testid="stSidebar"] .stCheckbox {
        background: rgba(255, 255, 255, 0.12);
        padding: 1.25rem;
        border-radius: 14px;
        margin-bottom: 1rem;
        border: 2px solid rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(12px);
    }
    
    [data-testid="stSidebar"] .stCheckbox:hover {
        background: rgba(255, 255, 255, 0.18);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    [data-testid="stSidebar"] .stCheckbox label {
        font-size: 1.0625rem !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar Divider */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
        margin: 2rem 0 !important;
    }
    
    /* ====== ALERT BOXES - ENHANCED ====== */
    .alert-danger {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border-left: 8px solid #EF4444;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 12px 32px rgba(239, 68, 68, 0.25);
        animation: pulse-alert 2.5s infinite;
    }
    
    @keyframes pulse-alert {
        0%, 100% { box-shadow: 0 12px 32px rgba(239, 68, 68, 0.25); }
        50% { box-shadow: 0 16px 40px rgba(239, 68, 68, 0.40); }
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border-left: 8px solid #F59E0B;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 12px 32px rgba(245, 158, 11, 0.25);
    }
    
    .alert-info {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-left: 8px solid #3B82F6;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.25);
    }
    
    .alert-danger h3,
    .alert-warning h3,
    .alert-info h3 {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 1.5rem;
        line-height: 1.4;
        margin: 0 0 12px 0;
    }
    
    .alert-danger p,
    .alert-warning p,
    .alert-info p {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.125rem;
        line-height: 1.7;
        margin: 0;
    }
    
    /* ====== SECTION HEADERS - ENHANCED ====== */
    .section-title::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 6px;
        background: linear-gradient(180deg, #3B82F6, #8B5CF6);
        border-radius: 4px;
    }
    
    /* ====== BUTTONS - ENHANCED ====== */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 14px;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.0625rem;
        letter-spacing: 0.03em;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.5);
    }
    
    /* ====== TABS - ENHANCED ====== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.6);
        padding: 10px;
        border-radius: 18px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.0625rem;
        letter-spacing: 0.02em;
        background: transparent;
        border-radius: 14px;
        padding: 14px 28px;
        border: none;
        color: #475569;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        color: white !important;
        box-shadow: 0 6px 18px rgba(59, 130, 246, 0.4);
    }
    
    /* ====== EXPANDERS - ENHANCED ====== */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #F8FAFC, #E2E8F0);
        border-radius: 14px;
        padding: 1.25rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.0625rem;
        letter-spacing: 0.02em;
        border: 2px solid #CBD5E1;
        color: #1E293B;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #E2E8F0, #CBD5E1);
    }
    
    .streamlit-expanderContent {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 1rem;
        line-height: 1.75;
        color: #334155;
    }
    
    /* ====== SIDEBAR EXPANDERS - SPECIAL STYLING ====== */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        backdrop-filter: blur(12px);
    }
    
    [data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.22) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        border-radius: 0 0 14px 14px !important;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .streamlit-expanderContent p,
    [data-testid="stSidebar"] .streamlit-expanderContent div {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderContent strong {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    
    /* ====== INFO/WARNING/ERROR BOXES ====== */
    .stAlert {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        line-height: 1.6;
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
    }
    
    /* ====== CHARTS ====== */
    .js-plotly-plot {
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);
    }
    
    /* ====== SCROLLBAR ====== */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F1F5F9;
        border-radius: 12px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #3B82F6, #8B5CF6);
        border-radius: 12px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #2563EB, #7C3AED);
    }
    
    /* ====== FOOTER ====== */
    .footer {
        background: linear-gradient(135deg, #F8FAFC, #E2E8F0);
        padding: 3rem 2rem;
        border-radius: 24px;
        margin-top: 4rem;
        text-align: center;
        border-top: 5px solid transparent;
        border-image: linear-gradient(90deg, #3B82F6, #8B5CF6, #EC4899) 1;
    }
    
    .footer h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 1.75rem;
        color: #1E3A8A;
        margin: 0;
    }
    
    .footer p {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.0625rem;
        line-height: 1.7;
        color: #475569;
        margin: 12px 0;
    }
    
    .footer .disclaimer {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.9375rem;
        line-height: 1.7;
        color: #64748B;
    }
    
    /* ====== RESPONSIVE DESIGN ====== */
    @media (max-width: 768px) {
        h1, .hero-title { font-size: 2.75rem; }
        h2, .section-title { font-size: 2rem; }
        h3 { font-size: 1.5rem; }
        .hero-subtitle { font-size: 1.25rem; }
        .metric-value { font-size: 2.5rem; }
        .metric-label { font-size: 0.875rem; }
        p, li { font-size: 1rem; }
    }
    
    @media (max-width: 480px) {
        h1, .hero-title { font-size: 2.25rem; }
        h2, .section-title { font-size: 1.75rem; }
        .hero-subtitle { font-size: 1.125rem; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== AQI CONFIGURATION ====================
AQI_CATEGORIES = {
    "Good": {
        "color": "#10B981",
        "gradient": "linear-gradient(135deg, #10B981, #34D399)",
        "description": "Air quality is satisfactory",
        "range": "0-12 µg/m³",
        "icon": "🌤️",
        "health_effects": "Minimal health risk",
        "recommendation": "Perfect for outdoor activities",
        "level": 1
    },
    "Moderate": {
        "color": "#F59E0B",
        "gradient": "linear-gradient(135deg, #F59E0B, #FCD34D)",
        "description": "Air quality is acceptable",
        "range": "12.1-35.4 µg/m³",
        "icon": "⛅",
        "health_effects": "Slight concerns for sensitive individuals",
        "recommendation": "Sensitive people should limit prolonged outdoor exposure",
        "level": 2
    },
    "Unhealthy": {
        "color": "#F97316",
        "gradient": "linear-gradient(135deg, #F97316, #FB923C)",
        "description": "Everyone may begin to experience health effects",
        "range": "35.5-55.4 µg/m³",
        "icon": "😷",
        "health_effects": "Increased risk for sensitive groups",
        "recommendation": "Limit prolonged outdoor exertion",
        "level": 3
    },
    "Very Unhealthy": {
        "color": "#EF4444",
        "gradient": "linear-gradient(135deg, #EF4444, #F87171)",
        "description": "Health alert: serious health effects possible",
        "range": "55.5+ µg/m³",
        "icon": "🚨",
        "health_effects": "Significant health effects",
        "recommendation": "Avoid outdoor activities",
        "level": 4
    }
}

# ==================== HELPER FUNCTIONS ====================

@st.cache_resource
def load_models():
    """Load ML models with progress indicator"""
    try:
        with st.spinner('🤖 Loading AI Models...'):
            best_model = joblib.load('best_model.pkl')
            label_encoder = joblib.load('label_encoder.pkl')
            city_encoder = joblib.load('city_encoder.pkl')
            feature_columns = joblib.load('feature_columns.pkl')
            
            try:
                predictions_df = pd.read_csv('aqi_predictions_3day.csv')
            except:
                predictions_df = None
            
            return best_model, label_encoder, city_encoder, feature_columns, predictions_df
    except Exception as e:
        st.error(f"❌ Error loading models: {str(e)}")
        return None, None, None, None, None

def generate_sample_data():
    """Generate realistic sample data for demo"""
    cities = ['Islamabad', 'Karachi', 'Lahore', 'Peshawar', 'Quetta', 'Multan', 'Faisalabad']
    dates = [datetime.date.today() + timedelta(days=i) for i in range(7)]
    
    sample_data = []
    city_baselines = {
        'Lahore': (180, 250),
        'Karachi': (100, 150),
        'Islamabad': (60, 100),
        'Peshawar': (120, 180),
        'Quetta': (50, 90),
        'Multan': (140, 200),
        'Faisalabad': (130, 190)
    }
    
    for city in cities:
        baseline_min, baseline_max = city_baselines.get(city, (80, 140))
        
        for i, date in enumerate(dates):
            variation = np.random.uniform(-20, 20)
            pm25 = np.clip(np.random.uniform(baseline_min, baseline_max) + variation, 0, 300)
            
            if pm25 <= 12:
                category = "Good"
            elif pm25 <= 35.4:
                category = "Moderate"
            elif pm25 <= 55.4:
                category = "Unhealthy"
            else:
                category = "Very Unhealthy"
            
            confidence = np.random.uniform(88, 98)
            
            sample_data.append({
                'City': city,
                'Date': date.strftime('%Y-%m-%d'),
                'AQI_Category': category,
                'PM2.5_Value': round(pm25, 1),
                'Confidence': f"{confidence:.1f}%",
                'Display_Date': date.strftime('%b %d, %Y')
            })
    
    return pd.DataFrame(sample_data)

def create_gauge_chart(pm25_value, category, city_name):
    """Create animated gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pm25_value,
        title={
            'text': f"<b>{city_name}</b><br><span style='font-size:18px'>PM2.5 Level</span>",
            'font': {'size': 26, 'color': AQI_CATEGORIES[category]['color'], 'family': 'Poppins'}
        },
        delta={
            'reference': 35.4,
            'increasing': {'color': "#EF4444"},
            'decreasing': {'color': "#10B981"}
        },
        number={'suffix': " µg/m³", 'font': {'size': 44, 'color': AQI_CATEGORIES[category]['color'], 'family': 'Outfit'}},
        gauge={
            'axis': {'range': [None, 300], 'tickwidth': 3, 'tickfont': {'size': 14, 'family': 'Inter'}},
            'bar': {'color': AQI_CATEGORIES[category]['color'], 'thickness': 0.85},
            'bgcolor': "white",
            'borderwidth': 4,
            'bordercolor': "rgba(255,255,255,0.6)",
            'steps': [
                {'range': [0, 12], 'color': '#D1FAE5'},
                {'range': [12, 35.4], 'color': '#FEF3C7'},
                {'range': [35.4, 55.4], 'color': '#FED7AA'},
                {'range': [55.4, 300], 'color': '#FECACA'}
            ],
            'threshold': {
                'line': {'color': AQI_CATEGORIES[category]['color'], 'width': 5},
                'thickness': 0.9,
                'value': pm25_value
            }
        }
    ))
    
    fig.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=90, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': "Inter, sans-serif"}
    )
    
    return fig

def create_timeline_chart(forecast_data, city):
    """Create enhanced timeline forecast chart"""
    fig = go.Figure()
    
    forecast_data = forecast_data.sort_values('Date')
    
    fig.add_trace(go.Scatter(
        x=forecast_data['Date'],
        y=forecast_data['PM2.5_Value'],
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.18)',
        line=dict(color='rgba(59, 130, 246, 0)', width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast_data['Date'],
        y=forecast_data['PM2.5_Value'],
        mode='lines+markers',
        name='PM2.5',
        line=dict(color='#1E3A8A', width=5),
        marker=dict(
            size=16,
            color='white',
            line=dict(width=4, color='#1E3A8A')
        ),
        text=[f"<b>{v:.0f}</b>" for v in forecast_data['PM2.5_Value']],
        textposition="top center",
        textfont=dict(size=15, color='#1E3A8A', family='Poppins', weight=700),
        hovertemplate="<b>%{x}</b><br>PM2.5: %{y:.1f} µg/m³<extra></extra>"
    ))
    
    y_max = max(forecast_data['PM2.5_Value'].max() * 1.3, 100)
    
    categories = [
        (0, 12, "Good", "#D1FAE5"),
        (12, 35.4, "Moderate", "#FEF3C7"),
        (35.4, 55.4, "Unhealthy", "#FED7AA"),
        (55.4, y_max, "Very Unhealthy", "#FECACA")
    ]
    
    for lower, upper, cat_name, color in categories:
        fig.add_hrect(
            y0=lower, y1=upper,
            fillcolor=color,
            opacity=0.25,
            layer="below",
            line_width=0
        )
    
    fig.update_layout(
        title=f"<b>{city} - Air Quality Forecast</b>",
        title_font=dict(size=22, color='#1E3A8A', family='Outfit'),
        xaxis_title="<b>Date</b>",
        yaxis_title="<b>PM2.5 (µg/m³)</b>",
        hovermode="x unified",
        height=420,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Inter, sans-serif", size=13),
        xaxis=dict(gridcolor='#E2E8F0', tickangle=-45, tickfont=dict(size=12, family='Inter')),
        yaxis=dict(gridcolor='#E2E8F0', range=[0, y_max], tickfont=dict(size=12, family='Inter'))
    )
    
    return fig

def create_comparison_chart(predictions_data):
    """Create city comparison bar chart"""
    latest_data = []
    for city in predictions_data['City'].unique():
        city_data = predictions_data[predictions_data['City'] == city]
        if len(city_data) > 0:
            latest_data.append(city_data.iloc[0])
    
    latest_df = pd.DataFrame(latest_data)
    
    fig = px.bar(
        latest_df,
        x='City',
        y='PM2.5_Value',
        color='AQI_Category',
        color_discrete_map={cat: info['color'] for cat, info in AQI_CATEGORIES.items()},
        title="<b>Current Air Quality Comparison</b>",
        labels={'PM2.5_Value': 'PM2.5 (µg/m³)', 'AQI_Category': 'Category'},
        text='PM2.5_Value'
    )
    
    fig.update_traces(
        texttemplate='<b>%{y:.0f}</b>',
        textposition='outside',
        marker_line_width=3,
        marker_line_color='white',
        textfont=dict(size=14, family='Poppins', color='#1E293B')
    )
    
    fig.update_layout(
        height=470,
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Inter, sans-serif", size=13),
        title_font=dict(size=22, color='#1E3A8A', family='Outfit'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=13, family='Poppins')
        ),
        xaxis=dict(tickfont=dict(size=13, family='Inter')),
        yaxis=dict(tickfont=dict(size=13, family='Inter'))
    )
    
    return fig

def get_health_recommendations(category):
    """Get detailed health recommendations"""
    recommendations = {
        "Good": [
            "✅ Ideal conditions for outdoor activities",
            "✅ Open windows for natural ventilation",
            "✅ Safe for all age groups",
            "✅ Perfect for outdoor exercise",
            "✅ No special precautions needed"
        ],
        "Moderate": [
            "⚠️ Unusually sensitive people should consider reducing prolonged outdoor exertion",
            "✅ Generally safe for most people",
            "⚠️ Monitor symptoms if you have respiratory conditions",
            "✅ Outdoor activities acceptable with precautions",
            "⚠️ Children and elderly should take breaks during strenuous activity"
        ],
        "Unhealthy": [
            "😷 Everyone should reduce prolonged outdoor exertion",
            "😷 Sensitive groups should avoid outdoor activities",
            "😷 Wear masks (N95) when outdoors",
            "😷 Keep windows closed",
            "😷 Use air purifiers indoors",
            "😷 Limit outdoor exercise to early morning"
        ],
        "Very Unhealthy": [
            "🚨 URGENT: Avoid all outdoor activities",
            "🚨 Stay indoors with windows closed",
            "🚨 Use HEPA air purifiers continuously",
            "🚨 Wear N95 masks if you must go outside",
            "🚨 Sensitive groups should monitor health closely",
            "🚨 Postpone outdoor events",
            "🚨 Keep emergency medications accessible"
        ]
    }
    return recommendations.get(category, [])

def calculate_city_risk_score(city_data):
    """Calculate comprehensive risk score for a city"""
    avg_pm25 = city_data['PM2.5_Value'].mean()
    max_pm25 = city_data['PM2.5_Value'].max()
    aqi_levels = [AQI_CATEGORIES[cat]['level'] for cat in city_data['AQI_Category']]
    avg_aqi_level = np.mean(aqi_levels)
    
    risk_score = (avg_pm25 * 0.4) + (max_pm25 * 0.3) + (avg_aqi_level * 30)
    
    return round(risk_score, 1)

# ==================== FIXED PREDICTION FUNCTION ====================
def predict_custom_input(best_model, city_encoder, label_encoder, feature_columns, input_data):
    """Make prediction based on custom user input - FIXED VERSION"""
    try:
        # Create feature dataframe with correct structure
        features_df = pd.DataFrame([input_data])
        
        # Ensure all required columns exist - fill missing ones with 0
        for col in feature_columns:
            if col not in features_df.columns:
                features_df[col] = 0
        
        # Reorder columns to match training
        features_df = features_df[feature_columns]
        
        # Make prediction
        prediction = best_model.predict(features_df)[0]
        prediction_proba = best_model.predict_proba(features_df)[0]
        
        # Get category name
        category = label_encoder.inverse_transform([prediction])[0]
        confidence = max(prediction_proba) * 100
        
        # Create a more realistic PM2.5 estimate based on the category
        # Use the middle of the range for each category
        pm25_estimates = {
            "Good": (0, 12),
            "Moderate": (12.1, 35.4),
            "Unhealthy": (35.5, 55.4),
            "Very Unhealthy": (55.5, 300)
        }
        
        pm25_range = pm25_estimates.get(category, (0, 100))
        # Add some randomness based on the input values
        if 'PM2.5' in input_data:
            base_pm25 = input_data['PM2.5']
        else:
            base_pm25 = (pm25_range[0] + pm25_range[1]) / 2
        
        # Adjust based on other factors
        factor = 1.0
        if 'Temperature' in input_data and input_data['Temperature'] > 30:
            factor *= 1.2  # Higher temp = higher pollution
        if 'Humidity' in input_data and input_data['Humidity'] > 70:
            factor *= 1.1  # Higher humidity = higher pollution
        if 'Wind_Speed' in input_data and input_data['Wind_Speed'] > 20:
            factor *= 0.8  # Higher wind = dispersion
        
        estimated_pm25 = base_pm25 * factor
        estimated_pm25 = max(pm25_range[0], min(pm25_range[1], estimated_pm25))
        
        return {
            'category': category,
            'confidence': confidence,
            'pm25_value': estimated_pm25,
            'probabilities': dict(zip(label_encoder.classes_, prediction_proba))
        }
    
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")
        return None

# ==================== FIXED PREDICTION FORM ====================
def create_prediction_form(best_model, city_encoder, label_encoder, feature_columns):
    """Create interactive prediction form - FIXED VERSION"""
    st.markdown('<div class="section-title">🎯 Custom Air Quality Prediction</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-left: 6px solid #3B82F6;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        ">
            <h4 style="margin: 0 0 10px 0; color: #1E3A8A; font-weight: 700;">
                📝 Enter Environmental Parameters
            </h4>
            <p style="margin: 0; color: #475569; font-weight: 500;">
                Fill in the form below to get a real-time air quality prediction based on your custom parameters.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for storing predictions
    if 'last_prediction' not in st.session_state:
        st.session_state.last_prediction = None
    
    # Create form with all inputs
    with st.form("prediction_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏙️ Location Information")
            
            city = st.selectbox(
                "Select City",
                options=['Islamabad', 'Karachi', 'Lahore', 'Peshawar', 'Quetta', 'Multan', 'Faisalabad'],
                help="Choose the city for prediction"
            )
            
            st.markdown("### 📅 Time Information")
            
            pred_date = st.date_input(
                "Prediction Date",
                value=datetime.date.today(),
                help="Select the date for prediction"
            )
            
            hour = st.slider(
                "Hour of Day",
                min_value=0,
                max_value=23,
                value=12,
                help="Select hour (0-23)"
            )
            
            st.markdown("### 🌡️ Weather Conditions")
            
            temperature = st.number_input(
                "Temperature (°C)",
                min_value=-10.0,
                max_value=50.0,
                value=25.0,
                step=0.5,
                help="Current temperature in Celsius"
            )
            
            humidity = st.slider(
                "Humidity (%)",
                min_value=0,
                max_value=100,
                value=60,
                help="Relative humidity percentage"
            )
        
        with col2:
            st.markdown("### 💨 Air Quality Parameters")
            
            pm25_current = st.number_input(
                "Current PM2.5 (µg/m³)",
                min_value=0.0,
                max_value=500.0,
                value=50.0,
                step=1.0,
                help="Current PM2.5 concentration"
            )
            
            pm10 = st.number_input(
                "PM10 (µg/m³)",
                min_value=0.0,
                max_value=600.0,
                value=100.0,
                step=1.0,
                help="PM10 particle concentration"
            )
            
            wind_speed = st.slider(
                "Wind Speed (km/h)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=0.5,
                help="Wind speed in km/h"
            )
            
            st.markdown("### 🌤️ Additional Factors")
            
            pressure = st.number_input(
                "Atmospheric Pressure (hPa)",
                min_value=900.0,
                max_value=1100.0,
                value=1013.0,
                step=0.1,
                help="Atmospheric pressure"
            )
            
            visibility = st.slider(
                "Visibility (km)",
                min_value=0.0,
                max_value=50.0,
                value=10.0,
                step=0.5,
                help="Visibility distance"
            )
            
            season = st.selectbox(
                "Season",
                options=['Winter', 'Spring', 'Summer', 'Autumn'],
                help="Current season"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button(
                "🔮 Predict Air Quality",
                use_container_width=True
            )
    
    # Handle form submission
    if submitted:
        try:
            # Encode city
            city_code = 0
            try:
                city_code = city_encoder.transform([city])[0]
            except:
                # If city not in encoder, assign a default
                city_codes = {'Islamabad': 0, 'Karachi': 1, 'Lahore': 2, 
                             'Peshawar': 3, 'Quetta': 4, 'Multan': 5, 'Faisalabad': 6}
                city_code = city_codes.get(city, 0)
            
            # Create input data dictionary
            input_data = {
                'city_encoded': city_code,
                'hour': hour,
                'day': pred_date.day,
                'month': pred_date.month,
                'weekday': pred_date.weekday(),
                'day_of_year': pred_date.timetuple().tm_yday,
                'Temperature': temperature,
                'Humidity': humidity,
                'PM2.5': pm25_current,
                'components.pm10': pm10,
                'Wind_Speed': wind_speed,
                'Pressure': pressure,
                'Visibility': visibility,
                'season_Winter': 1 if season == 'Winter' else 0,
                'season_Spring': 1 if season == 'Spring' else 0,
                'season_Summer': 1 if season == 'Summer' else 0,
                'season_Autumn': 1 if season == 'Autumn' else 0,
            }
            
            # Add lag and rolling features (simulated)
            input_data['pm2_5_lag1'] = pm25_current * np.random.uniform(0.8, 1.2)
            input_data['pm2_5_lag3'] = pm25_current * np.random.uniform(0.7, 1.3)
            input_data['pm2_5_lag7'] = pm25_current * np.random.uniform(0.6, 1.4)
            input_data['pm2_5_roll3'] = pm25_current * np.random.uniform(0.9, 1.1)
            input_data['pm2_5_roll7'] = pm25_current * np.random.uniform(0.8, 1.2)
            input_data['pm2_5_roll14'] = pm25_current * np.random.uniform(0.7, 1.3)
            
            # Add other pollutants (simulated based on PM2.5)
            input_data['components.co'] = pm25_current * np.random.uniform(5, 20)
            input_data['components.no'] = pm25_current * np.random.uniform(0.1, 0.5)
            input_data['components.no2'] = pm25_current * np.random.uniform(0.2, 0.8)
            input_data['components.o3'] = pm25_current * np.random.uniform(0.5, 1.5)
            input_data['components.so2'] = pm25_current * np.random.uniform(0.1, 0.3)
            input_data['components.nh3'] = pm25_current * np.random.uniform(0.05, 0.2)
            
            # Add derived features
            input_data['pm2_5_pm10_ratio'] = pm25_current / (pm10 + 0.001)
            input_data['no2_co_ratio'] = input_data['components.no2'] / (input_data['components.co'] + 0.001)
            
            # Add weather features
            input_data['dew_point_2m'] = temperature * 0.6  # Simple approximation
            input_data['relative_humidity_2m'] = humidity
            input_data['precipitation'] = 0  # Assuming no rain for prediction
            input_data['surface_pressure'] = pressure
            input_data['wind_direction_10m'] = np.random.randint(0, 360)
            input_data['shortwave_radiation'] = np.random.randint(0, 1000)
            
            # Add temporal features
            input_data['quarter'] = (pred_date.month - 1) // 3 + 1
            
            # Show loading animation
            with st.spinner('🤖 AI is analyzing your parameters...'):
                import time
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Make prediction
                result = predict_custom_input(best_model, city_encoder, label_encoder, feature_columns, input_data)
            
            if result:
                # Store in session state
                st.session_state.last_prediction = {
                    'result': result,
                    'inputs': input_data,
                    'city': city,
                    'date': pred_date,
                    'params': {
                        'temperature': temperature,
                        'humidity': humidity,
                        'pm25': pm25_current,
                        'wind_speed': wind_speed
                    }
                }
                
                # Clear progress bar
                progress_bar.empty()
                
                # Display results
                display_prediction_results(result, city, pred_date, input_data)
                
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")
            import traceback
            st.error(f"Detailed error: {traceback.format_exc()}")
    
    # Display last prediction if exists
    elif st.session_state.last_prediction is not None:
        result = st.session_state.last_prediction['result']
        city = st.session_state.last_prediction['city']
        pred_date = st.session_state.last_prediction['date']
        input_data = st.session_state.last_prediction['inputs']
        
        st.info("📊 Displaying last prediction. Submit form again with new parameters to update.")
        display_prediction_results(result, city, pred_date, input_data)

def display_prediction_results(result, city, pred_date, input_data):
    """Display prediction results - Fixed to show proper updates"""
    category = result['category']
    confidence = result['confidence']
    pm25_value = result['pm25_value']
    
    # Display results with animation
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Prediction Results</div>', unsafe_allow_html=True)
    
    # Result cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="premium-metric">
                <div class="metric-icon">{AQI_CATEGORIES[category]['icon']}</div>
                <div class="metric-value" style="font-size: 2rem;">{category}</div>
                <div class="metric-label">Predicted Category</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="premium-metric">
                <div class="metric-icon">📈</div>
                <div class="metric-value">{pm25_value:.1f}</div>
                <div class="metric-label">Estimated PM2.5 (µg/m³)</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="premium-metric">
                <div class="metric-icon">🎯</div>
                <div class="metric-value">{confidence:.1f}%</div>
                <div class="metric-label">Confidence Score</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Alert based on category
    if category in ["Unhealthy", "Very Unhealthy"]:
        alert_class = "alert-danger" if category == "Very Unhealthy" else "alert-warning"
        st.markdown(f"""
            <div class="{alert_class}">
                <h3 style="margin: 0 0 10px 0; color: {AQI_CATEGORIES[category]['color']}; font-weight: 800;">
                    🚨 {category.upper()} AIR QUALITY PREDICTED
                </h3>
                <p style="margin: 0; font-size: 1.1rem; font-weight: 600;">
                    {AQI_CATEGORIES[category]['description']}
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="alert-info">
                <h3 style="margin: 0 0 10px 0; color: {AQI_CATEGORIES[category]['color']}; font-weight: 800;">
                    ✅ {category.upper()} AIR QUALITY PREDICTED
                </h3>
                <p style="margin: 0; font-size: 1.1rem; font-weight: 600;">
                    {AQI_CATEGORIES[category]['description']}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Health recommendations
    st.markdown("### 💡 Health Recommendations")
    recommendations = get_health_recommendations(category)
    
    cols = st.columns(2)
    for i, rec in enumerate(recommendations):
        with cols[i % 2]:
            icon = rec.split()[0]
            text = ' '.join(rec.split()[1:])
            st.info(f"{icon} {text}")
    
    # Probability breakdown
    st.markdown("### 📊 Prediction Confidence Breakdown")
    
    prob_df = pd.DataFrame({
        'Category': list(result['probabilities'].keys()),
        'Probability': [v * 100 for v in result['probabilities'].values()]
    })
    
    fig = px.bar(
        prob_df,
        x='Category',
        y='Probability',
        color='Category',
        color_discrete_map={cat: info['color'] for cat, info in AQI_CATEGORIES.items()},
        title="<b>Prediction Probabilities by Category</b>",
        labels={'Probability': 'Confidence (%)'},
        text='Probability'
    )
    
    fig.update_traces(
        texttemplate='<b>%{y:.1f}%</b>',
        textposition='outside',
        marker_line_width=3,
        marker_line_color='white',
        textfont=dict(size=14, family='Poppins')
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Inter, sans-serif", size=13),
        title_font=dict(size=20, color='#1E3A8A', family='Outfit')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Input summary
    with st.expander("📋 View Input Parameters Summary"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                **Location:**
                - City: {city}
                - Date: {pred_date.strftime('%B %d, %Y')}
                - Hour: {input_data.get('hour', 'N/A')}:00
                - Season: {input_data.get('season', 'N/A')}
            """)
        
        with col2:
            st.markdown(f"""
                **Weather:**
                - Temperature: {input_data.get('Temperature', 'N/A')}°C
                - Humidity: {input_data.get('Humidity', 'N/A')}%
                - Wind Speed: {input_data.get('Wind_Speed', 'N/A')} km/h
                - Pressure: {input_data.get('Pressure', 'N/A')} hPa
            """)
        
        with col3:
            st.markdown(f"""
                **Air Quality:**
                - Current PM2.5: {input_data.get('PM2.5', 'N/A')} µg/m³
                - PM10: {input_data.get('components.pm10', 'N/A')} µg/m³
                - Visibility: {input_data.get('Visibility', 'N/A')} km
            """)
    
    # Download prediction
    prediction_data = {
        'City': [city],
        'Date': [pred_date.strftime('%Y-%m-%d')],
        'Hour': [input_data.get('hour', 'N/A')],
        'Temperature': [input_data.get('Temperature', 'N/A')],
        'Humidity': [input_data.get('Humidity', 'N/A')],
        'Wind_Speed': [input_data.get('Wind_Speed', 'N/A')],
        'PM2.5_Current': [input_data.get('PM2.5', 'N/A')],
        'PM10': [input_data.get('components.pm10', 'N/A')],
        'Predicted_Category': [category],
        'Predicted_PM2.5': [pm25_value],
        'Confidence': [f"{confidence:.1f}%"]
    }
    
    pred_df = pd.DataFrame(prediction_data)
    csv = pred_df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download Prediction Results",
        data=csv,
        file_name=f"air_quality_prediction_{pred_date.strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==================== MAIN APPLICATION ====================

def main():
    """Main application function"""
    
    # Hero Header
    st.markdown("""
        <div class="hero-header">
            <h1 class="hero-title">🌫️ Pakistan Air Quality AI</h1>
            <p class="hero-subtitle">Advanced Machine Learning Forecasting System</p>
            <div class="hero-badge">🏆 Powered by XGBoost | 92.25% Accuracy</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Load models
    best_model, label_encoder, city_encoder, feature_columns, predictions_df = load_models()
    
    # Use sample data if no predictions available
    if predictions_df is None:
        st.info("📊 **Demo Mode**: Using sample forecast data for demonstration")
        predictions_df = generate_sample_data()
    else:
        if 'PM2.5_Value' not in predictions_df.columns:
            predictions_df['PM2.5_Value'] = predictions_df.get('Actual_PM2.5', 0)
        if 'Display_Date' not in predictions_df.columns:
            predictions_df['Display_Date'] = pd.to_datetime(predictions_df['Date']).dt.strftime('%b %d, %Y')
    
    # Sidebar Configuration
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 1.5rem 0;">
                <div style="
                    width: 90px;
                    height: 90px;
                    margin: 0 auto 1.25rem;
                    background: linear-gradient(135deg, #3B82F6, #8B5CF6);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 10px 30px rgba(59, 130, 246, 0.5);
                ">
                    <span style="font-size: 3rem;">🌫️</span>
                </div>
                <h2 style="color: #FFFFFF; margin: 0; font-size: 1.75rem; font-weight: 800; text-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);">Dashboard Controls</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # City Selection
        available_cities = sorted(predictions_df['City'].unique().tolist())
        selected_city = st.selectbox(
            "🏙️ Select City",
            options=["📊 All Cities Overview", "🎯 Custom Prediction"] + available_cities,
            index=0
        )
        
        # Forecast Days
        forecast_days = st.slider(
            "📅 Forecast Horizon (Days)",
            min_value=1,
            max_value=7,
            value=3
        )
        
        st.markdown("---")
        
        # Display Options
        st.markdown("### ⚙️ Display Options")
        show_alerts = st.checkbox("🚨 Health Alerts", value=True)
        show_recommendations = st.checkbox("💡 Recommendations", value=True)
        show_ml_insights = st.checkbox("🤖 ML Insights", value=True)
        show_advanced_viz = st.checkbox("📊 Advanced Charts", value=True)
        
        st.markdown("---")
        
        # Refresh Button
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        
        # AQI Legend
        st.markdown("### 📚 AQI Categories")
        for category, info in AQI_CATEGORIES.items():
            with st.expander(f"{info['icon']} {category}"):
                st.markdown(f"""
                    <div style="
                        background: {info['gradient']};
                        padding: 16px;
                        border-radius: 14px;
                        color: white;
                        margin-bottom: 12px;
                        font-weight: 800;
                        font-family: 'Poppins', sans-serif;
                        font-size: 1.125rem;
                        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
                        text-align: center;
                    ">
                        {info['range']}
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                    <p style="color: #FFFFFF; font-weight: 700; font-size: 1rem; margin: 8px 0;">
                        <strong style="color: #A5F3FC;">Health:</strong> {info['health_effects']}
                    </p>
                    <p style="color: #FFFFFF; font-weight: 700; font-size: 1rem; margin: 8px 0;">
                        <strong style="color: #A5F3FC;">Action:</strong> {info['recommendation']}
                    </p>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Model Info
        st.markdown("### 🤖 Model Information")
        st.markdown("""
            <div style="
                background: rgba(59, 130, 246, 0.2);
                padding: 1.5rem;
                border-radius: 16px;
                color: white;
                font-family: 'Inter', sans-serif;
                border: 3px solid rgba(59, 130, 246, 0.4);
                backdrop-filter: blur(12px);
            ">
                <p style="margin: 10px 0; font-weight: 800; font-size: 1.0625rem; color: #FFFFFF;"><strong style="color: #A5F3FC;">Algorithm:</strong> XGBoost</p>
                <p style="margin: 10px 0; font-weight: 800; font-size: 1.0625rem; color: #FFFFFF;"><strong style="color: #A5F3FC;">Accuracy:</strong> 92.25%</p>
                <p style="margin: 10px 0; font-weight: 800; font-size: 1.0625rem; color: #FFFFFF;"><strong style="color: #A5F3FC;">Features:</strong> 50+</p>
                <p style="margin: 10px 0; font-weight: 800; font-size: 1.0625rem; color: #FFFFFF;"><strong style="color: #A5F3FC;">Cities:</strong> 7 Major</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Main Content
    if selected_city == "🎯 Custom Prediction":
        # ==================== CUSTOM PREDICTION VIEW ====================
        
        if best_model is not None and label_encoder is not None:
            create_prediction_form(best_model, city_encoder, label_encoder, feature_columns)
        else:
            st.error("❌ Models not loaded. Cannot perform custom predictions.")
            st.info("Please ensure all model files (best_model.pkl, label_encoder.pkl, etc.) are in the working directory.")
    
    elif selected_city == "📊 All Cities Overview":
        # ==================== ALL CITIES VIEW ====================
        
        # Quick Stats
        st.markdown('<div class="section-title">📊 Real-Time Statistics</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_cities = len(predictions_df['City'].unique())
            st.markdown(f"""
                <div class="premium-metric">
                    <div class="metric-icon">🏙️</div>
                    <div class="metric-value">{total_cities}</div>
                    <div class="metric-label">Cities Monitored</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_pm25 = predictions_df['PM2.5_Value'].mean()
            st.markdown(f"""
                <div class="premium-metric">
                    <div class="metric-icon">📈</div>
                    <div class="metric-value">{avg_pm25:.1f}</div>
                    <div class="metric-label">Avg PM2.5 (µg/m³)</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            unhealthy_count = len(predictions_df[
                predictions_df['AQI_Category'].isin(['Unhealthy', 'Very Unhealthy'])
            ])
            st.markdown(f"""
                <div class="premium-metric">
                    <div class="metric-icon">⚠️</div>
                    <div class="metric-value">{unhealthy_count}</div>
                    <div class="metric-label">Unhealthy Forecasts</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            confidence = predictions_df['Confidence'].str.rstrip('%').astype(float).mean()
            st.markdown(f"""
                <div class="premium-metric">
                    <div class="metric-icon">🎯</div>
                    <div class="metric-value">{confidence:.1f}%</div>
                    <div class="metric-label">Avg Confidence</div>
                </div>
            """, unsafe_allow_html=True)
        
        # City Cards
        st.markdown('<div class="section-title">🏙️ City-wise Current Status</div>', unsafe_allow_html=True)
        
        cols = st.columns(3)
        for idx, city in enumerate(available_cities):
            city_data = predictions_df[predictions_df['City'] == city]
            if len(city_data) > 0:
                latest = city_data.iloc[0]
                category = latest['AQI_Category']
                category_class = category.lower().replace(' ', '-')
                
                with cols[idx % 3]:
                    st.markdown(f"""
                        <div class="city-status-card {category_class}">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
                                <h3 style="margin: 0; color: {AQI_CATEGORIES[category]['color']}; font-size: 1.875rem; font-weight: 800;">
                                    {city}
                                </h3>
                                <span style="font-size: 2.25rem;">{AQI_CATEGORIES[category]['icon']}</span>
                            </div>
                            <div style="font-size: 2.25rem; font-weight: 900; color: {AQI_CATEGORIES[category]['color']}; margin: 0.75rem 0; font-family: 'Outfit', sans-serif;">
                                {latest['PM2.5_Value']} <span style="font-size: 1.125rem; font-weight: 700;">µg/m³</span>
                            </div>
                            <div style="font-weight: 700; color: {AQI_CATEGORIES[category]['color']}; margin: 0.75rem 0; font-size: 1.125rem; font-family: 'Poppins', sans-serif;">
                                {category}
                            </div>
                            <div style="color: #475569; font-size: 1rem; margin-top: 1.25rem; font-weight: 600;">
                                📅 {latest['Display_Date']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        
        # Charts Section
        st.markdown('<div class="section-title">📊 Comparative Analysis</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📊 Bar Chart", "🗺️ Heatmap", "📈 Trends"])
        
        with tab1:
            st.plotly_chart(create_comparison_chart(predictions_df), use_container_width=True)
        
        with tab2:
            # Create heatmap function
            pivot_data = predictions_df.pivot_table(
                values='PM2.5_Value',
                index='City',
                columns='Date',
                aggfunc='first'
            )
            
            fig = go.Figure(data=go.Heatmap(
                z=pivot_data.values,
                x=pivot_data.columns,
                y=pivot_data.index,
                colorscale=[
                    [0, '#D1FAE5'],
                    [0.2, '#FEF3C7'],
                    [0.5, '#FED7AA'],
                    [1, '#FECACA']
                ],
                text=np.round(pivot_data.values, 1),
                texttemplate='<b>%{text}</b>',
                textfont={"size": 13, "family": "Poppins"},
                colorbar=dict(title="PM2.5", titleside="right", titlefont=dict(size=14, family='Inter'))
            ))
            
            fig.update_layout(
                title="<b>PM2.5 Levels Heatmap</b>",
                title_font=dict(size=22, color='#1E3A8A', family='Outfit'),
                xaxis_title="Date",
                yaxis_title="City",
                height=420,
                font=dict(family="Inter, sans-serif", size=13),
                xaxis=dict(tickfont=dict(size=12)),
                yaxis=dict(tickfont=dict(size=13, family='Poppins'))
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            fig = go.Figure()
            for city in available_cities[:5]:
                city_data = predictions_df[predictions_df['City'] == city].head(forecast_days)
                fig.add_trace(go.Scatter(
                    x=city_data['Date'],
                    y=city_data['PM2.5_Value'],
                    mode='lines+markers',
                    name=city,
                    line=dict(width=4),
                    marker=dict(size=10)
                ))
            
            fig.update_layout(
                title="<b>Multi-City PM2.5 Trends</b>",
                title_font=dict(size=22, color='#1E3A8A', family='Outfit'),
                xaxis_title="Date",
                yaxis_title="PM2.5 (µg/m³)",
                height=470,
                hovermode='x unified',
                font=dict(family="Inter, sans-serif", size=13),
                legend=dict(font=dict(size=13, family='Poppins'))
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # City Rankings
        st.markdown('<div class="section-title">🏆 City Risk Rankings</div>', unsafe_allow_html=True)
        
        risk_data = []
        for city in available_cities:
            city_data = predictions_df[predictions_df['City'] == city].head(forecast_days)
            risk_score = calculate_city_risk_score(city_data)
            avg_pm25 = city_data['PM2.5_Value'].mean()
            max_pm25 = city_data['PM2.5_Value'].max()
            
            risk_data.append({
                'City': city,
                'Risk Score': risk_score,
                'Avg PM2.5': round(avg_pm25, 1),
                'Max PM2.5': round(max_pm25, 1),
                'Days Unhealthy': len(city_data[city_data['AQI_Category'].isin(['Unhealthy', 'Very Unhealthy'])])
            })
        
        risk_df = pd.DataFrame(risk_data).sort_values('Risk Score', ascending=False)
        
        for rank, row in enumerate(risk_df.itertuples(), 1):
            col1, col2, col3, col4, col5 = st.columns([0.5, 2, 2, 2, 1.5])
            
            with col1:
                medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
                st.markdown(f"<div style='font-size: 2.25rem; text-align: center;'>{medal}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"<p style='font-weight: 700; font-size: 1.125rem; margin: 0; color: #1E293B;'>{row.City}</p>", unsafe_allow_html=True)
            
            with col3:
                st.metric("Risk Score", row._2, help="Composite risk score based on PM2.5 levels")
            
            with col4:
                st.metric("Avg PM2.5", f"{row._3} µg/m³")
            
            with col5:
                st.metric("Unhealthy Days", f"{row._5}/{forecast_days}")
            
            st.markdown("---")
    
    else:
        # ==================== SINGLE CITY VIEW ====================
        
        city_data = predictions_df[predictions_df['City'] == selected_city].head(forecast_days)
        
        if len(city_data) > 0:
            latest = city_data.iloc[0]
            category = latest['AQI_Category']
            
            # City Header
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                    <div style="
                        background: {AQI_CATEGORIES[category]['gradient']};
                        padding: 2.5rem 2.5rem;
                        border-radius: 24px;
                        color: white;
                        box-shadow: 0 14px 48px {AQI_CATEGORIES[category]['color']}50;
                    ">
                        <h1 style="margin: 0; font-size: 2.75rem; font-weight: 900; text-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);">
                            {AQI_CATEGORIES[category]['icon']} {selected_city}
                        </h1>
                        <p style="margin: 12px 0 0 0; font-size: 1.375rem; opacity: 0.97; font-weight: 600;">
                            Air Quality Forecast
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style="
                        background: white;
                        padding: 2.5rem 2rem;
                        border-radius: 24px;
                        text-align: center;
                        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);
                    ">
                        <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">{AQI_CATEGORIES[category]['icon']}</div>
                        <div style="font-weight: 800; color: {AQI_CATEGORIES[category]['color']}; font-size: 1.375rem; font-family: 'Poppins', sans-serif;">
                            {category}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Alert if unhealthy
            if show_alerts and category in ["Unhealthy", "Very Unhealthy"]:
                alert_class = "alert-danger" if category == "Very Unhealthy" else "alert-warning"
                st.markdown(f"""
                    <div class="{alert_class}">
                        <h3 style="margin: 0 0 12px 0; color: {AQI_CATEGORIES[category]['color']}; font-weight: 800;">
                            🚨 HEALTH ALERT: {category.upper()}
                        </h3>
                        <p style="margin: 0; font-size: 1.1875rem; font-weight: 600;">
                            {AQI_CATEGORIES[category]['description']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Key Metrics
            st.markdown('<div class="section-title">📊 Key Metrics</div>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="premium-metric">
                        <div class="metric-icon">{AQI_CATEGORIES[category]['icon']}</div>
                        <div class="metric-value">{latest['PM2.5_Value']}</div>
                        <div class="metric-label">PM2.5 (µg/m³)</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="premium-metric">
                        <div class="metric-icon">📈</div>
                        <div class="metric-value" style="font-size: 1.75rem;">{category}</div>
                        <div class="metric-label">AQI Category</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if len(city_data) > 1:
                    trend = ((city_data.iloc[-1]['PM2.5_Value'] - latest['PM2.5_Value']) / 
                            latest['PM2.5_Value'] * 100)
                    arrow = "↑" if trend > 0 else "↓"
                    trend_color = "#EF4444" if trend > 0 else "#10B981"
                    st.markdown(f"""
                        <div class="premium-metric">
                            <div class="metric-icon">{arrow}</div>
                            <div class="metric-value" style="color: {trend_color};">{abs(trend):.1f}%</div>
                            <div class="metric-label">Trend</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class="premium-metric">
                            <div class="metric-icon">➡️</div>
                            <div class="metric-value">N/A</div>
                            <div class="metric-label">Trend</div>
                        </div>
                    """, unsafe_allow_html=True)
            
            with col4:
                confidence_val = latest['Confidence'].rstrip('%')
                st.markdown(f"""
                    <div class="premium-metric">
                        <div class="metric-icon">🎯</div>
                        <div class="metric-value">{confidence_val}%</div>
                        <div class="metric-label">Confidence</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Charts
            st.markdown('<div class="section-title">📈 Visual Analysis</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(create_gauge_chart(latest['PM2.5_Value'], category, selected_city), 
                               use_container_width=True)
            
            with col2:
                st.plotly_chart(create_timeline_chart(city_data, selected_city), 
                               use_container_width=True)
            
            # Health Recommendations
            if show_recommendations:
                st.markdown('<div class="section-title">💡 Health Recommendations</div>', unsafe_allow_html=True)
                
                recommendations = get_health_recommendations(category)
                cols = st.columns(2)
                
                for i, rec in enumerate(recommendations):
                    with cols[i % 2]:
                        icon = rec.split()[0]
                        text = ' '.join(rec.split()[1:])
                        st.info(f"{icon} {text}")
            
            # Detailed Forecast Table
            st.markdown('<div class="section-title">📅 Detailed Forecast</div>', unsafe_allow_html=True)
            
            for _, row in city_data.iterrows():
                cat = row['AQI_Category']
                cols = st.columns([2, 2, 2, 2, 1])
                
                with cols[0]:
                    st.markdown(f"<p style='font-weight: 700; font-size: 1.125rem; margin: 0; color: #1E293B;'>{row['Display_Date']}</p>", unsafe_allow_html=True)
                
                with cols[1]:
                    st.markdown(f"""
                        <span style="
                            background: {AQI_CATEGORIES[cat]['gradient']};
                            color: white;
                            padding: 10px 18px;
                            border-radius: 14px;
                            font-weight: 800;
                            display: inline-block;
                            font-family: 'Poppins', sans-serif;
                            font-size: 1rem;
                            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                        ">{cat}</span>
                    """, unsafe_allow_html=True)
                
                with cols[2]:
                    st.markdown(f"<p style='font-weight: 800; font-size: 1.125rem; margin: 0; color: #1E293B;'>{row['PM2.5_Value']} <span style='font-weight: 600;'>µg/m³</span></p>", unsafe_allow_html=True)
                
                with cols[3]:
                    st.markdown(f"<p style='font-weight: 700; font-size: 1rem; margin: 0; color: #475569;'>📊 {row['Confidence']}</p>", unsafe_allow_html=True)
                
                with cols[4]:
                    st.markdown(f"<div style='font-size: 2.25rem; text-align: center;'>{AQI_CATEGORIES[cat]['icon']}</div>", 
                               unsafe_allow_html=True)
                
                st.markdown("---")
            
            # Download Options
            st.markdown('<div class="section-title">💾 Export Data</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv = city_data.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"{selected_city.lower()}_forecast.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                json_data = city_data.to_json(orient='records', indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"{selected_city.lower()}_forecast.json",
                    mime="application/json",
                    use_container_width=True
                )
    
    # Footer
    st.markdown(f"""
        <div class="footer">
            <h3 style="margin: 0; color: #1E3A8A; font-weight: 900;">🌫️ Pakistan Air Quality Forecasting System</h3>
            <p style="color: #475569; margin: 12px 0; font-weight: 700;">
                Powered by Machine Learning | XGBoost Algorithm | 92.25% Accuracy
            </p>
            <p style="font-size: 1rem; color: #64748B; margin: 0; font-weight: 600;">
                📅 Last Updated: {datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")}
            </p>
            <p style="font-size: 0.9375rem; color: #94A3B8; margin: 18px 0 0 0; line-height: 1.7; font-weight: 500;">
                ⚠️ <strong>Disclaimer:</strong> Forecasts are ML-based predictions. Actual conditions may vary. 
                Always consult official sources for health advisories.
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
