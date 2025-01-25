from weight_manager import WeightManager
import geopandas as gpd
from shapely.geometry import Point

# Mock data
datasets = [
    gpd.GeoDataFrame({
        'attribute_1': ['619', '3410', '3301'],
        'attribute_2': ['Y', 'N', 'Y'],
        'geometry': [Point(-71.05, 42.35), Point(-71.07, 42.36), Point(-71.08, 42.37)]
    }, crs="EPSG:4326")
]

weights = [
    {'attribute': 'attribute_1', 'weight': 0.8, 'severity': {'619': 3, '3410': 4, '3301': 1}},
    {'attribute': 'attribute_2', 'weight': 0.2, 'severity': {'Y': 2, 'N': 1}}
]

# Inline Tests
weight_manager = WeightManager(weights)
processed_datasets = weight_manager.apply_severity(datasets)

# Check normalization
total_weight = sum(w['weight'] for w in weight_manager.weights)
assert abs(total_weight - 1.0) < 1e-6, "Weights should normalize to 1"

# Check severity application
processed_df = processed_datasets[0]
assert processed_df['attribute_1'].iloc[0] == 3 * 0.8, "Severity and weight calculation is incorrect"
assert processed_df['attribute_2'].iloc[0] == 2 * 0.2, "Severity and weight calculation is incorrect"

print("All inline tests for `weight_manager.py` passed!")
