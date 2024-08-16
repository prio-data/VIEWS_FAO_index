import numpy as np
import pandas as pd
from multiprocessing import Pool

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths
setup_project_paths(PATH)


def calculate_country_probabilities_per_country(country_df: pd.DataFrame, value_col: str, time_col: str) -> pd.DataFrame:
    """
    Calculate the probabilities p_i and P_i for each unique value in the dataset for a given country.

    Parameters:
    - country_df (pd.DataFrame): DataFrame containing data for a single country.
    - value_col (str): The column name for the voxel values.
    - time_col (str): The column name for the time periods.

    Returns:
    - pd.DataFrame: DataFrame with added columns for p_i and P_i probabilities.
    """
    if country_df.empty:
        raise ValueError("The input DataFrame for the country is empty.")
    
    if value_col not in country_df.columns:
        raise ValueError(f"The specified value column '{value_col}' does not exist in the country DataFrame.")
    
    if time_col not in country_df.columns:
        raise ValueError(f"The specified time column '{time_col}' does not exist in the country DataFrame.")
    
    # Calculate cumulative distribution
    cumulative_distribution = country_df[value_col].rank(method='max') / len(country_df)
    
    # Calculate total number of voxels
    total_units = len(country_df)
    
    # Calculate number of units per time unit
    num_units_per_time_unit = country_df.groupby(time_col).size().mean()
    
    # Calculate p_i
    p_i = cumulative_distribution / total_units
    
    # Calculate P_i
    P_i = 1 - (1 - p_i)**num_units_per_time_unit
    
    # Ensure p_i and P_i for 0 are set to 1
    zero_mask = country_df[value_col] == 0
    p_i[zero_mask] = 1
    P_i[zero_mask] = 1
    
    # Add results to DataFrame
    country_df[f'{value_col}_unit_likelihood_country'] = p_i.values
    country_df[f'{value_col}_time_unit_likelihood_country'] = P_i.values
    
    return country_df


def calculate_all_country_probabilities(df: pd.DataFrame, value_col: str, time_col: str) -> pd.DataFrame:
    """
    Calculate the probabilities p_i and P_i for each unique value in the dataset for all countries.

    Parameters:
    - df (pd.DataFrame): DataFrame containing data for all countries.
    - value_col (str): The column name for the voxel values.
    - time_col (str): The column name for the time periods.

    Returns:
    - pd.DataFrame: DataFrame with added columns for p_i and P_i probabilities for all countries.
    """
    if df.empty:
        raise ValueError("The input DataFrame is empty.")
    
    if value_col not in df.columns:
        raise ValueError(f"The specified value column '{value_col}' does not exist in the DataFrame.")
    
    if time_col not in df.columns:
        raise ValueError(f"The specified time column '{time_col}' does not exist in the DataFrame.")
    
    if 'c_id' not in df.columns:
        raise ValueError("The specified country ID column 'c_id' does not exist in the DataFrame.")
    
    countries = df['c_id'].unique()
    
    with Pool() as pool:
        results = pool.starmap(
            calculate_country_probabilities_per_country, 
            [(df[df['c_id'] == country], value_col, time_col) for country in countries]
        )
    
    result_df = pd.concat(results, ignore_index=True)
    
    return result_df


# unit test... 