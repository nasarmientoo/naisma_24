### geo_utils.py ###
"""
GeoUtils: A module for performing geospatial operations on GeoDataFrames.
"""

import geopandas as gpd
from rich.console import Console
from rich.theme import Theme

# Define the theme for console messages
custom_theme = Theme({
    "success": "bold #028090",
    "info": "bold #080357",
    "warning": "bold #F9B5AC",
    "error": "bold #89023E",
    "highlight": "bold #F4D35E"
})
console = Console(theme=custom_theme)

class GeoUtils:
    @staticmethod
    def calculate_centroids(geodataframe, target_crs="EPSG:3857"):
        """
        Calculate centroids of polygons in a projected CRS.
    
        Parameters:
        - geodataframe (GeoDataFrame): The input GeoDataFrame with polygon geometries.
        - target_crs (str): The projected CRS to use for centroid calculations (default: EPSG:3857 for Web Mercator).
    
        Returns:
        - GeoDataFrame: A GeoDataFrame with a new 'centroid' geometry column in the original CRS.
        """
        try:
            # Save the original CRS
            original_crs = geodataframe.crs
            
            # Convert to a projected CRS
            projected_gdf = geodataframe.to_crs(target_crs)
            
            # Calculate centroids in the projected CRS
            projected_gdf["centroid"] = projected_gdf.geometry.centroid
            
            # Convert centroids back to the original CRS
            projected_gdf["centroid"] = projected_gdf["centroid"].to_crs(original_crs)
            
            # Return the GeoDataFrame with centroids in the original CRS
            console.print("[success]Centroids calculated successfully.[/success]", style="success")
            return projected_gdf
        except Exception as e:
            console.print(f"[error]Error calculating centroids: {e}[/error]", style="error")
            return geodataframe


    @staticmethod
    def remove_low_security_areas(geodataframe, column="security_index", threshold=0.1):
        """
        Remove polygons where the security index is below a given threshold.

        Parameters:
        - geodataframe (GeoDataFrame): The input GeoDataFrame with a security index column.
        - column (str): The name of the security index column (default: "security_index").
        - threshold (float): The minimum security index required to retain a polygon.

        Returns:
        - GeoDataFrame: A filtered GeoDataFrame with only relevant polygons.
        """
        try:
            filtered_gdf = geodataframe[geodataframe[column] >= threshold]
            removed_count = len(geodataframe) - len(filtered_gdf)
            console.print(f"[info]{removed_count} polygons removed below threshold {threshold}.[/info]", style="info")
            return filtered_gdf
        except Exception as e:
            console.print(f"[error]Error removing low-security areas: {e}[/error]", style="error")
            return geodataframe
