
#input table = gdf_merged from query_geodataframe

#thresholds# = cleaned_thresholds from provide_values_at_input_return_periods
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx

from support_functions.functions_for_graphics.individual_graphics.map_helper.manipulate_tables_for_mapping import float_to_custom_string
from support_functions.universal_functions.setup.build_directory import ensure_directory_exists
from support_functions.functions_for_graphics.layout_formats.rgb import rgb_to_hex

def image_save_map(input_table, thresholds, country, method, returnperiodmethod, year, aggregation=1, field='percapita_100k', figure_height=3.5, figure_width=3.5):
    
    figure_height_str = float_to_custom_string(figure_height)
    figure_width_str = float_to_custom_string(figure_width)

    aggregation_string = str(aggregation) + 'x' + str(aggregation)

    base_directory = os.getcwd()
    # Ensure all path components are strings

    if aggregation == 1:
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  +  '/map_png'
    else:
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod + '/' + aggregation_string  + '/map_png'

    ensure_directory_exists(output_path)

    data = input_table.copy()  # Ensure we are not modifying the original input_table

    # Example data
    labels = ['Below 1 in 10 year', '1 in 10 year', '1 in 20 year', '1 in 50 year', '1 in 100 year']

    # Define the maximum threshold label
    labels.append('Max value')
    thresholds.append(np.inf)

    # Create a dictionary to map each threshold to its label
    # We use the ceiling of each threshold value to assign the label
    threshold_dict = {}
    for i in range(len(labels)):
        if i == len(labels) - 1:  # For the last label ('Max value')
            threshold_dict[thresholds[i]] = labels[i]
        else:
            threshold_dict[thresholds[i]] = labels[i]

    # Convert the dictionary to a DataFrame
    threshold_df = pd.DataFrame(list(threshold_dict.items()), columns=['threshold', 'label'])
    # Ensure thresholds are unique and sorted
    threshold_df = threshold_df.drop_duplicates(subset='threshold').sort_values(by='threshold').reset_index(drop=True)

    # Convert columns to lists
    thresholds_list = threshold_df['threshold'].tolist()
    labels_list = threshold_df['label'].tolist()

    # Drop the last value from the labels list
    labels_list = labels_list[:-1]

    # Define the color map
    colors = {
        'Below 1 in 10 year': rgb_to_hex((211, 211, 211)),  # Light grey color
        '1 in 10 year': rgb_to_hex((81, 142, 196)),
        '1 in 20 year': rgb_to_hex((60, 6, 161)),
        '1 in 50 year': rgb_to_hex((161, 105, 199)),
        '1 in 100 year': rgb_to_hex((105, 17, 10)),
        'Max value': rgb_to_hex((0, 0, 0)),  # Black color
    }
    
    # Ensure 'Max value' is a category in the 'category' column
    data['category'] = pd.cut(data[field], bins=thresholds_list, labels=labels_list, include_lowest=True, right=False)
    
    # Set the 'category' column to be categorical with all possible labels
    data['category'] = pd.Categorical(data['category'], categories=labels_list + ['Max value'])
    
    # Map categories to colors
    data['color'] = data['category'].map(colors)
    
    # Fill NaN values in 'color' with a default color (for values above max threshold)
    data['color'] = data['color'].fillna(colors['Max value'])

    # Reproject the GeoDataFrame to Web Mercator (EPSG:3857)
    data = data.to_crs(epsg=3857)

    # Create a plot
    fig, ax = plt.subplots(figsize=(figure_width, figure_height))

    # Plot the shapefile data with classified colors
    data.plot(color=data['color'], edgecolor='darkgrey', alpha=0.8, ax=ax, legend=False)

    # Add basemap
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

    # Turn off the x and y axes labels
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.xaxis.set_tick_params(labelbottom=False)
    ax.yaxis.set_tick_params(labelleft=False)

    output_file = os.path.join(output_path, f'{country} {year} with dimensions {figure_width_str}x{figure_height_str}.png')

    # Save the plot as an image file
    plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)

    # Show the plot
    plt.show()

# def image_save_map(input_table, thresholds, country, method, returnperiodmethod, year, aggregation=0, figure_height=3.5, figure_width=3.5): #input_table = gdf, and cleaned_thresholds

#     figure_height_str = float_to_custom_string(figure_height)
#     figure_width_str = float_to_custom_string(figure_width)

#     aggregation_string = aggregation + 'x' + aggregation

#     base_directory = os.getcwd()
#     if aggregation == 0:
#         output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'map_png/'
#     else:
#         output_path = base_directory + '/files/' + country + '/' + method + '/' + aggregation_string + '/' + returnperiodmethod  + '/' + 'map_png/'

#     ensure_directory_exists(output_path)

#     data = input_table

#     # Ensure thresholds has one more element than labels
#     labels = ['Below 1 in 10 year', '1 in 10 year', '1 in 20 year', '1 in 50 year', '1 in 100 year', 'Max value']

#     # Combine thresholds and labels into a list of tuples
#     threshold_label_pairs = list(zip(thresholds, labels))

#     # Create a DataFrame from the combined list
#     thresholds_labels_df = pd.DataFrame(threshold_label_pairs, columns=['thresholds', 'labels'])

#     # Remove duplicate thresholds, but keep the correct label (keeping the last occurrence)
#     thresholds_labels_df = thresholds_labels_df.drop_duplicates(subset='thresholds', keep='last')

#     # Extract the unique thresholds and corresponding labels
#     unique_thresholds = thresholds_labels_df['thresholds'].tolist()
#     adjusted_labels = thresholds_labels_df['labels'].tolist()

#     # Define the color map
#     colors = {
#         'Below 1 in 10 year': rgb_to_hex((211, 211, 211)),  # Light grey color
#         '1 in 10 year': rgb_to_hex((81, 142, 196)),
#         '1 in 20 year': rgb_to_hex((60, 6, 161)),
#         '1 in 50 year': rgb_to_hex((161, 105, 199)),
#         '1 in 100 year': rgb_to_hex((105, 17, 10)),
#         'Max value': rgb_to_hex((0, 0, 0))  # Black color
#     }

#     # Ensure the 'Above 1 in 100 year' category is recognized
#     #data['category'] = data['category'].cat.add_categories(['Above 1 in 100 year'])
#     data['category'] = pd.cut(data['percapita_100k'], bins=unique_thresholds, labels=adjusted_labels, include_lowest=True)

#     # Map categories to colors
#     data['color'] = data['category'].map(colors)

#     # Fill NaN values in 'color' with a default color (black)
#     data['color'] = data['color'].fillna(colors['Above 1 in 100 year'])

#     # Reproject the GeoDataFrame to Web Mercator (EPSG:3857)
#     data = data.to_crs(epsg=3857)

#     # Create a plot
#     fig, ax = plt.subplots(figsize=(figure_width, figure_height))

#     # Plot the shapefile data with classified colors
#     data.plot(color=data['color'], edgecolor='darkgrey', alpha=0.8, ax=ax, legend=False)

#     # Add basemap
#     ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

#     # Turn off the x and y axes labels
#     ax.set_xlabel('')
#     ax.set_ylabel('')
#     ax.xaxis.set_tick_params(labelbottom=False)
#     ax.yaxis.set_tick_params(labelleft=False)

#     output_file = output_path + country + ' ' + str(year) + ' with dimensions ' + figure_width_str + 'x' + figure_height_str + '.png'

#     # Save the plot as an image file
#     plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)

#     # Show the plot
#     plt.show()
