"""
Quick test script for polygon analysis utilities
Run: python test_polygon_utils.py
"""

import sys
sys.path.insert(0, '/home/sudarshanhegde/Sudarshan_Hegde/majorProject/geo-agri-analyst/backend')

from app.polygon_utils import (
    generate_grid_samples,
    estimate_polygon_area_km2,
    determine_optimal_zoom,
    calculate_polygon_bounds
)

# Test polygon: small agricultural plot
test_polygon_small = [
    [40.7128, -74.0060],
    [40.7138, -74.0050],
    [40.7135, -74.0040],
    [40.7125, -74.0045]
]

# Test polygon: medium farm (roughly 1km x 1km)
test_polygon_medium = [
    [40.7100, -74.0100],
    [40.7100, -74.0000],
    [40.7200, -74.0000],
    [40.7200, -74.0100]
]

print("=" * 60)
print("POLYGON ANALYSIS UTILITIES TEST")
print("=" * 60)

print("\n1. SMALL POLYGON TEST")
print("-" * 60)
area_small = estimate_polygon_area_km2(test_polygon_small)
print(f"   Area: {area_small:.6f} km² ({area_small * 100:.2f} hectares)")

bounds = calculate_polygon_bounds(test_polygon_small)
print(f"   Bounds: lat[{bounds[0]:.4f}, {bounds[1]:.4f}], lng[{bounds[2]:.4f}, {bounds[3]:.4f}]")

zoom_small = determine_optimal_zoom(area_small, is_polygon=True)
print(f"   Optimal zoom: {zoom_small}")

samples_small = generate_grid_samples(test_polygon_small, max_samples=50, min_samples=5)
print(f"   Sample points generated: {len(samples_small)}")
print(f"   First 3 samples: {samples_small[:3]}")

print("\n2. MEDIUM POLYGON TEST")
print("-" * 60)
area_medium = estimate_polygon_area_km2(test_polygon_medium)
print(f"   Area: {area_medium:.6f} km² ({area_medium * 100:.2f} hectares)")

bounds = calculate_polygon_bounds(test_polygon_medium)
print(f"   Bounds: lat[{bounds[0]:.4f}, {bounds[1]:.4f}], lng[{bounds[2]:.4f}, {bounds[3]:.4f}]")

zoom_medium = determine_optimal_zoom(area_medium, is_polygon=True)
print(f"   Optimal zoom: {zoom_medium}")

samples_medium = generate_grid_samples(test_polygon_medium, max_samples=50, min_samples=5)
print(f"   Sample points generated: {len(samples_medium)}")
print(f"   First 5 samples: {samples_medium[:5]}")

print("\n3. POINT ANALYSIS ZOOM TEST")
print("-" * 60)
zoom_point = determine_optimal_zoom(0, is_polygon=False)
print(f"   Point analysis zoom: {zoom_point}")

print("\n4. AGGREGATION TEST")
print("-" * 60)
from app.polygon_utils import aggregate_predictions

# Mock predictions
mock_predictions = [
    {"land_class": "Agricultural", "confidence": 0.85, "predictions": {}},
    {"land_class": "Agricultural", "confidence": 0.82, "predictions": {}},
    {"land_class": "Forest", "confidence": 0.75, "predictions": {}},
    {"land_class": "Agricultural", "confidence": 0.88, "predictions": {}},
    {"land_class": "Urban", "confidence": 0.70, "predictions": {}},
]

aggregated = aggregate_predictions(mock_predictions)
print(f"   Dominant class: {aggregated['dominant_class']}")
print(f"   Confidence: {aggregated['confidence']:.2%}")
print(f"   Sample count: {aggregated['sample_count']}")
print(f"   Class distribution:")
for cls, info in aggregated['class_distribution'].items():
    print(f"      - {cls}: {info['percentage']:.1f}% ({info['count']} samples, avg conf: {info['avg_confidence']:.2%})")

print("\n" + "=" * 60)
print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
print("=" * 60)
