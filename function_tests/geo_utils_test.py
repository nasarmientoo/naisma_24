import pytest
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, Point
from src.geo_utils import GeoUtils

@pytest.fixture
def sample_boundaries():
    """Create a sample GeoDataFrame with polygon geometries and a security index."""
    return gpd.GeoDataFrame({
        'id': [1, 2, 3, 4, 5],
        'security_index': [0.5, 0.2, 0.8, 0.05, 0.9],  # Different security index values
        'geometry': [
            Polygon([(-71.1, 42.3), (-71.1, 42.4), (-71.0, 42.4), (-71.0, 42.3)]),
            Polygon([(-71.2, 42.3), (-71.2, 42.4), (-71.1, 42.4), (-71.1, 42.3)]),
            Polygon([(-71.3, 42.3), (-71.3, 42.4), (-71.2, 42.4), (-71.2, 42.3)]),
            Polygon([(-71.4, 42.3), (-71.4, 42.4), (-71.3, 42.4), (-71.3, 42.3)]),
            Polygon([(-71.5, 42.3), (-71.5, 42.4), (-71.4, 42.4), (-71.4, 42.3)])
        ]
    }, crs="EPSG:4326")  # Using WGS84 CRS

def test_calculate_centroids(sample_boundaries):
    """Test centroid calculation ensuring correct coordinate system and values."""
    centroid_gdf = GeoUtils.calculate_centroids(sample_boundaries)
    
    assert "centroid" in centroid_gdf.columns, "Centroids column should be added to GeoDataFrame"
    assert all(centroid_gdf["centroid"].geom_type == "Point"), "All centroids should be Point geometries"
    
    # Check that centroids are inside original polygons
    for poly, centroid in zip(centroid_gdf.geometry, centroid_gdf["centroid"]):
        assert poly.contains(centroid), f"Centroid {centroid} should be inside its polygon"

def test_remove_low_security_areas(sample_boundaries):
    """Test removing polygons below a specified security index threshold."""
    threshold = 0.2
    filtered_gdf = GeoUtils.remove_low_security_areas(sample_boundaries, column="security_index", threshold=threshold)
    
    assert all(filtered_gdf["security_index"] >= threshold), "All remaining polygons should have security_index >= threshold"
    assert len(filtered_gdf) < len(sample_boundaries), "Some polygons should be removed"

def test_empty_geodataframe():
    """Test behavior when an empty GeoDataFrame is passed."""
    empty_gdf = gpd.GeoDataFrame(columns=["id", "security_index", "geometry"], crs="EPSG:4326")
    
    filtered_gdf = GeoUtils.remove_low_security_areas(empty_gdf)
    assert filtered_gdf.empty, "Filtering should return an empty GeoDataFrame"

def test_missing_security_index_column(sample_boundaries):
    """Test behavior when the security index column is missing."""
    sample_boundaries.drop(columns=["security_index"], inplace=True)

    with pytest.raises(KeyError):
        GeoUtils.remove_low_security_areas(sample_boundaries, column="security_index", threshold=0.2)

def test_invalid_crs_for_centroids():
    """Test centroid calculation when CRS is invalid (not projected)."""
    gdf = gpd.GeoDataFrame({
        'id': [1],
        'geometry': [Polygon([(-71.1, 42.3), (-71.1, 42.4), (-71.0, 42.4), (-71.0, 42.3)])]
    }, crs="EPSG:4326")  # WGS84 (Geographic CRS)

    with pytest.warns(UserWarning, match="Results from 'centroid' are likely incorrect"):
        GeoUtils.calculate_centroids(gdf)
