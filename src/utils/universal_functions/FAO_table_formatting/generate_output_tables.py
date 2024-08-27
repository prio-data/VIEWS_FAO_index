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

    collected.loc[collected['Percentile'] == '100', 'Return Period'] = 'Max'
    collected.loc[collected['Percentile'] == '100', 'Payout Rate'] = 'Max'
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