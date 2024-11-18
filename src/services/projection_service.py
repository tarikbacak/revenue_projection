import pandas as pd
from typing import List, Dict, Optional
from models.subscription import SubscriptionTier
from models.campaign import MarketingCampaign
from config.constants import (
    GROWTH_SCENARIOS,
    DEFAULT_CHURN_RATE,
    DEFAULT_INITIAL_USERS,
    MAX_PROJECTION_MONTHS
)

class ProjectionService:
    def __init__(self):
        self.subscriptions: List[SubscriptionTier] = []
        self.campaigns: List[MarketingCampaign] = []
        self.growth_scenario: str = "Moderate (8% monthly)"
        self.custom_growth_rate: Optional[float] = None
        self.enable_churn: bool = False
        self.churn_rate: float = 0.0
    
    def calculate_projections(self, months: int = 12) -> pd.DataFrame:
        """Calculate monthly revenue and user projections including campaign impacts."""
        self._validate_inputs(months)
        
        # Initialize DataFrame
        df = pd.DataFrame({
            'month': range(1, months + 1),
            'base_users': 0.0,
            'campaign_users': 0.0,
            'total_users': 0.0,
            'organic_growth_rate': 0.0,
            'campaign_growth_rate': 0.0,
            'growth_rate': 0.0,
            'total_revenue': 0.0
        })
        
        # Get growth rate
        growth_rate = self._get_growth_rate()
        if self.enable_churn:
            net_growth_rate = growth_rate - self.churn_rate
        else:
            net_growth_rate = growth_rate
        
        # Initialize first month's base users with growth
        df.loc[0, 'base_users'] = DEFAULT_INITIAL_USERS * (1 + net_growth_rate)
        
        # Calculate first month's organic growth rate based on DEFAULT_INITIAL_USERS
        df.loc[0, 'organic_growth_rate'] = ((df.loc[0, 'base_users'] - DEFAULT_INITIAL_USERS) / DEFAULT_INITIAL_USERS) * 100
        
        # Calculate campaign impacts
        self._add_campaign_impacts(df)
        
        # Calculate total users for first month
        df.loc[0, 'total_users'] = df.loc[0, 'base_users'] + df.loc[0, 'campaign_users']
        
        # Calculate first month's campaign growth rate if there are campaign users
        if df.loc[0, 'campaign_users'] > 0:
            df.loc[0, 'campaign_growth_rate'] = (df.loc[0, 'campaign_users'] / DEFAULT_INITIAL_USERS) * 100
        
        # Calculate first month's total growth rate
        df.loc[0, 'growth_rate'] = df.loc[0, 'organic_growth_rate'] + df.loc[0, 'campaign_growth_rate']
        
        # Calculate subsequent months
        for month in range(1, months):
            prev_total_users = df.loc[month-1, 'total_users']
            
            # Calculate new organic users based on previous month's total users
            new_organic_users = prev_total_users * net_growth_rate
            df.loc[month, 'base_users'] = prev_total_users + new_organic_users
            
            # Calculate total users for current month
            df.loc[month, 'total_users'] = df.loc[month, 'base_users'] + df.loc[month, 'campaign_users']
            
            # Calculate growth rates
            df.loc[month, 'organic_growth_rate'] = (new_organic_users / prev_total_users) * 100
            
            if df.loc[month, 'campaign_users'] > df.loc[month-1, 'campaign_users']:
                new_campaign_users = df.loc[month, 'campaign_users'] - df.loc[month-1, 'campaign_users']
                df.loc[month, 'campaign_growth_rate'] = (new_campaign_users / prev_total_users) * 100
            
            # Total growth rate is sum of organic and campaign growth
            df.loc[month, 'growth_rate'] = df.loc[month, 'organic_growth_rate'] + df.loc[month, 'campaign_growth_rate']
        
        # Calculate subscription metrics
        for tier in self.subscriptions:
            df[f'users_{tier.name.lower()}'] = df['total_users'] * tier.distribution_percentage
            df[f'revenue_{tier.name.lower()}'] = df[f'users_{tier.name.lower()}'] * tier.monthly_price
        
        df['total_revenue'] = sum(df[f'revenue_{tier.name.lower()}'] for tier in self.subscriptions)
        
        return df
    
    def _validate_inputs(self, months: int) -> None:
        """Validate input parameters."""
        if months > MAX_PROJECTION_MONTHS:
            raise ValueError(f"Projection months cannot exceed {MAX_PROJECTION_MONTHS}")
        
        if not self.subscriptions:
            raise ValueError("At least one subscription tier must be configured")
    
    def _get_growth_rate(self) -> float:
        """Determine the appropriate growth rate based on scenario."""
        if self.growth_scenario == "Custom" and self.custom_growth_rate is not None:
            return self.custom_growth_rate / 100  # Convert percentage to decimal
        return GROWTH_SCENARIOS[self.growth_scenario]
    
    def _add_campaign_impacts(self, df: pd.DataFrame) -> None:
        """
        Add campaign impacts to the projection with proper growth handling:
        1. Campaign users are added gradually during campaign
        2. Existing users from campaign remain after campaign ends
        3. Growth rate is applied to total user base
        """
        cumulative_campaign_users = pd.Series(0.0, index=df.index)
        
        for campaign in self.campaigns:
            # Calculate total new users from this campaign
            new_users = float(campaign.expected_reach * 
                             campaign.reach_to_download_rate * 
                             campaign.download_to_active_rate * 
                             campaign.active_to_subscriber_rate)
            
            # Calculate monthly user acquisition during campaign
            monthly_users = new_users / campaign.duration_months
            
            # Add users during campaign months
            campaign_period = range(
                campaign.start_month - 1,
                min(campaign.start_month - 1 + campaign.duration_months, len(df))
            )
            
            # Accumulate users during campaign
            for month in campaign_period:
                cumulative_campaign_users.iloc[month:] += monthly_users
        
        df['campaign_users'] = cumulative_campaign_users