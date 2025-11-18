# Enhanced Polygon Analysis - Quick Start Guide

## ✨ What's New

Your Geo-Agri Analyst now features **advanced multi-image polygon analysis**:
- 🔍 Intelligent grid-based sampling across polygon areas
- 📊 Comprehensive land type distribution analysis
- 🎯 Adaptive zoom levels based on area size
- 📈 Aggregated predictions with confidence metrics

## 🚀 Getting Started

### 1. Install Dependencies

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start the Server

```bash
# Option 1: Using the helper script
cd backend
source venv/bin/activate
./run_server.sh

# Option 2: Direct command
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Test the API

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Point Analysis:**
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "type": "point",
    "lat": 40.7128,
    "lng": -74.0060
  }'
```

**Polygon Analysis:**
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "type": "polygon",
    "points": [
      [40.7128, -74.0060],
      [40.7138, -74.0050],
      [40.7135, -74.0040],
      [40.7125, -74.0045]
    ]
  }'
```

## 📖 How It Works

### Point Analysis
- Uses **zoom level 15** (~150m coverage)
- Fetches single satellite image
- Returns classification with confidence

### Polygon Analysis
1. **Area Calculation**: Estimates polygon area in km²
2. **Zoom Selection**: Chooses optimal zoom based on area size
3. **Grid Sampling**: Generates 5-50 sample points across polygon
4. **Batch Processing**: Fetches and analyzes satellite image for each sample
5. **Aggregation**: Combines results into comprehensive breakdown

### Zoom Level Strategy

| Polygon Area | Zoom Level | Image Coverage | Samples |
|-------------|------------|----------------|---------|
| < 1 hectare | 17 | ~40m × 40m | 5-10 |
| 1-10 hectares | 16 | ~80m × 80m | 10-15 |
| 10-100 hectares | 15 | ~150m × 150m | 15-30 |
| > 100 hectares | 14 | ~300m × 300m | 30-50 |

## 📊 Response Format

### Polygon Analysis Response
```json
{
  "land_class": "Non-irrigated arable land",
  "confidence": 0.87,
  "analysis_type": "polygon",
  "zoom_level_used": 16,
  "area_info": {
    "estimated_area_hectares": 15.3,
    "estimated_area_km2": 0.153,
    "sample_count": 23,
    "class_distribution": {
      "Non-irrigated arable land": {
        "percentage": 65.22,
        "count": 15,
        "avg_confidence": 0.87
      },
      "Pastures": {
        "percentage": 26.09,
        "count": 6,
        "avg_confidence": 0.72
      }
    }
  },
  "weather_data": { ... },
  "detailed_samples": [ ... ]
}
```

## 🧪 Testing

Run the polygon utilities test:
```bash
cd backend
source venv/bin/activate
python test_polygon_utils.py
```

## 🔧 Configuration

### Environment Variables (Optional)

Create `.env` file in `backend/` directory:
```env
# HuggingFace Token (for private spaces)
HF_TOKEN=your_token_here

# Mapbox API Token (for satellite imagery)
MAPBOX_TOKEN=your_mapbox_token
```

### Adjust Sampling Parameters

In `app/polygon_utils.py`, modify `generate_grid_samples()`:
```python
sample_coords = generate_grid_samples(
    points, 
    max_samples=50,  # Maximum number of samples
    min_samples=5    # Minimum number of samples
)
```

## 📝 API Endpoints

### `/` - Root
- **Method**: GET
- **Returns**: API information

### `/health` - Health Check
- **Method**: GET
- **Returns**: Service status

### `/api/v1/weather` - Weather Data
- **Method**: POST
- **Body**: `{"lat": float, "lng": float}`
- **Returns**: Agricultural climate data

### `/api/v1/analyze` - Main Analysis
- **Method**: POST
- **Body**: Point or Polygon request
- **Returns**: Comprehensive analysis results

## 🎯 Use Cases

### Small Farm Plot Analysis
```json
{
  "type": "polygon",
  "points": [[lat1, lng1], [lat2, lng2], ...]
}
```
**Result**: High-detail analysis with 5-15 samples

### Large Agricultural Area
```json
{
  "type": "polygon",
  "points": [[lat1, lng1], [lat2, lng2], ...]
}
```
**Result**: Wide-coverage analysis with 30-50 samples

### Quick Point Check
```json
{
  "type": "point",
  "lat": 40.7128,
  "lng": -74.0060
}
```
**Result**: Single-point classification

## ⚡ Performance Tips

1. **For large polygons**: Processing may take 1-2 minutes due to multiple image fetches
2. **HuggingFace Space**: First request may be slow (cold start) - subsequent requests are faster
3. **Satellite Images**: Uses free tier APIs (ArcGIS, OSM) - rate limits may apply

## 🐛 Troubleshooting

**Server won't start:**
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill existing process
kill -9 <PID>
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Shapely errors:**
```bash
# Reinstall shapely
pip uninstall shapely
pip install shapely>=2.0.0
```

## 📚 Documentation

- Full feature documentation: `POLYGON_ANALYSIS_FEATURES.md`
- API documentation: Visit `http://localhost:8000/docs` when server is running
- Original README: `../README.md`

## 🎉 Summary

Your backend now supports:
- ✅ Multi-image polygon analysis with grid sampling
- ✅ Adaptive zoom levels based on area size
- ✅ Comprehensive land type distribution breakdown
- ✅ Batch prediction processing with progress tracking
- ✅ Configurable sampling parameters
- ✅ Enhanced response format with detailed statistics

**Ready to analyze agricultural land at scale!** 🌾🛰️📊
