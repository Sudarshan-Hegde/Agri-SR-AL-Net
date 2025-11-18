"""
Test script to verify satellite image fetching works
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from app.satellite_service import get_satellite_service

# Test coordinates (Berlin, Germany - agricultural area nearby)
test_locations = [
    (52.5200, 13.4050, "Berlin, Germany"),
    (40.7128, -74.0060, "New York, USA"),
    (51.5074, -0.1278, "London, UK"),
]

print("=" * 60)
print("Testing Satellite Image Fetching")
print("=" * 60)

satellite_svc = get_satellite_service()

for lat, lng, name in test_locations:
    print(f"\n📍 Testing: {name} (lat={lat}, lng={lng})")
    print("-" * 60)
    
    try:
        image = satellite_svc.get_satellite_image(lat, lng, size=30, zoom=17)
        
        if image:
            print(f"✅ SUCCESS!")
            print(f"   Image size: {image.size}")
            print(f"   Image mode: {image.mode}")
            
            # Save for inspection
            output_path = f"test_satellite_{name.replace(' ', '_').replace(',', '')}.png"
            image.save(output_path)
            print(f"   Saved to: {output_path}")
        else:
            print(f"❌ FAILED: No image returned")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
