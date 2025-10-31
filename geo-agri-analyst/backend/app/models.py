from pydantic import BaseModel

# Pydantic models for API
class Coords(BaseModel):
    lat: float
    lng: float

# Note: In the real implementation, you would have PyTorch models here:
# - RFBESRGANGenerator for super-resolution (16x16 -> 64x64)
# - RobustClassifier for land classification (10 classes)
# 
# For now, we're using a fake backend that returns mock data
# without actually loading or running any ML models.