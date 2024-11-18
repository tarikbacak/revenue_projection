from pydantic import BaseModel, validator
from typing import List

class SubscriptionTier(BaseModel):
    name: str
    monthly_price: float
    features: List[str]
    distribution_percentage: float
    
    @validator('monthly_price')
    def validate_price(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("Price must be between 0 and 100")
        return v
    
    @validator('distribution_percentage')
    def validate_distribution(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("Distribution must be between 0 and 1")
        return v 