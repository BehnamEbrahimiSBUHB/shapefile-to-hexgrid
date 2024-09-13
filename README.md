# shapefile-to-hexgrid

This Python script converts a shapefile into a hexagonal grid map and saves it as a TopoJSON file. It uses GeoPandas for geospatial data processing and TopoJSON for efficient storage and rendering of the hexagonal grid.

![image](https://github.com/user-attachments/assets/13d85bd3-13ae-4432-b52d-ced594a64e96)

## Maps
### 2022
* Welsh Local Authorities, 2022
![image](https://github.com/user-attachments/assets/eb1d001d-90e3-4e1b-9ad1-b8437b0207a5)
* Welsh Local Health Boards, 2022
![image](https://github.com/user-attachments/assets/94a188b0-4a4e-4af0-bc4d-22580b8977f5)
* Welsh Regions, 2022
![image](https://github.com/user-attachments/assets/f2d3c9b0-b899-490b-b8a2-cffd800a0ad7)

## Features

* Generates a hexagonal grid based on user-defined hexagon size.
* Performs a spatial join to transfer attributes from the shapefile to intersecting hexagons.
* Saves the resulting hexagonal grid map with attributes as a TopoJSON file.

## Requirements

* Python 3.7+
* geopandas
* numpy
* shapely
* tqdm
* json
* topojson

You can install these dependencies using pip:

pip install geopandas numpy shapely tqdm topojson


## Usage

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/shapefile-to-hexgrid.git
    cd shapefile-to-hexgrid
    ```
2. **Modify the script:**
    * Update the `shapefile_path` variable with the path to your input shapefile.
    * Adjust the `hex_size` variable to control the size of the hexagons (in degrees).
    * Change the `output_path` variable to specify the desired file name and location for the output TopoJSON file.
3.  **Run the script:**

    ```bash
    python shape2hex2.py 
    ```

## Example

```python
# Example usage:
shapefile_path = "path/to/your/shapefile.shp"
hex_size = 0.05  # Adjust the hexagon size as needed
output_path = "output/hex_map.topojson" 
generate_hex_map(shapefile_path, hex_size, output_path)
```

## Output

The script will generate a TopoJSON file containing the hexagonal grid map with attributes from the original shapefile. This file can be used for visualization and analysis in mapping libraries like Leaflet, D3.js, or Mapbox.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
