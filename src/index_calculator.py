### index_calculator.py ###
"""
This module calculates the security index for each zone based on weighted variables.
"""

import pandas as pd

class IndexCalculator:
    def __init__(self, boundaries, security_data, weights):
        """
        Initialize with boundaries, security data, and weights.

        Parameters:
        boundaries (GeoDataFrame): Geospatial data of political boundaries.
        security_data (DataFrame): Security-related data.
        weights (dict): Weights for variables.
        """
        self.boundaries = boundaries
        self.security_data = security_data
        self.weights = weights

    def calculate_index(self):
        """
        Compute the security index for each zone.

        Returns:
        GeoDataFrame: Boundaries with added security index.
        """
        security_data = self.security_data.copy()
        
        for variable, weight in self.weights.items():
            if variable not in security_data.columns:
                raise ValueError(f"Variable '{variable}' is not in the security data.")
            security_data[variable] *= weight

        security_data['security_index'] = security_data[list(self.weights.keys())].sum(axis=1)

        # Merge with boundaries
        result = self.boundaries.merge(security_data[['zone_id', 'security_index']], on='zone_id', how='left')
        return result
