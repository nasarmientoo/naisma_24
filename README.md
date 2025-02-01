# Security Navigator Library

Welcome to the **Security Navigator Library**, your go-to geospatial tool for analyzing, managing, and visualizing security-related data. This library offers an intuitive and robust framework to process geospatial datasets, calculate security indices, and generate actionable insights for decision-making.

## Features
- **Data Loader**: Load and validate boundaries and datasets in various geospatial formats.
- **Weight Manager**: Define and apply severities and weights to attributes in datasets.
- **Index Calculator**: Calculate and normalize security indices for geospatial polygons.
- **GeoUtils**: Handle advanced geospatial operations such as centroid calculation and filtering polygons based on conditions.
- **Visualizer**: Generate a variety of visualizations, including:
    - Choropleth maps with customizable color palettes.
    - Density maps to visualize the spatial distribution of points.
    - Histograms for attribute distribution analysis.
    - Centroid maps for polygon visualization.


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


### 4. **Visualier**
The `Visualizer` module provides tools to create visual representations of your geospatial data. You can generate choropleth maps, density maps, histograms, and centroid maps to gain insights into the spatial distribution of your data.

#### Key Features:
- Generate choropleth maps for geospatial polygons using customizable color palettes.
- Plot density maps to visualize the density of point-based datasets.
- Create histograms to understand the distribution of specific attributes.
- Plot centroids of polygons with optional boundary overlays.

#### Examples
#### Choropleth Map:
```python
from src.visualizer import Visualizer

Visualizer.plot_choropleth(
    geodataframe=boundaries_with_index,
    column="security_index",
    title="Security Index Map",
    boundaries=boundaries,  
    cmap="viridis",  # Using a built-in Matplotlib colormap
    save_path="outputs/security_index_map.png"
)
```
#### Choropleth Map with Custom Color Palette:
```python
from src.visualizer import Visualizer

custom_palette = ["#f7fcf0", "#ccebc5", "#a8ddb5", "#7bccc4", "#43a2ca", "#0868ac"]

Visualizer.plot_choropleth(
    geodataframe=boundaries_with_index,
    column="security_index",
    title="Security Index Map with Custom Colors",
    boundaries=boundaries,
    cmap=custom_palette,  # Using a custom color palette
    save_path="outputs/security_index_map_with_custom_palette.png"
)
```
#### Density Map:
```python
from src.visualizer import Visualizer

Visualizer.plot_density(
    processed_datasets[0],
    boundaries=boundaries,
    title="Point Density Map",
    save_path="outputs/crime_density_heatmap.png"
)
```
#### Histogram:
```python
from src.visualizer import Visualizer

Visualizer.plot_histogram(
    data=boundaries_with_index,
    column="security_index",
    bins=15,  # Number of bins
    title="Security Index Histogram",
    xlabel="Security Index",
    save_path="outputs/security_index_histogram.png"
)

```
#### Centroid Map:
```python
from src.visualizer import Visualizer

Visualizer.plot_centroids(
    centroid_geodataframe=centroid_boundaries,
    boundaries=boundaries,  # Optional: Overlay boundaries
    title="Centroids of Security Zones",
    save_path="outputs/centroids_map.png"
)

```
# Security Navigator Library - Testing Guide

## Overview
This document provides an in-depth overview of the testing scripts for the **Security Navigator Library**. This library includes modules for loading geospatial data, applying weighted attributes, calculating security indices, and visualizing the results. These tests ensure that all components function correctly, handle edge cases properly, and integrate smoothly within the system.

## Testing Scripts
The following test scripts validate both the individual functionalities of each module and the complete pipeline of the library:

### 1. `test_data_loader.py`
**Purpose:**
- Validates the loading of boundary files (GeoJSON, Shapefile, GeoPackage).
- Ensures point-based datasets (CSV) are correctly converted to GeoDataFrames.
- Checks for required columns (`LONGITUDE`, `LATITUDE`).
- Tests handling of empty or malformed files.
- Verifies that out-of-bound points are properly filtered.

**Run Command:**
```bash
pytest tests/test_data_loader.py
```

---
### 2. `test_weight_manager.py`
**Purpose:**
- Ensures that weights are correctly normalized to sum to 1.
- Verifies severity mappings are correctly applied to attributes.
- Checks behavior when attributes are missing or contain unexpected values.
- Tests handling of empty and malformed datasets.
- Confirms that severity multipliers correctly influence security index calculations.

**Run Command:**
```bash
pytest tests/test_weight_manager.py
```

---
### 3. `test_index_calculator.py`
**Purpose:**
- Validates security index calculations based on weighted attributes.
- Ensures normalization and outlier handling work correctly.
- Tests with missing attributes or invalid datasets.
- Verifies that index calculations scale appropriately across different dataset sizes.
- Ensures that polygonal spatial joins correctly associate data with boundaries.

**Run Command:**
```bash
pytest tests/test_index_calculator.py
```

---
### 4. `test_visualizer.py`
**Purpose:**
- Ensures that choropleth, density, and histogram plots are generated correctly.
- Checks that plots are saved as images in the expected directories.
- Tests invalid or empty datasets for graceful error handling.
- Confirms that custom color palettes are applied correctly.
- Validates that density maps represent data distribution accurately.

**Run Command:**
```bash
pytest tests/test_visualizer.py
```

---
### 5. `test_pipeline.py`
**Purpose:**
- Tests full integration of all modules in sequence.
- Loads test boundary and dataset files and validates preprocessing steps.
- Applies weight processing and ensures consistency across datasets.
- Computes security indices and checks expected results against baseline values.
- Generates and validates visual outputs, ensuring correct file exports.
- Handles potential errors that could disrupt the full pipeline execution.

**Run Command:**
```bash
pytest tests/test_pipeline.py
```

## Running All Tests
To execute all tests at once, use:
```bash
pytest tests/
```

For more detailed output, run:
```bash
pytest -v tests/
```

## Coverage Analysis
To analyze test coverage and identify untested code paths, install and use `pytest-cov`:
```bash
pip install pytest-cov
pytest --cov=src tests/
```
This will generate a report showing how much of the code is tested.

## Additional Notes
- Ensure all required dependencies are installed before running tests:
  ```bash
  pip install -r requirements.txt
  ```
- Run tests inside a virtual environment to avoid conflicts with system dependencies:
  ```bash
  python -m venv env
  source env/bin/activate  # Windows: env\Scripts\activate
  ```
- If tests fail, use `pytest --tb=short` to get a concise traceback of errors.
- To rerun only failed tests:
  ```bash
  pytest --lf
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
- **Email**: natalyalejandra.sarmiento@mail.polimi.it, mariafernanda.molina@mail.polimi.it, claudiaisabela.saud@mail.polimi.it
- **GitHub**: (https://github.com/nasarmientoo/naisma_24)

---

Let the **Security Navigator Library** guide you to insightful geospatial analysis!

