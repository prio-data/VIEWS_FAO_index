import os
import pandas as pd
import matplotlib.pyplot as plt
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


from src.utils.universal_functions.setup.build_directory import float_to_custom_string, ensure_directory_exists

#import: query_and_sort_annual_table from universal folder / FAO / generate output tables
from src.utils.universal_functions.setup.build_directory import float_to_custom_string, ensure_directory_exists


#from src.utils.functions_for_graphics.individual_graphics.map_helper.manipulate_tables_for_mapping import query_and_sort_annual_table, provide_values_at_input_return_periods, retrieve_geodataframe, define_year_to_map, query_geodataframe
from src.utils.functions_for_graphics.layout_formats.rgb import rgb_to_hex

#from src.utils.functions_for_graphics.individual_graphics.image_map import image_save_map

# def image_save_returnperiodtable(input_table, country, method, returnperiodmethod, aggregation=1, figure_height=1.75, figure_width=2.5,): #input_table = Jerry_table

#     figure_height_str = float_to_custom_string(figure_height)
#     figure_width_str = float_to_custom_string(figure_width)

#     aggregation_string = str(aggregation) + 'x' + str(aggregation)


#     base_directory = os.getcwd()
#     if aggregation == 1:
#         output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'table_png/percentile and payout table/'
#     else:
#         output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod + '/' + aggregation_string  + '/' + 'table_png/percentile and payout table/'

#     ensure_directory_exists(output_path)

#     df = input_table.rename(columns={'percapita_100k':'Fatalities P.C. '})

#     colors = {
#         '90': rgb_to_hex((81, 142, 196)),
#         '95': rgb_to_hex((60, 6, 161)),
#         '98': rgb_to_hex((161, 105, 199)),
#         '99': rgb_to_hex((105, 17, 10))
#     }
#     light_grey = rgb_to_hex((211, 211, 211))  # Light grey color
#     dark_grey = rgb_to_hex((64, 64, 64))  # Dark grey color

#     # Plot the table
#     fig, ax = plt.subplots(figsize=(figure_width, figure_height))  # Size in inches (width, height)
#     ax.axis('tight')
#     ax.axis('off')

#     # Create the table
#     table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

#     # Adjust table properties
#     table.auto_set_font_size(False)  # Disable automatic font size
#     table.set_fontsize(8)  # Set font size

#     # Calculate cell widths and heights to fit the figure size exactly
#     n_rows, n_cols = df.shape
#     cell_width = 2.5 / n_cols
#     cell_height = 1.75 / (n_rows + 1)  # +1 for the header row

#     # Set the size of each cell
#     for i in range(n_rows + 1):
#         for j in range(n_cols):
#             table[(i, j)].set_width(cell_width)
#             table[(i, j)].set_height(cell_height)

#     for j in range(n_cols):
#         table[(0, j)].set_facecolor(dark_grey)
#         table[(0, j)].set_text_props(color='white')

#     # Apply colors to the cells based on the 'percentile' column
#     percentile_col_idx = df.columns.get_loc('Percentile')
#     for i in range(1, n_rows + 1):  # Skip header row
#         percentile_value = df.iloc[i - 1, percentile_col_idx]
#         if percentile_value in colors:
#             color = colors[percentile_value]
#         else:
#             color = light_grey
#         for j in range(n_cols):
#             table[(i, j)].set_facecolor(color)
#             table[(i, j)].set_text_props(color='white' if color != light_grey else 'black')

#     output_file = output_path + country +' with dimensions ' + figure_width_str + 'x' + figure_height_str
#     # Save the table as PNG with exact size and no white space
#     plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)

#     # Show the table plot
#     plt.show()

def image_save_returnperiodtable(input_table, colors, column_to_apply_symbology, country, method, returnperiodmethod, aggregation='1', figure_height=1.75, figure_width=2.5): #input_table = Jerry_table

    figure_height_str = float_to_custom_string(figure_height)
    figure_width_str = float_to_custom_string(figure_width)

    aggregation_string = str(aggregation) + 'x' + str(aggregation)


    base_directory = os.getcwd()
    if aggregation == '1':
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'table_png/percentile and payout table/'
    else:
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod + '/' + aggregation_string  + '/' + 'table_png/percentile and payout table/'

    ensure_directory_exists(output_path)

    df = input_table.rename(columns={'percapita_100k':'Fatalities P.C.'})


    light_grey = rgb_to_hex((211, 211, 211))  # Light grey color
    dark_grey = rgb_to_hex((64, 64, 64))  # Dark grey color

    # Plot the table
    fig, ax = plt.subplots(figsize=(figure_width, figure_height))  # Size in inches (width, height)
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    # Adjust table properties
    table.auto_set_font_size(False)  # Disable automatic font size
    table.set_fontsize(8)  # Set font size

    # Calculate cell widths and heights to fit the figure size exactly
    n_rows, n_cols = df.shape
    cell_width = 2.5 / n_cols
    cell_height = 1.75 / (n_rows + 1)  # +1 for the header row

    # Set the size of each cell
    for i in range(n_rows + 1):
        for j in range(n_cols):
            table[(i, j)].set_width(cell_width)
            table[(i, j)].set_height(cell_height)

    for j in range(n_cols):
        table[(0, j)].set_facecolor(dark_grey)
        table[(0, j)].set_text_props(color='white')

    # Apply colors to the cells based on the 'percentile' column
    percentile_col_idx = df.columns.get_loc(column_to_apply_symbology)
    for i in range(1, n_rows + 1):  # Skip header row
        percentile_value = df.iloc[i - 1, percentile_col_idx]
        if percentile_value in colors:
            color = colors[percentile_value]
        else:
            color = light_grey
        for j in range(n_cols):
            table[(i, j)].set_facecolor(color)
            table[(i, j)].set_text_props(color='white' if color != light_grey else 'black')

    output_file = output_path + country +' with dimensions ' + figure_width_str + 'x' + figure_height_str + '.png'
    # Save the table as PNG with exact size and no white space
    plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)

    # Show the table plot
    plt.show()