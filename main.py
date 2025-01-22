from src.data_loader import DataLoader
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel

# Define the theme
custom_theme = Theme({
    "dataLoader": "bold #29339B",
    "weightManager": "bold #ADF5FF",
    "indexCalculator": "bold #0496FF",
    "geoUtils": "bold #EEFC57",
    "visualizer": "bold #FF3A20"
})
console = Console(theme=custom_theme)

# Fancy Welcome Message
welcome_message = Panel(
    "Welcome to the [highlight]Security Navigator Library[/highlight]\n"
    "\nAvailable Functions:\n"
    "- [dataLoader]DataLoader[/dataLoader]: Load and validate boundaries and datasets\n"
    "- [weightManager]WeightManager[/weightManager]: Process attributes with assigned weights\n"
    "- [indexCalculator]IndexCalculator[/indexCalculator]: Calculate security indices\n"
    "- [geoUtils]GeoUtils[/geoUtils]: Handle spatial operations\n"
    "- [visualizer]Visualizer[/visualizer]: Create heatmaps for security indices",
    title="[bold #028090]Welcome[/bold #028090]",
    border_style="bold #F9B5AC"
)
console.print(welcome_message)

# Load boundaries and datasets
data_loader = DataLoader('data/boston_neighborhoods.geojson', ['data/cleaned_crimes.csv'])
boundaries = data_loader.load_boundaries()
datasets = data_loader.load_datasets()