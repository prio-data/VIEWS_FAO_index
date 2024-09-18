import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
from matplotlib import patheffects


import os
import sys

# Get the current working directory
current_directory = os.getcwd()

# Print the current working directory
print("The current Working Directory is:", current_directory)

# Get the path to the base directory (VIEWS_FAO_index)
base_dir = os.path.abspath(os.path.join(os.getcwd(), '..', '..'))
print(f'The base directory will be set to: {base_dir}')

# Add the base directory to sys.path
sys.path.insert(0, base_dir)

# from src.utils.functions_for_graphics.individual_graphics.map_helper.manipulate_tables_for_mapping import float_to_custom_string
# from src.utils.universal_functions.setup.build_directory import ensure_directory_exists
# from src.utils.functions_for_graphics.layout_formats.rgb import rgb_to_hex

#this is an old version --
#would be good to document the specific changes between image_map_E_i and image_save_map_E_i

def image_map_E_i(gdf, thresholds, labels, color_df, country, method, returnperiodmethod, eval_attribute, year, aggregation=1, field='percapita_100k', figure_height=3.5, figure_width=3.5, year_id=1):
    """
    Save a categorized map image based on specified thresholds and labels.

    Parameters:
    - gdf: GeoDataFrame containing geometries and data.
    - thresholds: List of numeric thresholds for categorizing data.
    - labels: List of labels corresponding to the thresholds.
    - color_df: DataFrame with labels and corresponding colors.
    - country: Country name for the title of the map.
    - method: Method used for the analysis (e.g., 'Aggregation').
    - returnperiodmethod: Method used for return period calculation (e.g., 'Cell Year').
    - year: Year of the analysis.
    - aggregation: Aggregation level (default is 1).
    - field: Field in the GeoDataFrame to be used for categorization (default is 'percapita_100k').
    - figure_height: Height of the figure (default is 3.5).
    - figure_width: Width of the figure (default is 3.5).
    """
    
    # Ensure thresholds and labels are aligned
    if len(thresholds) + 1 != len(labels):
        raise ValueError("The number of thresholds must be one less than the number of labels.")
    
    # Create a dictionary for color mapping
    color_map = dict(zip(color_df['label'], color_df['color']))
    
    # Ensure thresholds include the minimum and maximum edge values
    thresholds_with_edges = [0] + thresholds + [100000]
    
    # Assign categories to the GeoDataFrame based on thresholds
    gdf['category'] = pd.cut(
        gdf[field], 
        bins=thresholds_with_edges,  # Add `float('inf')` for the last interval
        labels=labels, 
        include_lowest=True
    )
    
    # Map colors to categories
    gdf['color'] = gdf['category'].map(color_map)
    
    # Fill NaN values with a default color (dark red)
    default_color = '#8B0000'  # Dark red
    gdf['color'].fillna(default_color, inplace=True)

    gdf = gdf.to_crs(epsg=3857)
    
    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(figure_width, figure_height))
    
    # Plot the shapefile data with classified colors
    gdf.plot(color=gdf['color'], edgecolor='darkgrey', alpha=0.8, ax=ax, legend=False)
    
    # Add basemap
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    
    # Set title and other properties
    ax.set_title(f'{country} - {method} - {returnperiodmethod} - {year}', fontsize=12)
    ax.set_axis_off()

        # Create a legend
    # Filter out the default color for the legend
    unique_color_df = color_df[~color_df['color'].isin([default_color])]
    
    # # Add legend manually
    # handles = [plt.Line2D([0], [0], marker='o', color='w', label=label, markersize=10, markerfacecolor=color_map[label]) 
    #            for label in unique_color_df['label']]
    # ax.legend(handles=handles, title="Return Period", bbox_to_anchor=(1.05, 1), loc='upper left')

    
    # Save the figure
    filename = f'{country}_{method}_{returnperiodmethod}_{eval_attribute}_{year}_map.png'
    #plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.show()
    
    print(f'Map saved as {filename}')

    # Apply transparency to values that are 0
    

# def image_save_map_E_i(gdf, thresholds, labels, color_df, country, method, returnperiodmethod, year, aggregation='1', field='percapita_100k', country_label = 'yes', figure_height=3.5, figure_width=3.5, year_id=1):
#     """
#     Save a categorized map image based on specified thresholds and labels.

#     Parameters:
#     - gdf: GeoDataFrame containing geometries and data.
#     - thresholds: List of numeric thresholds for categorizing data.
#     - labels: List of labels corresponding to the thresholds.
#     - color_df: DataFrame with labels and corresponding colors.
#     - country: Country name for the title of the map.
#     - method: Method used for the analysis (e.g., 'Aggregation').
#     - returnperiodmethod: Method used for return period calculation (e.g., 'Cell Year').
#     - year: Year of the analysis.
#     - aggregation: Aggregation level (default is 1).
#     - field: Field in the GeoDataFrame to be used for categorization (default is 'percapita_100k').
#     - figure_height: Height of the figure (default is 3.5).
#     - figure_width: Width of the figure (default is 3.5).
#     """

#     def float_to_custom_string(value):
#         return f"{value:.2f}"

#     def ensure_directory_exists(path):
#         if not os.path.exists(path):
#             os.makedirs(path)

#     figure_height_str = float_to_custom_string(figure_height)
#     figure_width_str = float_to_custom_string(figure_width)

#     aggregation_string = str(aggregation) + 'x' + str(aggregation)

#     base_directory = os.getcwd()
#     # Ensure all path components are strings

#     if aggregation == '1':
#         output_path = os.path.join(base_directory, 'files', country, method, returnperiodmethod, 'map_png')
#     else:
#         output_path = os.path.join(base_directory, 'files', country, method, returnperiodmethod, aggregation_string, 'map_png')

#     ensure_directory_exists(output_path)

#     # Ensure thresholds and labels are aligned
#     if len(thresholds) + 1 != len(labels):
#         raise ValueError("The number of thresholds must be one less than the number of labels.")
    
#     # Add the new threshold of 0.1 to separate the "zero" category
#     thresholds_with_edges = [0, 0.1] + thresholds + [float('inf')]
    
#     # Extend the labels list with "zero" for the new category
#     labels = ['zero'] + labels

#     # Create a dictionary for color mapping with RGBA values
#     color_map = dict(zip(color_df['Label'], color_df['Color']))
    
#     # Set the color for the "zero" category to white
#     color_map['zero'] = '#d5dbdb'  # White color

#     # Assign categories to the GeoDataFrame based on thresholds
#     gdf['category'] = pd.cut(
#         gdf[field], 
#         bins=thresholds_with_edges,
#         labels=labels, 
#         include_lowest=True,
    #     right=False
    # )
    
    # # Convert categories to strings to avoid TypeError
    # gdf['category'] = gdf['category'].astype(str)

    # # Map colors to categories
    # gdf['color'] = gdf['category'].map(color_map)

    # # Fill NaN values with a default color (dark red)
    # default_color = '#8B0000'  # Dark red
    # gdf['color'].fillna(default_color, inplace=True)

    # # Reproject the GeoDataFrame to Web Mercator (EPSG:3857)
    # gdf = gdf.to_crs(epsg=3857)
    
    # output_file = os.path.join(output_path, f'{country} conflict year {year_id} in {year}  with dimensions {figure_width_str}x{figure_height_str}.png')

    # fig, ax = plt.subplots(figsize=(figure_width, figure_height))
    # gdf.plot(color=gdf['color'], edgecolor='darkgrey', alpha=0.8, ax=ax, legend=False)
    # ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)


    
    # ax.set_axis_off()
    # ax.set_xlim(gdf.total_bounds[[0, 2]])
    # ax.set_ylim(gdf.total_bounds[[1, 3]])
    # ax.set_aspect('equal', adjustable='datalim')


    # if country_label == 'yes':
    #     title_text = f'{country}, {year}'
    #     text = ax.text(1, 0, title_text, transform=ax.transAxes, fontsize=10, va='bottom', ha='right')
        
    #     # Add path effect for halo
    #     text.set_path_effects([
    #         patheffects.withStroke(linewidth=3, foreground="white"),
    #         patheffects.Normal()
    #     ])

    # plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)
    # plt.show()

    # print(f'Map saved to {output_file}')


def image_save_map_E_i(gdf, thresholds, labels, color_df, country, method, returnperiodmethod, year, eval_attribute, aggregation='1', field='percapita_100k', country_label='yes', figure_height=3.5, figure_width=3.5, year_id=1):
    """
    Save a categorized map image based on specified thresholds and labels, ensuring exact dimensions.
    """

    def float_to_custom_string(value):
        return f"{value:.2f}"

    def ensure_directory_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)

    figure_height_str = float_to_custom_string(figure_height)
    figure_width_str = float_to_custom_string(figure_width)

    aggregation_string = str(aggregation) + 'x' + str(aggregation)

    base_directory = os.getcwd()

    if aggregation == '1':
        output_path = os.path.join(base_directory, 'files', country, method, returnperiodmethod, 'map_png')
    else:
        output_path = os.path.join(base_directory, 'files', country, method, returnperiodmethod, aggregation_string, 'map_png')

    ensure_directory_exists(output_path)

    # Ensure thresholds and labels are aligned
    if len(thresholds) + 1 != len(labels):
        raise ValueError("The number of thresholds must be one less than the number of labels.")
    
    # Add a new threshold of 0.1 to separate the "zero" category
    thresholds_with_edges = [0, 0.1] + thresholds + [float('inf')]
    
    # Extend the labels list with "zero" for the new category
    labels = ['zero'] + labels

    # Create a color mapping dictionary
    color_map = dict(zip(color_df['Label'], color_df['Color']))
    
    # Set color for "zero" category
    color_map['zero'] = '#d5dbdb'

    # Assign categories to the GeoDataFrame based on thresholds
    gdf['category'] = pd.cut(
        gdf[field], 
        bins=thresholds_with_edges,
        labels=labels, 
        include_lowest=True,
        right=False
    )

    gdf['category'] = gdf['category'].astype(str)

    # Map colors to categories
    gdf['color'] = gdf['category'].map(color_map)

    # Fill NaN values with a default color (dark red)
    default_color = 'lightgray'
    gdf['color'].fillna(default_color, inplace=True)

    # Reproject the GeoDataFrame to Web Mercator (EPSG:3857)
    gdf = gdf.to_crs(epsg=3857)

    output_file = os.path.join(output_path, f'{country} conflict year {year_id} in {year} investigating {eval_attribute} with dimensions {figure_width_str}x{figure_height_str}.png')

    # Create the plot with exact figure dimensions
    fig, ax = plt.subplots(figsize=(figure_width, figure_height))
    
    # Plot the data with the assigned colors
    gdf.plot(color=gdf['color'], edgecolor='darkgrey', alpha=0.8, ax=ax)

    # Use the zoom level or aspect ratio to adjust basemap within bounds
    bounds = gdf.total_bounds

    # Get the aspect ratio of the bounds
    aspect_ratio = (bounds[3] - bounds[1]) / (bounds[2] - bounds[0])

    # Set limits while ensuring the content is centered
    if aspect_ratio > 1:  # More vertical
        ax.set_xlim(bounds[0] - (aspect_ratio - 1) * (bounds[2] - bounds[0]) / 2, bounds[2] + (aspect_ratio - 1) * (bounds[2] - bounds[0]) / 2)
        ax.set_ylim(bounds[1], bounds[3])
    else:  # More horizontal
        ax.set_xlim(bounds[0], bounds[2])
        ax.set_ylim(bounds[1] - (1 - aspect_ratio) * (bounds[3] - bounds[1]) / 2, bounds[3] + (1 - aspect_ratio) * (bounds[3] - bounds[1]) / 2)

    # Ensure the aspect ratio remains fixed
    ax.set_aspect('equal', adjustable='datalim')

    # Add a basemap
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=10)

    # Hide the axis
    ax.set_axis_off()

    # If the country label is requested, add it
    if country_label == 'yes':
        title_text = f'{country}, {year}'
        text = ax.text(1, 0, title_text, transform=ax.transAxes, fontsize=10, va='bottom', ha='right')

        text.set_path_effects([
            patheffects.withStroke(linewidth=3, foreground="white"),
            patheffects.Normal()
        ])

    # Save the figure with tight layout ensuring no additional margins
    plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.show()

    print(f'Map saved to {output_file}')



def remove_duplicate_thresholds(thresholds, labels):
    """
    Remove duplicate thresholds and adjust labels accordingly,
    ensuring that all unique thresholds are preserved.

    Parameters:
    - thresholds: List of numeric thresholds.
    - labels: List of labels corresponding to the thresholds.

    Returns:
    - Unique thresholds and their corresponding labels.
    """
    unique_thresholds = []
    unique_labels = []
    
    # Track the last threshold added
    last_threshold = None
    
    for i, threshold in enumerate(thresholds):
        if threshold != last_threshold:
            unique_thresholds.append(threshold)
            unique_labels.append(labels[i])
            last_threshold = threshold

    # Add the final threshold with its corresponding label
    #unique_thresholds.append(100000)
    unique_labels.append('1 in 30 year')
    
    return unique_thresholds, unique_labels

