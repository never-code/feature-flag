from pydantic import BaseModel, field_validator
from typing import List, Dict, Optional
from datetime import datetime

class FeatureFlagBase(BaseModel):
    name: str
    environment: Optional[str] = "prod"
    description: Optional[str] = None
    enabled: bool = False
    rollout_percentage: int = 0
    allowed_users: List[str] = []
    allowed_groups: List[str] = []
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    extra_metadata: Dict = {}

class FeatureFlagCreate(FeatureFlagBase):
    pass

class FeatureFlagUpdate(BaseModel):
    description: Optional[str] = None
    enabled: Optional[bool] = None
    rollout_percentage: Optional[int] = None
    allowed_users: Optional[List[str]] = None
    allowed_groups: Optional[List[str]] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    extra_metadata: Optional[Dict] = None

class FeatureFlagOut(FeatureFlagBase):
    id: int

    @field_validator("allowed_users", "allowed_groups", mode="before")
    def default_empty_list(cls, v):
        return v or []

    model_config = {
        "from_attributes": True
    }

