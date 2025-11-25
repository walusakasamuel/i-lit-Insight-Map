# i-Lit Insight Map Configuration
PROJECT_NAME = "i-Lit Insight Map"
VERSION = "1.0.0"
DESCRIPTION = "AI-Powered Mental Health Risk Stratification System"

# Data paths
DATA_RAW_PATH = "../data/raw/synthetic_mh_data.csv"
DATA_PROCESSED_PATH = "../data/processed/cleaned_mh_data.csv"

# Model parameters
RISK_THRESHOLDS = {
    'low_risk': 0.3,
    'medium_risk': 0.7,
    'high_risk': 1.0
}

# Clinical thresholds (based on literature)
CLINICAL_THRESHOLDS = {
    'phq9_moderate': 10,
    'phq9_severe': 15,
    'gad7_moderate': 10,
    'gad7_severe': 15
}

# Visualization settings
COLOR_SCHEME = {
    'low_risk': '#2E8B57',      # Sea Green
    'medium_risk': '#FFA500',   # Orange
    'high_risk': '#DC143C',     # Crimson
    'background': '#F5F5F5'     # Light Gray
}