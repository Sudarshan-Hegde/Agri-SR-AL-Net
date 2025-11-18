"""
Polygon Analysis Utilities
Provides grid-based sampling and polygon operations for multi-point analysis
"""

import math
from typing import List, Tuple
from shapely.geometry import Point, Polygon
import numpy as np


def point_in_polygon(point: Tuple[float, float], polygon_points: List[List[float]]) -> bool:
    """
    Check if a point is inside a polygon using ray casting algorithm
    
    Args:
        point: (lat, lng) tuple
        polygon_points: List of [lat, lng] coordinates forming the polygon
        
    Returns:
        True if point is inside polygon, False otherwise
    """
    x, y = point
    n = len(polygon_points)
    inside = False
    
    p1x, p1y = polygon_points[0]
    for i in range(n + 1):
        p2x, p2y = polygon_points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside


def calculate_polygon_bounds(points: List[List[float]]) -> Tuple[float, float, float, float]:
    """
    Calculate bounding box of polygon
    
    Args:
        points: List of [lat, lng] coordinates
        
    Returns:
        (min_lat, max_lat, min_lng, max_lng)
    """
    lats = [p[0] for p in points]
    lngs = [p[1] for p in points]
    
    return (min(lats), max(lats), min(lngs), max(lngs))


def estimate_polygon_area_km2(points: List[List[float]]) -> float:
    """
    Estimate polygon area in square kilometers using Shoelace formula
    
    Args:
        points: List of [lat, lng] coordinates
        
    Returns:
        Area in square kilometers
    """
    if len(points) < 3:
        return 0.0
    
    # Calculate centroid for reference point
    center_lat = sum(p[0] for p in points) / len(points)
    center_lng = sum(p[1] for p in points) / len(points)
    
    # Convert to meters using approximation
    lat_to_m = 111320.0  # meters per degree latitude
    lng_to_m = 111320.0 * math.cos(math.radians(center_lat))
    
    # Convert points to Cartesian coordinates
    x_coords = [(p[1] - center_lng) * lng_to_m for p in points]
    y_coords = [(p[0] - center_lat) * lat_to_m for p in points]
    
    # Apply Shoelace formula
    area = 0.0
    n = len(points)
    for i in range(n):
        j = (i + 1) % n
        area += x_coords[i] * y_coords[j]
        area -= x_coords[j] * y_coords[i]
    
    area = abs(area) / 2.0  # Area in square meters
    
    # Convert to square kilometers
    area_km2 = area / 1_000_000.0
    
    return area_km2


def calculate_optimal_grid_spacing(polygon_area_km2: float, target_samples: int = 20) -> float:
    """
    Calculate optimal grid spacing to get approximately target number of samples
    
    Args:
        polygon_area_km2: Polygon area in square kilometers
        target_samples: Target number of sample points
        
    Returns:
        Grid spacing in degrees (approximate)
    """
    # Estimate spacing to get target samples
    # For a square area: num_samples ≈ (area / spacing²)
    if polygon_area_km2 <= 0:
        return 0.001  # Default small spacing
    
    # spacing_km = sqrt(area_km2 / target_samples)
    spacing_km = math.sqrt(polygon_area_km2 / target_samples)
    
    # Convert km to degrees (rough approximation: 1 degree ≈ 111 km)
    spacing_degrees = spacing_km / 111.0
    
    # Set bounds
    min_spacing = 0.0005  # ~55 meters minimum
    max_spacing = 0.01    # ~1.1 km maximum
    
    return max(min_spacing, min(spacing_degrees, max_spacing))


def generate_grid_samples(
    polygon_points: List[List[float]], 
    max_samples: int = 50,
    min_samples: int = 5
) -> List[Tuple[float, float]]:
    """
    Generate grid-based sample points within a polygon
    
    Args:
        polygon_points: List of [lat, lng] coordinates forming the polygon
        max_samples: Maximum number of sample points to generate
        min_samples: Minimum number of sample points (will include centroid if needed)
        
    Returns:
        List of (lat, lng) sample points inside the polygon
    """
    if len(polygon_points) < 3:
        return []
    
    # Calculate polygon bounds
    min_lat, max_lat, min_lng, max_lng = calculate_polygon_bounds(polygon_points)
    
    # Calculate polygon area
    area_km2 = estimate_polygon_area_km2(polygon_points)
    
    # Determine grid spacing based on area
    if area_km2 < 0.01:  # Very small area (< 0.01 km² = 1 hectare)
        # For small areas, just use centroid or a few points
        target_samples = min_samples
    elif area_km2 < 0.5:  # Small to medium area (< 0.5 km²)
        target_samples = min(15, max_samples)
    elif area_km2 < 2.0:  # Medium area (< 2 km²)
        target_samples = min(30, max_samples)
    else:  # Large area
        target_samples = max_samples
    
    # Calculate grid spacing
    spacing = calculate_optimal_grid_spacing(area_km2, target_samples)
    
    # Generate grid points
    sample_points = []
    
    lat = min_lat
    while lat <= max_lat:
        lng = min_lng
        while lng <= max_lng:
            point = (lat, lng)
            if point_in_polygon(point, polygon_points):
                sample_points.append(point)
            lng += spacing
        lat += spacing
    
    # If we got too few samples, add centroid
    if len(sample_points) < min_samples:
        centroid_lat = sum(p[0] for p in polygon_points) / len(polygon_points)
        centroid_lng = sum(p[1] for p in polygon_points) / len(polygon_points)
        sample_points.append((centroid_lat, centroid_lng))
    
    # Limit to max_samples by sampling evenly
    if len(sample_points) > max_samples:
        # Use numpy to select evenly spaced indices
        indices = np.linspace(0, len(sample_points) - 1, max_samples, dtype=int)
        sample_points = [sample_points[i] for i in indices]
    
    return sample_points


def determine_optimal_zoom(polygon_area_km2: float, is_polygon: bool = True) -> int:
    """
    Determine optimal zoom level based on polygon area or analysis type
    
    Args:
        polygon_area_km2: Area of polygon in square kilometers
        is_polygon: True if polygon analysis, False if point analysis
        
    Returns:
        Optimal zoom level (1-20)
    """
    if not is_polygon:
        # For single point analysis, use lower zoom to capture more context
        return 15  # ~150m coverage per 30x30 image
    
    # For polygon analysis with multiple samples
    if polygon_area_km2 < 0.01:  # Very small (< 1 hectare)
        return 17  # High detail (~35-40m coverage)
    elif polygon_area_km2 < 0.1:  # Small (< 10 hectares)
        return 16  # Medium-high detail (~70-80m coverage)
    elif polygon_area_km2 < 1.0:  # Medium (< 1 km²)
        return 15  # Medium detail (~150m coverage)
    else:  # Large area
        return 14  # Lower detail for wider coverage (~300m coverage)


def aggregate_predictions(predictions: List[dict]) -> dict:
    """
    Aggregate multiple predictions into a comprehensive summary
    
    Args:
        predictions: List of prediction dicts, each containing:
            - land_class: str
            - confidence: float
            - predictions: dict of {class: confidence}
            
    Returns:
        Aggregated results with:
            - dominant_class: Most common prediction
            - confidence: Average confidence for dominant class
            - class_distribution: Percentage breakdown of all classes
            - detailed_predictions: All individual predictions
    """
    if not predictions:
        return {
            "dominant_class": "Unknown",
            "confidence": 0.0,
            "class_distribution": {},
            "sample_count": 0
        }
    
    # Count occurrences of each class
    class_counts = {}
    class_confidences = {}
    
    for pred in predictions:
        land_class = pred.get("land_class", "Unknown")
        confidence = pred.get("confidence", 0.0)
        
        if land_class not in class_counts:
            class_counts[land_class] = 0
            class_confidences[land_class] = []
        
        class_counts[land_class] += 1
        class_confidences[land_class].append(confidence)
    
    # Calculate percentages
    total_samples = len(predictions)
    class_distribution = {
        cls: {
            "percentage": round((count / total_samples) * 100, 2),
            "count": count,
            "avg_confidence": round(sum(class_confidences[cls]) / len(class_confidences[cls]), 3)
        }
        for cls, count in class_counts.items()
    }
    
    # Sort by percentage
    class_distribution = dict(
        sorted(class_distribution.items(), key=lambda x: x[1]["percentage"], reverse=True)
    )
    
    # Dominant class is the most common one
    dominant_class = max(class_counts.items(), key=lambda x: x[1])[0]
    dominant_confidence = class_distribution[dominant_class]["avg_confidence"]
    
    return {
        "dominant_class": dominant_class,
        "confidence": dominant_confidence,
        "class_distribution": class_distribution,
        "sample_count": total_samples,
        "area_coverage": "multi-sample"
    }
