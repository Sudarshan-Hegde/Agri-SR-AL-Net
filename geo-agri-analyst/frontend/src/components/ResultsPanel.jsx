import { useState, useEffect } from 'react'

function ResultsPanel({ isLoading, error, data }) {
  const [currentStep, setCurrentStep] = useState(0)
  
  const steps = [
    "Fetching satellite imagery...",
    "Enhancing image quality...", 
    "Analyzing land classification..."
  ]

  // Show step-by-step loading messages
  useEffect(() => {
    if (isLoading) {
      setCurrentStep(0)
      const interval = setInterval(() => {
        setCurrentStep(prev => {
          if (prev < steps.length - 1) {
            return prev + 1
          }
          return 0 // Loop back to start
        })
      }, 800)
      
      return () => clearInterval(interval)
    }
  }, [isLoading])

  // Loading state
  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-4 relative">
            <div className="absolute inset-0 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            <div className="absolute inset-2 border-2 border-emerald-500 border-b-transparent rounded-full animate-spin" style={{animationDirection: 'reverse'}}></div>
          </div>
          <p className="text-white font-semibold text-lg mb-2">Processing Analysis</p>
          <p className="text-blue-400 font-medium animate-pulse">{steps[currentStep]}</p>
        </div>
        
        <div className="glass rounded-xl p-4">
          <div className="space-y-3">
            {steps.map((step, index) => (
              <div key={index} className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full transition-all duration-300 ${
                  index < currentStep 
                    ? 'bg-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.5)]'
                    : index === currentStep 
                      ? 'bg-blue-400 animate-pulse shadow-[0_0_10px_rgba(59,130,246,0.5)]'
                      : 'bg-gray-600'
                }`}></div>
                <span className={`text-sm transition-colors duration-300 ${
                  index <= currentStep ? 'text-white' : 'text-gray-500'
                }`}>
                  {step}
                </span>
              </div>
            ))}
          </div>
        </div>
        
        <div className="glass rounded-xl p-4 border border-blue-500/30">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full flex items-center justify-center">
              <span className="text-white text-sm">⏳</span>
            </div>
            <div>
              <p className="text-white font-medium text-sm">Please wait</p>
              <p className="text-gray-300 text-xs">Processing satellite imagery with AI...</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Error state  
  if (error) {
    return (
      <div className="glass rounded-xl p-6 border border-red-500/30 glow-red">
        <div className="flex items-start space-x-4">
          <div className="w-10 h-10 bg-gradient-to-r from-red-500 to-pink-500 rounded-full flex items-center justify-center flex-shrink-0">
            <span className="text-white text-lg">❌</span>
          </div>
          <div>
            <h3 className="text-red-400 font-semibold mb-2">Analysis Failed</h3>
            <p className="text-gray-300 text-sm leading-relaxed">{error}</p>
          </div>
        </div>
      </div>
    )
  }

  // Results state
  if (data) {
    const isPolygonAnalysis = data.analysis_type === 'polygon';
    
    return (
      <div className="space-y-6">
        {/* Analysis Type Indicator */}
        <div className="glass rounded-xl p-4 border border-purple-500/30 glow-indigo">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full flex items-center justify-center">
              <span className="text-white text-lg">{isPolygonAnalysis ? '🔷' : '📍'}</span>
            </div>
            <div>
              <h3 className="text-purple-400 font-bold text-sm">Analysis Type</h3>
              <p className="text-white font-medium">
                {isPolygonAnalysis ? 'Polygon Area Analysis' : 'Point Location Analysis'}
              </p>
            </div>
          </div>
        </div>

        {/* Polygon Area Information */}
        {isPolygonAnalysis && data.area_info && (
          <div className="glass rounded-xl p-6 border border-emerald-500/30 glow-green">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-gradient-to-r from-emerald-500 to-green-500 rounded-full flex items-center justify-center">
                <span className="text-white text-lg">📐</span>
              </div>
              <h3 className="text-emerald-400 font-bold text-lg">Area Information</h3>
            </div>
            
            <div className="grid grid-cols-2 gap-3">
              <div className="glass rounded-lg p-3">
                <p className="text-gray-300 text-xs">Points</p>
                <p className="text-white font-bold text-lg">{data.area_info.total_points}</p>
              </div>
              
              <div className="glass rounded-lg p-3">
                <p className="text-gray-300 text-xs">Est. Area</p>
                <p className="text-white font-bold text-lg">{data.area_info.estimated_area_hectares} ha</p>
              </div>
              
              <div className="glass rounded-lg p-3">
                <p className="text-gray-300 text-xs">Perimeter</p>
                <p className="text-white font-bold text-lg">{data.area_info.perimeter_km} km</p>
              </div>
              
              <div className="glass rounded-lg p-3">
                <p className="text-gray-300 text-xs">Dominant Type</p>
                <p className="text-emerald-400 font-bold text-sm">{data.area_info.dominant_land_type}</p>
              </div>
            </div>
          </div>
        )}

        {/* Land Classification Results */}
        <div className="glass rounded-xl p-6 border border-emerald-500/30 glow-green">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-gradient-to-r from-emerald-500 to-green-500 rounded-full flex items-center justify-center">
              <span className="text-white text-lg">🌱</span>
            </div>
            <h3 className="text-emerald-400 font-bold text-lg">Land Classification</h3>
            {data.ml_source === 'huggingface' && (
              <span className="glass px-2 py-1 rounded-full text-xs text-blue-400">🤖 AI-Powered</span>
            )}
          </div>
          
          <div className="space-y-3">
            <div className="glass rounded-lg p-3">
              <p className="text-gray-300 text-sm">Primary Land Type</p>
              <p className="text-white font-bold text-lg">{data.land_class}</p>
            </div>
            
            <div className="glass rounded-lg p-3">
              <p className="text-gray-300 text-sm mb-2">Confidence Level</p>
              <div className="flex items-center space-x-3">
                <div className="flex-1 bg-gray-700 rounded-full h-2 overflow-hidden">
                  <div 
                    className="bg-gradient-to-r from-emerald-500 to-green-400 h-full rounded-full transition-all duration-1000 shadow-[0_0_10px_rgba(16,185,129,0.5)]"
                    style={{ width: `${data.confidence * 100}%` }}
                  ></div>
                </div>
                <span className="text-emerald-400 font-bold text-lg">
                  {Math.round(data.confidence * 100)}%
                </span>
              </div>
            </div>

            {/* Top Predictions from ML Model */}
            {data.top_predictions && Object.keys(data.top_predictions).length > 0 && (
              <div className="glass rounded-lg p-3">
                <p className="text-gray-300 text-sm mb-3">Top Predictions</p>
                <div className="space-y-2">
                  {Object.entries(data.top_predictions).slice(0, 5).map(([label, score], idx) => (
                    <div key={idx} className="flex items-center justify-between">
                      <span className="text-xs text-gray-400 flex-1 truncate pr-2">{label}</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-16 bg-gray-700 rounded-full h-1.5 overflow-hidden">
                          <div 
                            className={`h-full rounded-full ${
                              idx === 0 ? 'bg-emerald-400' : 'bg-blue-400'
                            }`}
                            style={{ width: `${score * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-xs font-medium text-white w-10 text-right">
                          {Math.round(score * 100)}%
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Before/After Images */}
        <div className="glass rounded-xl p-6 border border-blue-500/30 glow-blue">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full flex items-center justify-center">
              <span className="text-white text-lg">🖼️</span>
            </div>
            <h3 className="text-blue-400 font-bold text-lg">Image Enhancement</h3>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="glass rounded-lg p-4 text-center">
              <p className="text-gray-300 text-sm font-medium mb-3">Before (30×30)</p>
              <div className="w-24 h-24 mx-auto mb-3 rounded-lg overflow-hidden border border-gray-600">
                <img 
                  src={`data:image/png;base64,${data.before_image_b64}`}
                  alt="Before enhancement"
                  className="w-full h-full object-cover"
                  style={{ imageRendering: 'pixelated' }}
                />
              </div>
              <p className="text-xs text-gray-400">Low Resolution</p>
            </div>
            
            <div className="glass rounded-lg p-4 text-center">
              <p className="text-gray-300 text-sm font-medium mb-3">After (120×120)</p>
              <div className="w-24 h-24 mx-auto mb-3 rounded-lg overflow-hidden border border-emerald-500 shadow-[0_0_15px_rgba(16,185,129,0.3)]">
                <img 
                  src={`data:image/png;base64,${data.after_image_b64}`}
                  alt="After enhancement"
                  className="w-full h-full object-cover"
                />
              </div>
              <p className="text-xs text-emerald-400">4× Enhanced</p>
            </div>
          </div>
          
          <div className="mt-4 glass rounded-lg p-3">
            <div className="flex items-center space-x-2 text-sm text-gray-300">
              <span className="text-blue-400">✨</span>
              <span>RFB-ESRGAN super-resolution (4× upscaling)</span>
            </div>
          </div>
          
          {data.ml_source === 'fallback' && (
            <div className="mt-3 glass rounded-lg p-3 border border-yellow-500/30">
              <div className="flex items-center space-x-2 text-sm text-yellow-400">
                <span>⚠️</span>
                <span>Using fallback predictions - HuggingFace model may be sleeping</span>
              </div>
            </div>
          )}
        </div>

        {/* Future Features */}
        <div className="space-y-4">
          <div className="glass rounded-xl p-4 border border-gray-600/30">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm">📊</span>
                </div>
                <h4 className="text-gray-300 font-semibold">Crop History Analysis</h4>
              </div>
              <span className="glass px-2 py-1 rounded-full text-xs text-gray-400">Coming Soon</span>
            </div>
            <p className="text-gray-400 text-sm">
              Historical patterns and seasonal crop rotation analysis
            </p>
          </div>
          
          <div className="glass rounded-xl p-4 border border-gray-600/30">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-r from-orange-500 to-yellow-500 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm">🌾</span>
                </div>
                <h4 className="text-gray-300 font-semibold">Smart Recommendations</h4>
              </div>
              <span className="glass px-2 py-1 rounded-full text-xs text-gray-400">Coming Soon</span>
            </div>
            <p className="text-gray-400 text-sm">
              AI-powered crop suggestions based on soil and climate data
            </p>
          </div>
        </div>
      </div>
    )
  }

  // Default state (no location selected)
  return (
    <div className="text-center py-12">
      <div className="w-20 h-20 mx-auto mb-6 glass rounded-full flex items-center justify-center animate-float">
        <span className="text-4xl">📍</span>
      </div>
      <h3 className="text-white font-semibold text-lg mb-2">Ready for Analysis</h3>
      <p className="text-gray-400 text-sm leading-relaxed">
        Select any location on the interactive map to begin AI-powered satellite imagery analysis
      </p>
      <div className="mt-6 glass rounded-lg p-3 inline-block">
        <p className="text-xs text-gray-400">Click anywhere on the map to get started</p>
      </div>
    </div>
  )
}

export default ResultsPanel