from pydantic import BaseModel
from typing import List

class EvaluateRequest(BaseModel):
    flag_name: str
    user_id: str
    groups: List[str] = []

class EvaluateResponse(BaseModel):
    enabled: bool
    reason: str

