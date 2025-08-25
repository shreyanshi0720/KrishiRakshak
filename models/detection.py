from pydantic import BaseModel
from datetime import datetime

class DetectionResponse(BaseModel):
    id: int
    user_id: int
    plant_type: str
    disease_name: str
    confidence: float
    treatment_advice: str
    detected_at: datetime

    class Config:
        from_attributes = True

class DetectionRequest(BaseModel):
    plant_type: str
    user_id: int