# Security Navigator Library

Welcome to the **Security Navigator Library**, your go-to geospatial tool for analyzing, managing, and visualizing security-related data. This library offers an intuitive and robust framework to process geospatial datasets, calculate security indices, and generate actionable insights for decision-making.

## Features
- **Data Loader**: Load and validate boundaries and datasets in various geospatial formats.
- **Weight Manager**: Define and apply severities and weights to attributes in datasets.
- **Index Calculator**: Calculate and normalize security indices for geospatial polygons.
- **GeoUtils (coming soon)**: Handle advanced geospatial operations.
- **Visualizer (coming soon)**: Generate heatmaps and visual representations of your security indices.

---

## Installation
To install the library, clone the repository and install the dependencies:

```bash
# Clone the repository
git clone https://github.com/nasarmientoo/naisma_24

# Navigate to the project directory
cd security-navigator

# Install dependencies
pip install -r requirements.txt
```

---

## Modules Overview

### 1. **DataLoader**
The `DataLoader` module allows users to load and validate geospatial boundaries and datasets. It supports multiple file formats, ensuring compatibility with most geospatial data sources.

#### Key Features:
- Load boundaries in formats like GeoJSON, Shapefile, and GeoPackage.
- Validate datasets to ensure they include necessary columns and geometries.
- Automatically remove points outside specified boundaries.

#### Example:
```python
from src.data_loader import DataLoader

data_loader = DataLoader('data/boundaries.geojson', ['data/points.csv'])
boundaries = data_loader.load_boundaries()
datasets = data_loader.load_datasets()
```

---

### 2. **WeightManager**
The `WeightManager` module processes attribute values by mapping them to predefined severity levels and applying weights.

#### Key Features:
- Define severities for specific attribute values.
- Normalize weights to ensure consistent contributions to the index.
- Apply severities and weights to attributes in the dataset.

#### Example:
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

### 3. **IndexCalculator**
The `IndexCalculator` module computes the security index for each polygon in the boundaries by aggregating values from associated points.

#### Key Features:
- Aggregate attribute values from points within polygons.
- Normalize the resulting index to a 0-1 scale.
- Handle outliers using the Interquartile Range (IQR) method.

#### Example:
```python
from src.index_calculator import IndexCalculator

index_calculator = IndexCalculator(boundaries, processed_datasets, weights)
boundaries_with_index = index_calculator.calculate_index(normalize=True, handle_outliers=True)
index_calculator.display_results()

# Save the results
boundaries_with_index.to_file('data/boundaries_with_index.geojson', driver='GeoJSON')
```

---

## Contributing
We welcome contributions to enhance this library! If you encounter any issues or have ideas for improvement, feel free to submit a pull request or open an issue.

---

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Contact
For any inquiries or support, please reach out to us:
- **Email**: natalyalejandra.sarmiento@polimi.it
- **GitHub**: (https://github.com/nasarmientoo/naisma_24)

---

Let the **Security Navigator Library** guide you to insightful geospatial analysis!

