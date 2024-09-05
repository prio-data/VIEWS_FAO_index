import geopandas as gpd
import fiona
import pyogrio
import contextily as ctx
import numpy as np
import os
import pandas as pd
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


def clean_info_dataframe(info_df, return_period_to_drop):
    #--------------------------------------------------------------------------------
    #     This SHOULD NOT NEED TO BE CHANGED     ------------------------------------
    #--------------------------------------------------------------------------------
    # Drop the rows with the specified return periods
    filtered_info_to100 = info_df[~info_df['Return Period'].isin(return_period_to_drop)]

    # Get the list of values in the 'Label' column
    cleaned_labels = filtered_info_to100['Label'].tolist()

    if not filtered_info_to100.empty:
            # Extract the 'Range' value of the last row
            last_range = filtered_info_to100.iloc[-1]['Range']
            
            # Split the range to get the end value
            start, end = last_range.split(' - ')
            
            # Check if the end value is '100,000'
            if end.strip() != '100000':  # Note: Removing any leading/trailing spaces
                # Update the last row with the new range ending at '100,000'
                filtered_info_to100.at[filtered_info_to100.index[-1], 'Range'] = f"{start} - 100000"

    # Extract the maximum values from the 'Range' column
    cleaned_thresholds = filtered_info_to100['Range'].apply(lambda x: float(x.split('-')[1].strip()))

    # Filter out the value 100000
    cleaned_thresholds = cleaned_thresholds[cleaned_thresholds != 100000]

    # Convert the filtered series to a list
    cleaned_thresholds = cleaned_thresholds.tolist()

    return(cleaned_labels, cleaned_thresholds, filtered_info_to100)


def query_and_sort_annual_table(input_table, field_to_sort='first_value', number_of_rows=10):
    sorted_input_table = input_table.sort_values(by=field_to_sort, ascending = False)

    top_n_rows = sorted_input_table.head(number_of_rows)
    return(top_n_rows)


# def provide_values_at_input_return_periods(input_table, return_periods, field='percapita_100k'):
#     """
#     Fetch values from the input table corresponding to specified return periods.

#     Parameters:
#     input_table (pd.DataFrame): The DataFrame containing the data.
#     return_periods (list): A list of return periods to fetch values for.
#     field (str): The name of the field to retrieve values from.

#     Returns:
#     list: A list of values corresponding to the provided return periods.
#     """
#     values = []

#     for rp in return_periods:
#         if rp == 'Max':
#             value = input_table[field].max()
#         else:
#             value = input_table.loc[input_table['Return Period'] == rp, field].values
#             if len(value) > 0:
#                 value = value[0]
#             else:
#                 value = np.nan  # If the return period does not exist, assign NaN
#         values.append(value)

#     # Define thresholds for classification
#     cleaned_thresholds = [float(v) for v in values if not isinstance(v, np.ndarray)]

#     return values, cleaned_thresholds

def provide_values_at_input_return_periods(input_table, return_periods, value_field='percapita_100k', return_period_field='Return Period'):
    """
    Fetch values from the input table corresponding to specified return periods.

    Parameters:
    input_table (pd.DataFrame): The DataFrame containing the data.
    return_periods (list): A list of return periods to fetch values for.
    field (str): The name of the field to retrieve values from.

    Returns:
    list: A list of values corresponding to the provided return periods.
    """
    values = []

    for rp in return_periods:
        if rp == 'Max':
            value = input_table[value_field].max()
        else:
            value = input_table.loc[input_table[return_period_field] == rp, value_field].values
            if len(value) > 0:
                value = value[0]
            else:
                value = np.nan  # If the return period does not exist, assign NaN
        values.append(value)

    # Define thresholds for classification
    cleaned_thresholds = [float(v) for v in values if not isinstance(v, np.ndarray)]

    return cleaned_thresholds

def retrieve_geodataframe(unit):

    file = f'pg{unit}x{unit}.shp'

    shapefile_path = f'{base_dir}/data/generated/spatial reference/{file}'
    gdf = gpd.read_file(shapefile_path)

    return(gdf)

def define_year_to_map(annual_table, row_selection):
    sorted_annual_table = annual_table
    year_to_eval = sorted_annual_table.iloc[row_selection]['year']
    return(year_to_eval)

def query_geodataframe(gdf, method_annual__country, year_to_evaluate, field='percapita_100k'):


    # Column to check and rename
    gis_column_to_check = 'priogrid_g' #GIS__Index #priogrid_gid (from E_i)
    gis_new_column_name = 'TARGET_FID'

    # Check if the column exists and rename it if it does
    if gis_column_to_check in gdf.columns:
        gdf_renamed = gdf.rename(columns={gis_column_to_check: gis_new_column_name})
    else:
         gdf_renamed = gdf
         #raise ValueError(f"This tools expected to find a column: {gis_column_to_check}, in the gdf file... which was not located ")

    # Column to check and rename
    column_to_check = ['pg_id', 'priogrid_gid']
    new_column_name = 'GIS__Index'

    # # Check if the column exists and rename it if it does
    # if column_to_check in method_annual__country.columns:
    #     method_annual__country_renamed = method_annual__country.rename(columns={column_to_check: new_column_name})
    # else:
    #     method_annual__country_renamed = method_annual__country
    #     #raise ValueError(f"This tools expected to find a column: {column_to_check}, which was not located ")

    for column in column_to_check:
        if column in method_annual__country.columns:
            method_annual__country_renamed = method_annual__country.rename(columns={column: new_column_name})
            break  # Exit the loop once the first match is found
    else:
        method_annual__country_renamed = method_annual__country


    df_query_year = method_annual__country_renamed[method_annual__country_renamed['year'] == year_to_evaluate]

    gdf_merged = gdf_renamed.merge(df_query_year, left_on='TARGET_FID', right_on='GIS__Index', how='inner')
    return(gdf_merged)

def float_to_custom_string(value):
    # Convert float to string
    value_str = str(value)
    # Replace the decimal point with an underscore
    custom_str = value_str.replace('.', '_')
    return custom_str

