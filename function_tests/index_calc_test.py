from index_calculator import IndexCalculator
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, Point

# Mock data
boundaries = gpd.GeoDataFrame({
    'id': [1],
    'geometry': [Polygon([(-71.1, 42.3), (-71.1, 42.4), (-71.0, 42.4), (-71.0, 42.3), (-71.1, 42.3)])]
}, crs="EPSG:4326")

datasets = [
    gpd.GeoDataFrame({
        'attribute_1': [10, 20],
        'geometry': [Point(-71.05, 42.35), Point(-71.07, 42.36)]
    }, crs="EPSG:4326")
]

weights = [{'attribute': 'attribute_1', 'weight': 0.8}]

# Inline Tests
index_calculator = IndexCalculator(boundaries, datasets, weights)
result = index_calculator.calculate_index()

assert 'security_index' in result.columns, "Boundaries should include 'security_index'"
assert result['security_index'].iloc[0] > 0, "Security index should be greater than 0"

print("All inline tests for `index_calculator.py` passed!")
