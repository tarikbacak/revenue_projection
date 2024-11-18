import streamlit as st
import pandas as pd
from services.projection_service import ProjectionService

def display_projections_table(projections: pd.DataFrame, projection_service: ProjectionService):
    st.subheader("Monthly Projections")
    
    display_df = projections.copy()
    
    # Rename columns for better readability
    column_renames = {
        'month': 'Month',
        'base_users': 'Total Organic Growth',
        'campaign_users': 'Total Campaign-Driven Users',
        'total_users': 'Total Active Users',
        'organic_growth_rate': 'Monthly Organic Growth Rate (%)',
        'campaign_growth_rate': 'Monthly Campaign Growth Rate (%)',
        'growth_rate': 'Total Monthly Growth Rate (%)',
        'total_revenue': 'Total Monthly Revenue'
    }
    
    for tier in projection_service.subscriptions:
        column_renames.update({
            f'users_{tier.name.lower()}': f'{tier.name} Plan Users',
            f'revenue_{tier.name.lower()}': f'{tier.name} Plan Revenue'
        })
    
    display_df = display_df.rename(columns=column_renames)
    
    # Format numeric columns
    for col in display_df.columns:
        if 'Revenue' in col:
            display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")
        elif 'Rate (%)' in col or 'Growth (%)' in col:
            display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}%")
        elif 'Users' in col or 'Growth' in col:
            display_df[col] = display_df[col].apply(lambda x: f"{int(x):,}")
    
    # Calculate height based on number of rows plus some padding for header
    # Using 35 pixels per row and adding 100 pixels for header and padding
    height = (len(display_df) * 35) + 37
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=height,
        key="projections_table"
    ) 