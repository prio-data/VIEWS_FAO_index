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


from src.utils.functions_for_graphics.layout_formats.rgb import rgb_to_hex

    # Function to determine the color based on the ranges

def get_color(value, ranges, rgb_colors):
        for lower, upper, percentile in ranges:
            if lower <= value < upper:
                return rgb_colors.get(percentile, None)
        return None

def image_save_annualsummary_table(input_table, thresholds, country, method, returnperiodmethod, aggregation=0, figure_height=5.5, figure_width=4.0, number_of_rows=15, attribute='first_value'):
    def query_and_sort_annual_table(table, attr, rows):
        return table.nlargest(rows, attr)

    figure_height_str = float_to_custom_string(figure_height)
    figure_width_str = float_to_custom_string(figure_width)

    aggregation_string = aggregation + 'x' + aggregation

    base_directory = os.getcwd()
    if aggregation == '1':
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  +  '/table_png/annual summary table'
    else:
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod + '/' + aggregation_string  + '/table_png/annual summary table'

    ensure_directory_exists(output_path)

    top_n_years = query_and_sort_annual_table(input_table, attribute, number_of_rows)

    dark_grey = rgb_to_hex((64, 64, 64))
    light_grey = rgb_to_hex((211, 211, 211))
    black = rgb_to_hex((0, 0, 0))

    df_rounded = top_n_years.round(1)
    df_rounded = df_rounded.rename(columns={'year': 'Year', 'first_value': 'First', 'second_value': 'Second', 'third_value': 'Third', 'average_value': 'Avg.'})

    fig, ax = plt.subplots(figsize=(figure_width, figure_height))

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    table = ax.table(cellText=df_rounded.values, colLabels=df_rounded.columns, cellLoc='center', loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(6)
    table.scale(1, 1.5)

    for key, cell in table.get_celld().items():
        if key[0] == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(dark_grey)
        if key[1] == 0:
            cell.set_text_props(color='white')
            cell.set_facecolor(dark_grey)

    rgb_colors = {
        0: light_grey,
        1: rgb_to_hex((81, 142, 196)),
        2: rgb_to_hex((60, 6, 161)),
        3: rgb_to_hex((161, 105, 199)),
        4: rgb_to_hex((105, 17, 10)),
        5: black
    }

    def get_color(value, thresholds, rgb_colors):
        for i in range(len(thresholds) - 1):
            if thresholds[i] <= value < thresholds[i + 1]:
                return rgb_colors[i]
        if value >= thresholds[-1]:
            return rgb_colors[len(thresholds) - 1]
        return rgb_colors[0]

    # Iterating through each cell to set the color based on the thresholds
    for i in range(df_rounded.shape[0]):
        for j in range(1, df_rounded.shape[1]):
            value = df_rounded.iloc[i, j]
            color = get_color(value, thresholds, rgb_colors)
            table[(i+1, j)].set_facecolor(color)
            if color != light_grey:
                table[(i+1, j)].set_text_props(color='white')

    output_file = os.path.join(output_path, f'{country} top{number_of_rows} summarized by {attribute} with dimensions {figure_height_str}x{figure_width_str}.png')
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.show()

def plot_and_colorize_annual_table(annual_df, info_df, country, method, returnperiodmethod, aggregation, figure_height=5.5, figure_width=4.0):


    figure_height_str = float_to_custom_string(figure_height)
    figure_width_str = float_to_custom_string(figure_width)

    aggregation_string = str(aggregation) + 'x' + str(aggregation)

    base_directory = os.getcwd()
    # Ensure all path components are strings

    if aggregation == 1:
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  +  '/table_png'
    else:
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod + '/' + aggregation_string  + '/table_png'

    ensure_directory_exists(output_path)


    # Step 1: Create a color map from info_df
    def create_color_map(df):
        color_map = {}
        for _, row in df.iterrows():
            start, end = map(float, row['Range'].split(' - '))
            color_map[(start, end)] = row['Color']
        return color_map
    
    color_map = create_color_map(info_df)

    # Step 2: Define the function to apply colors
    def get_color(value, color_map):
        for (start, end), color in color_map.items():
            if start <= value < end:
                return color
        return '#FFFFFF'  # Default color if not found

    def colorize_dataframe(df, color_map):
        colored_df = df.copy()
        for column in df.columns[1:]:  # Skip the 'year' column
            colored_df[f'{column}_color'] = df[column].apply(lambda x: get_color(x, color_map))
        return colored_df

    # Step 3: Format numeric values to one decimal place
    def format_dataframe(df):
        formatted_df = df.copy()
        for column in df.columns[1:]:  # Skip the 'year' column
            formatted_df[column] = formatted_df[column].apply(lambda x: f'{x:.1f}')
        return formatted_df

    colored_df = colorize_dataframe(annual_df, color_map)
    formatted_annual_df = format_dataframe(annual_df)

    output_file = os.path.join(output_path, f'{country} Annual Summary Image with dimensions {figure_width_str}x{figure_height_str}.png')

    # Step 4: Plot and save the colored table
    fig, ax = plt.subplots(figsize=(figure_width, figure_height))

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    # Create a table from the formatted DataFrame
    table = ax.table(cellText=formatted_annual_df.values, colLabels=formatted_annual_df.columns, cellLoc='center', loc='center')

    # Apply colors to the table cells
    for (i, j), cell in table.get_celld().items():
        if i > 0:  # Skip the header row
            column_name = annual_df.columns[j]
            if f'{column_name}_color' in colored_df.columns:
                cell_color = colored_df.iloc[i - 1][f'{column_name}_color']
                cell.set_facecolor(cell_color)
                if cell_color != '#d5dbdb':  # Set text color if cell is colored
                    cell.set_text_props(color='white')
                    if cell_color == '#FFFFFF':
                        cell.set_text_props(color='black')
                else:
                    cell.set_text_props(color='black')
    
    dark_grey = rgb_to_hex((64, 64, 64))
    for key, cell in table.get_celld().items():
        if key[0] == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(dark_grey)
        if key[1] == 0:
            cell.set_text_props(color='white')
            cell.set_facecolor(dark_grey)

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    # Adjust the scale to fit the specified figure size
    table.scale(1, 1.5)

    # Adjust row heights and column widths

    #plt.title('Annual Summary Table with Colors')
    plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.show()
# Example usage:
#thresholds = [0.0, 3.6, 14.1, 47.3, 113.1, 6774.6]
