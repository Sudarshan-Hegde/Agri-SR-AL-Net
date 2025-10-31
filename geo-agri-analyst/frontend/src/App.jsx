import { useState } from 'react'
import axios from 'axios'
import MapComponent from './components/MapComponent'
import ResultsPanel from './components/ResultsPanel'

function App() {
  // State management
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [predictionData, setPredictionData] = useState(null)
  const [selectedPos, setSelectedPos] = useState(null)

  // Handle analysis request
  const handleAnalyze = async () => {
    if (!selectedPos) {
      setError('Please select a location on the map first')
      return
    }

    setIsLoading(true)
    setError(null)
    setPredictionData(null)

    try {
      const response = await axios.post('http://localhost:8000/api/v1/analyze', {
        lat: selectedPos.lat,
        lng: selectedPos.lng
      })
      
      setPredictionData(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed: Could not retrieve satellite data')
    } finally {
      setIsLoading(false)
    }
  }

  // Reset all states
  const handleReset = () => {
    setIsLoading(false)
    setError(null)
    setPredictionData(null)
    setSelectedPos(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white">
      {/* Animated background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gray-800 rounded-full opacity-3 animate-pulse-glow"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gray-700 rounded-full opacity-3 animate-float"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gray-900 rounded-full opacity-2 animate-pulse-glow"></div>
      </div>

      {/* Floating Glossy Navbar */}
      <nav className="fixed top-4 left-4 right-4 z-50 glass rounded-xl lg:rounded-2xl border border-white/10 shadow-[0_8px_32px_rgba(0,0,0,0.3)]">
        <div className="w-full px-4 sm:px-6 lg:px-8 py-3 lg:py-4">
          <div className="flex items-center justify-between">
            {/* Logo and Brand */}
            <div className="flex items-center space-x-2 lg:space-x-3">
              <div className="w-8 h-8 lg:w-10 lg:h-10 bg-gradient-to-r from-emerald-500 to-blue-500 rounded-full flex items-center justify-center shadow-[0_0_20px_rgba(16,185,129,0.3)]">
                <span className="text-white text-lg lg:text-xl font-bold">🌍</span>
              </div>
              <div>
                <h1 className="text-lg lg:text-xl font-bold gradient-text">Geo-Agri Analyst</h1>
                <p className="text-xs text-gray-400 hidden sm:block">AI-Powered Agriculture</p>
              </div>
            </div>

            {/* Navigation Links */}
            <div className="hidden lg:flex items-center space-x-4 xl:space-x-6">
              <a href="#" className="glass-button px-3 py-2 xl:px-4 xl:py-2 rounded-lg text-white hover:text-emerald-400 transition-colors duration-300 flex items-center space-x-2">
                <span>🗺️</span>
                <span className="text-sm">Map</span>
              </a>
              <a href="#" className="glass-button px-3 py-2 xl:px-4 xl:py-2 rounded-lg text-white hover:text-blue-400 transition-colors duration-300 flex items-center space-x-2">
                <span>📊</span>
                <span className="text-sm">Analytics</span>
              </a>
              <a href="#" className="glass-button px-3 py-2 xl:px-4 xl:py-2 rounded-lg text-white hover:text-purple-400 transition-colors duration-300 flex items-center space-x-2">
                <span>🌾</span>
                <span className="text-sm">Crops</span>
              </a>
              <a href="#" className="glass-button px-3 py-2 xl:px-4 xl:py-2 rounded-lg text-white hover:text-orange-400 transition-colors duration-300 flex items-center space-x-2">
                <span>⚙️</span>
                <span className="text-sm">Settings</span>
              </a>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center space-x-2 lg:space-x-3">
              {/* Status Indicator */}
              <div className="hidden md:flex items-center space-x-2 glass px-2 py-1 lg:px-3 lg:py-2 rounded-lg">
                <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse shadow-[0_0_10px_rgba(16,185,129,0.5)]"></div>
                <span className="text-xs text-gray-300">AI Ready</span>
              </div>
              
              {/* Mobile Menu Button */}
              <button className="lg:hidden glass-button p-2 rounded-lg text-white hover:text-emerald-400 transition-colors duration-300">
                <span className="text-lg">☰</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="relative z-10 w-full px-4 sm:px-6 lg:px-8 py-4 pt-24 lg:pt-28">
        {/* Main content - Responsive grid layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 xl:grid-cols-4 gap-4 lg:gap-6 min-h-[calc(100vh-140px)]">
          {/* Map Section - Responsive sizing */}
          <div className="lg:col-span-2 xl:col-span-3 glass-card rounded-xl lg:rounded-2xl overflow-hidden hover:shadow-2xl transition-all duration-500">
            {/* Map Header - Compact */}
            <div className="absolute top-0 left-0 right-0 z-[999] bg-black/20 backdrop-blur-sm border-b border-white/10">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-3 lg:p-4 gap-2 sm:gap-0">
                <div className="flex items-center space-x-2 lg:space-x-3">
                  <div className="w-2 h-2 lg:w-3 lg:h-3 bg-emerald-400 rounded-full animate-pulse"></div>
                  <h2 className="text-lg lg:text-xl font-bold text-white">Interactive Map</h2>
                </div>
                <div className="text-xs lg:text-sm text-gray-400 glass px-2 lg:px-3 py-1 rounded-full">
                  Click anywhere to analyze
                </div>
              </div>
            </div>
            
            {/* Full-size Map */}
            <div className="w-full h-full">
              <MapComponent 
                selectedPos={selectedPos}
                setSelectedPos={setSelectedPos}
                onAnalyze={handleAnalyze}
                isLoading={isLoading}
              />
            </div>
          </div>

          {/* Results Section - Takes 1/4 of the screen */}
                    {/* Results Section - Responsive sizing */}
          <div className="lg:col-span-1 xl:col-span-1 space-y-4 lg:space-y-6">
            {/* Analysis Controls */}
            <div className="glass-card rounded-xl lg:rounded-2xl p-4 lg:p-6">
              <div className="flex items-center space-x-3 mb-4 lg:mb-6">
                <div className="w-3 h-3 bg-blue-400 rounded-full animate-pulse"></div>
                <h3 className="text-lg lg:text-xl font-bold text-white">Analysis Control</h3>
              </div>
              
              <div className="space-y-3 lg:space-y-4">
                {selectedPos && (
                  <div className="glass rounded-lg p-3 lg:p-4">
                    <p className="text-xs lg:text-sm text-gray-400 mb-1">Selected Location</p>
                    <p className="text-sm lg:text-base text-white font-mono">
                      {selectedPos.lat.toFixed(4)}, {selectedPos.lng.toFixed(4)}
                    </p>
                  </div>
                )}
                
                <button
                  onClick={handleAnalyze}
                  disabled={!selectedPos || isLoading}
                  className="w-full glass-button bg-gradient-to-r from-emerald-500 to-blue-500 hover:from-emerald-600 hover:to-blue-600 text-white font-bold py-3 lg:py-4 px-4 lg:px-6 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-[0_0_20px_rgba(16,185,129,0.3)] hover:shadow-[0_0_30px_rgba(16,185,129,0.5)] text-sm lg:text-base"
                >
                  {isLoading ? (
                    <div className="flex items-center justify-center space-x-2">
                      <div className="w-4 h-4 lg:w-5 lg:h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Analyzing...</span>
                    </div>
                  ) : (
                    <div className="flex items-center justify-center space-x-2">
                      <span>�</span>
                      <span>Start Analysis</span>
                    </div>
                  )}
                </button>
              </div>
            </div>

            {/* Results Panel */}
            <div className="glass-card rounded-xl lg:rounded-2xl p-4 lg:p-6 flex-1 overflow-y-auto max-h-[calc(100vh-400px)] lg:max-h-[calc(100vh-300px)]">
              <ResultsPanel 
                isLoading={isLoading}
                error={error}
                data={predictionData}
              />
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 glass rounded-xl p-4 lg:p-6">
          <div className="flex flex-col lg:flex-row items-center justify-between text-xs lg:text-sm text-gray-400 gap-4">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
                <span>Backend: Ready</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                <span>Map: Interactive</span>
              </div>
            </div>
            <div className="text-xs text-center lg:text-right">
              Powered by PyTorch • Super-Resolution + Classification • Satellite Analysis
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App