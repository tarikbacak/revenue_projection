import streamlit as st
import pandas as pd

def display_metrics(projections: pd.DataFrame):
    # Revenue Metrics Row
    st.subheader("Revenue Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Revenue (12 months)",
            f"${projections['total_revenue'].sum():,.2f}",
            help="Total revenue across all subscription tiers for the next 12 months"
        )
    with col2:
        st.metric(
            "Average Monthly Revenue",
            f"${projections['total_revenue'].mean():,.2f}",
            help="Average monthly revenue across all subscription tiers"
        )
    with col3:
        first_month_rev = projections['total_revenue'].iloc[0]
        last_month_rev = projections['total_revenue'].iloc[-1]
        rev_growth = ((last_month_rev - first_month_rev) / first_month_rev) * 100
        st.metric(
            "Revenue Growth (M1 to M12)",
            f"{rev_growth:,.1f}%",
            help="Percentage growth in monthly revenue from Month 1 to Month 12"
        )
    with col4:
        last_month_rev = projections['total_revenue'].iloc[-1]
        st.metric(
            "Month 12 Run Rate (ARR)",
            f"${last_month_rev * 12:,.2f}",
            help="Annual Run Rate based on Month 12 revenue"
        )

    # User Metrics Row
    st.subheader("User Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = projections['total_users'].iloc[-1]
        st.metric(
            "Total Users (Month 12)",
            f"{int(total_users):,}",
            help="Total active users by the end of Month 12"
        )
    with col2:
        avg_growth_rate = projections['growth_rate'].mean()
        st.metric(
            "Avg Monthly Growth Rate",
            f"{avg_growth_rate:.1f}%",
            help="Average monthly user growth rate including organic and campaign-driven growth"
        )
    with col3:
        organic_users = projections['base_users'].iloc[-1]
        st.metric(
            "Organic Users (Month 12)",
            f"{int(organic_users):,}",
            help="Users from organic growth by Month 12"
        )
    with col4:
        campaign_users = projections['campaign_users'].iloc[-1]
        st.metric(
            "Campaign Users (Month 12)",
            f"{int(campaign_users):,}",
            help="Users from marketing campaigns by Month 12"
        )

    # Subscription Metrics Row
    st.subheader("Subscription Metrics")
    cols = st.columns(4)
    
    # Get subscription tier columns
    tier_columns = [col for col in projections.columns if col.startswith('revenue_')]
    
    for idx, col in enumerate(tier_columns):
        with cols[idx]:
            tier_name = col.split('_')[1].title()
            tier_revenue = projections[col].iloc[-1]
            tier_users = projections[f'users_{tier_name.lower()}'].iloc[-1]
            
            st.metric(
                f"{tier_name} Tier (Month 12)",
                f"${tier_revenue:,.2f}",
                f"{int(tier_users):,} users",
                help=f"Month 12 revenue and user count for {tier_name} tier"
            )

    # Campaign Impact Row (if campaigns exist)
    campaign_columns = [col for col in projections.columns if 'campaign' in col.lower()]
    if campaign_columns:
        st.subheader("Campaign Impact")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_campaign_revenue = (projections['campaign_users'].iloc[-1] * 
                                    (projections['total_revenue'].iloc[-1] / 
                                     projections['total_users'].iloc[-1]))
            st.metric(
                "Campaign-Driven Revenue (M12)",
                f"${total_campaign_revenue:,.2f}",
                help="Estimated revenue from campaign-acquired users in Month 12"
            )
        with col2:
            campaign_percentage = (projections['campaign_users'].iloc[-1] / 
                                 projections['total_users'].iloc[-1] * 100)
            st.metric(
                "Campaign User %",
                f"{campaign_percentage:.1f}%",
                help="Percentage of total users acquired through campaigns"
            )
        with col3:
            avg_campaign_growth = projections['campaign_growth_rate'].mean()
            st.metric(
                "Avg Campaign Growth",
                f"{avg_campaign_growth:.1f}%",
                help="Average monthly growth rate from campaigns"
            )
        with col4:
            revenue_per_user = projections['total_revenue'].iloc[-1] / projections['total_users'].iloc[-1]
            st.metric(
                "Revenue per User (M12)",
                f"${revenue_per_user:.2f}",
                help="Average monthly revenue per user in Month 12"
            )
 