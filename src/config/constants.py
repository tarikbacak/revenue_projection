from typing import Dict, List

# Subscription Tiers
SUBSCRIPTION_TIERS = {
    "Basic": {
        "price": 0.70,
        "features": ["Basic Analytics", "Limited Storage", "Email Support"],
        "default_distribution": 0.70
    },
    "Standard": {
        "price": 5.00,
        "features": ["Advanced Analytics", "Unlimited Storage", "Priority Support"],
        "default_distribution": 0.22
    },
    "Premium": {
        "price": 12.50,
        "features": ["Custom Analytics", "Enterprise Storage", "24/7 Support"],
        "default_distribution": 0.08
    }
}

# Growth Scenarios
GROWTH_SCENARIOS = {
    "Conservative (3% monthly)": 0.03,
    "Moderate (8% monthly)": 0.08,
    "Aggressive (12% monthly)": 0.12,
}

# Default Campaign Parameters
DEFAULT_CAMPAIGN_PARAMS = {
    "reach_to_download_rate": 0.05,
    "download_to_active_rate": 0.25,   
    "active_to_subscriber_rate": 1.0, 
}

# Financial Constants
DEFAULT_CAC = 50.0  # Default Customer Acquisition Cost
DEFAULT_CHURN_RATE = 0.05  # 5% monthly churn
DEFAULT_INITIAL_USERS = 100
MAX_PROJECTION_MONTHS = 36

# Sidebar UI Constants
LOGO_WIDTH = 100

# Campaign Settings Constants
CAMPAIGN_START_MONTH_MIN = 1
CAMPAIGN_START_MONTH_MAX = 12
CAMPAIGN_START_MONTH_DEFAULT = 1

CAMPAIGN_DURATION_MIN = 1
CAMPAIGN_DURATION_MAX = 12
CAMPAIGN_DURATION_DEFAULT = 3

CAMPAIGN_REACH_MIN = 1000
CAMPAIGN_REACH_MAX = 1000000
CAMPAIGN_REACH_DEFAULT = 10000
CAMPAIGN_REACH_STEP = 1000

CAMPAIGN_BUDGET_MIN = 100.0
CAMPAIGN_BUDGET_MAX = 100000.0
CAMPAIGN_BUDGET_DEFAULT = 2500.0
CAMPAIGN_BUDGET_STEP = 100.0

# Conversion Rate Constants
REACH_TO_DOWNLOAD_MIN = 0.1
REACH_TO_DOWNLOAD_MAX = 10.0
REACH_TO_DOWNLOAD_DEFAULT = 3.0

DOWNLOAD_TO_ACTIVE_MIN = 1.0
DOWNLOAD_TO_ACTIVE_MAX = 50.0
DOWNLOAD_TO_ACTIVE_DEFAULT = 20.0

# Growth Rate Constants
CUSTOM_GROWTH_RATE_MIN = 1.0
CUSTOM_GROWTH_RATE_MAX = 200.0
CUSTOM_GROWTH_RATE_DEFAULT = 5.0

# Active to Subscriber Rate Constants
ACTIVE_TO_SUBSCRIBER_MIN = 1
ACTIVE_TO_SUBSCRIBER_MAX = 100
ACTIVE_TO_SUBSCRIBER_DEFAULT = 100

# Churn Rate Constants
CHURN_RATE_MIN = 0.0
CHURN_RATE_MAX = 15.0
DEFAULT_CHURN_RATE = 0.0

# Chart Color Constants
CHART_COLORS = {
    # Tier Colors
    'Basic': '#FF6F61',    
    'Standard': '#5F9EFF', 
    'Premium': '#FFC857',  
    
    # UI Theme Colors (from .streamlit/config.toml)
    'primary': '#5358FF',
    'background': '#0E1117',
    'secondary_background': '#1F2128',
    'text': '#FAFAFA',
    
    # Campaign Colors
    'campaign_colors': ['#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#17BECF']
}