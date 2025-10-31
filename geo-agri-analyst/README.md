# 🌍 Geo-Agri Analyst

AI-powered agricultural land classification using satellite imagery and deep learning. This application allows users to click on a map, analyze satellite imagery, and get land use classifications with super-resolution image enhancement.

## 🚀 Features

- **Interactive Map**: Click anywhere to select a location for analysis
- **Satellite Imagery Analysis**: Fetches live satellite data for the selected coordinates  
- **AI-Powered Classification**: 2-stage PyTorch model pipeline:
  1. **Super-Resolution**: Enhances image quality from 30x30 to 120x120 pixels (4x upscaling)
  2. **Land Classification**: Classifies land use into 10 categories (Arable Land, Forest, Grassland, etc.)
- **Real-time Results**: View before/after images and classification confidence
- **Modern UI**: Built with React, Tailwind CSS, and Leaflet maps

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PyTorch** - Deep learning models for super-resolution and classification
- **Uvicorn** - ASGI server

### Frontend  
- **React** - User interface framework
- **Vite** - Build tool and dev server
- **React-Leaflet** - Interactive maps
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client for API calls

## 📋 Prerequisites

Before running this project, make sure you have:

- **Python 3.8+** installed
- **Node.js 16+** and **npm** installed
- **Git** (for cloning the repository)

## 🚀 How to Run (Development Mode)

### 1. Run the Backend (FastAPI)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a Python virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   
   **On Linux/macOS:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```

   ✅ **Backend server is now running on http://localhost:8000**

### 2. Run the Frontend (React)

1. **Open a new terminal and navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   ✅ **Frontend app is now running on http://localhost:5173**

## 🎯 How to Use

1. **Open your browser** and go to `http://localhost:5173`

2. **Click anywhere on the map** to drop a pin and select a location

3. **Click the "Analyze this Area" button** to start the analysis

4. **Wait for processing** - you'll see step-by-step status updates:
   - Fetching live satellite imagery...
   - Enhancing image quality...
   - Analyzing land class...

5. **View results** including:
   - Land classification (e.g., "Arable Land", "Forest", etc.)
   - Confidence score
   - Before/After images showing super-resolution enhancement
   - Placeholder sections for future features

## 📁 Project Structure

```
geo-agri-analyst/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app with fake backend
│   │   └── models.py            # Placeholder PyTorch models
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── MapComponent.jsx # Interactive Leaflet map
│   │   │   └── ResultsPanel.jsx # Results display component
│   │   ├── App.jsx              # Main React component
│   │   ├── index.css            # Tailwind CSS setup
│   │   └── main.jsx             # React entry point
│   ├── package.json             # Node.js dependencies
│   ├── tailwind.config.js       # Tailwind configuration
│   ├── postcss.config.js        # PostCSS configuration
│   └── vite.config.js           # Vite configuration
└── README.md                    # This file
```

## 🔧 Development Notes

### Current Status: Fake Backend Mode

This version uses a **fake backend** that:
- Accepts coordinates from the frontend
- Simulates processing time with `time.sleep(2.5)`
- Returns hard-coded mock data for development
- Uses tiny 1x1 pixel placeholder images

### Future Development

The application is designed to easily transition to a real backend that will:
- Fetch actual satellite imagery from APIs (e.g., Sentinel Hub)
- Load trained PyTorch models for super-resolution and classification
- Process real satellite data through the ML pipeline
- Return actual enhanced images and classification results

### API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status  
- `POST /api/v1/analyze` - Analyze coordinates (accepts `{lat: float, lng: float}`)

## 🐛 Troubleshooting

### Backend Issues

**"Module not found" errors:**
- Make sure you're in the virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**Port 8000 already in use:**
- Change the port: `uvicorn app.main:app --reload --port 8001`
- Update the frontend API URL in `App.jsx` accordingly

### Frontend Issues

**Dependencies installation fails:**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Try using `npm install --legacy-peer-deps` for React compatibility

**Map not loading:**
- Check browser console for errors
- Ensure Leaflet CSS is imported correctly
- Verify internet connection for map tiles

## 📄 License

This project is for educational and research purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Happy Analyzing! 🌱🛰️**