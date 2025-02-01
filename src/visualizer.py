"""
Visualizer: A module for generating visual representations of geospatial data.
"""
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from rich.console import Console
from rich.theme import Theme
from scipy.stats import gaussian_kde


# Define the theme
custom_theme = Theme({
    "success": "bold #028090",
    "info": "bold #080357",
    "warning": "bold #F9B5AC",
    "error": "bold #89023E",
    "highlight": "bold #F4D35E"
})
console = Console(theme=custom_theme)

class Visualizer:
    @staticmethod
    def plot_choropleth(geodataframe, column, title="Choropleth Map", boundaries=None, save_path=None, cmap='coolwarm'):
        """
        Plot a choropleth map based on a specific column in a GeoDataFrame, with optional boundary overlay and customizable colormap.

        Parameters:
        - geodataframe (GeoDataFrame): Input GeoDataFrame.
        - column (str): Column name to visualize.
        - title (str): Title of the plot.
        - boundaries (GeoDataFrame): Optional GeoDataFrame for boundary overlay.
        - save_path (str): Path to save the plot (optional).
        - cmap (str or list): Colormap name (str) or a list of colors (list) for the map.

        Returns:
        - None
        """
        try:
            # Convert custom color palette to colormap if provided
            if isinstance(cmap, list):  # If cmap is a list, create a custom colormap
                cmap = ListedColormap(cmap)
            
            # Create the plot
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            geodataframe.plot(column=column, ax=ax, legend=True, cmap=cmap)
            
            # Add boundary overlay if provided
            if boundaries is not None:
                boundaries.plot(ax=ax, edgecolor="black", linewidth=0.5, facecolor="none")
    
            # Set title and remove axes
            ax.set_title(title)
            ax.axis('off')
    
            # Save the figure if a save path is provided
            if save_path:
                plt.savefig(save_path, dpi=300)
                console.print(f"[success]Plot saved at {save_path}.[/success]", style="success")
    
            # Show the plot
            plt.show(block=False)
        except Exception as e:
            console.print(f"[error]Error generating plot: {e}[/error]", style="error")


    @staticmethod
    def plot_density(points_geodataframe, boundaries=None, title="Density Heatmap", save_path=None):
        """
        Plot a density heatmap for point-based datasets using semi-transparent points.
    
        Parameters:
        - points_geodataframe (GeoDataFrame): Input GeoDataFrame with point geometries.
        - boundaries (GeoDataFrame): Optional GeoDataFrame for boundary overlay.
        - title (str): Title of the plot.
        - save_path (str): Path to save the plot (optional).
        """
        try:
            # Plot setup
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
            # Plot points with transparency
            points_geodataframe.plot(
                ax=ax,
                color="blue",  # Color for the points
                alpha=0.3,  # Transparency to show overlap
                markersize=2  # Adjust point size as needed
            )
    
            # Overlay boundaries if provided
            if boundaries is not None:
                boundaries.plot(ax=ax, edgecolor="black", linewidth=1.0, facecolor="none")
    
            # Set title and axis off
            ax.set_title(title)
            ax.axis("off")
    
            # Save the figure if a save path is provided
            if save_path:
                plt.savefig(save_path, dpi=300)
                console.print(f"[success]Density plot saved at {save_path}.[/success]", style="success")
    
            plt.show(block=False)  # Non-blocking show for interactive environments
            plt.close()  # Close the plot to free up memory
    
        except Exception as e:
            console.print(f"[error]Error generating density plot: {e}[/error]", style="error")

    @staticmethod
    def plot_histogram(data, column, bins=10, title="Histogram", xlabel=None, ylabel="Frequency", save_path=None):
        """
        Plot a histogram for a specific column in the dataset.

        Parameters:
        - data (DataFrame): Input DataFrame or GeoDataFrame.
        - column (str): Column name for which to generate the histogram.
        - bins (int): Number of bins (default: 10).
        - title (str): Title of the histogram.
        - xlabel (str): Label for the x-axis (default: column name).
        - ylabel (str): Label for the y-axis (default: 'Frequency').
        - save_path (str): Path to save the plot (optional).

        Returns:
        - None
        """
        try:
            # Extract column data
            values = data[column].dropna()  # Drop null values
            xlabel = xlabel if xlabel else column  # Default to column name if xlabel is not provided

            # Create the histogram
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            ax.hist(values, bins=bins, color="skyblue", edgecolor="black")
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)

            # Save the figure if a save path is provided
            if save_path:
                plt.savefig(save_path, dpi=300)
                console.print(f"[success]Histogram saved at {save_path}.[/success]", style="success")

            # Show the plot
            plt.show(block=False)
            plt.close()
        except Exception as e:
            console.print(f"[error]Error generating histogram: {e}[/error]", style="error")

    @staticmethod
    def plot_centroids(centroid_geodataframe, boundaries=None, title="Centroids Map", save_path=None):
        """
        Plot centroids of polygons with optional boundary overlay.

        Parameters:
        - centroid_geodataframe (GeoDataFrame): Input GeoDataFrame containing centroids.
        - boundaries (GeoDataFrame): Optional GeoDataFrame for boundary overlay.
        - title (str): Title of the plot.
        - save_path (str): Path to save the plot (optional).

        Returns:
        - None
        """
        try:
            # Create plot
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            
            # Plot boundaries if provided
            if boundaries is not None:
                boundaries.plot(ax=ax, edgecolor="black", linewidth=0.5, facecolor="none")

            # Plot centroids
            centroid_geodataframe.plot(
                ax=ax, color="red", marker="o", markersize=30, alpha=0.7, label="Centroids"
            )

            # Set title
            ax.set_title(title)
            ax.legend()

            # Save the figure if a save path is provided
            if save_path:
                plt.savefig(save_path, dpi=300)
                console.print(f"[success]Centroid plot saved at {save_path}.[/success]", style="success")

            plt.show(block=False)
            plt.close()
        except Exception as e:
            console.print(f"[error]Error generating centroid plot: {e}[/error]", style="error")
