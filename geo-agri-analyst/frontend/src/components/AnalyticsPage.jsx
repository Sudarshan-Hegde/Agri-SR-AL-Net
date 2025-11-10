import { useState, useEffect } from 'react'

// Convert distance based on selected unit
function convertDistance(kilometers, unit = 'km') {
  if (unit === 'miles') {
    return (kilometers * 0.621371).toFixed(2) + ' mi';
  }
  return kilometers.toFixed(2) + ' km';
}

// Calculate area of polygon in hectares
function calculateArea(points) {
  if (!points || points.length < 3) return 0;
  
  // Convert lat/lng to approximate meters
  const earthRadius = 6371000; // meters
  const pointsInMeters = points.map(([lat, lng]) => [
    lat * (Math.PI / 180) * earthRadius,
    lng * (Math.PI / 180) * earthRadius * Math.cos(points[0][0] * Math.PI / 180)
  ]);

  // Calculate area using shoelace formula
  let area = 0;
  for (let i = 0; i < pointsInMeters.length; i++) {
    const j = (i + 1) % pointsInMeters.length;
    area += pointsInMeters[i][0] * pointsInMeters[j][1];
    area -= pointsInMeters[j][0] * pointsInMeters[i][1];
  }
  area = Math.abs(area) / 2;
  
  // Convert to hectares
  return (area / 10000).toFixed(2);
}

function formatAnalysisResult(result) {
  if (!result) return [{ title: 'Status', value: 'No results available' }]

  const formattedResults = []

  // Convert all result properties into readable format
  Object.entries(result).forEach(([key, value]) => {
    if (typeof value === 'object' && value !== null) {
      // Handle nested objects
      Object.entries(value).forEach(([nestedKey, nestedValue]) => {
        formattedResults.push({
          title: nestedKey.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
          value: typeof nestedValue === 'number' ? 
            (nestedKey.includes('percentage') || nestedKey.includes('confidence') ? 
              `${(nestedValue * 100).toFixed(1)}%` : 
              nestedValue.toFixed(2)
            ) : 
            nestedValue
        })
      })
    } else {
      // Handle direct properties
      const title = key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
      let displayValue = value

      // Format numbers appropriately
      if (typeof value === 'number') {
        if (key.includes('percentage') || key.includes('confidence')) {
          displayValue = `${(value * 100).toFixed(1)}%`
        } else {
          displayValue = value.toFixed(2)
        }
      }

      formattedResults.push({
        title,
        value: displayValue
      })
    }
  })

  console.log('Formatted Results:', formattedResults) // For debugging
  return formattedResults
}

function AnalyticsPage({ history, settings }) {
  const [analyticsHistory, setAnalyticsHistory] = useState([])
  const distanceUnit = settings?.displaySettings?.distanceUnit || 'km'

  useEffect(() => {
    if (history) {
      setAnalyticsHistory(history)
    }
  }, [history])

  return (
    <div className="relative z-10 w-full px-4 sm:px-6 lg:px-8 py-4 pt-24 lg:pt-28">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-3 h-3 bg-blue-400 rounded-full animate-pulse"></div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white">Analytics History</h1>
        </div>
        
        <div className="space-y-6">
          {analyticsHistory.length === 0 ? (
            <div className="glass-card rounded-xl lg:rounded-2xl p-8 text-center">
              <div className="flex flex-col items-center space-y-4">
                <div className="w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center">
                  <span className="text-2xl">📊</span>
                </div>
                <p className="text-gray-400">No analytics history available for this session</p>
                <p className="text-sm text-gray-500">Select a location on the map to perform your first analysis</p>
              </div>
            </div>
          ) : (
            analyticsHistory.map((analysis, index) => (
              <div key={index} className="glass-card rounded-xl lg:rounded-2xl p-6 hover:shadow-2xl transition-all duration-500">
                <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                  <div>
                    <div className="flex items-center space-x-3">
                      <span className="glass px-3 py-1 rounded-full text-sm text-blue-400">
                        Analysis #{analyticsHistory.length - index}
                      </span>
                      <span className="text-gray-400 text-sm">
                        {new Date(analysis.timestamp).toLocaleString()}
                      </span>
                    </div>
                    
                    <div className="mt-3 flex items-center space-x-4">
                      <div className="glass px-3 py-1 rounded-lg text-sm text-emerald-400">
                        Type: {analysis.type}
                      </div>
                      <div className="glass px-3 py-1 rounded-lg text-sm text-gray-300">
                        {analysis.type === 'point' ? 
                          `Location: (${analysis.lat.toFixed(4)}°N, ${analysis.lng.toFixed(4)}°E)` :
                          `Polygon: ${analysis.points?.length || 0} points - ${calculateArea(analysis.points)} hectares - ${convertDistance(analysis.perimeter || 0, distanceUnit)} perimeter`
                        }
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-6 space-y-6">
                  {/* Satellite Images Section */}
                  <div className="glass rounded-xl p-5">
                    <h4 className="text-lg font-medium text-white mb-4">Satellite Imagery</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {/* Before Image */}
                      <div className="space-y-2">
                        <div className="text-sm text-gray-400">Original Image</div>
                        {analysis.results?.before_image ? (
                          <div className="glass p-2 rounded-lg overflow-hidden">
                            <img 
                              src={`data:image/jpeg;base64,${analysis.results.before_image}`}
                              alt="Original satellite image"
                              className="w-full h-48 object-cover rounded-lg"
                            />
                          </div>
                        ) : (
                          <div className="glass p-4 rounded-lg text-gray-500 text-center">
                            No original image available
                          </div>
                        )}
                      </div>

                      {/* After Image */}
                      <div className="space-y-2">
                        <div className="text-sm text-gray-400">Enhanced Image</div>
                        {analysis.results?.after_image ? (
                          <div className="glass p-2 rounded-lg overflow-hidden">
                            <img 
                              src={`data:image/jpeg;base64,${analysis.results.after_image}`}
                              alt="Enhanced satellite image"
                              className="w-full h-48 object-cover rounded-lg"
                            />
                          </div>
                        ) : (
                          <div className="glass p-4 rounded-lg text-gray-500 text-center">
                            No enhanced image available
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Analysis Results Section */}
                  <div className="glass rounded-xl p-5 space-y-4">
                    <h4 className="text-lg font-medium text-white mb-4">Analysis Results</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {formatAnalysisResult(analysis.results).map((result, idx) => (
                        <div key={idx} className="glass p-4 rounded-lg">
                          <div className="text-sm text-gray-400 mb-1">{result.title}</div>
                          <div className="text-white font-medium">
                            {typeof result.value === 'object' ? 
                              JSON.stringify(result.value, null, 2) : 
                              result.value.toString()}
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="mt-4 p-4 glass rounded-lg">
                      <details>
                        <summary className="text-sm text-gray-400 cursor-pointer hover:text-gray-300">
                          View Raw Data
                        </summary>
                        <pre className="mt-2 text-xs text-gray-400 overflow-auto">
                          {JSON.stringify(analysis.results, null, 2)}
                        </pre>
                      </details>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="mt-8 glass rounded-xl p-4 lg:p-6">
        <div className="flex flex-col lg:flex-row items-center justify-between text-xs lg:text-sm text-gray-400 gap-4">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
              <span>Analytics Ready</span>
            </div>
          </div>
          <div className="text-xs text-center lg:text-right">
            Machine Learning • Satellite Analysis • Agricultural Intelligence
          </div>
        </div>
      </div>
    </div>
  )
}

export default AnalyticsPage