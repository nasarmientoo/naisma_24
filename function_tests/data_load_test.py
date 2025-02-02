from src.data_loader import DataLoader
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, Point

# Mock data
boundaries_path = "test_boundaries.geojson"
dataset_path = "test_dataset.csv"

# Create a boundaries GeoDataFrame
boundaries = gpd.GeoDataFrame({
    'id': [1],
    'geometry': [Polygon([(-71.1, 42.3), (-71.1, 42.4), (-71.0, 42.4), (-71.0, 42.3), (-71.1, 42.3)])]
}, crs="EPSG:4326")
boundaries.to_file(boundaries_path, driver="GeoJSON")

# Create a dataset as CSV
df = pd.DataFrame({
    'LONGITUDE': [-71.05, -71.07],
    'LATITUDE': [42.35, 42.36],
    'OFFENSE_CODE': [619, 3410]
})
df.to_csv(dataset_path, index=False)

# Inline Tests
data_loader = DataLoader(boundaries_path, [dataset_path])

# Test loading boundaries
loaded_boundaries = data_loader.load_boundaries()
assert not loaded_boundaries.empty, "Boundaries should not be empty"

# Test loading datasets
datasets = data_loader.load_datasets()
assert len(datasets) == 1, "Should load one dataset"
assert 'geometry' in datasets[0].columns, "Dataset should have a 'geometry' column"

# Cleanup
import os
os.remove(boundaries_path)
os.remove(dataset_path)

print("All inline tests for `data_loader.py` passed!")
