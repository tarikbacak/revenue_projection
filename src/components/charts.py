import plotly.graph_objects as go
import streamlit as st
from services.projection_service import ProjectionService
from config.constants import CHART_COLORS

def get_tier_color(tier_name: str) -> str:
    """Return a consistent color for each subscription tier"""
    return CHART_COLORS.get(tier_name, CHART_COLORS['primary'])

def get_campaign_color(campaign_index: int) -> str:
    """Return a consistent color for each campaign"""
    return CHART_COLORS['campaign_colors'][campaign_index % len(CHART_COLORS['campaign_colors'])]

def plot_revenue_chart(projections, projection_service: ProjectionService, key=None):
    fig = go.Figure()
    
    for tier in projection_service.subscriptions:
        column_name = f'revenue_{tier.name.lower()}'
        fig.add_trace(go.Scatter(
            x=projections['month'],
            y=projections[column_name],
            name=f"{tier.name} Revenue",
            stackgroup='one',
            line=dict(color=get_tier_color(tier.name))
        ))
    
    # Add campaign indicators
    campaign_colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    for i, campaign in enumerate(projection_service.campaigns):
        color = get_campaign_color(i)
        
        # Calculate campaign revenue impact
        campaign_impact = (campaign.expected_reach * 
                         campaign.reach_to_download_rate * 
                         campaign.download_to_active_rate * 
                         campaign.active_to_subscriber_rate)
        
        avg_revenue_per_user = projections['total_revenue'].iloc[campaign.start_month - 1] / projections['total_users'].iloc[campaign.start_month - 1]
        revenue_impact = campaign_impact * avg_revenue_per_user
        
        # Add campaign marker
        fig.add_trace(go.Scatter(
            x=[campaign.start_month],
            y=[projections['total_revenue'].iloc[campaign.start_month - 1]],
            mode='markers',
            name=f'Campaign {i+1}',
            marker=dict(
                symbol='star',
                size=12,
                color=color
            ),
            hovertemplate=(
                f"<b>Campaign {i+1}</b><br>" +
                f"Month: {campaign.start_month}<br>" +
                f"Revenue Impact: +${revenue_impact:,.2f}<br>" +
                f"Duration: {campaign.duration_months} months<br>" +
                f"<extra></extra>"
            )
        ))
    
    fig.update_layout(
        title="Projected Revenue by Tier",
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        showlegend=True,
        xaxis=dict(
            range=[0.5, 12.5],  # This keeps the chart centered and prevents shifting
            tickmode='linear',
            tick0=1,
            dtick=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, key=key)

def plot_users_chart(projections, projection_service: ProjectionService):
    fig = go.Figure()
    
    # Add individual tier lines
    for tier in projection_service.subscriptions:
        user_column = f'users_{tier.name.lower()}'
        fig.add_trace(go.Scatter(
            x=projections['month'],
            y=projections[user_column],
            name=f"{tier.name} Users",
            mode='lines',
            line=dict(color=get_tier_color(tier.name))
        ))
    
    # Add total users line
    fig.add_trace(go.Scatter(
        x=projections['month'],
        y=projections['total_users'],
        name="Total Users",
        mode='lines',
        line=dict(
            width=3,
            dash='dot',
            color=CHART_COLORS['text']  # Using theme's text color
        ),
    ))
    
    # Add campaign indicators with consistent colors
    for i, campaign in enumerate(projection_service.campaigns):
        color = get_campaign_color(i)
        
        campaign_impact = (campaign.expected_reach * 
                         campaign.reach_to_download_rate * 
                         campaign.download_to_active_rate * 
                         campaign.active_to_subscriber_rate)
        
        fig.add_trace(go.Scatter(
            x=[campaign.start_month],
            y=[projections['total_users'].iloc[campaign.start_month - 1]],
            mode='markers',
            name=f'Campaign {i+1}',
            marker=dict(
                symbol='star',
                size=12,
                color=color
            ),
            hovertemplate=(
                f"<b>Campaign {i+1}</b><br>" +
                f"Month: {campaign.start_month}<br>" +
                f"User Impact: +{int(campaign_impact):,}<br>" +
                f"Duration: {campaign.duration_months} months<br>" +
                f"<extra></extra>"
            )
        ))
    
    fig.update_layout(
        title="User Growth Projection",
        xaxis_title="Month",
        yaxis_title="Number of Users",
        showlegend=True,
        xaxis=dict(
            range=[0.5, 12.5],  # This keeps the chart centered and prevents shifting
            tickmode='linear',
            tick0=1,
            dtick=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, key="users_chart") 