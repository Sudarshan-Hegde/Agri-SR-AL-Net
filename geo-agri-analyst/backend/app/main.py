from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
import logging
from .ml_service import ModelService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Geo-Agri Analyst API",
    description="Agricultural land classification using satellite imagery and deep learning",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model service instance
ml_service: Optional[ModelService] = None


# Pydantic models for request/response
class AnalysisRequest(BaseModel):
    lat: float
    lng: float


class AnalysisResponse(BaseModel):
    land_class: str
    confidence: float
    before_image_b64: str
    after_image_b64: str
    processing_steps: list[str]


@app.on_event("startup")
async def startup_event():
    """Initialize the ML service on startup"""
    global ml_service
    try:
        logger.info("🚀 Starting Geo-Agri Analyst API...")
        logger.info("📦 Loading ML models...")
        ml_service = ModelService()
        logger.info("✅ ML models loaded successfully!")
    except Exception as e:
        logger.error(f"❌ Error initializing ML service: {e}")
        # Continue with a placeholder service for development
        ml_service = ModelService()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Geo-Agri Analyst API is running!",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/api/v1/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "ml_service_loaded": ml_service is not None,
        "models_available": {
            "sr_model": ml_service.sr_model is not None if ml_service else False,
            "clf_model": ml_service.clf_model is not None if ml_service else False
        }
    }


@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def analyze_location(request: AnalysisRequest):
    """
    Analyze satellite imagery for a given location
    
    Args:
        request: Contains latitude and longitude
    
    Returns:
        Analysis results including land class, confidence, and before/after images
    """
    try:
        logger.info(f"🌍 Analyzing location: {request.lat}, {request.lng}")
        
        if ml_service is None:
            raise HTTPException(status_code=503, detail="ML service not available")
        
        # Processing steps for frontend feedback
        processing_steps = [
            "Fetching live satellite imagery...",
            "Preprocessing satellite data...", 
            "Enhancing image quality with AI...",
            "Running land classification model...",
            "Generating final analysis..."
        ]
        
        # Simulate processing delay for better UX
        await asyncio.sleep(0.5)
        
        # TODO: 1. Call Sentinel Hub API with (lat, lng) to get real satellite image
        # For now, create a fake satellite image
        logger.info("📡 Fetching satellite imagery...")
        fake_satellite_image = ml_service.create_fake_satellite_image(64, 64)
        
        # TODO: 2. The real satellite image would be HR, we need to create LR version
        # For now, our fake image will be processed through the pipeline
        logger.info("🔍 Processing through ML pipeline...")
        
        # 3. Run the ML pipeline
        results = ml_service.run_pipeline(fake_satellite_image)
        
        logger.info(f"✅ Analysis complete: {results['land_class_name']} ({results['confidence_score']:.2%})")
        
        # 4. Return the results
        return AnalysisResponse(
            land_class=results["land_class_name"],
            confidence=results["confidence_score"],
            before_image_b64=results["lr_image_b64"],
            after_image_b64=results["sr_image_b64"],
            processing_steps=processing_steps
        )
        
    except Exception as e:
        logger.error(f"❌ Error during analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/api/v1/classes")
async def get_land_classes():
    """Get available land classification classes"""
    if ml_service is None or ml_service.clf_model is None:
        return {"classes": ["Arable Land", "Forest", "Grassland", "Urban Area", "Water Body"]}
    
    return {"classes": ml_service.clf_model.class_names}


# For development: if running this file directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )