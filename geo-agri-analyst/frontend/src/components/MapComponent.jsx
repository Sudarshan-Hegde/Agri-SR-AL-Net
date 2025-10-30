import React from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet'
import L from 'leaflet'

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

// Custom marker for selected location
const selectedLocationIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
})

// Component to handle map click events
function MapClickHandler({ onMapClick }) {
  useMapEvents({
    click: (e) => {
      onMapClick(e.latlng)
    }
  })
  return null
}

// Analyze button component (positioned on the map)
function AnalyzeButton({ onAnalyze, isLoading, selectedPos }) {
  if (!selectedPos) return null

  return (
    <div className="absolute top-4 right-4 z-[1000]">
      <button
        onClick={onAnalyze}
        disabled={isLoading}
        className={`px-6 py-3 rounded-lg font-semibold text-white shadow-lg transition-all duration-200 ${
          isLoading
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-agri-green hover:bg-green-600 hover:scale-105 active:scale-95'
        }`}
      >
        {isLoading ? (
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <span>Analyzing...</span>
          </div>
        ) : (
          <div className="flex items-center space-x-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <span>Analyze this Area</span>
          </div>
        )}
      </button>
    </div>
  )
}

function MapComponent({ onMapClick, onAnalyze, selectedPos, isLoading }) {
  // Default center (can be changed to your preferred location)
  const defaultCenter = [40.7128, -74.0060] // New York City
  const defaultZoom = 10

  return (
    <div className="relative h-full w-full">
      <MapContainer
        center={defaultCenter}
        zoom={defaultZoom}
        className="h-full w-full"
        zoomControl={true}
        scrollWheelZoom={true}
      >
        {/* Base map tiles */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {/* Satellite imagery option (uncomment to use) */}
        {/*
        <TileLayer
          attribution='&copy; <a href="https://www.esri.com/">Esri</a>'
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        />
        */}

        {/* Click handler */}
        <MapClickHandler onMapClick={onMapClick} />

        {/* Selected location marker */}
        {selectedPos && (
          <Marker 
            position={selectedPos} 
            icon={selectedLocationIcon}
          >
            <Popup>
              <div className="text-center">
                <h3 className="font-semibold text-gray-900">Selected Location</h3>
                <p className="text-sm text-gray-600">
                  Lat: {selectedPos[0].toFixed(6)}<br/>
                  Lng: {selectedPos[1].toFixed(6)}
                </p>
                <button
                  onClick={onAnalyze}
                  disabled={isLoading}
                  className="mt-2 px-4 py-2 bg-agri-green text-white text-sm rounded hover:bg-green-600 disabled:bg-gray-400"
                >
                  {isLoading ? 'Analyzing...' : 'Analyze Area'}
                </button>
              </div>
            </Popup>
          </Marker>
        )}
      </MapContainer>

      {/* Analyze button overlay */}
      <AnalyzeButton 
        onAnalyze={onAnalyze} 
        isLoading={isLoading} 
        selectedPos={selectedPos} 
      />

      {/* Map instructions overlay */}
      {!selectedPos && (
        <div className="absolute bottom-4 left-4 z-[1000] bg-white bg-opacity-90 rounded-lg p-3 shadow-lg">
          <p className="text-sm text-gray-700 flex items-center">
            <svg className="w-4 h-4 mr-2 text-agri-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Click anywhere on the map to select a location
          </p>
        </div>
      )}

      {/* Loading overlay */}
      {isLoading && (
        <div className="absolute inset-0 bg-black bg-opacity-20 z-[1001] flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 shadow-xl">
            <div className="flex items-center space-x-3">
              <div className="w-6 h-6 border-3 border-agri-green border-t-transparent rounded-full animate-spin"></div>
              <span className="text-gray-700 font-medium">Processing satellite imagery...</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default MapComponent