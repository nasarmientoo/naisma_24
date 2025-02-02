from src.visualizer import Visualizer
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

# Mock data
boundaries = gpd.GeoDataFrame({
    'id': [1],
    'geometry': [Polygon([(-71.1, 42.3), (-71.1, 42.4), (-71.0, 42.4), (-71.0, 42.3), (-71.1, 42.3)])]
}, crs="EPSG:4326")

points = gpd.GeoDataFrame({
    'value': [10, 15, 20],
    'geometry': [Point(-71.05, 42.35), Point(-71.07, 42.36), Point(-71.08, 42.37)]
}, crs="EPSG:4326")

data = pd.DataFrame({'values': [10, 20, 30, 40, 50]})

# Inline Tests
Visualizer.plot_choropleth(boundaries, column='id', title="Test Choropleth")
Visualizer.plot_density(points, boundaries=boundaries, title="Test Density Heatmap")
Visualizer.plot_histogram(data, column='values', bins=5, title="Test Histogram")

print("All inline tests for `visualizer.py` passed!")
