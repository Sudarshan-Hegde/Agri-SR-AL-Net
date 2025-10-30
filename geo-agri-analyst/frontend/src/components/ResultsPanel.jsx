import React from 'react'

function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center space-x-2">
      <div className="w-4 h-4 border-2 border-agri-green border-t-transparent rounded-full animate-spin"></div>
    </div>
  )
}

function ProcessingSteps({ currentStep }) {
  const steps = [
    'Fetching live satellite imagery...',
    'Preprocessing satellite data...',
    'Enhancing image quality with AI...',
    'Running land classification model...',
    'Generating final analysis...'
  ]

  return (
    <div className="space-y-3">
      {steps.map((step, index) => (
        <div key={index} className="flex items-center space-x-3">
          <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
            index < currentStep 
              ? 'bg-green-500 text-white' 
              : index === currentStep 
                ? 'bg-agri-blue text-white' 
                : 'bg-gray-200 text-gray-500'
          }`}>
            {index < currentStep ? '✓' : index + 1}
          </div>
          <span className={`text-sm ${
            index <= currentStep ? 'text-gray-900 font-medium' : 'text-gray-500'
          }`}>
            {step}
          </span>
          {index === currentStep && <LoadingSpinner />}
        </div>
      ))}
    </div>
  )
}

function ConfidenceBar({ confidence }) {
  const percentage = Math.round(confidence * 100)
  const getColorClass = (conf) => {
    if (conf >= 0.8) return 'bg-green-500'
    if (conf >= 0.6) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-gray-700">Confidence</span>
        <span className="text-sm font-bold text-gray-900">{percentage}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-3">
        <div 
          className={`h-3 rounded-full transition-all duration-500 ${getColorClass(confidence)}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  )
}

function ImageComparison({ beforeImage, afterImage }) {
  return (
    <div className="space-y-4">
      <h4 className="font-semibold text-gray-900 text-center">Image Enhancement</h4>
      
      <div className="grid grid-cols-2 gap-4">
        {/* Before Image */}
        <div className="text-center">
          <h5 className="text-sm font-medium text-gray-700 mb-2">Before (16x16)</h5>
          <div className="border-2 border-gray-200 rounded-lg overflow-hidden bg-gray-50">
            <img
              src={`data:image/png;base64,${beforeImage}`}
              alt="Low Resolution"
              className="w-full h-32 object-cover"
              style={{ imageRendering: 'pixelated' }}
            />
          </div>
          <p className="text-xs text-gray-500 mt-1">Original satellite image</p>
        </div>

        {/* After Image */}
        <div className="text-center">
          <h5 className="text-sm font-medium text-gray-700 mb-2">After (64x64)</h5>
          <div className="border-2 border-agri-green rounded-lg overflow-hidden bg-gray-50">
            <img
              src={`data:image/png;base64,${afterImage}`}
              alt="Super Resolution"
              className="w-full h-32 object-cover"
            />
          </div>
          <p className="text-xs text-agri-green font-medium mt-1">AI Enhanced (4x)</p>
        </div>
      </div>

      {/* Enhancement info */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
        <div className="flex items-center space-x-2">
          <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="text-sm text-blue-800 font-medium">Super-Resolution Enhancement</span>
        </div>
        <p className="text-xs text-blue-700 mt-1">
          Our AI model enhanced the image resolution by 4x for better classification accuracy.
        </p>
      </div>
    </div>
  )
}

function FutureFeatures() {
  return (
    <div className="space-y-4">
      <h4 className="font-semibold text-gray-900">Future Features</h4>
      
      {/* Crop History */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <div className="flex items-center space-x-2 mb-2">
          <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h5 className="font-medium text-gray-900">Crop History Analysis</h5>
        </div>
        <p className="text-sm text-gray-600">
          Historical crop analysis and seasonal patterns are in development. 
          This will provide insights into land use changes over time.
        </p>
      </div>

      {/* Crop Recommendations */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <div className="flex items-center space-x-2 mb-2">
          <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          <h5 className="font-medium text-gray-900">Crop Recommendations</h5>
        </div>
        <p className="text-sm text-gray-600">
          Soil and weather analysis for personalized crop recommendations is in development.
          This will help optimize agricultural productivity.
        </p>
      </div>
    </div>
  )
}

function ResultsPanel({ isLoading, error, predictionData, currentStep, selectedPos }) {
  // No location selected
  if (!selectedPos && !isLoading && !predictionData && !error) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="text-center text-gray-500">
          <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <h3 className="text-lg font-medium mb-2">Select a Location</h3>
          <p className="text-sm">
            Click anywhere on the map to start analyzing satellite imagery for agricultural land classification.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Loading State */}
      {isLoading && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <LoadingSpinner />
            <span className="ml-2">Processing Analysis</span>
          </h3>
          <ProcessingSteps currentStep={currentStep} />
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="flex items-center space-x-2 mb-2">
            <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 className="text-lg font-semibold text-red-900">Analysis Failed</h3>
          </div>
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {/* Results */}
      {predictionData && (
        <div className="space-y-6">
          {/* Main Result */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-center mb-4">
              <div className="w-16 h-16 bg-agri-green rounded-full flex items-center justify-center mx-auto mb-3">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-1">
                {predictionData.land_class}
              </h3>
              <p className="text-gray-600">Land Classification Result</p>
            </div>
            
            <ConfidenceBar confidence={predictionData.confidence} />
          </div>

          {/* Image Comparison */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <ImageComparison 
              beforeImage={predictionData.before_image_b64}
              afterImage={predictionData.after_image_b64}
            />
          </div>

          {/* Future Features */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <FutureFeatures />
          </div>
        </div>
      )}

      {/* Location Info */}
      {selectedPos && (
        <div className="bg-white rounded-lg shadow-lg p-4">
          <h4 className="font-medium text-gray-900 mb-2">Selected Coordinates</h4>
          <div className="text-sm text-gray-600 space-y-1">
            <p>Latitude: {selectedPos[0].toFixed(6)}</p>
            <p>Longitude: {selectedPos[1].toFixed(6)}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default ResultsPanel