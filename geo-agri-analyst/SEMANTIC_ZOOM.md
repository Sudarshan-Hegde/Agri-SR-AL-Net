# Semantic Zoom Feature

## Overview
The semantic zoom feature has been implemented in the map component to provide contextual information based on the current zoom level. This prevents information overload by showing only relevant labels for the current view altitude.

## How It Works

### Zoom Levels & Information Hierarchy

1. **Zoom 1-4: Continental View** 🌍
   - Shows: Major countries and continents
   - Color: Blue (#60A5FA)
   - Font Size: 16px (largest)
   - Examples: India, China, United States, Brazil, Germany

2. **Zoom 5-7: State/Province View** 🗺️
   - Shows: States, provinces, major regions
   - Color: Emerald (#34D399)
   - Font Size: 14px
   - Examples: Maharashtra, Delhi, Tamil Nadu, Karnataka

3. **Zoom 8-10: City View** 🏙️
   - Shows: Major cities
   - Color: Amber (#FBBF24)
   - Font Size: 13px
   - Examples: New Delhi, Mumbai, Bengaluru, Chennai

4. **Zoom 11-13: District/Neighborhood View** 🏘️
   - Shows: Districts, neighborhoods, localities
   - Color: Violet (#A78BFA)
   - Font Size: 12px
   - Examples: Connaught Place, Andheri, Whitefield

5. **Zoom 14+: Landmark View** 📍
   - Shows: Local landmarks, specific locations
   - Color: Pink (#F472B6)
   - Font Size: 11px (smallest, most detailed)
   - Examples: India Gate, Gateway of India, MG Road

## Visual Features

- **Progressive Disclosure**: Labels appear and disappear smoothly as you zoom
- **Color Coding**: Each zoom level has a distinct color to help identify the scale
- **Size Gradation**: Larger text for broader areas, smaller for specific locations
- **Dark Theme Integration**: Labels use semi-transparent black backgrounds that blend with the map
- **No Clutter**: Labels are positioned strategically to avoid overlap

## User Experience Benefits

1. **Reduced Cognitive Load**: Only see information relevant to current view
2. **Better Navigation**: Colors and sizes help orient users to their zoom level
3. **Context Awareness**: Always know what level of detail you're viewing
4. **Smooth Transitions**: Labels fade in/out as you zoom, not jarring

## Technical Implementation

- **Component**: `SemanticZoomLabels` in `MapComponent.jsx`
- **Technology**: React-Leaflet `CircleMarker` with permanent popups
- **Performance**: Efficient re-rendering only on zoom changes
- **Customizable**: Easy to add more locations or adjust zoom ranges

## Customization

To add more locations, edit the `labelData` object in the `SemanticZoomLabels` component:

```javascript
const labelData = {
  city: [
    { 
      position: [lat, lng], 
      name: 'City Name', 
      minZoom: 8, 
      maxZoom: 10 
    },
    // Add more cities...
  ],
  // Add more categories...
};
```

## Agricultural Use Cases

This feature is particularly useful for agricultural analysis:
- **Zoom out**: See entire agricultural regions (e.g., "Punjab - Wheat Belt")
- **Zoom to state level**: Identify crop zones (e.g., "Haryana - Rice Growing Region")
- **Zoom to district**: See specific farming areas (e.g., "Sonipat District")
- **Zoom to landmark**: Identify specific farms or agricultural landmarks

## Future Enhancements

Potential improvements:
- [ ] Dynamic loading of labels based on map bounds (for better performance)
- [ ] Integration with agricultural data (show crop types at different zoom levels)
- [ ] User-customizable label categories
- [ ] Multi-language support for labels
- [ ] Integration with satellite imagery analysis results
