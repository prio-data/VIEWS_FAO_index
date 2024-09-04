import pandas as pd

def calculate_cumulative_distribution(data, field='percapita_100k'):
    """
    Calculate the cumulative distribution of values across all voxels.
    
    Parameters:
    data (pd.DataFrame): The voxel data with columns ['cell_id', 'time_id', 'value', 'row', 'col']
    
    Returns:
    pd.Series: Cumulative counts of voxels with value >= each unique value
    """
    # Calculate the frequency of each value
    value_counts = data[field].value_counts().sort_index(ascending=False)
    
    # Calculate the cumulative distribution
    cumulative_distribution = value_counts.cumsum()
    
    return cumulative_distribution

def calculate_probabilities(cumulative_distribution, data, id_column='percapita_100k'):
    """
    Calculate the probabilities p_i and P_i for each value i.
    
    Parameters:
    cumulative_distribution (pd.Series): Cumulative counts of voxels with value >= each unique value
    data (pd.DataFrame): The voxel data with columns ['cell_id', 'year_id', 'row', 'col']
    value_col (str): The column name for the values
    
    Returns:
    pd.DataFrame: DataFrame containing values, p_i, and P_i
    """
    # Calculate total number of voxels
    total_voxels = len(data)
    
    # Number of unique grid cells observed at each time period
    num_cells_per_time_period = data[id_column].nunique()
    
    # Calculate p_i for each value
    p_i = cumulative_distribution / total_voxels
    
    # Calculate P_i for each value
    P_i = 1 - (1 - p_i) ** num_cells_per_time_period # THIS IS SUPER IMPORTANT.
    
    # Combine into a DataFrame
    probabilities = pd.DataFrame({
        'value': cumulative_distribution.index,
        'p_i': p_i.values,
        'P_i': P_i.values
    })
    
    return probabilities

def calculate_expected_time_periods(P_i):
    """
    Calculate the expected number of time periods to check (E_i) for each value i.
    
    Parameters:
    P_i (pd.Series): Probability of seeing one or more voxels with value >= i in a random time period
    
    Returns:
    pd.Series: Expected number of time periods to check for each value
    """
    # Calculate E_i for each value
    E_i = 1 / P_i
    
    return E_i

def calculate_expected_voxels(p_i):
    """
    Calculate the expected number of voxels to draw (E_i^voxels) to see a value >= i.
    
    Parameters:
    p_i (pd.Series): Probability of drawing a voxel with value >= i
    
    Returns:
    pd.Series: Expected number of voxels to draw for each value
    """
    # Calculate E_i^voxels for each value
    E_i_voxels = 1 / p_i
    
    return E_i_voxels

def compare_empirical_vs_expected(data, probabilities, time_column='year', value_column = 'percapita_100k'):
    """
    Compare empirical frequencies of E_i values with their expected frequencies
    in terms of both time periods and individual voxels for all unique values.
    
    Parameters:
    data (pd.DataFrame): The voxel data with columns ['cell_id', 'time_id', 'value', 'row', 'col']
    probabilities (pd.DataFrame): DataFrame containing values, p_i, P_i, E_i, and E_i_voxels
    
    Returns:
    pd.DataFrame: DataFrame containing the comparison of empirical vs expected frequencies
    """
    # Number of time periods in the dataset
    num_time_periods = data[time_column].nunique()
    
    # Unique values from the 'value' column
    unique_values = data[value_column].unique()
    
    results = []

    for val in unique_values:
        # Find the corresponding E_i and E_i_voxels for the given value
        E_i_row = probabilities[probabilities[value_column] == val]

        if not E_i_row.empty:
            E_i_val = E_i_row['E_i'].values[0]
            E_i_voxels_val = E_i_row['E_i_voxels'].values[0]
            
            if E_i_val > 0 and E_i_voxels_val > 0:
                # Empirical frequency in time periods
                empirical_freq_time = data.groupby(time_column).apply(
                    lambda x: (x[value_column] >= val).any()).sum()
                expected_freq_time = num_time_periods / E_i_val

                # Empirical frequency in voxels
                empirical_freq_voxels = (data[value_column] >= val).sum()
                expected_freq_voxels = num_time_periods / E_i_voxels_val

                results.append({
                    value_column: val,
                    'E_i_value': E_i_val,
                    'empirical_freq_time': empirical_freq_time,
                    'expected_freq_time': expected_freq_time,
                    'empirical_freq_voxels': empirical_freq_voxels,
                    'expected_freq_voxels': expected_freq_voxels
                })
    
    results_df = pd.DataFrame(results)
    
    return results_df
