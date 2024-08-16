import sys
import os
import numpy as np
import pandas as pd

from viewser import Queryset, Column


import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths, setup_root_paths, get_logo_path, get_data_paths
setup_project_paths(PATH)

from config_input_data import get_base_input_data_config


def fetch_data_from_viewser():
    """
    Fetches and prepares the initial DataFrame from viewser.

    Returns:
        pd.DataFrame: The prepared DataFrame with initial processing done.
    """
    print(f'Beginning file download through viewser')
    queryset_base = get_base_input_data_config()

    df = queryset_base.publish().fetch()
    
    # Print the size of the DataFrame to see if it is empty
    print(f'Size of DataFrame: {df.shape}')
    
    df.reset_index(inplace=True)

    # Rename and add columns specific to HydraNet or vol specific
    df.rename(columns={'priogrid_gid': 'pg_id'}, inplace=True)
    
    return df

def get_year_range():
    """
    Gets the year range for the data as specified in Håvard's mail.

    Returns:
        tuple: A tuple containing the first and last years.
    """
    year_first = 1989
    year_last = 2023

    return year_first, year_last


def filter_dataframe_by_year_range(df, year_first, year_last): # NOT USING THIS YET
    """
    Filters the DataFrame to include only the specified year range.

    Args:
        df (pd.DataFrame): The input DataFrame to be filtered.
        year_first (int): The first year ID to include.
        year_last (int): The last year ID to include.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    year_range = np.arange(year_first, year_last + 1)  # Adding 1 to include year_last in the range
    new_df = df[df['year_id'].isin(year_range)].copy()

    # chek if the size of the new DataFrame is empty
    print(f'Size of new DataFrame: {new_df.shape}')

    return new_df


def validate_dataframe(df: pd.DataFrame):
    """
    Validate the DataFrame to ensure it meets the specified conditions.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to validate.
    
    Raises:
    ValueError: If any of the validation checks fail.
    """
    # Check that the DataFrame is not empty
    if df.empty:
        raise ValueError("The DataFrame is empty. Please provide a DataFrame with data.")
    
    # Check that the DataFrame has the right columns
    required_columns = ['month_id', 'pg_id', 'month', 'year_id', 'c_id', 'col', 'row', 'sb_best', 'ns_best', 'os_best', 'pop_gpw_sum']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The DataFrame is missing the following required columns: {missing_columns}")
    
    # Check for missing values and NaN values
    if df.isnull().values.any() or df.isna().values.any():
        # which columns have missing values
        missing_cols = df.columns[df.isnull().any()]
        raise ValueError(f"The DataFrame contains missing values in the following columns: {missing_cols}")
    
    # check for inf and negative inf values
    if np.isinf(df.values).any():
        # which columns have inf values
        inf_cols = df.columns[(df == np.inf).any()]
        raise ValueError(f"The DataFrame contains inf values in the following columns: {inf_cols}")    
    
    if np.isneginf(df.values).any():
        # which columns have negative inf values
        neg_inf_cols = df.columns[(df == -np.inf).any()]
        raise ValueError(f"The DataFrame contains negative inf values in the following columns: {neg_inf_cols}")
    
    # Check if any of the columns are empty, containing only whitespace or zero
    empty_cols = df.columns[(df.eq('') | df.eq(' ') | df.eq(0)).all()]
    if empty_cols.any():
        raise ValueError(f"The DataFrame contains empty columns: {empty_cols}")
    
    # Check that the DataFrame has the years and months from Jan 1989 to Dec 2023
    if df['year_id'].nunique() != 35:  # 1989 to 2023
        raise ValueError("The DataFrame does not contain data for all years from 1989 to 2023.")
    
    if df['month_id'].nunique() != 420:  # 35 years * 12 months
        raise ValueError("The DataFrame does not contain data for all months from Jan 1989 to Dec 2023.")
    
    # Check that every grid id (pg_id) is observed for all 420 months and all 35 years
    grid_check = df.groupby('pg_id').agg({'year_id': 'nunique', 'month_id': 'nunique'})
    if not ((grid_check['year_id'] == 35) & (grid_check['month_id'] == 420)).all():
        raise ValueError("Not all grid IDs have data for all 35 years and 420 months.")
        
    # Data Type Checks
    expected_dtypes = {
        'month_id': 'int64',
        'pg_id': 'int64',
        'month': 'int64',
        'year_id': 'int64',
        'c_id': 'int64',
        'col': 'int64',
        'row': 'int64',
        'sb_best': 'float64',
        'ns_best': 'float64',
        'os_best': 'float64',
        'pop_gpw_sum': 'float64'
    }
    for col, dtype in expected_dtypes.items():
        if df[col].dtype != dtype:
            raise ValueError(f"Column {col} does not have the expected data type {dtype}.")
    
    # Range Checks
    if not df['month'].between(1, 12).all():
        raise ValueError("Column 'month' contains values outside the range 1-12.")
    
    if not df['year_id'].between(1989, 2023).all():
        raise ValueError("Column 'year_id' contains values outside the range 1989-2023.")
    
    if not df['month_id'].between(109, 528).all():
        raise ValueError("Column 'month_id' contains values outside the range 121-1000.")
    
    # Unique Constraints
    if df.duplicated(subset=['month_id', 'pg_id', 'year_id', 'c_id']).any():
        raise ValueError("The DataFrame contains duplicate rows based on ['month_id', 'pg_id', 'year_id', 'c_id'].")
    
    # Value Consistency - mosut be above 0
    if not (df['sb_best'] >= 0).all():
        raise ValueError("Column 'sb_best' contains values that are not above 0.") 

    if not (df['ns_best'] >= 0).all():
        raise ValueError("Column 'ns_best' contains values that are not above 0.")
    
    if not (df['os_best'] >= 0).all():
        raise ValueError("Column 'os_best' contains values that are not above 0.")
    
    # Row Count
    if len(df) < 1000:
        raise ValueError("The DataFrame has fewer than 1000 rows - that is sus...")
    
    print("DataFrame validation passed.")

    return True


def fetch_views_df(PATH_RAW):
    """
    Fetches or loads the views DataFrame and saves it to a pickle file.

    Args:
        partition (str): The partition type (e.g., 'calibration').
        PATH_RAW (str): The path to the directory where raw data is stored.

    Returns:
        pd.DataFrame: The fetched or loaded DataFrame.
    """
    path_viewser_df = os.path.join(PATH_RAW, f'full_base_01_viewser_df.pkl') 

    # Create the folders if they don't exist
    os.makedirs(PATH_RAW, exist_ok=True)

    print('Fetching file...')
    df = fetch_data_from_viewser()

    # get the year range 
    year_first, year_last = get_year_range()

    # Filter the DataFrame by the year range
    df = filter_dataframe_by_year_range(df, year_first, year_last)

    # Save the DataFrame to a pickle file
    print(f'Saving file to {path_viewser_df}')
    df.to_pickle(path_viewser_df)

    # print the final size of the DataFrame
    print(f'Final size of DataFrame: {df.shape}')

    validate_dataframe(df)

    return df

if __name__ == "__main__":

    PATH_RAW_VIEWSER, PATH_RAW_EXTERNAL, PATH_PROCESSED, PATH_GENERATED = get_data_paths(PATH)
    df = fetch_views_df(PATH_RAW_VIEWSER)