from src.data_loader import DataLoader
from src.weight_manager import WeightManager
from src.index_calculator import IndexCalculator
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel

# Initialize console
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

# Step 1: Load boundaries and datasets
data_loader = DataLoader('data/boston_neighborhoods.geojson', ['data/cleaned_crimes.csv'])
boundaries = data_loader.load_boundaries()
datasets = data_loader.load_datasets()

# Ensure non-numerical columns are strings
for i, dataset in enumerate(datasets):
    if 'OFFENSE_CODE' in dataset.columns:
        datasets[i]['OFFENSE_CODE'] = dataset['OFFENSE_CODE'].astype(str)
    if 'MONTH' in dataset.columns:
        datasets[i]['MONTH'] = dataset['MONTH'].astype(str)

# Step 2: Prepare and process datasets with WeightManager
weights = {
    'OFFENSE_CODE': 0.5,  
    'MONTH': 0.2        
}

weight_manager = WeightManager(weights)
processed_weights = weight_manager.prepare_and_process(datasets)

# Step 3: Calculate the security index with IndexCalculator
index_calculator = IndexCalculator(boundaries, datasets, processed_weights)
boundaries_with_index = index_calculator.calculate_index()

# Step 4: Display the calculated security index
index_calculator.display_results()

output_path = 'data/boundaries_with_index.geojson'
boundaries_with_index.to_file(output_path, driver='GeoJSON')