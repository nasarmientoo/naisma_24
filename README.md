# [bold #028090]Security Navigator Library[/bold #028090]

Welcome to the **[bold #028090]Security Navigator Library[/bold #028090]**, your go-to geospatial tool for analyzing, managing, and visualizing security-related data. This library offers an intuitive and robust framework to process geospatial datasets, calculate security indices, and generate actionable insights for decision-making.

## [bold #ADF5FF]Features[/bold #ADF5FF]
- **[bold #29339B]Data Loader[/bold #29339B]**: Load and validate boundaries and datasets in various geospatial formats.
- **[bold #ADF5FF]Weight Manager[/bold #ADF5FF]**: Define and apply severities and weights to attributes in datasets.
- **[bold #0496FF]Index Calculator[/bold #0496FF]**: Calculate and normalize security indices for geospatial polygons.
- **[bold #EEFC57]GeoUtils (coming soon)[/bold #EEFC57]**: Handle advanced geospatial operations.
- **[bold #FF3A20]Visualizer (coming soon)[/bold #FF3A20]**: Generate heatmaps and visual representations of your security indices.

---

## [bold #ADF5FF]Installation[/bold #ADF5FF]
To install the library, clone the repository and install the dependencies:

```bash
# Clone the repository
git clone https://github.com/your-repo/security-navigator.git

# Navigate to the project directory
cd security-navigator

# Install dependencies
pip install -r requirements.txt
```

---

## [bold #ADF5FF]Modules Overview[/bold #ADF5FF]

### 1. **[bold #29339B]DataLoader[/bold #29339B]**
The `DataLoader` module allows users to load and validate geospatial boundaries and datasets. It supports multiple file formats, ensuring compatibility with most geospatial data sources.

#### [bold #080357]Key Features:[/bold #080357]
- Load boundaries in formats like GeoJSON, Shapefile, and GeoPackage.
- Validate datasets to ensure they include necessary columns and geometries.
- Automatically remove points outside specified boundaries.

#### [bold #080357]Example:[/bold #080357]
```python
from src.data_loader import DataLoader

data_loader = DataLoader('data/boundaries.geojson', ['data/points.csv'])
boundaries = data_loader.load_boundaries()
datasets = data_loader.load_datasets()
```

---

### 2. **[bold #ADF5FF]WeightManager[/bold #ADF5FF]**
The `WeightManager` module processes attribute values by mapping them to predefined severity levels and applying weights.

#### [bold #080357]Key Features:[/bold #080357]
- Define severities for specific attribute values.
- Normalize weights to ensure consistent contributions to the index.
- Apply severities and weights to attributes in the dataset.

#### [bold #080357]Example:[/bold #080357]
```python
weights = [
    {
        'attribute': 'OFFENSE_CODE',
        'severity': {
            '619': 3,
            '3410': 4,
            '3301': 2
        },
        'weight': 0.6
    },
    {
        'attribute': 'SHOOTING',
        'severity': {
            'Y': 4
        },
        'weight': 0.4
    }
]

from src.weight_manager import WeightManager

weight_manager = WeightManager(weights)
processed_datasets = weight_manager.apply_severity(datasets)
```

---

### 3. **[bold #0496FF]IndexCalculator[/bold #0496FF]**
The `IndexCalculator` module computes the security index for each polygon in the boundaries by aggregating values from associated points.

#### [bold #080357]Key Features:[/bold #080357]
- Aggregate attribute values from points within polygons.
- Normalize the resulting index to a 0-1 scale.
- Handle outliers using the Interquartile Range (IQR) method.

#### [bold #080357]Example:[/bold #080357]
```python
from src.index_calculator import IndexCalculator

index_calculator = IndexCalculator(boundaries, processed_datasets, weights)
boundaries_with_index = index_calculator.calculate_index(normalize=True, handle_outliers=True)
index_calculator.display_results()

# Save the results
boundaries_with_index.to_file('data/boundaries_with_index.geojson', driver='GeoJSON')
```

---

## [bold #ADF5FF]Contributing[/bold #ADF5FF]
We welcome contributions to enhance this library! If you encounter any issues or have ideas for improvement, feel free to submit a pull request or open an issue.

---

## [bold #ADF5FF]License[/bold #ADF5FF]
This project is licensed under the MIT License. See the LICENSE file for more details.

---

## [bold #ADF5FF]Contact[/bold #ADF5FF]
For any inquiries or support, please reach out to us:
- **Email**: natalyalejandra.sarmiento@polimi.it
- **GitHub**: (https://github.com/nasarmientoo/naisma_24)

---

Let the **[bold #028090]Security Navigator Library[/bold #028090]** guide you to insightful geospatial analysis!
