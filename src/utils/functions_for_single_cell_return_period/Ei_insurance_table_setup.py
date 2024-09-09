import pandas as pd

def insurance_table_for_E_i(target_return_periods, E_i_dataframe, original_data, value_field='percapita_100k'):
    """
    Create a DataFrame that matches the intended return periods with the closest E_i values,
    corresponding per capita values, and observations from the sorted list.

    Parameters:
    target_return_periods (list): List of target return periods.
    E_i_dataframe (pd.DataFrame): DataFrame containing E_i values and other related columns.
    value_field (str): The name of the column in E_i_dataframe that contains per capita values.

    Returns:
    pd.DataFrame: A DataFrame with the closest E_i values, intended return periods, corresponding per capita values, and observations.
    """
    
    # Initialize lists to store the results
    closest_E_i = []
    intended_return_period = []
    corresponding_percapita_100k = []
    closest_percapita_list = []

    # Extract and sort the per capita values
    percapita_list = original_data[value_field].tolist()
    sorted_percapita_list = sorted(percapita_list)

    # Iterate over each target value
    for target in target_return_periods:
        # Find the row with the closest E_i_value
        closest_index = (E_i_dataframe['E_i_value'] - target).abs().idxmin()
        
        # Retrieve the corresponding values
        closest_E_i_val = E_i_dataframe.loc[closest_index, 'E_i_value']
        percapita_100k_val = E_i_dataframe.loc[closest_index, value_field]
        
        # Append the results to the lists
        closest_E_i.append(closest_E_i_val)
        intended_return_period.append(target)
        corresponding_percapita_100k.append(percapita_100k_val)
        closest_percapita_list.append(percapita_100k_val)
    
    # Create the preliminary DataFrame
    temp_df = pd.DataFrame({
        'return period': intended_return_period,
        'closest r.p.': closest_E_i,
        value_field: corresponding_percapita_100k
    })

    # Initialize list to store the observations counts
    observations = []

    # Calculate the observations for each row in the DataFrame
    for i, row in temp_df.iterrows():
        current_period = row[value_field]
        if i < len(temp_df) - 1:
            next_period = temp_df.loc[i + 1, value_field]
        else:
            next_period = float('inf')
        
        # Count occurrences in the sorted list
        count = sum(current_period <= x < next_period for x in sorted_percapita_list)
        observations.append(count)

    # Add the observations to the DataFrame
    temp_df['Observations'] = observations
    temp_df['Payout'] = 'Undefined'  # Placeholder for the payout field

    return temp_df
