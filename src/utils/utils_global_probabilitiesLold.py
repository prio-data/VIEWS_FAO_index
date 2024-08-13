import numpy as np
import pandas as pd

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths
setup_project_paths(PATH)

from utils_cumulative_distribution import calculate_global_cumulative_distribution

def calculate_global_probabilities(df, value_col, time_col):
    """
    Calculate probabilities p_i and P_i for each unique value in the dataset and map them to the original DataFrame.

    Parameters:
    df (pd.DataFrame): The dataframe containing voxel data.
    value_col (str): The name of the column containing voxel values.
    time_col (str): The name of the column representing time units.
    stat_measure (str): The statistical measure to use for num_units_per_time_unit ('mean', 'median', 'mode').

    Returns:
    pd.DataFrame: The original dataframe with added columns for unit_likelihood and time_unit_likelihood.
    """
    # Check if the DataFrame is empty
    if df.empty:
        raise ValueError("The input DataFrame is empty.")
    
    # Check if the specified columns exist in the DataFrame
    if value_col not in df.columns:
        raise ValueError(f"The specified value column '{value_col}' does not exist in the DataFrame.")
    if time_col not in df.columns:
        raise ValueError(f"The specified time column '{time_col}' does not exist in the DataFrame.")
    
    # Calculate cumulative distribution
    try:
        cumulative_distribution = calculate_global_cumulative_distribution(df, value_col)
        
    except Exception as e:
        raise RuntimeError(f"Error calculating cumulative distribution: {e}")
    
    # Calculate total number of units
    total_units = df.shape[0]
    
    # Calculate the number of units per time unit
    num_units_per_time_unit = df.groupby(time_col).size().mean() # same as just taking one month

    # Calculate p_i (unit likelihood)
    p_i = cumulative_distribution / total_units
    
    # Calculate P_i (time unit likelihood)
    P_i = 1 - (1 - p_i)**num_units_per_time_unit
    
    # Create a DataFrame with values, p_i, and P_i
    probabilities_df = pd.DataFrame({
        value_col: cumulative_distribution.index,
        f'{value_col}_unit_likelihood': p_i.values,
        f'{value_col}_time_unit_likelihood': P_i.values
    })
    
    # Merge the probabilities_df with the original df on the value_col
    df = df.merge(probabilities_df, left_on=value_col, right_on=value_col, how='left')
    
    return df


# unittest... 