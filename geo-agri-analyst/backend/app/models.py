from pydantic import BaseModel
from typing import List, Optional

# Pydantic models for API
class Coords(BaseModel):
    lat: float
    lng: float

class AnalysisRequest(BaseModel):
    type: str  # 'point' or 'polygon'
    lat: Optional[float] = None
    lng: Optional[float] = None
    points: Optional[List[List[float]]] = None  # For polygon points [[lat, lng], ...]

class PredictionResponse(BaseModel):
    land_class: str
    confidence: float
    before_image_b64: str
    after_image_b64: str
    analysis_type: str
    area_info: Optional[dict] = None

# Note: In the real implementation, you would have PyTorch models here:
# - RFBESRGANGenerator for super-resolution (16x16 -> 64x64)
# - RobustClassifier for land classification (10 classes)
# 
# For now, we're using a fake backend that returns mock data
# without actually loading or running any ML models.