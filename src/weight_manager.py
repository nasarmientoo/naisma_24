### weight_manager.py ###
"""
This module manages weights assigned to security-related variables.
Users can specify weights for each variable to calculate the security index.
"""
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
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

def one_hot_encode(df, columns):
    """
    Apply one-hot encoding to the specified columns.

    Parameters:
    - df (pd.DataFrame): The dataset.
    - columns (list of str): List of column names to encode.

    Returns:
    - pd.DataFrame: The dataset with one-hot encoded columns.
    """
    console.print(f"[info]Applying one-hot encoding to columns: {columns}[/info]", style="info")
    return pd.get_dummies(df, columns=columns, drop_first=True)

class WeightManager:
    def __init__(self, weights):
        """
        Initialize the WeightManager class.

        Parameters:
        - weights (dict): Dictionary of user-assigned weights for attributes.
        """
        self.weights = weights

    def prepare_and_process(self, datasets):
        """
        Prepare dataset for the security index calculator by handling non-numerical values
        and displaying weights consistently for the one-hot encoded attributes.

        Parameters:
        - datasets (list of GeoDataFrames): The point-based spatial datasets.

        Returns:
        - dict: Dictionary mapping attributes to their assigned weights.
        """
        attribute_weights = {}

        for dataset in datasets:
            df = dataset.copy()

            # Identify non-numerical columns that are in weights
            non_numerical_columns = [col for col in df.select_dtypes(exclude=['number']).columns if col in self.weights]

            # Table for displaying attributes and weights
            table = Table(title="Processed Attributes and Weights", show_lines=True)
            table.add_column("Attribute", justify="left", style="info")
            table.add_column("Weight", justify="center", style="highlight")

            # Apply one-hot encoding to non-numerical columns
            if len(non_numerical_columns) > 0:
                console.print(f"[info]One-hot encoding attributes: {non_numerical_columns}[/info]", style="info")
                df = one_hot_encode(df, non_numerical_columns)

                # Assign the same weight to all one-hot encoded columns
                for original_column in non_numerical_columns:
                    matching_columns = [col for col in df.columns if col.startswith(f"{original_column}_")]
                    original_weight = self.weights[original_column]
                    distributed_weight = original_weight / len(matching_columns)

                    for col in matching_columns:
                        attribute_weights[col] = distributed_weight
                        table.add_row(col, str(distributed_weight))

            # Assign weights only to specified attributes
            for attribute, weight in self.weights.items():
                if attribute in df.columns:
                    attribute_weights[attribute] = weight
                    table.add_row(attribute, str(weight))
                else:
                    console.print(f"[warning]Attribute '{attribute}' not found in dataset. Skipping...[/warning]", style="warning")

            # Display processed attributes in a table
            console.print(table)

        console.print(f"[success]Attributes and weights have been successfully processed![/success]", style="success")
        return attribute_weights
