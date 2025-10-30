# Geo-Agri Analyst

AI-powered agricultural land classification using satellite imagery, super-resolution enhancement, and deep learning.

## 🌟 Features

- **Interactive Map Interface**: Click anywhere on the map to select locations for analysis
- **AI-Powered Classification**: Deep learning models classify land use into 10 categories
- **Super-Resolution Enhancement**: 4x image enhancement using RFB-ESRGAN architecture  
- **Real-time Processing**: Live satellite imagery analysis with step-by-step feedback
- **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PyTorch** - Deep learning models
- **Uvicorn** - ASGI server

### Frontend  
- **React** - UI framework
- **Vite** - Build tool
- **React Leaflet** - Interactive maps
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

### Models
- **SR Model**: RFBESRGANGenerator for 4x super-resolution (16x16 → 64x64)
- **Classification Model**: RobustClassifier for land use classification (10 classes)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your trained model weights:**
   ```
   backend/model_weights/
   ├── sr_model_final.pth      # Your trained super-resolution model
   └── clf_model_final.pth     # Your trained classification model
   ```

4. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173`

## 📁 Project Structure

```
geo-agri-analyst/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # PyTorch model definitions
│   │   └── ml_service.py        # ML pipeline service
│   ├── model_weights/           # Trained model files
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── MapComponent.jsx     # Interactive map
│   │   │   └── ResultsPanel.jsx     # Results display
│   │   ├── App.jsx              # Main application
│   │   ├── main.jsx             # Entry point
│   │   └── index.css            # Global styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md
```

## 🔧 API Endpoints

### Health Check
```
GET /
GET /api/v1/health
```

### Analysis
```
POST /api/v1/analyze
```
**Request Body:**
```json
{
  "lat": 40.7128,
  "lng": -74.0060
}
```

**Response:**
```json
{
  "land_class": "Arable Land",
  "confidence": 0.92,
  "before_image_b64": "base64_encoded_lr_image",
  "after_image_b64": "base64_encoded_sr_image",
  "processing_steps": ["step1", "step2", ...]
}
```

### Land Classes
```
GET /api/v1/classes
```

## 🎯 Land Use Classes

The model classifies land into 10 categories:

1. **Arable Land** - Cropland and agricultural fields
2. **Forest** - Wooded areas and tree coverage
3. **Grassland** - Natural grasslands and meadows
4. **Urban Area** - Cities, towns, and built-up areas
5. **Water Body** - Rivers, lakes, and water features
6. **Wetland** - Swamps, marshes, and wetland areas
7. **Barren Land** - Desert, rock, and bare soil
8. **Permanent Crops** - Orchards and permanent cultivation
9. **Pasture** - Livestock grazing areas
10. **Industrial Area** - Factories and industrial zones

## 🔮 Future Features (In Development)

- **Crop History Analysis**: Historical crop patterns and seasonal changes
- **Crop Recommendations**: Soil and weather-based crop suggestions
- **Real Sentinel Hub Integration**: Live satellite imagery from ESA Sentinel satellites
- **Multi-temporal Analysis**: Time-series land use change detection

## 🛠️ Development

### Adding Your Trained Models

1. Replace the placeholder model classes in `backend/app/models.py` with your actual `RFBESRGANGenerator` and `RobustClassifier` implementations

2. Place your trained model weights in `backend/model_weights/`:
   - `sr_model_final.pth` - Your super-resolution model
   - `clf_model_final.pth` - Your classification model

3. Update the class names in `CLF_Model.class_names` if different from the defaults

### Customization

- **Map Center**: Change `defaultCenter` in `MapComponent.jsx`
- **Styling**: Modify colors in `tailwind.config.js`
- **Processing Steps**: Update steps in `main.py` and `ResultsPanel.jsx`

## 📊 Model Requirements

### Super-Resolution Model
- **Input**: (B, 3, 16, 16) tensors
- **Output**: (B, 3, 64, 64) tensors  
- **Architecture**: RFB-ESRGAN based
- **Upscaling Factor**: 4x

### Classification Model  
- **Input**: (B, 3, 64, 64) tensors
- **Output**: (B, 10) logits
- **Architecture**: ResNet-like with SE blocks
- **Classes**: 10 land use categories

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **PyTorch** team for the deep learning framework
- **FastAPI** for the excellent web framework
- **React Leaflet** for map components
- **OpenStreetMap** for map tiles
- **Tailwind CSS** for styling utilities

---

**Built with ❤️ for sustainable agriculture and AI-powered environmental monitoring**