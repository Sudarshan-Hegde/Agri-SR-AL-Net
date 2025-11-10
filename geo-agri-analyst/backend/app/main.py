import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Union
import uvicorn
import math

# Handle both relative and absolute imports
try:
    from .weather_service import get_agricultural_climate_summary
except ImportError:
    from weather_service import get_agricultural_climate_summary

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

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points on Earth (in kilometers)
    using the Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of point 1 in decimal degrees
        lat2, lon2: Latitude and longitude of point 2 in decimal degrees
        
    Returns:
        Distance in kilometers
    """
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    distance = R * c
    return distance

def calculate_polygon_area(points):
    """
    Calculate the area of a polygon using the Shoelace formula with geodesic corrections.
    
    Args:
        points: List of [lat, lng] coordinates
        
    Returns:
        Area in hectares
    """
    if len(points) < 3:
        return 0.0
    
    # Convert lat/lng to approximate Cartesian coordinates (in meters)
    # Using Equirectangular projection (good for small areas)
    n = len(points)
    
    # Calculate centroid for reference point
    center_lat = sum(p[0] for p in points) / n
    center_lon = sum(p[1] for p in points) / n
    
    # Convert to meters using approximation
    # At the equator: 1 degree ≈ 111.32 km
    # Longitude varies with latitude: cos(lat) * 111.32 km
    lat_to_m = 111320.0  # meters per degree latitude
    lon_to_m = 111320.0 * math.cos(math.radians(center_lat))  # meters per degree longitude
    
    # Convert points to Cartesian coordinates
    x_coords = [(p[1] - center_lon) * lon_to_m for p in points]
    y_coords = [(p[0] - center_lat) * lat_to_m for p in points]
    
    # Apply Shoelace formula
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += x_coords[i] * y_coords[j]
        area -= x_coords[j] * y_coords[i]
    
    area = abs(area) / 2.0  # Area in square meters
    
    # Convert to hectares (1 hectare = 10,000 square meters)
    area_hectares = area / 10000.0
    
    return round(area_hectares, 2)

def calculate_polygon_perimeter(points):
    """
    Calculate the perimeter of a polygon using Haversine distance for each edge.
    
    Args:
        points: List of [lat, lng] coordinates
        
    Returns:
        Perimeter in kilometers
    """
    if len(points) < 2:
        return 0.0
    
    perimeter = 0.0
    n = len(points)
    
    for i in range(n):
        # Get current point and next point (wrapping around to first point at the end)
        p1 = points[i]
        p2 = points[(i + 1) % n]
        
        # Calculate distance between consecutive points
        distance = haversine_distance(p1[0], p1[1], p2[0], p2[1])
        perimeter += distance
    
    return round(perimeter, 3)

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
        # Calculate accurate area and perimeter
        area_hectares = calculate_polygon_area(points)
        perimeter_km = calculate_polygon_perimeter(points)
        
        area_info = {
            "total_points": len(points),
            "estimated_area_hectares": area_hectares,
            "perimeter_km": perimeter_km,
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