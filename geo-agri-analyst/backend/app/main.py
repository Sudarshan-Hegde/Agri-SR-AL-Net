import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Union
import uvicorn
from .weather_service import get_agricultural_climate_summary

app = FastAPI(title="Geo-Agri Analyst API", version="1.0.0")

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for coordinates
class Coords(BaseModel):
    lat: float
    lng: float

class AnalysisRequest(BaseModel):
    type: str  # 'point' or 'polygon'
    lat: Optional[float] = None
    lng: Optional[float] = None
    points: Optional[List[List[float]]] = None  # For polygon points [[lat, lng], ...]

# Tiny placeholder images (1x1 pixels) as base64 strings
# Red 1x1 pixel for "before" image
IMG_LR_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhqsxYAAAAABJRU5ErkJggg=="

# Green 1x1 pixel for "after" image  
IMG_SR_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60eADgAAAABJRU5ErkJggg=="

@app.get("/")
async def root():
    return {"message": "Geo-Agri Analyst API - Enhanced with Live Weather Data", "version": "2.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "live_backend_with_weather"}

@app.post("/api/v1/weather")
async def get_weather_data(coords: Coords):
    """
    Dedicated endpoint for fetching weather/climate data.
    
    Args:
        coords: Coordinates object with lat and lng
        
    Returns:
        Agricultural climate analysis data
    """
    try:
        weather_data = await get_agricultural_climate_summary(coords.lat, coords.lng)
        if weather_data:
            return {
                "status": "success",
                "coordinates": {"lat": coords.lat, "lng": coords.lng},
                "data": weather_data
            }
        else:
            return {
                "status": "error",
                "message": "Unable to fetch weather data for the specified coordinates",
                "coordinates": {"lat": coords.lat, "lng": coords.lng}
            }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Weather service error: {str(e)}",
            "coordinates": {"lat": coords.lat, "lng": coords.lng}
        }

@app.post("/api/v1/analyze")
async def analyze_location(request: Union[Coords, AnalysisRequest]):
    """
    Enhanced analysis endpoint that combines satellite image analysis with weather/climate data.
    Supports both point and polygon analysis.
    
    Args:
        request: Either Coords (for backward compatibility) or AnalysisRequest
        
    Returns:
        Comprehensive analysis results including land classification and climate data
    """
    
    # Handle both old Coords format and new AnalysisRequest format
    if hasattr(request, 'type'):
        # New AnalysisRequest format
        analysis_type = request.type
        lat, lng = request.lat, request.lng
        points = request.points
        
        if analysis_type == "polygon" and points:
            num_points = len(points)
            print(f"Received polygon analysis with {num_points} points")
            # Calculate area (simplified)
            if num_points >= 3:
                print(f"Polygon points: {points}")
                # For polygon analysis, use centroid coordinates for weather data
                if lat is None or lng is None:
                    # Calculate centroid if not provided
                    lat = sum(point[0] for point in points) / len(points)
                    lng = sum(point[1] for point in points) / len(points)
        else:
            print(f"Received point analysis at: {lat}, {lng}")
    else:
        # Old Coords format (backward compatibility)
        analysis_type = "point"
        lat, lng = request.lat, request.lng
        points = None
        print(f"Received point analysis at: {lat}, {lng}")
    
    # Simulate processing delay for land classification
    time.sleep(1.0)  # Reduced delay since we're now making real API calls
    
    # Generate land classification results
    land_classes = ["Farmland", "Forest", "Urban", "Water Body", "Grassland", "Desert", "Industrial"]
    selected_class = land_classes[hash(f"{lat}{lng}") % len(land_classes)]
    confidence = 0.85 + (hash(f"{lat}{lng}") % 15) / 100  # Between 0.85-0.99
    
    # Fetch real weather/climate data
    weather_data = None
    try:
        print(f"Fetching weather data for coordinates: {lat}, {lng}")
        weather_data = await get_agricultural_climate_summary(lat, lng)
        if weather_data:
            print("Successfully retrieved weather data")
        else:
            print("No weather data returned")
    except Exception as e:
        print(f"Error fetching weather data: {str(e)}")
        # Weather data is optional, continue with analysis even if it fails
    
    # Additional info for polygon analysis
    area_info = None
    if analysis_type == "polygon" and points:
        area_info = {
            "total_points": len(points),
            "estimated_area_hectares": len(points) * 2.5,  # Fake calculation
            "perimeter_km": len(points) * 0.8,
            "dominant_land_type": selected_class,
            "centroid_coordinates": {"lat": lat, "lng": lng}
        }
    
    # Combine results
    result = {
        "land_class": selected_class,
        "confidence": confidence,
        "before_image_b64": IMG_LR_B64,
        "after_image_b64": IMG_SR_B64,
        "analysis_type": analysis_type,
        "coordinates": {"lat": lat, "lng": lng},
        "area_info": area_info,
        "weather_data": weather_data  # Include weather data in response
    }
    
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)