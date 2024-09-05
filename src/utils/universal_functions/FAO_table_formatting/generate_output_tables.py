import pandas as pd
import numpy as np

from src.utils.universal_functions.FAO_table_formatting.calculate_percentiles import convert_to_float_or_null

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

def generate_and_give_info_dataframe(insurance_table, return_period, value_column, rp_column, cmap=None):

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
    
        cleaned_thresholds = provide_values_at_input_return_periods(insurance_table, [10,20,50,100], value_column, rp_column) #(insurance_from_E_i, [5,10,20,30], 'percapita_100k', 'Intended Return Period')
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
        cleaned_thresholds = provide_values_at_input_return_periods(insurance_table, [5,10,20,30], value_column, rp_column)

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


def insurance_table(perc_df, orginal_df, percentiles_of_interest, attribute_to_explore='percapita_100k', append_1_value='yes'):
    give_value_at_one = None

    # If the option to append 1 value is 'yes'
    if append_1_value == 'yes':
        for idx, value in perc_df[attribute_to_explore].items():
            if value >= 1.0:
                give_value_at_one = perc_df.loc[idx, 'percentile']
                break

        # Check if give_value_at_one was assigned a value
        if give_value_at_one is not None:
            print(f"Index where {attribute_to_explore} equals 1: {give_value_at_one}: {value}")
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



def annual_summary_table(input_df,fat_or_pcf='percapita_100k'):

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

    # Calculate the average value for each year -- df_sorted was org_df
    average_values = df_sorted.groupby('year')[fat_or_pcf].mean().reset_index().rename(columns={fat_or_pcf: 'average_value'})

    # Merge the result_df with average_values
    year_df = pd.merge(result_df, average_values, on='year')
    return(year_df)

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