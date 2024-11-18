from pydantic import BaseModel, validator

class MarketingCampaign(BaseModel):
    name: str
    campaign_id: str
    start_month: int
    duration_months: int
    budget: float
    expected_reach: int
    reach_to_download_rate: float
    download_to_active_rate: float
    active_to_subscriber_rate: float
    
    @validator('start_month')
    def validate_start_month(cls, v):
        if not 1 <= v <= 12:
            raise ValueError("Start month must be between 1 and 12")
        return v
    
    @validator('duration_months')
    def validate_duration(cls, v):
        if not 1 <= v <= 12:
            raise ValueError("Duration must be between 1 and 12 months")
        return v 