import pandas as pd
import matplotlib.pyplot as plt
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



from src.utils.universal_functions.setup.build_directory import float_to_custom_string, ensure_directory_exists
from src.utils.functions_for_graphics.individual_graphics.map_helper.manipulate_tables_for_mapping import provide_values_at_input_return_periods, calculate_histogram_data
from src.utils.functions_for_graphics.layout_formats.rgb import rgb_to_hex


def float_to_custom_string(value):
    return f"{value:.1f}"

def insurance_lineplot(main_method_dataframe, insurance_table, thresholds, country, method, returnperiodmethod, aggregation=1, field='percapita_100k', figure_height=3.0, figure_width=6.0):
    figure_height_str = float_to_custom_string(figure_height)
    figure_width_str = float_to_custom_string(figure_width)

    aggregation_string = str(aggregation) + 'x' + str(aggregation)

    base_directory = os.getcwd()
    if aggregation == 1:
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'lineplot_png/Payout occurrence graph/'
    else:
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod + '/' + aggregation_string  + '/' + 'lineplot_png/Payout occurrence graph/'

    ensure_directory_exists(output_path)

    min_year = min(main_method_dataframe['year'])
    start_year = (min_year // 5) * 5

    # Initialize main_method_dataframe_renamed with main_method_dataframe
    main_method_dataframe_renamed = main_method_dataframe

    # If the field name 'GIS__Index' exists, we will then convert it to 'priogrid_gid'
    check_fieldname = 'GIS__Index'
    if check_fieldname in main_method_dataframe.columns:
        main_method_dataframe_renamed = main_method_dataframe.rename(columns={check_fieldname: 'priogrid_gid'})

    relevant_data = main_method_dataframe_renamed[['priogrid_gid', 'year', field]]

    cleaned_thresholds = provide_values_at_input_return_periods(insurance_table, field)

    # Define the thresholds
    # thresholds = [4.3, 30.7, 113.7, 290.4]

    for i in range(len(cleaned_thresholds) - 1):
        lower_threshold = cleaned_thresholds[i]
        upper_threshold = cleaned_thresholds[i + 1]
        col_name = f'count_{lower_threshold}_to_{upper_threshold}'
        relevant_data[col_name] = ((relevant_data[field] >= lower_threshold) &
                                   (relevant_data[field] < upper_threshold)).astype(int)

    # Create a column for values above the last threshold
    col_name = f'count_above_{cleaned_thresholds[-1]}'
    relevant_data[col_name] = (relevant_data[field] >= cleaned_thresholds[-1]).astype(int)

    # Group by year and sum the counts
    grouped_data = relevant_data.groupby(['year']).sum().reset_index()

    # Drop the 'priogrid_gid' column from the grouped data as it is not needed in the result
    grouped_data = grouped_data.drop(columns='priogrid_gid')

    columns_to_drop = [field, f'count_{cleaned_thresholds[0]}_to_{cleaned_thresholds[1]}']

    # Drop the identified columns
    grouped_data = grouped_data.drop(columns=columns_to_drop, errors='ignore')

    colors = [
        # (177.0/255, 218.0/255, 165.0/255),  # RGB for 5 yr
        rgb_to_hex((81, 142, 196)),  # RGB for 10y
        rgb_to_hex((60, 6, 161)),  # RGB for 20y
        rgb_to_hex((161, 105, 199)),  # RGB for 50y
        rgb_to_hex((105, 17, 10))    # RGB for 100y
    ]

    # Set the x-axis column and y-axis columns
    x_column = 'year'  # Replace with the name of your x-axis column
    y_columns = grouped_data.columns.drop(x_column)  # All columns except the x-axis column
    
    output_file = output_path + country + ' with dimensions ' + figure_width_str + 'x' + figure_height_str + '.png'

    # Plot the data
    plt.figure(figsize=(figure_width, figure_height))

    for y_column, color in zip(y_columns, colors):
        plt.plot(grouped_data[x_column], grouped_data[y_column], label=y_column, color=color)

    plt.xlabel('Year')
    plt.ylabel('Payout Occurrence')
    plt.title('Annual Count of Return Periods')

    # Set the x-axis ticks to show every 5 years starting from the start year
    plt.xticks(ticks=range(start_year, grouped_data[x_column].max() + 1, 5), 
               labels=range(start_year, grouped_data[x_column].max() + 1, 5), 
               rotation=45)

    plt.gcf().set_facecolor('none')
    plt.grid(True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)

    plt.show()

# def lineplot_frominfo(table, info_dataframe, country, method, returnperiodmethod, aggregation, value_field='percapita_100k', labels_to_omit='Below 1 in 10 year', figure_height=3.0, figure_width=6.0):

#     figure_height_str = float_to_custom_string(figure_height)
#     figure_width_str = float_to_custom_string(figure_width)

#     aggregation_string = str(aggregation) + 'x' + str(aggregation)

#     base_directory = os.getcwd()
#     # Ensure all path components are strings

#     if aggregation == '1':
#         output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  +  '/plot_png'
#     else:
#         output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod + '/' + aggregation_string  + '/plot_png'

#     ensure_directory_exists(output_path)


# #WE DO NOT WANT TO PRINT LABELS THAT HAVE A RANGE STARTING AT 0!
# # Initialize the list
#     list_of_labels_to_omit = []

#     # Check if any range starts with '0.0' and add corresponding labels to labels_to_omit
#     for index, row in info_dataframe.iterrows():
#         if row['Range'].startswith('0.0'):
#             list_of_labels_to_omit.append(row['Label'])

#     # Additional label to omit

#     # Append the additional label to the list
#     list_of_labels_to_omit.append(labels_to_omit)
# #------------------------------------------------------------------------------------
#     # Initialize results dictionary
#     results = {'year': [], 'Label': [], 'count': []}

#     # Debug: print unique years from table
#     print("Unique years in table:", table['year'].unique())

#     # Debug: print initial info_dataframe
#     print("Initial info_dataframe:\n", info_dataframe)

#     # Iterate over each year and range to count occurrences
#     for year in table['year'].unique():
#         for _, row in info_dataframe.iterrows():
#             range_start, range_end = map(float, row['Range'].split(' - '))
#             label = row['Label']

#             # Debug: print current label and range being processed
#             print(f"Processing: Year: {year}, Label: {label}, Range: {range_start} - {range_end}")

#             count = table[(table['year'] == year) & 
#                           (table[value_field] >= range_start) & 
#                           (table[value_field] < range_end)].shape[0]

#             results['year'].append(year)
#             results['Label'].append(label)
#             results['count'].append(count)

#     # Convert results to DataFrame
#     results_df = pd.DataFrame(results)

#     # Debug: print results_df before merging
#     print("Results DataFrame before merging:\n", results_df)

#     # Merge with info_df to add Color column
#     results_df = results_df.merge(info_dataframe[['Label', 'Color']], on='Label', how='left')

#     # Debug: print results_df after merging
#     print("Results DataFrame after merging:\n", results_df)

#     # Filter out the 'Below 1 in 10 year' label
#     results_df = results_df[~results_df['Label'].isin(list_of_labels_to_omit)]

#     # Debug: print results_df after filtering
#     print("Results DataFrame after filtering:\n", results_df)

#     results_df = results_df.sort_values(by='year')

#     output_file = os.path.join(output_path, f'{country} Annual Return Period LinePlot with dimensions {figure_width_str}x{figure_height_str}.png')

#     # Plotting
#     plt.figure(figsize=(6, 3))
#     line_widths = [4, 3, 2, 1]  # Define line widths
#     labels = results_df['Label'].unique()
    
#     # Adjust the number of widths if there are more labels
#     if len(labels) > len(line_widths):
#         line_widths = [1.0 + 0.1 * i for i in range(len(labels))]

#     # Reverse the order of labels for plotting thicker lines first
#     labels = labels[::-1]
    
#     for i, label in enumerate(labels):
#         subset = results_df[results_df['Label'] == label]
#         plt.plot(subset['year'], subset['count'], label=label, color=subset['Color'].iloc[0], linewidth=line_widths[i % len(line_widths)])


#     # for label in results_df['Label'].unique():
#     #     subset = results_df[results_df['Label'] == label]
#     #     plt.plot(subset['year'], subset['count'], label=label, color=subset['Color'].iloc[0])

#     plt.xlabel('Year')
#     plt.ylabel('Count')
#     plt.title('Occurrences by Year and Return Period Label')
#     plt.grid(True)

#     fig = plt.gcf()  # Get the current figure
#     fig.patch.set_facecolor('white')  # Set the figure's face color to white


#     plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)

#     plt.show()
    

def lineplot_frominfo(table, info_dataframe, country, method, returnperiodmethod, aggregation, value_field='percapita_100k', labels_to_omit='Below 1 in 10 year', figure_height=3.0, figure_width=6.0):

    figure_height_str = float_to_custom_string(figure_height)
    figure_width_str = float_to_custom_string(figure_width)

    aggregation_string = str(aggregation) + 'x' + str(aggregation)

    base_directory = os.getcwd()
    # Ensure all path components are strings

    if aggregation == '1':
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  +  '/plot_png'
    else:
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod + '/' + aggregation_string  + '/plot_png'

    ensure_directory_exists(output_path)


#WE DO NOT WANT TO PRINT LABELS THAT HAVE A RANGE STARTING AT 0!
# Initialize the list
    list_of_labels_to_omit = []

    # Check if any range starts with '0.0' and add corresponding labels to labels_to_omit
    for index, row in info_dataframe.iterrows():
        if row['Range'].startswith('0.0'):
            list_of_labels_to_omit.append(row['Label'])

    # Additional label to omit

    # Append the additional label to the list
    list_of_labels_to_omit.append(labels_to_omit)
#------------------------------------------------------------------------------------
    # Initialize results dictionary
    results = {'year': [], 'Label': [], 'count': []}

    # Debug: print unique years from table
    print("Unique years in table:", table['year'].unique())

    # Debug: print initial info_dataframe
    print("Initial info_dataframe:\n", info_dataframe)

    # Iterate over each year and range to count occurrences
    for year in table['year'].unique():
        for _, row in info_dataframe.iterrows():
            range_start, range_end = map(float, row['Range'].split(' - '))
            label = row['Label']

            # Debug: print current label and range being processed
            print(f"Processing: Year: {year}, Label: {label}, Range: {range_start} - {range_end}")

            count = table[(table['year'] == year) & 
                          (table[value_field] >= range_start) & 
                          (table[value_field] < range_end)].shape[0]

            results['year'].append(year)
            results['Label'].append(label)
            results['count'].append(count)

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    # Debug: print results_df before merging
    print("Results DataFrame before merging:\n", results_df)

    # Merge with info_df to add Color column
    results_df = results_df.merge(info_dataframe[['Label', 'Color']], on='Label', how='left')

    # Debug: print results_df after merging
    print("Results DataFrame after merging:\n", results_df)

    # Filter out the 'Below 1 in 10 year' label
    results_df = results_df[~results_df['Label'].isin(list_of_labels_to_omit)]

    # Debug: print results_df after filtering
    print("Results DataFrame after filtering:\n", results_df)

    results_df = results_df.sort_values(by='year')

    output_file = os.path.join(output_path, f'{country} Annual Return Period LinePlot with dimensions {figure_width_str}x{figure_height_str}.png')

    # Plotting
    plt.figure(figsize=(6, 3))
    line_widths = [4, 3, 2, 1]  # Define line widths
    labels = results_df['Label'].unique()
    
    # Adjust the number of widths if there are more labels
    if len(labels) > len(line_widths):
        line_widths = [1.0 + 0.1 * i for i in range(len(labels))]

    # Reverse the order of labels for plotting thicker lines first
    labels = labels[::-1]
    
    for i, label in enumerate(labels):
        subset = results_df[results_df['Label'] == label]
        plt.plot(subset['year'], subset['count'], label=label, color=subset['Color'].iloc[0], linewidth=line_widths[i % len(line_widths)])


    # for label in results_df['Label'].unique():
    #     subset = results_df[results_df['Label'] == label]
    #     plt.plot(subset['year'], subset['count'], label=label, color=subset['Color'].iloc[0])

    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.title('Occurrences by Year and Return Period Label')
    plt.grid(True)

    fig = plt.gcf()  # Get the current figure
    fig.patch.set_facecolor('white')  # Set the figure's face color to white


    plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.05)

    plt.show()

from matplotlib.ticker import MaxNLocator

def plot_histogram_with_lineplot_4(df, info_dataframe, country, method, returnperiodmethod, aggregation, value_field='percapita_100k', labels_to_omit='Below 1 in 10 year', figure_height=3.0, figure_width=6.0, histogram='on'):
    figure_height_str = float_to_custom_string(figure_height)
    figure_width_str = float_to_custom_string(figure_width)

    aggregation_string = str(aggregation) + 'x' + str(aggregation)

    base_directory = os.getcwd()

    if aggregation == '1':
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  +  '/plot_png'
    else:
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod + '/' + aggregation_string  + '/plot_png'

    ensure_directory_exists(output_path)

    output_file = os.path.join(output_path, f'{country} Annual Return Period LinePlot with dimensions {figure_width_str}x{figure_height_str}.png')

    # Calculate histogram data
    df_histogram = calculate_histogram_data(df)

    # Initialize the list of labels to omit
    list_of_labels_to_omit = []
    for index, row in info_dataframe.iterrows():
        if row['Range'].startswith('0.0'):
            list_of_labels_to_omit.append(row['Label'])
    list_of_labels_to_omit.append(labels_to_omit)

    # Begin plotting
    fig, ax1 = plt.subplots(figsize=(figure_width, figure_height))

    # Plot the line plot (triggers) on the primary axis (ax1)
    results = {'year': [], 'Label': [], 'count': []}
    for year in df['year'].unique():
        for _, row in info_dataframe.iterrows():
            range_start, range_end = map(float, row['Range'].split(' - '))
            label = row['Label']

            count = df[(df['year'] == year) & 
                       (df[value_field] >= range_start) & 
                       (df[value_field] < range_end)].shape[0]

            results['year'].append(year)
            results['Label'].append(label)
            results['count'].append(count)

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    results_df = results_df.merge(info_dataframe[['Label', 'Color']], on='Label', how='left')

    # Filter out labels to omit
    results_df = results_df[~results_df['Label'].isin(list_of_labels_to_omit)]

    # Sort the DataFrame by year
    results_df = results_df.sort_values(by='year')

    # Plotting the line plot (for return period triggers) on the left axis (ax1)
    line_width = 1.2
    labels = results_df['Label'].unique()
    
    for label in labels:
        subset = results_df[results_df['Label'] == label]
        ax1.plot(subset['year'], subset['count'], label=label, color=subset['Color'].iloc[0], linewidth=line_width)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Count of return period triggers', color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    # Set integer ticks on ax1
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

    if histogram == 'on':
        # Create the second y-axis for the histogram (per capita fatalities) on the right
        ax2 = ax1.twinx()

        # Plot histogram
        ax2.bar(df_histogram['year'], df_histogram['average_value'], color='gray', label='Per Capita Fatalities', alpha=0.25)
        ax2.set_ylabel('Per capita fatalities (100k)', color='gray')
        ax2.tick_params(axis='y', labelcolor='gray')

        # Adjust the y-axis limits for ax1 and ax2
        ax1_y_lim = ax1.get_ylim()
        ax2_y_lim = ax2.get_ylim()

        ax1.set_ylim(bottom=0, top=ax1_y_lim[1] * 1.05)
        ax2.set_ylim(bottom=0, top=ax2_y_lim[1] * 1.05)

    else:
        # If histogram is off, adjust only the primary axis (ax1)
        ax1_y_lim = ax1.get_ylim()
        ax1.set_ylim(bottom=0, top=ax1_y_lim[1] * 1.05)

    # Adjust the padding and margins to ensure alignment
    fig.subplots_adjust(left=0.1, right=0.9, bottom=0.15, top=0.85)

    # Add a legend
    lines, labels = ax1.get_legend_handles_labels()

    # Set the title of the plot
    plt.title(f'Return period thresholds over time')

    fig = plt.gcf()
    fig.patch.set_facecolor('white')

    plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.show()