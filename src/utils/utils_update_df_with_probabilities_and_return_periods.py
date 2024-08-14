import numpy as np
import pandas as pd

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths
setup_project_paths(PATH)

from utils_get_time_period import get_time_period
from utils_p_i import calculate_p_i
from utils_P_i import calculate_P_i
from utils_return_periods import calculate_return_periods


import pandas as pd
import numpy as np

def update_df_with_probabilities_and_return_periods_pretest(df, feature):
    """
    Pre-test the DataFrame to ensure it meets the requirements for processing.

    Parameters:
    df (pd.DataFrame): The DataFrame to be tested.
    feature (str): The feature column to be checked.

    Raises:
    ValueError: If the DataFrame is not a pandas DataFrame.
    ValueError: If the DataFrame is empty.
    ValueError: If the time period columns are not found.
    ValueError: If relevant columns are not found.
    ValueError: If the feature column is empty.
    ValueError: If the feature column contains negative values.
    ValueError: If the DataFrame contains NaN or infinite values.

    Returns:
    bool: True if all checks pass.
    """

    # Check that it is a pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError('df is not a pandas DataFrame')

    # Check the DataFrame is not empty
    if df.empty:
        raise ValueError('DataFrame is empty')

    # Check that the time period is present
    time_period_column = ['month_id', 'year_id']
    if time_period_column[0] not in df.columns and time_period_column[1] not in df.columns:
        raise ValueError('Time period not found')

    # Check that the other relevant columns are present
    relevant_columns = ['pg_id', 'c_id', 'row', 'col', feature]
    for column in relevant_columns:
        if column not in df.columns:
            raise ValueError(f'{column} not found in df')

    # Check that the feature is not empty
    if df[feature].isnull().all():
        raise ValueError(f'{feature} is empty')

    # Check that the feature is not negative
    if (df[feature] < 0).any():
        raise ValueError(f'{feature} contains negative values')

    # Check for null, inf and NaN
    if df.isnull().values.any():
        raise ValueError('DataFrame contains NaN values')

    if np.isinf(df.values).any():
        raise ValueError('DataFrame contains infinite values')

    return True

def check_region_id(region_id_type, region_id, df):
    """
    Check if the region_id is present in the DataFrame based on the region_id_type.

    Parameters:
    region_id_type (str): The type of region ID ('pg_ids', 'c_ids', or 'global').
    region_id (int): The region ID to be checked.
    df (pd.DataFrame): The DataFrame containing the region IDs.

    Raises:
    ValueError: If the region_id is not found in the specified region_id_type column.
    ValueError: If the region_id_type is not recognized.

    Returns:
    bool: True if the region_id is found.
    """

    if region_id_type == 'pg_ids':
        # Check that the region_id is present in the df pg_ids
        if region_id not in df['pg_id'].unique():
            raise ValueError(f'{region_id} not found in pg_id column')
        
    elif region_id_type == 'c_ids':
        # Check that the region_id is present in the df c_ids
        if region_id not in df['c_id'].unique():
            raise ValueError(f'{region_id} not found in c_id column')
        
    elif region_id_type == 'global':
        pass

    else:
        raise ValueError(f'{region_id_type} not recognized')

    return True

def subset_regional_df(df, region_id_type, region_id):
    """
    Subset the DataFrame based on the region_id_type and region_id.

    Parameters:
    df (pd.DataFrame): The DataFrame to be subsetted.
    region_id_type (str): The type of region ID ('pg_ids', 'c_ids', or 'global').
    region_id (int): The region ID to subset the DataFrame by.

    Raises:
    ValueError: If the region_id_type is not recognized.

    Returns:
    pd.DataFrame: The subsetted DataFrame.
    """

    if region_id_type == 'pg_ids':
        sub_df = df[df['pg_id'] == region_id].copy()
        
    elif region_id_type == 'c_ids':
        sub_df = df[df['c_id'] == region_id].copy()
        
    elif region_id_type == 'global':
        sub_df = df.copy()

    else:
        raise ValueError(f'{region_id_type} not recognized')
    
    return sub_df

def update_df_with_probabilities_and_return_periods(df, feature, region_id_type, region_id):
    """
    Update the DataFrame with probabilities and return periods for a given feature and region.

    Parameters:
    df (pd.DataFrame): The DataFrame to be updated.
    feature (str): The feature column to calculate probabilities and return periods for.
    region_id_type (str): The type of region ID ('pg_ids', 'c_ids', or 'global').
    region_id (int): The region ID to subset the DataFrame by.

    Raises:
    ValueError: If any of the pre-tests fail.
    ValueError: If the region_id is not found.
    ValueError: If the DataFrame contains NaN values after merging.

    Returns:
    pd.DataFrame: The updated DataFrame with new columns for probabilities and return periods.
    """

    # Pre-test the DataFrame
    update_df_with_probabilities_and_return_periods_pretest(df, feature)
    
    # Check if the region_id is valid
    check_region_id(region_id_type, region_id, df)
    
    # Get the time period (assuming get_time_period is defined elsewhere)
    time_period = get_time_period(df)

    # Subset the DataFrame according to the region_id_type and region_id
    sub_df = subset_regional_df(df, region_id_type, region_id)

    feature_series = sub_df[feature]
    n_cells = sub_df['pg_id'].unique().shape[0]  # Number of unique grid cells

    # Check if the feature has any values apart from 0
    if (feature_series == 0).all():
        print(f'WARNING: {feature} in {region_id_type} {region_id} contains only 0 values - filling the new columns with appropriate values, i.e. 1 for p_i, 1 for P_i, 1 for e_i, 1 for E_i')
        value_counts = feature_series.value_counts().sort_index(ascending=False)
        df_probabilities = pd.DataFrame({'value_count': value_counts, 'value': value_counts.index}).reset_index(drop=True)
        df_probabilities[f'p_i'] = 1
        df_probabilities[f'P_i'] = 1
        df_probabilities[f'e_i'] = 1
        df_probabilities[f'E_i'] = 1
    else:
        print(f'Calculating probabilities and return periods for {feature} in {region_id_type} {region_id}')
        # Calculate the probabilities and return periods
        df_probabilities = calculate_p_i(feature_series)
        df_probabilities = calculate_P_i(df_probabilities, n_cells)
        df_probabilities = calculate_return_periods(df_probabilities)

    # Rename the calculated columns to match the original DataFrame feature
    df_probabilities.rename(columns={'value': feature, 'value_count': f'{feature}_value_count', 'p_i': f"{feature}_p_i", 'P_i': f"{feature}_P_i", 'e_i': f"{feature}_e_i", 'E_i': f"{feature}_E_i"}, inplace=True)

    # Merge the probabilities DataFrame with the subset DataFrame
    merged_df = pd.merge(sub_df, df_probabilities, on=[feature], how='left')

    # Delete the temporary DataFrames to free up memory
    del sub_df
    del df_probabilities

    # Check for null, inf and NaN in the merged DataFrame
    if merged_df.isnull().values.any():
        raise ValueError('DataFrame contains NaN values')

    return merged_df