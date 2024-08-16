import numpy as np
import pandas as pd

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths
setup_project_paths(PATH)

from utils_get_time_period import get_time_period
from utils_update_df_with_probabilities_and_return_periods import update_df_with_probabilities_and_return_periods


def process_data_country_wise_pretest(df, feature):
    """
    Processes the data for a given country by performing pre-test checks.

    Parameters:
    - df (pd.DataFrame): Input dataframe containing the data.
    - feature (str): The feature column to be processed.

    Returns:
    - bool: True if all checks pass, otherwise raises a ValueError.

    Raises:
    - ValueError: If the input is not a pandas DataFrame.
    - ValueError: If the DataFrame is empty.
    - ValueError: If the feature is not a string.
    - ValueError: If required columns are missing from the DataFrame.
    - ValueError: If any required column contains NaN values.
    - ValueError: If any required column contains infinite values.
    """
    
    # check that the df is a pandas dataframe
    if not isinstance(df, pd.DataFrame):
        raise ValueError('Input should be a pandas DataFrame')
    
    # check that the df is not empty
    if df.empty:
        raise ValueError('DataFrame is empty')

    # check that the feature is a string
    if not isinstance(feature, str):
        raise ValueError('Feature should be a string')

    # get the time period
    time_priode = get_time_period(df)

    # check if required columns are present and not null nan of inf
    required_columns = ['c_id', 'row', 'col', 'pg_id', feature, time_priode]
    for feature in required_columns:

        if feature not in df.columns:
            raise ValueError(f'Required column {feature} not found in the DataFrame')
        
        if df[feature].isnull().values.any():
            raise ValueError(f'Column {feature} contains NaN values')
        
        if np.isinf(df[feature].values).any():
            raise ValueError(f'Column {feature} contains infinite values')
        
    return True


def process_data_country_wise_posttest(df, feature):
    """
    Processes the data for a given country by performing post-test checks.

    Parameters:
    - df (pd.DataFrame): Input dataframe containing the data.
    - feature (str): The feature column to be processed.

    Returns:
    - bool: True if all checks pass, otherwise raises a ValueError.

    Raises:
    - ValueError: If the input is not a pandas DataFrame.
    - ValueError: If the DataFrame is empty.
    - ValueError: If the DataFrame contains NaN values.
    - ValueError: If the DataFrame contains infinite values.
    - ValueError: If any column contains only one unique value.
    """
    
    # check that the df is a pandas dataframe
    if not isinstance(df, pd.DataFrame):
        raise ValueError('Input should be a pandas DataFrame')
    
    # check that the df is not empty
    if df.empty:
        raise ValueError('DataFrame is empty')
    
    # check that it does not contain NaN or inf values
    if df.isnull().values.any():
        raise ValueError('DataFrame contains NaN values')
    
    if np.isinf(df.values).any():
        raise ValueError('DataFrame contains infinite values')
    
    # check that no columns only contain one unique value
    for column in df.columns:
        if len(df[column].unique()) == 1:
            unique_value = df[column].unique()[0]
            raise ValueError(f'Column {column} only contains one unique value {unique_value}')
    
    return True

 
def process_data_country_wise(df, feature):
    """
    Process data for each country and merge the results into a single DataFrame.
    This function can handle both monthly and yearly data frames.

    Parameters:
    df (pd.DataFrame): The data DataFrame (can be monthly or yearly).
    feature (str): The feature column to be processed.

    Returns:
    pd.DataFrame: A DataFrame containing the processed data for all countries.

    Raises:
    Exception: If there is an error processing data for a specific country.
    """
    
    # Pre-test
    process_data_country_wise_pretest(df, feature)

    unique_country_ids = df['c_id'].unique()
    
    # Create an empty DataFrame to store the results
    df_country_wise = pd.DataFrame()
    
    for i, country_id in enumerate(unique_country_ids):
        print(f'Processing country_id: {country_id} {i}/{len(unique_country_ids)}') #, country_name: {get_country_names_by_ids([country_id])}')
    
        try:
            new_df_country = update_df_with_probabilities_and_return_periods(df, feature, 'c_ids', country_id)
            df_country_wise = pd.concat([df_country_wise, new_df_country])

        except Exception as e:
            print(f'Error with {country_id}: {e}') #, country_name: {get_country_names_by_ids([country_id])}. Skipping...')

    # Post-test
    process_data_country_wise_posttest(df, feature)

    return df_country_wise