import os
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
from src.data_loader import DataLoader
from src.weight_manager import WeightManager
from src.index_calculator import IndexCalculator
from src.visualizer import Visualizer
from src.geo_utils import GeoUtils


# Setup Mock Data
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Create boundaries GeoJSON
boundaries_path = "data/boston_neighborhoods.geojson"
boundaries = gpd.GeoDataFrame({
    'id': [1, 2],
    'geometry': [
        Polygon([(-71.1, 42.3), (-71.1, 42.4), (-71.0, 42.4), (-71.0, 42.3), (-71.1, 42.3)]),
        Polygon([(-71.2, 42.3), (-71.2, 42.4), (-71.1, 42.4), (-71.1, 42.3), (-71.2, 42.3)])
    ]
}, crs="EPSG:4326")
boundaries.to_file(boundaries_path, driver="GeoJSON")

# Create dataset CSV
dataset_path = "data/cleaned_crimes.csv"
df = pd.DataFrame({
    'LONGITUDE': [-71.05, -71.07, -71.12],
    'LATITUDE': [42.35, 42.36, 42.33],
    'OFFENSE_CODE': [619, 3410, 3301],
    'SHOOTING': ['Y', 'N', 'Y']
})
df.to_csv(dataset_path, index=False)

# Inline Test Code

# Step 1: Load boundaries and datasets
data_loader = DataLoader(boundaries_path, [dataset_path])
boundaries = data_loader.load_boundaries()
datasets = data_loader.load_datasets()

assert not boundaries.empty, "Boundaries should not be empty"
assert len(datasets) == 1, "Should load one dataset"
assert 'geometry' in datasets[0].columns, "Dataset should have a 'geometry' column"

# Step 2: Apply WeightManager
weights = [
    {
        'attribute': 'OFFENSE_CODE',
        'weight': 0.8,
        'severity': {
            '619': 3,
            '3410': 4,
            '3301': 1
        }
    },
    {
        'attribute': 'SHOOTING',
        'weight': 0.2,
        'severity': {
            'Y': 2
        }
    }
]
weight_manager = WeightManager(weights)
processed_datasets = weight_manager.apply_severity(datasets)

assert processed_datasets[0]['OFFENSE_CODE'].iloc[0] == 3 * 0.8, "Weight and severity for OFFENSE_CODE incorrect"
assert processed_datasets[0]['SHOOTING'].iloc[0] == 2 * 0.2, "Weight and severity for SHOOTING incorrect"

# Step 3: Calculate Security Index
index_calculator = IndexCalculator(boundaries, processed_datasets, weights)
boundaries_with_index = index_calculator.calculate_index(normalize=True, handle_outliers=True)

assert 'security_index' in boundaries_with_index.columns, "Boundaries should have 'security_index'"
assert boundaries_with_index['security_index'].max() <= 1, "Security index should be normalized to 1"

# Step 4: Test GeoUtils Functions
# Centroid Calculation
centroid_boundaries = GeoUtils.calculate_centroids(boundaries_with_index)
assert "centroid" in centroid_boundaries.columns, "Centroid column should exist"
assert centroid_boundaries["centroid"].geom_type[0] == "Point", "Centroids should be of type Point"

# Save Centroid Map
Visualizer.plot_centroids(
    centroid_boundaries,
    boundaries=boundaries,
    title="Centroids of Security Zones",
    save_path="outputs/centroids_map.png"
)
assert os.path.exists("outputs/centroids_map.png"), "Centroids map not saved"

# Remove low-security areas
threshold = 0.2
filtered_boundaries = GeoUtils.remove_low_security_areas(boundaries_with_index, column="security_index", threshold=threshold)
assert all(filtered_boundaries["security_index"] >= threshold), "Filtered boundaries should have security_index >= threshold"
assert len(filtered_boundaries) < len(boundaries_with_index), "Some polygons should be removed"


# Step 5: Generate Visualizations
Visualizer.plot_choropleth(
    geodataframe=boundaries_with_index,
    column="security_index",
    title="Security Index Map",
    boundaries=boundaries,
    cmap="viridis",
    save_path="outputs/security_index_map.png"
)
assert os.path.exists("outputs/security_index_map.png"), "Choropleth map not saved"

Visualizer.plot_density(
    points_geodataframe=processed_datasets[0],
    boundaries=boundaries,
    title="Point Density Map",
    save_path="outputs/crime_density_heatmap.png"
)
assert os.path.exists("outputs/crime_density_heatmap.png"), "Density heatmap not saved"

Visualizer.plot_histogram(
    data=boundaries_with_index,
    column="security_index",
    bins=15,
    title="Security Index Histogram",
    xlabel="Security Index",
    save_path="outputs/security_index_histogram.png"
)
assert os.path.exists("outputs/security_index_histogram.png"), "Histogram not saved"

# Cleanup
os.remove(boundaries_path)
os.remove(dataset_path)
os.rmdir("data")

print("All tests passed successfully!")
