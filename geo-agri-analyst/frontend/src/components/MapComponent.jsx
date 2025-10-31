import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

// Custom glowing marker for selected location
const createGlowingIcon = () => {
  return L.divIcon({
    className: 'custom-div-icon',
    html: `
      <div style="
        position: relative;
        width: 30px;
        height: 30px;
      ">
        <div style="
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 20px;
          height: 20px;
          background: linear-gradient(135deg, #3b82f6, #10b981);
          border-radius: 50%;
          box-shadow: 
            0 0 20px rgba(59, 130, 246, 0.6),
            0 0 40px rgba(59, 130, 246, 0.3),
            inset 0 2px 4px rgba(255, 255, 255, 0.3);
          animation: pulse-glow 2s ease-in-out infinite;
        "></div>
        <div style="
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 8px;
          height: 8px;
          background: white;
          border-radius: 50%;
          box-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
        "></div>
      </div>
    `,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
    popupAnchor: [0, -15],
  })
}

// Component to handle map clicks
function MapClickHandler({ setSelectedPos }) {
  useMapEvents({
    click: (e) => {
      setSelectedPos({ lat: e.latlng.lat, lng: e.latlng.lng })
    }
  })
  return null
}

// Floating analyze button with glassmorphism
function AnalyzeButton({ onAnalyze, isLoading, selectedPos }) {
  if (!selectedPos) return null

  return (
    <div className="absolute top-16 right-4 lg:top-20 lg:right-6 z-[1000]">
      <button
        onClick={onAnalyze}
        disabled={isLoading}
        className={`glass-button text-white font-semibold py-2 px-4 lg:py-3 lg:px-6 rounded-lg lg:rounded-xl text-sm lg:text-base transition-all duration-300 ${
          isLoading 
            ? 'opacity-50 cursor-not-allowed'
            : 'hover:scale-105 hover:glow-blue'
        }`}
      >
        {isLoading ? (
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 lg:w-5 lg:h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <span>Analyzing...</span>
          </div>
        ) : (
          <div className="flex items-center space-x-2">
            <span>🔍</span>
            <span>Analyze Area</span>
          </div>
        )}
      </button>
    </div>
  )
}

// Instructions overlay
function MapInstructions({ selectedPos }) {
  if (selectedPos) return null

  return (
    <div className="absolute bottom-4 left-4 lg:bottom-6 lg:left-6 z-[1000] glass rounded-lg lg:rounded-xl p-3 lg:p-4 max-w-xs">
      <div className="flex items-center space-x-2 lg:space-x-3">
        <div className="w-6 h-6 lg:w-8 lg:h-8 bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full flex items-center justify-center">
          <span className="text-white text-xs lg:text-sm">💡</span>
        </div>
        <div>
          <p className="text-white font-medium text-xs lg:text-sm">Click anywhere on the map</p>
          <p className="text-gray-300 text-xs">to select a location for analysis</p>
        </div>
      </div>
    </div>
  )
}

function MapComponent({ selectedPos, setSelectedPos, onAnalyze, isLoading }) {
  return (
    <div className="relative h-full w-full min-h-[400px] sm:min-h-[500px] lg:min-h-[600px]">
      <MapContainer 
        center={[40.7128, -74.0060]} // NYC default
        zoom={6}
        style={{ height: '100%', width: '100%' }}
        className="w-full h-full"
        attributionControl={false}
      >
        {/* Dark theme tile layer */}
        <TileLayer
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
          attribution='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        />
        
        <MapClickHandler setSelectedPos={setSelectedPos} />
        
        {selectedPos && (
          <Marker position={[selectedPos.lat, selectedPos.lng]} icon={createGlowingIcon()}>
            <Popup
              className="dark-popup"
              closeButton={false}
            >
              <div className="text-center p-2">
                <div className="mb-3">
                  <h3 className="text-white font-semibold mb-2">📍 Selected Location</h3>
                  <div className="text-gray-300 text-sm space-y-1">
                    <p><strong>Lat:</strong> {selectedPos.lat.toFixed(6)}</p>
                    <p><strong>Lng:</strong> {selectedPos.lng.toFixed(6)}</p>
                  </div>
                </div>
                <button
                  onClick={onAnalyze}
                  disabled={isLoading}
                  className="glass-button text-white text-sm font-medium py-2 px-4 rounded-lg transition-all duration-300 hover:scale-105"
                >
                  {isLoading ? (
                    <div className="flex items-center space-x-2">
                      <div className="w-3 h-3 border border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Analyzing...</span>
                    </div>
                  ) : (
                    'Analyze this Location'
                  )}
                </button>
              </div>
            </Popup>
          </Marker>
        )}
      </MapContainer>

      {/* Overlays */}
      <AnalyzeButton onAnalyze={onAnalyze} isLoading={isLoading} selectedPos={selectedPos} />
      <MapInstructions selectedPos={selectedPos} />
      
      {/* Loading overlay */}
      {isLoading && (
        <div className="absolute inset-0 bg-black bg-opacity-50 z-[1001] flex items-center justify-center">
          <div className="glass rounded-xl lg:rounded-2xl p-6 lg:p-8 text-center">
            <div className="w-10 h-10 lg:w-12 lg:h-12 border-3 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-3 lg:mb-4"></div>
            <p className="text-white font-medium text-sm lg:text-base">Processing satellite imagery...</p>
            <p className="text-gray-300 text-xs lg:text-sm mt-1">This may take a few moments</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default MapComponent