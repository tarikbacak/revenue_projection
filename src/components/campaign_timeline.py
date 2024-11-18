import streamlit as st
import plotly.graph_objects as go
from models.campaign import MarketingCampaign
from typing import List

def display_campaign_timeline(campaigns: List[MarketingCampaign]):
    if not campaigns:
        st.info("No campaigns have been set yet.")
        return
        
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, campaign in enumerate(campaigns):
        color = colors[i % len(colors)]
        
        fig.add_trace(go.Bar(
            name=campaign.name,
            x=[campaign.duration_months],
            y=[campaign.campaign_id],
            orientation='h',
            marker=dict(color=color),
            base=campaign.start_month - 1,
            customdata=[[
                campaign.name,
                campaign.start_month,
                campaign.duration_months,
                campaign.budget,
                campaign.expected_reach
            ]],
            hovertemplate="<br>".join([
                "<b>%{customdata[0]}</b>",
                "Start Month: %{customdata[1]}",
                "Duration: %{customdata[2]} months",
                "Budget: $%{customdata[3]:,.2f}",
                "Expected Reach: %{customdata[4]:,}",
                "<extra></extra>"
            ])
        ))
    
    fig.update_layout(
        title="Campaign Timeline",
        showlegend=False,
        height=100 + (len(campaigns) * 40),
        xaxis=dict(
            title="Month",
            tickmode='linear',
            tick0=1,
            dtick=1,
            range=[0, 13]
        ),
        yaxis=dict(
            title="",
            showticklabels=False
        ),
        barmode='overlay'
    )
    
    st.plotly_chart(fig, use_container_width=True) 