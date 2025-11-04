#!/usr/bin/env python3
"""
Test script for the enhanced Geo-Agri Analyst API with weather integration
"""

import asyncio
import httpx
import json
import sys

async def test_weather_service():
    """Test the weather service directly"""
    print("=== Testing Weather Service ===")
    
    sys.path.append('.')
    from app.weather_service import get_agricultural_climate_summary
    
    # Test coordinates: New York City
    lat, lng = 40.7128, -74.0060
    
    try:
        result = await get_agricultural_climate_summary(lat, lng)
        print(f"Weather data for NYC ({lat}, {lng}):")
        print(json.dumps(result, indent=2))
        return True
    except Exception as e:
        print(f"Weather service error: {e}")
        return False

async def test_analysis_endpoint():
    """Test the enhanced analysis endpoint"""
    print("\n=== Testing Enhanced Analysis Endpoint ===")
    
    # Test data for point analysis
    test_data = {
        'type': 'point',
        'lat': 40.7128,
        'lng': -74.0060
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post('http://localhost:8000/api/v1/analyze', json=test_data)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Analysis endpoint working!")
                print("Response includes:")
                print(f"  - Land class: {result.get('land_class')}")
                print(f"  - Confidence: {result.get('confidence')}")
                print(f"  - Weather data: {'Yes' if result.get('weather_data') else 'No'}")
                
                if result.get('weather_data'):
                    weather = result['weather_data']
                    print(f"  - Temperature: {weather.get('avg_temp_c')}°C")
                    print(f"  - Classification: {weather.get('agricultural_classification', {}).get('classification')}")
                
                return True
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                return False
                
    except httpx.ConnectError:
        print("❌ Cannot connect to server. Make sure FastAPI is running on port 8000")
        print("Start server with: python app/main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_polygon_analysis():
    """Test polygon analysis with weather data"""
    print("\n=== Testing Polygon Analysis ===")
    
    # Test data for polygon analysis (small square around NYC)
    test_data = {
        'type': 'polygon',
        'points': [
            [40.7100, -74.0100],  # SW corner
            [40.7100, -74.0000],  # SE corner  
            [40.7200, -74.0000],  # NE corner
            [40.7200, -74.0100]   # NW corner
        ]
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post('http://localhost:8000/api/v1/analyze', json=test_data)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Polygon analysis working!")
                print(f"  - Analysis type: {result.get('analysis_type')}")
                print(f"  - Area info: {result.get('area_info', {}).get('estimated_area_hectares')} hectares")
                print(f"  - Weather data: {'Yes' if result.get('weather_data') else 'No'}")
                return True
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 Geo-Agri Analyst API Integration Tests")
    print("=" * 50)
    
    # Test 1: Weather service
    weather_ok = await test_weather_service()
    
    # Test 2: Analysis endpoint (only if server is available)
    analysis_ok = await test_analysis_endpoint()
    
    # Test 3: Polygon analysis (only if server is available)
    if analysis_ok:
        polygon_ok = await test_polygon_analysis()
    else:
        polygon_ok = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"  ✅ Weather Service: {'PASS' if weather_ok else 'FAIL'}")
    print(f"  ✅ Analysis Endpoint: {'PASS' if analysis_ok else 'FAIL'}")
    print(f"  ✅ Polygon Analysis: {'PASS' if polygon_ok else 'FAIL'}")
    
    if weather_ok and analysis_ok and polygon_ok:
        print("\n🎉 All tests passed! The integration is working correctly.")
    elif weather_ok:
        print("\n⚠️  Weather service works, but server tests failed.")
        print("   Start the FastAPI server with: python app/main.py")
    else:
        print("\n❌ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main())