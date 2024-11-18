import streamlit as st
from models.subscription import SubscriptionTier
from models.campaign import MarketingCampaign
from services.projection_service import ProjectionService
from utils.utils import get_image_base64
from config.constants import (
    SUBSCRIPTION_TIERS, GROWTH_SCENARIOS, LOGO_WIDTH,
    CAMPAIGN_START_MONTH_MIN, CAMPAIGN_START_MONTH_MAX, CAMPAIGN_START_MONTH_DEFAULT,
    CAMPAIGN_DURATION_MIN, CAMPAIGN_DURATION_MAX, CAMPAIGN_DURATION_DEFAULT,
    CAMPAIGN_REACH_MIN, CAMPAIGN_REACH_MAX, CAMPAIGN_REACH_DEFAULT, CAMPAIGN_REACH_STEP,
    CAMPAIGN_BUDGET_MIN, CAMPAIGN_BUDGET_MAX, CAMPAIGN_BUDGET_DEFAULT, CAMPAIGN_BUDGET_STEP,
    REACH_TO_DOWNLOAD_MIN, REACH_TO_DOWNLOAD_MAX, REACH_TO_DOWNLOAD_DEFAULT,
    DOWNLOAD_TO_ACTIVE_MIN, DOWNLOAD_TO_ACTIVE_MAX, DOWNLOAD_TO_ACTIVE_DEFAULT,
    ACTIVE_TO_SUBSCRIBER_MIN, ACTIVE_TO_SUBSCRIBER_MAX, ACTIVE_TO_SUBSCRIBER_DEFAULT,
    CUSTOM_GROWTH_RATE_MIN, CUSTOM_GROWTH_RATE_MAX, CUSTOM_GROWTH_RATE_DEFAULT,
    CHURN_RATE_MIN, CHURN_RATE_MAX, DEFAULT_CHURN_RATE
)

def render_sidebar(projection_service: ProjectionService):
    with st.sidebar:
        # Add logo with rounded style
        st.markdown(
            """
            <style>
                .rounded-image {
                    border-radius: 50%;
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }
                .centered-button {
                    display: flex;
                    justify-content: center;
                    margin-top: 10px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Center the image using HTML
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{get_image_base64('assets/logo.png')}" 
                     width="{LOGO_WIDTH}" 
                     class="rounded-image">
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Center the button
        with st.container():
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; margin: 1rem 0;">
                """,
                unsafe_allow_html=True
            )
            st.link_button("Lis.Ai", "https://luminousis.co/", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.header("Configuration")
        
        # Growth Scenario Selection in an expander
        with st.expander("📈 Growth Scenario", expanded=True):
            scenario_options = list(GROWTH_SCENARIOS.keys()) + ["Custom"]
            selected_scenario_display = st.selectbox(
                "Select Scenario",
                options=scenario_options
            )
            
            if selected_scenario_display == "Custom":
                custom_growth_rate = st.number_input(
                    "Custom Monthly Growth Rate (%)",
                    min_value=CUSTOM_GROWTH_RATE_MIN,
                    max_value=CUSTOM_GROWTH_RATE_MAX,
                    value=CUSTOM_GROWTH_RATE_DEFAULT,
                    help="Enter a monthly growth rate between 1% and 200%"
                )
                projection_service.growth_scenario = "Custom"
                projection_service.custom_growth_rate = custom_growth_rate
            else:
                projection_service.growth_scenario = selected_scenario_display
            
            # Add churn rate checkbox and slider
            enable_churn = st.checkbox(
                "Include Churn Rate",
                value=projection_service.enable_churn,
                help="Enable to model monthly subscriber churn"
            )
            
            if enable_churn:
                churn_rate = st.slider(
                    "Monthly Churn Rate (%)",
                    min_value=CHURN_RATE_MIN,
                    max_value=CHURN_RATE_MAX,
                    value=DEFAULT_CHURN_RATE,
                    step=0.1,
                    help="Percentage of users who cancel their subscription each month"
                )
                projection_service.churn_rate = churn_rate / 100
            else:
                projection_service.churn_rate = 0.0
            
            projection_service.enable_churn = enable_churn
        
        # Subscription Tiers in an expander
        with st.expander("💳 Subscription Tiers", expanded=True):
            for tier_name, tier_data in SUBSCRIPTION_TIERS.items():
                st.write(f"### {tier_name} Plan")
                
                price_col, dist_col = st.columns(2)
                with price_col:
                    price = st.number_input(
                        "Price ($)",
                        min_value=0.0,
                        max_value=100.0,
                        value=tier_data["price"],
                        key=f"price_{tier_name}"
                    )
                with dist_col:
                    distribution = st.number_input(
                        "Distribution (%)",
                        min_value=0.0,
                        max_value=100.0,
                        value=tier_data["default_distribution"] * 100,
                        key=f"dist_{tier_name}"
                    )
                
                projection_service.subscriptions.append(
                    SubscriptionTier(
                        name=tier_name,
                        monthly_price=price,
                        features=tier_data["features"],
                        distribution_percentage=distribution / 100
                    )
                )
        
        # Marketing Campaign in an expander
        with st.expander("📢 Marketing", expanded=True):
            st.write("### Campaign Settings")
            
            # Campaign timing
            col1, col2 = st.columns(2)
            with col1:
                start_month = st.number_input(
                    "Start Month",
                    min_value=CAMPAIGN_START_MONTH_MIN,
                    max_value=CAMPAIGN_START_MONTH_MAX,
                    value=CAMPAIGN_START_MONTH_DEFAULT,
                    help="Campaign start month (1-12)"
                )
            with col2:
                duration = st.number_input(
                    "Duration (months)",
                    min_value=CAMPAIGN_DURATION_MIN,
                    max_value=CAMPAIGN_DURATION_MAX,
                    value=CAMPAIGN_DURATION_DEFAULT,
                    help=(
                        "Specify the number of months over which the campaign will run. "
                        "The total expected new users from the campaign will be evenly distributed "
                        "across these months. For example, if the campaign is expected to bring in "
                        "200 new users and the duration is set to 3 months, approximately 67 users "
                        "will be added each month. This setting helps in planning the timing and "
                        "impact of user growth due to marketing efforts."
                    )
                )
            
            # Campaign metrics
            reach = st.number_input(
                "Expected Reach",
                min_value=CAMPAIGN_REACH_MIN,
                max_value=CAMPAIGN_REACH_MAX,
                value=CAMPAIGN_REACH_DEFAULT,
                step=CAMPAIGN_REACH_STEP,
                help="Expected number of people the campaign will reach"
            )
            
            budget = st.number_input(
                "Campaign Budget ($)",
                min_value=CAMPAIGN_BUDGET_MIN,
                max_value=CAMPAIGN_BUDGET_MAX,
                value=CAMPAIGN_BUDGET_DEFAULT,
                step=CAMPAIGN_BUDGET_STEP,
                help="Total campaign budget"
            )
            
            # Conversion rates
            st.write("### Conversion Rates")
            reach_to_download = st.slider(
                "Reach to Download Rate (%)",
                min_value=REACH_TO_DOWNLOAD_MIN,
                max_value=REACH_TO_DOWNLOAD_MAX,
                value=REACH_TO_DOWNLOAD_DEFAULT,
                help="Percentage of reached users who will download"
            )
            
            download_to_active = st.slider(
                "Download to Active Rate (%)",
                min_value=DOWNLOAD_TO_ACTIVE_MIN,
                max_value=DOWNLOAD_TO_ACTIVE_MAX,
                value=DOWNLOAD_TO_ACTIVE_DEFAULT,
                help="Percentage of downloads that become active users"
            )
            
            st.write("")  # Add vertical space
            
            # Show existing campaigns
            if projection_service.campaigns:
                st.write("### Active Campaigns")
                selected_campaign = st.selectbox(
                    "Select Campaign",
                    options=[f"Campaign {idx + 1}" for idx in range(len(projection_service.campaigns))],
                    key="campaign_selector"
                )
                
                if selected_campaign:
                    idx = int(selected_campaign.split()[-1]) - 1
                    campaign = projection_service.campaigns[idx]
                    
                    with st.expander("Campaign Details", expanded=True):
                        st.write(f"**Start Month:** {campaign.start_month}")
                        st.write(f"**Duration:** {campaign.duration_months} months")
                        st.write(f"**Budget:** ${campaign.budget:,.2f}")
                        st.write(f"**Expected Reach:** {campaign.expected_reach:,}")
                        
                        if st.button("Delete Campaign", type="error", key=f"delete_{campaign.campaign_id}"):
                            projection_service.campaigns.remove(campaign)
                            st.success(f"{selected_campaign} deleted!")
                            st.rerun()
            
            # Add Set Campaign button
            if st.button("Add New Campaign", type="primary", use_container_width=True):
                campaign = MarketingCampaign(
                    name=f"Campaign {len(projection_service.campaigns) + 1}",
                    campaign_id=f"camp_{len(projection_service.campaigns) + 1}",
                    start_month=start_month,
                    duration_months=duration,
                    budget=budget,
                    expected_reach=reach,
                    reach_to_download_rate=reach_to_download / 100,
                    download_to_active_rate=download_to_active / 100,
                    active_to_subscriber_rate=1.0
                )
                
                # Check for campaign overlap
                has_overlap = False
                for existing_campaign in projection_service.campaigns:
                    if (campaign.start_month <= existing_campaign.start_month + existing_campaign.duration_months and
                        campaign.start_month + campaign.duration_months >= existing_campaign.start_month):
                        has_overlap = True
                        st.warning(f"⚠️ Campaign overlaps with existing campaign starting in month {existing_campaign.start_month}")
                
                projection_service.campaigns.append(campaign)
                st.success(f"✅ Campaign {len(projection_service.campaigns)} has been added!")
