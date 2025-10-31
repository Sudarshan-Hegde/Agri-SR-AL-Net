import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Geo-Agri Analyst API", version="1.0.0")

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for coordinates
class Coords(BaseModel):
    lat: float
    lng: float

# Tiny placeholder images (1x1 pixels) as base64 strings
# Red 1x1 pixel for "before" image
IMG_LR_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhqsxYAAAAABJRU5ErkJggg=="

# Green 1x1 pixel for "after" image  
IMG_SR_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60eADgAAAABJRU5ErkJggg=="

@app.get("/")
async def root():
    return {"message": "Geo-Agri Analyst API - Fake Backend for Development"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "fake_backend"}

@app.post("/api/v1/analyze")
async def analyze_location(coords: Coords):
    """
    Fake backend endpoint that simulates satellite image analysis.
    
    Args:
        coords: Coordinates containing lat and lng
        
    Returns:
        Mock analysis results with hard-coded data
    """
    print(f"Received click at: {coords.lat}, {coords.lng}")
    
    # Simulate processing time (satellite fetch + model inference)
    time.sleep(2.5)
    
    # Return hard-coded mock response
    return {
        "land_class": "Arable Land (Mock Data)",
        "confidence": 0.92,
        "before_image_b64": IMG_LR_B64,
        "after_image_b64": IMG_SR_B64
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)