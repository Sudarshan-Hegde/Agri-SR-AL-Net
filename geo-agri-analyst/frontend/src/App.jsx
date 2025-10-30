import React, { useState } from 'react'
import MapComponent from './components/MapComponent'
import ResultsPanel from './components/ResultsPanel'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  // State management
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [predictionData, setPredictionData] = useState(null)
  const [selectedPos, setSelectedPos] = useState(null) // [lat, lng]
  const [currentStep, setCurrentStep] = useState(0)

  // Handle map click - sets the selected position
  const handleMapClick = (latlng) => {
    setSelectedPos([latlng.lat, latlng.lng])
    setPredictionData(null) // Clear previous results
    setError(null)
    console.log('Selected position:', latlng.lat, latlng.lng)
  }

  // Handle analysis request
  const handleAnalyze = async () => {
    if (!selectedPos) {
      setError('Please select a location on the map first')
      return
    }

    setIsLoading(true)
    setError(null)
    setCurrentStep(0)

    try {
      // Simulate step-by-step progress
      const steps = [
        'Fetching live satellite imagery...',
        'Preprocessing satellite data...',
        'Enhancing image quality with AI...',
        'Running land classification model...',
        'Generating final analysis...'
      ]

      // Show progress updates
      for (let i = 0; i < steps.length; i++) {
        setCurrentStep(i)
        await new Promise(resolve => setTimeout(resolve, 800)) // Simulate processing time
      }

      // Make API call
      const response = await axios.post(`${API_BASE_URL}/api/v1/analyze`, {
        lat: selectedPos[0],
        lng: selectedPos[1]
      })

      setPredictionData(response.data)
      console.log('Analysis results:', response.data)
      
    } catch (err) {
      console.error('Analysis failed:', err)
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
    } finally {
      setIsLoading(false)
      setCurrentStep(0)
    }
  }

  // Clear results and selection
  const handleClear = () => {
    setSelectedPos(null)
    setPredictionData(null)
    setError(null)
    setIsLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      {/* Header */}
      <header className="bg-white shadow-lg border-b-4 border-agri-green">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-agri-green rounded-lg flex items-center justify-center">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Geo-Agri Analyst</h1>
                <p className="text-gray-600">AI-powered agricultural land classification</p>
              </div>
            </div>
            
            {selectedPos && (
              <button
                onClick={handleClear}
                className="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Clear Selection
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Instructions */}
        <div className="mb-6 bg-white rounded-lg shadow-md p-6 border-l-4 border-agri-blue">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">How to use:</h2>
          <ol className="text-gray-700 space-y-1">
            <li>1. Click anywhere on the map to select a location</li>
            <li>2. Click "Analyze this Area" to run AI analysis</li>
            <li>3. View the land classification results and enhanced imagery</li>
          </ol>
        </div>

        {/* Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Map Section */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-lg overflow-hidden">
              <div className="h-[600px]">
                <MapComponent
                  onMapClick={handleMapClick}
                  onAnalyze={handleAnalyze}
                  selectedPos={selectedPos}
                  isLoading={isLoading}
                />
              </div>
            </div>
          </div>

          {/* Results Section */}
          <div className="lg:col-span-1">
            <ResultsPanel
              isLoading={isLoading}
              error={error}
              predictionData={predictionData}
              currentStep={currentStep}
              selectedPos={selectedPos}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-12">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-gray-400">
            Powered by PyTorch • Super-Resolution + Classification • Satellite Imagery Analysis
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App