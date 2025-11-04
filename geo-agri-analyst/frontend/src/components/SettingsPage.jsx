import { useState } from 'react'

function SettingsPage({ settings: initialSettings, onSettingsChange }) {
  const [settings, setSettings] = useState(initialSettings || {
    mapSettings: {
      defaultZoom: 13,
      defaultCenter: { lat: 20.5937, lng: 78.9629 }, // India center
      satelliteView: true,
    },
    analysisSettings: {
      autoAnalyze: false,
      saveHistory: true,
      historyLimit: 50,
      showCoordinates: true,
    },
    displaySettings: {
      darkMode: true,
      showTips: true,
      language: 'en',
      distanceUnit: 'km', // 'km' or 'miles'
    }
  })

  const handleSettingChange = (category, setting, value) => {
    const newSettings = {
      ...settings,
      [category]: {
        ...settings[category],
        [setting]: value
      }
    };
    setSettings(newSettings);
    if (onSettingsChange) {
      onSettingsChange(newSettings);
    }
  }

  return (
    <div className="relative z-10 w-full px-4 sm:px-6 lg:px-8 py-4 pt-24 lg:pt-28">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-3 h-3 bg-purple-400 rounded-full animate-pulse"></div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white">Settings</h1>
        </div>

        <div className="space-y-6">
          {/* Map Settings */}
          <div className="glass-card rounded-xl lg:rounded-2xl p-6">
            <h2 className="text-xl font-semibold text-white mb-4">Map Settings</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="text-gray-300">Default Zoom Level</label>
                <select 
                  className="glass px-3 py-1 rounded-lg text-white bg-transparent"
                  value={settings.mapSettings.defaultZoom}
                  onChange={(e) => handleSettingChange('mapSettings', 'defaultZoom', parseInt(e.target.value))}
                >
                  {[10, 11, 12, 13, 14, 15].map(zoom => (
                    <option key={zoom} value={zoom}>{zoom}</option>
                  ))}
                </select>
              </div>
              <div className="flex items-center justify-between">
                <label className="text-gray-300">Satellite View</label>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={settings.mapSettings.satelliteView}
                    onChange={(e) => handleSettingChange('mapSettings', 'satelliteView', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
                </label>
              </div>
            </div>
          </div>

          {/* Analysis Settings */}
          <div className="glass-card rounded-xl lg:rounded-2xl p-6">
            <h2 className="text-xl font-semibold text-white mb-4">Analysis Settings</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="text-gray-300">Auto-Analyze</label>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={settings.analysisSettings.autoAnalyze}
                    onChange={(e) => handleSettingChange('analysisSettings', 'autoAnalyze', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
                </label>
              </div>
              <div className="flex items-center justify-between">
                <label className="text-gray-300">Save History</label>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={settings.analysisSettings.saveHistory}
                    onChange={(e) => handleSettingChange('analysisSettings', 'saveHistory', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
                </label>
              </div>
              <div className="flex items-center justify-between">
                <label className="text-gray-300">History Limit</label>
                <select 
                  className="glass px-3 py-1 rounded-lg text-white bg-transparent"
                  value={settings.analysisSettings.historyLimit}
                  onChange={(e) => handleSettingChange('analysisSettings', 'historyLimit', parseInt(e.target.value))}
                >
                  {[10, 20, 50, 100].map(limit => (
                    <option key={limit} value={limit}>{limit} entries</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Display Settings */}
          <div className="glass-card rounded-xl lg:rounded-2xl p-6">
            <h2 className="text-xl font-semibold text-white mb-4">Display Settings</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="text-gray-300">Dark Mode</label>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={settings.displaySettings.darkMode}
                    onChange={(e) => handleSettingChange('displaySettings', 'darkMode', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
                </label>
              </div>
              <div className="flex items-center justify-between">
                <label className="text-gray-300">Show Tips</label>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={settings.displaySettings.showTips}
                    onChange={(e) => handleSettingChange('displaySettings', 'showTips', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
                </label>
              </div>
              <div className="flex items-center justify-between">
                <label className="text-gray-300">Language</label>
                <select 
                  className="glass px-3 py-1 rounded-lg text-white bg-transparent"
                  value={settings.displaySettings.language}
                  onChange={(e) => handleSettingChange('displaySettings', 'language', e.target.value)}
                >
                  <option value="en">English</option>
                  <option value="hi">हिंदी</option>
                  <option value="kn">ಕನ್ನಡ</option>
                </select>
              </div>
              
              <div className="flex items-center justify-between">
                <label className="text-gray-300">Distance Unit</label>
                <select 
                  className="glass px-3 py-1 rounded-lg text-white bg-transparent"
                  value={settings.displaySettings.distanceUnit}
                  onChange={(e) => handleSettingChange('displaySettings', 'distanceUnit', e.target.value)}
                >
                  <option value="km">Kilometers (km)</option>
                  <option value="miles">Miles (mi)</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 glass rounded-xl p-4 lg:p-6">
          <div className="flex flex-col lg:flex-row items-center justify-between text-xs lg:text-sm text-gray-400 gap-4">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
                <span>Settings Saved Automatically</span>
              </div>
            </div>
            <div className="text-xs text-center lg:text-right">
              Preferences • Customization • User Experience
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SettingsPage