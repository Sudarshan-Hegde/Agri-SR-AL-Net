import { useState, useRef } from 'react'

function SearchBar({ onLocationSelect }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const searchTimeoutRef = useRef(null);

  const searchLocation = async (query) => {
    if (!query || query.length < 3) {
      setSearchResults([]);
      return;
    }

    setIsSearching(true);
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5`,
        {
          headers: {
            'Accept-Language': 'en'
          }
        }
      );
      const data = await response.json();
      setSearchResults(data);
      setShowResults(true);
    } catch (error) {
      console.error('Error searching location:', error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setSearchQuery(value);

    // Debounce search
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    searchTimeoutRef.current = setTimeout(() => {
      searchLocation(value);
    }, 500);
  };

  const handleSelectLocation = (result) => {
    const lat = parseFloat(result.lat);
    const lng = parseFloat(result.lon);
    onLocationSelect(lat, lng, result.display_name);
    setSearchQuery(result.display_name);
    setShowResults(false);
    setSearchResults([]);
  };

  const handleClearSearch = () => {
    setSearchQuery('');
    setSearchResults([]);
    setShowResults(false);
  };

  return (
    <div 
      className="fixed top-24 left-1/2 w-11/12 max-w-2xl" 
      style={{ 
        transform: 'translateX(-50%)',
        zIndex: 9999,
        pointerEvents: 'auto'
      }}
    >
      <div 
        className="bg-gray-900/95 backdrop-blur-md rounded-xl shadow-2xl border-2 border-blue-500/50" 
        onClick={(e) => e.stopPropagation()}
        onMouseDown={(e) => e.stopPropagation()}
      >
        <div className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={handleInputChange}
            onFocus={() => searchResults.length > 0 && setShowResults(true)}
            onMouseDown={(e) => e.stopPropagation()}
            onClick={(e) => e.stopPropagation()}
            placeholder="🔍 Search for any location... (e.g., New York, London, Tokyo)"
            className="w-full px-6 py-4 pr-28 bg-transparent text-white placeholder-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 text-lg font-medium"
            style={{ cursor: 'text' }}
          />
          <div className="absolute right-4 top-1/2 transform -translate-y-1/2 flex items-center space-x-3">
            {isSearching && (
              <div className="w-6 h-6 border-3 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
            )}
            {searchQuery && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleClearSearch();
                }}
                onMouseDown={(e) => e.stopPropagation()}
                className="text-gray-300 hover:text-white p-2 hover:bg-white/20 rounded-lg transition-all text-xl font-bold"
                style={{ cursor: 'pointer' }}
              >
                ✕
              </button>
            )}
          </div>
        </div>

        {/* Search Results Dropdown */}
        {showResults && searchResults.length > 0 && (
          <div className="mt-2 max-h-80 overflow-y-auto bg-gray-900/98 rounded-lg border-t border-gray-700">
            {searchResults.map((result, index) => (
              <button
                key={index}
                onClick={(e) => {
                  e.stopPropagation();
                  handleSelectLocation(result);
                }}
                onMouseDown={(e) => e.stopPropagation()}
                className="w-full text-left px-6 py-5 hover:bg-blue-500/30 active:bg-blue-500/40 transition-all border-b border-gray-700/50 last:border-b-0"
                style={{ cursor: 'pointer' }}
              >
                <div className="flex items-start space-x-4">
                  <span className="text-blue-400 mt-1 text-2xl">📍</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-white text-lg font-semibold line-clamp-2 mb-1">
                      {result.display_name}
                    </p>
                    <p className="text-gray-400 text-base">
                      {result.lat.substring(0, 8)}, {result.lon.substring(0, 8)}
                    </p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}

        {/* No results message */}
        {showResults && searchResults.length === 0 && searchQuery.length >= 3 && !isSearching && (
          <div className="mt-2 px-6 py-5 bg-gray-900/98 rounded-lg border-t border-gray-700">
            <p className="text-gray-400 text-lg">No locations found</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default SearchBar
