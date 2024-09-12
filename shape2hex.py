import geopandas as gpd  # Import the geopandas library for geospatial data handling.
import numpy as np  # Import numpy for numerical operations.
from shapely.geometry import Polygon  # Import Polygon from shapely to create hexagon geometries.
from tqdm import tqdm  # Import tqdm to display a progress bar during hexagon generation.
import json  # Import json to work with GeoJSON data.
import topojson as tp  # Import topojson to convert GeoJSON to TopoJSON.

def create_hex_grid(minx, miny, maxx, maxy, hex_size):
    """
    Generates a hexagonal grid covering the specified bounding box.

    Args:
        minx (float): Minimum longitude of the bounding box.
        miny (float): Minimum latitude of the bounding box.
        maxx (float): Maximum longitude of the bounding box.
        maxy (float): Maximum latitude of the bounding box.
        hex_size (float): Size of each hexagon edge, in degrees.

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing the hexagonal grid.
    """
    width = hex_size * 2  # Calculate the width of each hexagon.
    height = np.sqrt(3) * hex_size  # Calculate the height of each hexagon.
    cols = int((maxx - minx) / width) + 1  # Calculate the number of columns in the grid.
    rows = int((maxy - miny) / height) + 1  # Calculate the number of rows in the grid.
    hexagons = []  # Initialize an empty list to store the hexagon polygons.
    for col in tqdm(range(cols), desc="Generating hexagons"):  # Iterate over columns with a progress bar.
        for row in range(rows):  # Iterate over rows.
            x = minx + col * width * 0.75  # Calculate the x-coordinate of the hexagon center.
            y = miny + row * height + (col % 2) * (height / 2)  # Calculate the y-coordinate of the hexagon center, adjusting for offset rows.
            hexagon = Polygon([
                (x, y),  # Define the vertices of the hexagon polygon.
                (x + hex_size, y),
                (x + 1.5 * hex_size, y + height / 2),
                (x + hex_size, y + height),
                (x, y + height),
                (x - 0.5 * hex_size, y + height / 2)
            ])
            hexagons.append(hexagon)  # Add the hexagon polygon to the list.
    return gpd.GeoDataFrame(geometry=hexagons, crs="EPSG:4326")  # Create and return a GeoDataFrame from the hexagon polygons with the specified coordinate system.

def generate_hex_map(shapefile_path, hex_size, output_path):
    """
    Generates a hexagonal tile map from a shapefile, performs a spatial join to map attributes
    from the shapefile to the hexagons, and saves the result as a TopoJSON file.

    Args:
        shapefile_path (str): Path to the input shapefile.
        hex_size (float): Size of each hexagon edge, in degrees.
        output_path (str): Path to save the output TopoJSON file. 
    """
    gdf = gpd.read_file(shapefile_path)  # Read the shapefile into a GeoDataFrame.
    gdf = gdf.to_crs(epsg=4326)  # Convert the coordinate system of the GeoDataFrame to WGS84 (EPSG:4326).

    minx, miny, maxx, maxy = gdf.total_bounds  # Get the bounding box of the GeoDataFrame.

    hex_grid = create_hex_grid(minx, miny, maxx, maxy, hex_size)  # Generate the hexagonal grid using the bounding box and hexagon size.

    hex_grid_with_attributes = gpd.sjoin(hex_grid, gdf, how="inner", predicate="intersects")  # Perform a spatial join between the hex grid and the shapefile, keeping only intersecting hexagons and their attributes.
    hex_grid_with_attributes = hex_grid_with_attributes.reset_index()  # Reset the index of the GeoDataFrame after the spatial join.
    
    geojson_data = hex_grid_with_attributes.to_json()  # Convert the GeoDataFrame with attributes to GeoJSON format.

    topojson_output = tp.Topology(json.loads(geojson_data), prequantize=False)  # Convert the GeoJSON data to TopoJSON format.

    with open(output_path, "w") as f:
        json.dump(topojson_output.to_dict(), f)  # Save the TopoJSON data to the specified output file.

    print(f"Hexagonal tile map with attributes saved as {output_path}")  # Print a confirmation message with the output file path.

# Example usage:
shapefile_path = "wales_lsoa_2021.shp"  # Define the path to the input shapefile.
hex_size = 0.05  # Set the desired hexagon size in degrees.
output_path = "LSOA_wales_hex_map.topojson"  # Define the desired output file path for the TopoJSON file.
generate_hex_map(shapefile_path, hex_size, output_path)  # Call the function to generate the hexagonal tile map.