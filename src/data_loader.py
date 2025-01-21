### data_loader.py ###
"""
This module handles loading and validating geospatial and security-related datasets. 
Users must upload a GeoJSON file for boundaries and at least one CSV for security data.
"""

import geopandas as gpd
import pandas as pd

class DataLoader:
    def __init__(self):
        self.boundaries = None
        self.security_data = None

    def load_boundaries(self, filepath):
        """
        Load and validate the GeoJSON file defining the political boundaries.
        
        Parameters:
        filepath (str): Path to the GeoJSON file.

        Returns:
        GeoDataFrame: Loaded boundaries.
        """
        try:
            self.boundaries = gpd.read_file(filepath)
            if not self.boundaries.crs:
                raise ValueError("GeoJSON file must have a defined coordinate reference system (CRS).")
        except Exception as e:
            raise ValueError(f"Error loading boundaries: {e}")
        return self.boundaries

    def load_security_data(self, filepath):
        """
        Load and validate the CSV file containing security-related data.
        
        Parameters:
        filepath (str): Path to the CSV file.

        Returns:
        DataFrame: Loaded security data.
        """
        try:
            self.security_data = pd.read_csv(filepath)
            if 'zone_id' not in self.security_data.columns:
                raise ValueError("CSV file must contain a 'zone_id' column.")
        except Exception as e:
            raise ValueError(f"Error loading security data: {e}")
        return self.security_data

    def get_data(self):
        """
        Retrieve loaded boundaries and security data.

        Returns:
        tuple: (GeoDataFrame, DataFrame)
        """
        if self.boundaries is None or self.security_data is None:
            raise ValueError("Both boundaries and security data must be loaded.")
        return self.boundaries, self.security_data