### index_calculator.py ###
"""
This module calculates the security index for each zone based on weighted variables.
"""
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
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

class IndexCalculator:
    def __init__(self, boundaries, datasets, weights):
        """
        Initialize the IndexCalculator class.

        Parameters:
        - boundaries (GeoDataFrame): The boundaries of the study area.
        - datasets (list of GeoDataFrames): Point-based spatial datasets.
        - weights (dict): Dictionary mapping attributes to their weights.
        """
        self.boundaries = boundaries
        self.datasets = datasets
        self.weights = weights

    def calculate_index(self, normalize=True, handle_outliers=True):
        """
        Calculate the security index for each polygon in the boundaries.

        Parameters:
        - normalize (bool): Whether to normalize the index to a 0-1 range.
        - handle_outliers (bool): Whether to cap outliers using quantiles.

        Returns:
        - GeoDataFrame: Boundaries with an added 'security_index' column.
        """
        # Initialize security index column
        self.boundaries["security_index"] = 0.0

        for dataset in self.datasets:
            if "geometry" not in dataset.columns:
                raise ValueError("Each dataset must have a 'geometry' column with point geometries.")

            joined = gpd.sjoin(self.boundaries, dataset, how="left", predicate="contains")
            joined = joined.reset_index()

            for weight in self.weights:
                attribute = weight['attribute']
                if attribute in joined.columns:
                    try:
                        joined[attribute] = pd.to_numeric(joined[attribute], errors='coerce').fillna(0)
                    except Exception as e:
                        console.print(f"[error]Error processing attribute '{attribute}': {e}[/error]", style="error")

            if "geometry" in joined.columns:
                joined = joined.drop(columns=["geometry"])

            aggregated = joined.groupby("index").sum()

            for weight in self.weights:
                attribute = weight['attribute']
                attr_weight = weight.get('weight', 1)
                if attribute in aggregated.columns:
                    self.boundaries.loc[aggregated.index, "security_index"] += aggregated[attribute] * attr_weight

        if handle_outliers:
            q1 = self.boundaries["security_index"].quantile(0.25)
            q3 = self.boundaries["security_index"].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            self.boundaries["security_index"] = self.boundaries["security_index"].clip(lower=lower_bound, upper=upper_bound)

        if normalize:
            max_index = self.boundaries["security_index"].max()
            if max_index > 0:
                self.boundaries["security_index"] = self.boundaries["security_index"] / max_index

        console.print(f"[success]Security index successfully calculated for all polygons.[/success]", style="success")
        return self.boundaries

    def display_results(self):
        """
        Display the calculated security index as a table in the console.
        """
        table = Table(title="Security Index by Polygon", show_lines=True)
        table.add_column("Polygon ID", justify="left", style="info")
        table.add_column("Security Index", justify="center", style="highlight")

        for idx, row in self.boundaries.iterrows():
            table.add_row(str(idx), f"{row['security_index']:.4f}")

        console.print(table)
