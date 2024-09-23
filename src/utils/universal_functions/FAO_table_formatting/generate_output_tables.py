import pandas as pd
import numpy as np

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

from src.utils.universal_functions.FAO_table_formatting.calculate_percentiles import convert_to_float_or_null
from src.utils.functions_for_graphics.individual_graphics.map_helper.manipulate_tables_for_mapping import calculate_histogram_data

def develop_info_dataframe(rp,threshold_value, colors, defined_labels):
    data = {
        'Return Period': [],
        'Range': [],
        'Color': [],
        'Label': []
    }

    for i in range(len(rp)):
        lower_bound = threshold_value[i]
        upper_bound = threshold_value[i + 1]
        period = rp[i]
        color = colors.get(period, '#FFFFFF')  # Default to white if not found
        element_label = defined_labels[i]
        
        data['Return Period'].append(period)
        data['Range'].append(f"{lower_bound} - {upper_bound}")
        data['Color'].append(color)
        data['Label'].append(element_label)
    # Create DataFrame
    info_df = pd.DataFrame(data)
    
    return(info_df)

from src.utils.functions_for_graphics.individual_graphics.map_helper.manipulate_tables_for_mapping import provide_values_at_input_return_periods

def update_preceding_row_if_not_in_return_period(df, periods_to_check, value_column):
    # Iterate through the DataFrame to check for values not in return_periods
    for idx, row in df.iterrows():
        percentile_value = row['Return Period']

        # Skip the first row as it has no preceding row
        if idx == 0:
            continue

        # Ignore rows where Percentile is 'max'
        if percentile_value == 'max':
            continue
        
        # Skip if the percentile is in the list of return periods
        if isinstance(percentile_value, (int, float)) and percentile_value in periods_to_check:
            continue

        # For the identified value, copy the percapita_100k and Occurrence values to the preceding row
        if idx > 0:
            df.at[idx - 1, value_column] = row[value_column]
            df.at[idx - 1, 'Occurrence'] = row['Occurrence']
            print(f"Updated row {idx-1} with values from row {idx}: {row[value_column]}, {row['Occurrence']}")

        # Stop after updating the first row that matches the condition
        break

    return df


def generate_and_give_info_dataframe(data, return_period, value_column, rp_column, cmap=None):

    # We do not want to make changes to the original insurance table!
    insurance_table_copy = data.copy()

    if return_period == 'Country year':

        default_color_map = {
            0:  '#d5dbdb',   
            10: '#377eb8',
            20: '#e6ab02',
            50: '#762a83',
            100: '#b2182b'
        }

        if cmap is None:
            color_map = default_color_map
        else: 
            color_map = cmap

        periods_to_check = [10.0, 20.0, 50.0, 100.0]
        insurance_table_fixed_for_insurance_application = update_preceding_row_if_not_in_return_period(insurance_table_copy, periods_to_check, value_column)

        cleaned_thresholds = provide_values_at_input_return_periods(insurance_table_fixed_for_insurance_application, [10,20,50,100], value_column, rp_column) #(insurance_from_E_i, [5,10,20,30], 'percapita_100k', 'Intended Return Period')
        # Define the thresholds and include 0 and 100000
        thresholds = [0] + cleaned_thresholds + [100000]
        return_periods = [0, 10, 20, 50, 100]

        if len(thresholds) - 1 != len(return_periods):
            raise ValueError("The number of thresholds should be one more than the number of return periods.")
        
        labels = ['Below 1 in 10 year', '1 in 10 year',  '1 in 20 year',  '1 in 50 year', '1 in 100 year',]

        info_df = develop_info_dataframe(return_periods, thresholds, color_map, labels)
        return(info_df, color_map)


    if return_period == 'Event year':

        default_color_map = {
                0:  '#d5dbdb',   
                5: '#4daf4a',
                10: '#377eb8',
                20: '#e6ab02',
                30: '#c51b7d',
        }
        if cmap is None:
            color_map = default_color_map
        else: 
            color_map = cmap

        # For E-i---------------------------------------------------------------------------------------------------------------
        cleaned_thresholds = provide_values_at_input_return_periods(insurance_table_copy, [5,10,20,30], value_column, rp_column)

            #Now we make to make a reference dataframe regardless if there are duplicates:
            # Define the return periods and their associated color map

        print('This is a critical dataframe:')
            #----- Define Map Pallete:-------------------------------------------------------------------------------------------

            # Define the thresholds and include 0 and 100000
        thresholds_to30 = [0] + cleaned_thresholds + [100000]
        return_periods_to30 = [0, 5, 10, 20, 30]

        if len(thresholds_to30) - 1 != len(return_periods_to30):
                    raise ValueError("The number of thresholds should be one more than the number of return periods.")
                
        labels_to30 = ['Below 1 in 5 year', '1 in 5 year', '1 in 10 year',  '1 in 20 year',  '1 in 30 year']

        info_df_to30 = develop_info_dataframe(return_periods_to30, thresholds_to30, color_map, labels_to30)
        return(info_df_to30, color_map)

# def generate_and_give_info_dataframe(insurance_table, return_period, value_column, rp_column, cmap=None):

#     if return_period == 'Country year':

#         default_color_map = {
#             0:  '#d5dbdb',   
#             10: '#377eb8',
#             20: '#e6ab02',
#             50: '#762a83',
#             100: '#b2182b'
#         }

#         if cmap is None:
#             color_map = default_color_map
#         else: 
#             color_map = cmap
    
#         cleaned_thresholds = provide_values_at_input_return_periods(insurance_table, [10,20,50,100], value_column, rp_column) #(insurance_from_E_i, [5,10,20,30], 'percapita_100k', 'Intended Return Period')
#         # Define the thresholds and include 0 and 100000
#         thresholds = [0] + cleaned_thresholds + [100000]
#         return_periods = [0, 10, 20, 50, 100]

#         if len(thresholds) - 1 != len(return_periods):
#             raise ValueError("The number of thresholds should be one more than the number of return periods.")
        
#         labels = ['Below 1 in 10 year', '1 in 10 year',  '1 in 20 year',  '1 in 50 year', '1 in 100 year',]


#         info_df = develop_info_dataframe(return_periods, thresholds, color_map, labels)
#         return(info_df, color_map)


#     if return_period == 'Event year':

#         default_color_map = {
#                 0:  '#d5dbdb',   
#                 5: '#4daf4a',
#                 10: '#377eb8',
#                 20: '#e6ab02',
#                 30: '#c51b7d',
#         }
#         if cmap is None:
#             color_map = default_color_map
#         else: 
#             color_map = cmap

#         # For E-i---------------------------------------------------------------------------------------------------------------
#         cleaned_thresholds = provide_values_at_input_return_periods(insurance_table, [5,10,20,30], value_column, rp_column)

#             #Now we make to make a reference dataframe regardless if there are duplicates:
#             # Define the return periods and their associated color map

#         print('This is a critical dataframe:')
#             #----- Define Map Pallete:-------------------------------------------------------------------------------------------

#             # Define the thresholds and include 0 and 100000
#         thresholds_to30 = [0] + cleaned_thresholds + [100000]
#         return_periods_to30 = [0, 5, 10, 20, 30]

#         if len(thresholds_to30) - 1 != len(return_periods_to30):
#                     raise ValueError("The number of thresholds should be one more than the number of return periods.")
                
#         labels_to30 = ['Below 1 in 5 year', '1 in 5 year', '1 in 10 year',  '1 in 20 year',  '1 in 30 year']

#         info_df_to30 = develop_info_dataframe(return_periods_to30, thresholds_to30, color_map, labels_to30)
#         return(info_df_to30, color_map)


def insurance_table(perc_df, orginal_df, percentiles_of_interest, attribute_to_explore='percapita_100k', append_1_value='yes'):
    give_value_at_one = None

    # If the option to append 1 value is 'yes'


    if append_1_value == 'yes':
        if attribute_to_explore == 'fatalities_sum':
            for idx, value in perc_df[attribute_to_explore].items():
                if value >= 1.0:
                    give_value_at_one = perc_df.loc[idx, 'percentile']
                    break
        if attribute_to_explore == 'percapita_100k':
            for idx, value in perc_df[attribute_to_explore].items():
                if value >= 0.1:
                    give_value_at_one = perc_df.loc[idx, 'percentile']
                    break

        # Check if give_value_at_one was assigned a value
        if give_value_at_one is not None:
            print(f"Index where {attribute_to_explore} equals 1 (fatalities) or 0.1 (per capita): {give_value_at_one}: {value}")
            give_value_at_one = str(give_value_at_one)
            percentiles_of_interest.append(give_value_at_one)
            percentiles_of_interest = sorted(percentiles_of_interest, key=float)
        else:
            print(f"No value in {attribute_to_explore} column is greater than or equal to 1.0.")

    perc_df['percentile'] = perc_df['percentile'].astype('string')
    from_sub_perc = perc_df[perc_df['percentile'].isin(percentiles_of_interest)]
    def_values = from_sub_perc['percentile'].unique()

    id_attribute = []
    id_triggers = []
    id_p = []

    collected = pd.DataFrame()

    for i in range(len(def_values)):
        current_percentile = def_values[i]
        next_percentile = def_values[i + 1] if i + 1 < len(def_values) else None

        get_row = perc_df.loc[perc_df['percentile'] == current_percentile]
        attribute = get_row.at[get_row.index[0], attribute_to_explore]

        if next_percentile:
            next_row = perc_df.loc[perc_df['percentile'] == next_percentile]
            next_attribute = next_row.at[next_row.index[0], attribute_to_explore]
            limit = orginal_df.loc[(orginal_df[attribute_to_explore] >= attribute) & (orginal_df[attribute_to_explore] < next_attribute)]
        else:
            limit = orginal_df.loc[orginal_df[attribute_to_explore] >= attribute]

        triggers = len(limit.index)
        percentile = current_percentile

        id_p.append(percentile)
        id_attribute.append(attribute)
        id_triggers.append(triggers)

        Out_Percentile = pd.DataFrame(list(zip(id_p, id_attribute, id_triggers)),
            columns=['Percentile', attribute_to_explore, 'Occurrence'])

    collected = pd.concat([collected, Out_Percentile], ignore_index=True)

    p_from_jerry_table = list((collected['Percentile']))

    b_values_map = {'90': '30%', '95': '55%', '98': '75%', '99': '100%', '100': '100'}

    a_values_map = {}
    for key in p_from_jerry_table:
        if key == '100':
            a_values_map[key] = 0
        else:
            a_values_map[key] = (1 / (100 - float(key))) * 100

    collected['Return Period'] = collected['Percentile'].map(a_values_map)
    collected['Payout Rate'] = collected['Percentile'].map(b_values_map)

    collected[attribute_to_explore] = convert_to_float_or_null(collected[attribute_to_explore])
    collected['Return Period'] = convert_to_float_or_null(collected['Return Period'])

    collected[attribute_to_explore] = np.floor(collected[attribute_to_explore] * 10) / 10
    collected['Return Period'] = np.floor(collected['Return Period'] * 10) / 10


    collected.loc[collected['Percentile'] == '100', 'Return Period'] = '--'
    collected.loc[collected['Percentile'] == '100', 'Payout Rate'] = '--'
    #Finally, on Sept 05, ViEWS determined to change '100' percentile label to 'Max'.
    collected.loc[collected['Percentile'] == '100', 'Percentile'] = 'max'

    collected['Payout Rate'] = collected['Payout Rate'].fillna('undefined')

    return collected

# def calculate_histogram_data(df,field):
#     # Group by year and sum relevant columns
#     df_grouped = df.groupby('year').agg({
#         'fatalities_sum': 'sum',
#         'pop_gpw_sum': 'sum'
#     }).reset_index()
    
#     # Recalculate per capita fatalities per 100k population
#     df_grouped[field] = (df_grouped['fatalities_sum'] / df_grouped['pop_gpw_sum']) * 100000
#     return df_grouped


# def annual_summary_table(input_df,fat_or_pcf='percapita_100k'):

# # Group by year and sort values within each group
#     df_sorted = input_df.sort_values(by=['year', fat_or_pcf], ascending=[True, False])

# # Extract the top 3 values for each year
#     df_top3 = df_sorted.groupby('year').head(3)

# # Aggregate to get the top three values and average value for each year
#     result_df = df_top3.groupby('year').agg(
#         first_value=(fat_or_pcf, lambda x: x.iloc[0] if len(x) > 0 else None),
#         second_value=(fat_or_pcf, lambda x: x.iloc[1] if len(x) > 1 else None),
#         third_value=(fat_or_pcf, lambda x: x.iloc[2] if len(x) > 2 else None)
#     ).reset_index()

#     # Calculate the average value for each year -- df_sorted was org_df
#     average_values = df_sorted.groupby('year')[fat_or_pcf].mean().reset_index().rename(columns={fat_or_pcf: 'average_value'})
    
#     # Merge the result_df with average_values
#     year_df = pd.merge(result_df, average_values, on='year')
#     return(year_df)

# def calculate_histogram_data(df):
#     # Group by year and sum relevant columns
#     df_grouped = df.groupby('year').agg({
#         'fatalities_sum': 'sum',
#         'pop_gpw_sum': 'sum'
#     }).reset_index()
    
#     # Recalculate per capita fatalities per 100k population
#     df_grouped['average_value'] = (df_grouped['fatalities_sum'] / df_grouped['pop_gpw_sum']) * 100000
#     return df_grouped

def annual_summary_table(input_df, method, fat_or_pcf='percapita_100k'):

# Group by year and sort values within each group
    df_sorted = input_df.sort_values(by=['year', fat_or_pcf], ascending=[True, False])

# Extract the top 3 values for each year
    df_top3 = df_sorted.groupby('year').head(3)

# Aggregate to get the top three values and average value for each year
    result_df = df_top3.groupby('year').agg(
        first_value=(fat_or_pcf, lambda x: x.iloc[0] if len(x) > 0 else None),
        second_value=(fat_or_pcf, lambda x: x.iloc[1] if len(x) > 1 else None),
        third_value=(fat_or_pcf, lambda x: x.iloc[2] if len(x) > 2 else None)
    ).reset_index()

    if method != 'smoothing':
        average_values = calculate_histogram_data(input_df)
        # List of columns to keep
        columns_to_keep = ['year', 'average_value']  # Replace with your column names

        # Filter the dataframe to keep only the specified columns
        average_values_filtered = average_values[columns_to_keep]
        
        # Calculate the average value for each year -- df_sorted was org_df
        #average_values = df_sorted.groupby('year')[fat_or_pcf].mean().reset_index().rename(columns={fat_or_pcf: 'average_value'})
        
        # Merge the result_df with average_values
        result_df = pd.merge(result_df, average_values_filtered, on='year')
        
    return(result_df)


""" 
Accepts the dataframe which hosts fields:
1. year
2. first_value
3. second_value
4. third_value
5. average_value


then accepts the arguments: 
1. name of the dataframe
2. the field informing the sort  
-- it may be desirable to sort by the max observed value OR the average value
3. the number of rows you want any number within the number of observed years
-- some graphics may be more desirable to take the top 5, 10, or 15
"""

def query_and_sort_annual_table(input_table, field_to_sort='first_value', number_of_rows=10):
    sorted_input_table = input_table.sort_values(by=field_to_sort, ascending = False)

    top_n_rows = sorted_input_table.head(number_of_rows)
    return(top_n_rows)

import pandas as pd
# Step 2: Create a function to map per capita values to the appropriate 'Return Period' and 'Label'


# def append_return_periods_to_annual_table(x, y, filtered_info):
    
#     # Step 1: Split the 'Range' column into two columns (min and max)
#     filtered_info[['Range_min', 'Range_max']] = filtered_info['Range'].str.split(' - ', expand=True)
#     filtered_info['Range_min'] = filtered_info['Range_min'].astype(float)
#     filtered_info['Range_max'] = filtered_info['Range_max'].astype(float)

#     # Step 2: Create a function to map per capita values to the appropriate 'Return Period' and 'Label'
#     def map_return_period(value):
#         for _, row in filtered_info.iterrows():
#             if row['Range_min'] <= value < row['Range_max']:
#                 return pd.Series([row['Return Period'], row['Label']])
#         return pd.Series([None, None])

#     # Step 3: Apply the function to the per_capita_df and assign the new 'Return Period' and 'Label' columns
#     x[['Return Period', 'Label']] = x['percapita_100k'].apply(map_return_period)

#     # Output the dataframe
#     #print(expl_x)

#     # Group by 'year' and 'Return Period', then count occurrences
#     aggregated_series = x.groupby(['year', 'Return Period']).size().reset_index(name='Count')

#     # Pivot the DataFrame
#     pivoted_df = aggregated_series.pivot_table(index='year', columns='Return Period', values='Count', fill_value=0)

#     # Reset the index to make 'year' a column
#     pivoted_df = pivoted_df.reset_index()

#     pivoted_df = pivoted_df.rename_axis(None, axis=1)

#     #change label for '0' column:
#     if 0 in pivoted_df.columns:
#         label_for_zero = x.loc[x['Return Period'] == 0, 'Label'].values[0]
#         pivoted_df.rename(columns={0: label_for_zero}, inplace=True)

#     #Reformat the annual summary table to only contain the max event and average event
#     annual_summary_df = y.drop(columns=['second_value', 'third_value'])

#     #Then merge the with count of R.P. events table just created on the field 'year'
#     merged_annual_summary = pd.merge(annual_summary_df, pivoted_df, on='year')
#     return(merged_annual_summary)

import re
def append_return_periods_to_annual_table(x, y, filtered_info, value_field, population_field):
    # Calculate the total population for percentage calculation

    # Initialize the results dictionary for storing year, label, count, population sum, and percentage
    results = {
        'year': [], 
        'Label': [], 
        'count': [], 
        'population_rp_sum': [], 
        'population_percentage': []
    }

    # Loop over each unique year in the dataset 'x'
    for year in x['year'].unique():
        for _, row in filtered_info.iterrows():
            range_start, range_end = map(float, row['Range'].split(' - '))
            label = row['Label']

            #subset by year and sum by population so pop sum is specific to that year
            total_population = x[(x['year'] == year)][population_field].sum()

            # Count occurrences within the range for the current year
            count = x[(x['year'] == year) & 
                      (x[value_field] >= range_start) & 
                      (x[value_field] < range_end)].shape[0]

            # Sum the population within the range for the current year
            population_sum = x[(x['year'] == year) & 
                               (x[value_field] >= range_start) & 
                               (x[value_field] < range_end)][population_field].sum()

            # Calculate the population percentage relative to the total population
            pop_perc = population_sum / total_population

            # Append the year, label, count, population sum, and percentage to the results dictionary
            results['year'].append(year)
            results['Label'].append(label)
            results['count'].append(count)
            results['population_rp_sum'].append(population_sum)
            results['population_percentage'].append(pop_perc)

    # Convert the results to a DataFrame
    results_df = pd.DataFrame(results)

    # Pivot the DataFrame to get counts and population sums for each 'Return Period'
    pivoted_df = results_df.pivot_table(index='year', columns='Label', values=['count', 'population_rp_sum', 'population_percentage'], fill_value=0)

    # Reset the index to make 'year' a column, and flatten the column MultiIndex
    pivoted_df.columns = ['_'.join(col).strip() for col in pivoted_df.columns.values]
    pivoted_df = pivoted_df.reset_index()

    # Reformat the annual summary table to only contain the max event and average event
    annual_summary_df = y.drop(columns=['second_value', 'third_value'])

    # Merge the count of Return Period events with the annual summary table on the field 'year'
    merged_annual_summary = pd.merge(annual_summary_df, pivoted_df, on='year')

    # Check to make sure none of the columns refer to 'Below X Return Period'
    columns_to_drop = merged_annual_summary.filter(like='Below', axis=1).columns

    # Drop the identified columns
    merged_annual_summary = merged_annual_summary.drop(columns=columns_to_drop)

    fixed_order = ['year', 'first_value', 'average_value']

    columns = list(merged_annual_summary.columns)

    # Extract columns that contain "in " followed by a number
    numeric_columns = [col for col in columns if re.search(r'in \d+', col)]

    # Sort the numeric columns by the number that comes after "in "
    sorted_numeric_columns = sorted(numeric_columns, key=lambda x: int(re.search(r'in (\d+)', x).group(1)), reverse=True)
    print(sorted_numeric_columns)
    # Combine the fixed columns with the sorted numeric columns
    new_column_order = fixed_order + sorted_numeric_columns

    # Reorder the DataFrame columns based on the new order
    merged_annual_summary = merged_annual_summary[new_column_order]

    # Handle the case where there are multiple numeric columns for calculating weighted sums
    if len(sorted_numeric_columns) > 1:
        sorted_numeric_columns_dropbottom = sorted_numeric_columns[:-1]

        # Initialize a new column with zeros to accumulate the weighted sum
        merged_annual_summary['weighted_sum_return_periods'] = 0

        # Loop through each column in sorted_numeric_columns_dropbottom
        for col in sorted_numeric_columns_dropbottom:
            # Extract the numerical part of the column name (assumes the pattern '1 in X year')
            numeric_value = int(re.search(r'in (\d+)', col).group(1))
            
            # Multiply the entire column by the extracted numeric value and accumulate the result
            merged_annual_summary['weighted_sum_return_periods'] += merged_annual_summary[col] * numeric_value

    else:
        # If only one column, copy that column as the sum
        merged_annual_summary['weighted_sum_return_periods'] = 0

        for col in sorted_numeric_columns:
            # Extract the numerical part of the column name (assumes the pattern '1 in X year')
            numeric_value = int(re.search(r'in (\d+)', col).group(1))
            
            # Multiply the entire column by the extracted numeric value and accumulate the result
            merged_annual_summary['weighted_sum_return_periods'] += merged_annual_summary[col] * numeric_value
    
    return merged_annual_summary
#--------------------------------------------------------------------------------------------