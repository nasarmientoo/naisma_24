### data_loader.py ###
"""
This module handles loading and validating geospatial and security-related datasets. 
Users must upload a GeoJSON file for boundaries and at least one CSV for security data.
"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from rich.console import Console
from rich.theme import Theme
from rich.table import Table

custom_theme = Theme({
    "success": "bold #028090",
    "info": "bold #080357",
    "warning": "bold #F9B5AC",
    "error": "bold #89023E",
    "highlight": "bold #F4D35E"
})
console = Console(theme=custom_theme)


class DataLoader:
    def __init__(self, boundaries_path, dataset_paths):
        """
        Initialize the DataLoader class.

        Parameters:
        - boundaries_path (str): Path to the geospatial boundaries file (GeoJSON, Shapefile, or GeoPackage).
        - dataset_paths (list of str): List of paths to point-based spatial datasets.
        """
        self.boundaries_path = boundaries_path
        self.dataset_paths = dataset_paths
        self.boundaries = None
        self.datasets = []

    def load_boundaries(self):
        """
        Load and validate the geospatial boundaries file.

        Returns:
        - GeoDataFrame containing the boundaries.
        """
        try:
            if self.boundaries_path.endswith('.geojson'):
                self.boundaries = gpd.read_file(self.boundaries_path)
            elif self.boundaries_path.endswith('.shp'):
                self.boundaries = gpd.read_file(self.boundaries_path)
            elif self.boundaries_path.endswith('.gpkg'):
                self.boundaries = gpd.read_file(self.boundaries_path, layer=0)
            else:
                raise ValueError("Unsupported file format. Please provide a GeoJSON, Shapefile, or GeoPackage.")

            if self.boundaries.empty:
                raise ValueError("The boundaries file is empty.")

            console.print(f"[success]Boundaries loaded successfully from {self.boundaries_path}![/success]", style="success")
            return self.boundaries

        except Exception as e:
            console.print(f"[error]Error loading boundaries: {e}[/error]", style="error")
            raise RuntimeError(f"Error loading boundaries: {e}")

    def load_datasets(self):
        """
        Load and validate the point-based spatial datasets.

        Returns:
        - List of GeoDataFrames containing the datasets.
        """
        for path in self.dataset_paths:
            try:
                if path.endswith('.csv'):
                    dataset = pd.read_csv(path, encoding='latin1')  
                    if 'LONGITUDE' not in dataset.columns or 'LATITUDE' not in dataset.columns:
                        raise ValueError(f"The dataset at {path} must contain 'LONGITUDE' and 'LATITUDE' columns.")
                    
                    # Convert to GeoDataFrame with Point geometry
                    geometry = [Point(xy) for xy in zip(dataset['LONGITUDE'], dataset['LATITUDE'])]
                    dataset = gpd.GeoDataFrame(dataset, geometry=geometry, crs="EPSG:4326")
                else:
                    dataset = gpd.read_file(path)
                
                table = Table(title=f"Attributes in dataset: {path}", show_lines=True)
                table.add_column("Attribute", justify="left", style="info")
                table.add_column("Type", justify="left", style="highlight")

                for column in dataset.columns:
                    column_type = "Numerical" if pd.api.types.is_numeric_dtype(dataset[column]) else "Non-Numerical"
                    table.add_row(column, column_type)

                console.print(table)
                    
                if dataset.empty:
                    raise ValueError(f"The dataset at {path} is empty.")

                # Remove points outside the boundaries
                if self.boundaries is not None:
                    initial_count = len(dataset)
                    dataset = dataset[dataset.geometry.within(self.boundaries.unary_union)]
                    removed_points = initial_count - len(dataset)

                    if removed_points > 0:
                        console.print(f"[info]{removed_points} points removed as they were outside the boundaries for dataset {path}.[/info]", style="info")

                self.datasets.append(dataset)
                console.print(f"[success]Dataset loaded successfully from {path}![/success]", style="success")

            except Exception as e:
                console.print(f"[error]Error loading dataset at {path}: {e}[/error]", style="error")
                raise RuntimeError(f"Error loading dataset at {path}: {e}")

        return self.datasets