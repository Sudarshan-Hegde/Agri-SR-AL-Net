"""
Satellite Imagery Service
Fetches real satellite images from various sources based on coordinates
"""

import httpx
from PIL import Image
import io
from typing import Optional, Tuple
import os
from datetime import datetime, timedelta


class SatelliteImageService:
    """
    Service for fetching real satellite imagery from various sources
    """
    
    def __init__(self):
        """Initialize satellite service with API configurations"""
        # Mapbox API (provides satellite imagery)
        # Get free token at: https://account.mapbox.com/
        self.mapbox_token = os.getenv("MAPBOX_TOKEN", "")
        
        # Sentinel Hub API (for Sentinel-2 data)
        # Get free trial at: https://www.sentinel-hub.com/
        self.sentinel_hub_token = os.getenv("SENTINEL_HUB_TOKEN", "")
        
        print(f"📡 Satellite Service initialized")
        if self.mapbox_token:
            print(f"✅ Mapbox API configured")
        if self.sentinel_hub_token:
            print(f"✅ Sentinel Hub API configured")
    
    def get_satellite_image(
        self, 
        lat: float, 
        lng: float, 
        size: int = 30,
        zoom: int = 17
    ) -> Optional[Image.Image]:
        """
        Fetch real satellite image for given coordinates
        
        Args:
            lat: Latitude
            lng: Longitude
            size: Image size in pixels (default 30x30)
            zoom: Zoom level (higher = more detail, 1-20)
        
        Returns:
            PIL Image or None if fetch fails
        """
        # Try different sources in order of preference
        sources = [
            ("Mapbox Static Tiles", self._fetch_from_mapbox),
            ("ArcGIS World Imagery", self._fetch_from_arcgis),
            ("OpenStreetMap Tiles", self._fetch_from_osm)
        ]
        
        for source_name, fetch_func in sources:
            try:
                print(f"🛰️ Attempting to fetch from {source_name}...")
                image = fetch_func(lat, lng, size, zoom)
                if image:
                    print(f"✅ Successfully fetched {size}x{size} image from {source_name}")
                    return image
            except Exception as e:
                print(f"⚠️ {source_name} failed: {e}")
                continue
        
        print("❌ All satellite image sources failed")
        return None
    
    def _fetch_from_mapbox(
        self, 
        lat: float, 
        lng: float, 
        size: int = 30,
        zoom: int = 17
    ) -> Optional[Image.Image]:
        """
        Fetch satellite image from Mapbox Static API
        Requires MAPBOX_TOKEN environment variable
        
        Free tier: 50,000 requests/month
        Get token at: https://account.mapbox.com/
        """
        if not self.mapbox_token:
            raise Exception("MAPBOX_TOKEN not configured")
        
        # Mapbox Static Images API
        # https://docs.mapbox.com/api/maps/static-images/
        url = (
            f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/"
            f"{lng},{lat},{zoom},0/{size}x{size}"
            f"?access_token={self.mapbox_token}"
        )
        
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        
        image = Image.open(io.BytesIO(response.content))
        return image.convert('RGB')
    
    def _fetch_from_arcgis(
        self, 
        lat: float, 
        lng: float, 
        size: int = 30,
        zoom: int = 17
    ) -> Optional[Image.Image]:
        """
        Fetch satellite image from ArcGIS World Imagery (ESRI)
        
        Free to use with attribution
        No API key required
        """
        # Convert lat/lng to tile coordinates
        # Using Web Mercator projection (EPSG:3857)
        import math
        
        def deg2num(lat_deg, lon_deg, zoom):
            """Convert lat/lng to tile numbers"""
            lat_rad = math.radians(lat_deg)
            n = 2.0 ** zoom
            xtile = int((lon_deg + 180.0) / 360.0 * n)
            ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
            return (xtile, ytile)
        
        # Get tile coordinates
        xtile, ytile = deg2num(lat, lng, zoom)
        
        # Fetch tile from ArcGIS
        url = (
            f"https://server.arcgisonline.com/ArcGIS/rest/services/"
            f"World_Imagery/MapServer/tile/{zoom}/{ytile}/{xtile}"
        )
        
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        
        # Open tile image (typically 256x256)
        tile_image = Image.open(io.BytesIO(response.content))
        
        # Calculate pixel offset within tile for exact lat/lng
        import math
        n = 2.0 ** zoom
        lat_rad = math.radians(lat)
        x = (lng + 180.0) / 360.0 * n
        y = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
        
        # Get fractional part to find position within tile
        x_offset = int((x - xtile) * 256)
        y_offset = int((y - ytile) * 256)
        
        # Crop centered on the target coordinates
        half_size = size // 2
        left = max(0, x_offset - half_size)
        top = max(0, y_offset - half_size)
        right = min(256, left + size)
        bottom = min(256, top + size)
        
        # Crop and resize to exact size
        cropped = tile_image.crop((left, top, right, bottom))
        resized = cropped.resize((size, size), Image.Resampling.LANCZOS)
        
        return resized.convert('RGB')
    
    def _fetch_from_osm(
        self, 
        lat: float, 
        lng: float, 
        size: int = 30,
        zoom: int = 17
    ) -> Optional[Image.Image]:
        """
        Fetch map tile from OpenStreetMap
        Note: OSM provides map tiles, not satellite imagery
        This is a fallback option only
        """
        import math
        
        def deg2num(lat_deg, lon_deg, zoom):
            lat_rad = math.radians(lat_deg)
            n = 2.0 ** zoom
            xtile = int((lon_deg + 180.0) / 360.0 * n)
            ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
            return (xtile, ytile)
        
        xtile, ytile = deg2num(lat, lng, zoom)
        
        # Use OSM tile server
        url = f"https://tile.openstreetmap.org/{zoom}/{xtile}/{ytile}.png"
        
        headers = {
            'User-Agent': 'Geo-Agri-Analyst/1.0'  # OSM requires user agent
        }
        
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        tile_image = Image.open(io.BytesIO(response.content))
        
        # Crop and resize as with ArcGIS
        import math
        n = 2.0 ** zoom
        lat_rad = math.radians(lat)
        x = (lng + 180.0) / 360.0 * n
        y = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
        
        x_offset = int((x - xtile) * 256)
        y_offset = int((y - ytile) * 256)
        
        half_size = size // 2
        left = max(0, x_offset - half_size)
        top = max(0, y_offset - half_size)
        right = min(256, left + size)
        bottom = min(256, top + size)
        
        cropped = tile_image.crop((left, top, right, bottom))
        resized = cropped.resize((size, size), Image.Resampling.LANCZOS)
        
        return resized.convert('RGB')


# Global service instance
satellite_service = None

def get_satellite_service() -> SatelliteImageService:
    """
    Get or create the global satellite service instance
    
    Returns:
        SatelliteImageService instance
    """
    global satellite_service
    if satellite_service is None:
        satellite_service = SatelliteImageService()
    return satellite_service
