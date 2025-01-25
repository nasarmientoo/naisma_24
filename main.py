import os
from src.data_loader import DataLoader
from src.weight_manager import WeightManager
from src.index_calculator import IndexCalculator
from src.visualizer import Visualizer
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel

os.makedirs("outputs", exist_ok=True)

console = Console()

# Fancy Welcome Message
welcome_message = Panel(
    "Welcome to the [highlight]Security Navigator Library[/highlight]\n"
    "\nAvailable Modules:\n"
    "- [bold #29339B]DataLoader[/bold #29339B]: Load and validate boundaries and datasets\n"
    "- [bold #ADF5FF]WeightManager[/bold #ADF5FF]: Process attributes with assigned weights\n"
    "- [bold #0496FF]IndexCalculator[/bold #0496FF]: Calculate security indices\n"
    "- [bold #EEFC57]GeoUtils[/bold #EEFC57]: Handle spatial operations\n"
    "- [bold #FF3A20]Visualizer[/bold #FF3A20]: Create heatmaps for security indices",
    title="[bold #028090]Welcome[/bold #028090]",
    border_style="bold #F9B5AC"
)
console.print(welcome_message)

# Load boundaries and datasets
data_loader = DataLoader('data/boston_neighborhoods.geojson', ['data/cleaned_crimes.csv'])
boundaries = data_loader.load_boundaries()
datasets = data_loader.load_datasets()

# Ensure non-numerical columns are strings
for i, dataset in enumerate(datasets):
    if 'OFFENSE_CODE' in dataset.columns:
        datasets[i]['OFFENSE_CODE'] = dataset['OFFENSE_CODE'].astype(str)

weights = [
    {
        'attribute': 'OFFENSE_CODE',
        'weight': 0.8,
        'severity':{
            '619': 3,
            '3410': 4,
            '3301': 1
        }
    },
    {
        'attribute': 'SHOOTING',
        'weight': 0.2,
        'severity':{
            'Y': 2,
        }
    } 
]

#Apply WeightManager to process the datasets
weight_manager = WeightManager(weights)
processed_datasets = weight_manager.apply_severity(datasets)

#Calculate the security index using IndexCalculator
index_calculator = IndexCalculator(boundaries, processed_datasets, weights)
boundaries_with_index = index_calculator.calculate_index(normalize=True, handle_outliers=True)
index_calculator.display_results()

output_path = 'data/boundaries_with_index.geojson'
boundaries_with_index.to_file(output_path, driver='GeoJSON')

"""
# Choropleth Plot
Visualizer.plot_choropleth(
    geodataframe=boundaries_with_index,
    column="security_index",
    title="Security Index Map",
    boundaries=boundaries,  
    cmap="viridis",  # Using a built-in Matplotlib colormap
    save_path="outputs/security_index_map.png"
)
"""

# Choropleth Plot with custom color palette
custom_palette = ["#f7fcf0", "#ccebc5", "#a8ddb5", "#7bccc4", "#43a2ca", "#0868ac"]

Visualizer.plot_choropleth(
    geodataframe=boundaries_with_index,
    column="security_index",
    title="Security Index Map with Custom Colors",
    boundaries=boundaries,
    cmap=custom_palette,  # Using a custom color palette
    save_path="outputs/security_index_map_with_custom_palette.png"
)

#Density Plot
Visualizer.plot_density(
    processed_datasets[0],
    boundaries=boundaries,
    title="Point Density Map",
    save_path="outputs/crime_density_heatmap.png"
)

#Plot Histogram 
Visualizer.plot_histogram(
    data=boundaries_with_index,
    column="security_index",
    bins=15,  # Number of bins
    title="Security Index Histogram",
    xlabel="Security Index",
    save_path="outputs/security_index_histogram.png"
)



