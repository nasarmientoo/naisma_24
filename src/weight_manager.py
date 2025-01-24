### weight_manager.py ###
"""
This module manages weights assigned to security-related variables.
Users can specify weights for each variable to calculate the security index.
"""
from rich.console import Console
from rich.theme import Theme
import geopandas as gpd
import pandas as pd

# Define the theme
custom_theme = Theme({
    "success": "bold #028090",
    "info": "bold #080357",
    "warning": "bold #F9B5AC",
    "error": "bold #89023E",
    "highlight": "bold #F4D35E"
})
console = Console(theme=custom_theme)

class WeightManager:
    def __init__(self, weights):
        """
        Initialize the WeightManager class.

        Parameters:
        - weights (list of dict): List of dictionaries defining attributes, their severity mappings, and optional weights.
          
        """
        self.weights = weights
        self.normalize_weights()

    def normalize_weights(self):
        """
        Normalize the weights so that they sum up to 1.
        """
        total_weight = sum(weight.get('weight', 1) for weight in self.weights)
        for weight in self.weights:
            if 'weight' in weight:
                weight['weight'] = weight['weight'] / total_weight

        console.print("[info]Weights have been normalized.", style="info")

    def apply_severity(self, datasets):
        """
        Apply severity levels to the specified attributes in the datasets.

        Parameters:
        - datasets (list of GeoDataFrames): The point-based spatial datasets.

        Returns:
        - List of GeoDataFrames with severity levels and weights applied to the specified attributes.
        """
        processed_datasets = []

        for dataset in datasets:
            df = dataset.copy()

            for weight in self.weights:
                attribute = weight['attribute']
                severity = weight['severity']
                attr_weight = weight.get('weight', 1)  

                if attribute in df.columns:
                    console.print(f"[info]Processing attribute '{attribute}' with defined severities and weight {attr_weight}.[/info]", style="info")

                    # Map severities to the attribute values and apply the weight
                    df[attribute] = df[attribute].astype(str).map(severity).fillna(1) * attr_weight
                else:
                    console.print(f"[warning]Attribute '{attribute}' not found in dataset. Skipping...[/warning]", style="warning")

            processed_datasets.append(df)

        console.print(f"[success]Severity levels and weights successfully applied to specified attributes.[/success]", style="success")
        return processed_datasets
