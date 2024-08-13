import numpy as np 
import pandas as pd
import unittest

def calculate_cumulative_distribution_pretest(df, value_col):

    # check that the input is a DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a pandas DataFrame")

    # Check if the DataFrame is empty
    if df.empty:
        raise ValueError("The input DataFrame is empty.")
    
    # Check if the column exists in the DataFrame
    if value_col not in df.columns:
        raise KeyError(f"The column '{value_col}' does not exist in the DataFrame.")
    
    # Check if the column contains numeric values
    if not np.issubdtype(df[value_col].dtype, np.number):
        raise TypeError(f"The column '{value_col}' does not contain numeric values.")
    


def calculate_cumulative_distribution_posttest(cdf_values, feature_values):
    # Check if a Series is returned
    if not isinstance(cdf_values, pd.Series):
        raise ValueError("The output is not a pandas Series.")
    
    # Check that it is not empty
    if cdf_values.empty:
        raise ValueError("The output Series is empty.")
    
    # Check for NaN values
    if cdf_values.isna().any():
        raise ValueError("The CDF contains NaN values.")
    
    # Check non-decreasing property
    if not np.all(np.diff(cdf_values) >= 0):
        raise ValueError("CDF is not non-decreasing.")
    
    # Check for strict monotonicity
    if not np.all(np.diff(cdf_values) > 0):
        raise ValueError("CDF is not strictly increasing.")
    
    # Check range
    if not (np.all(cdf_values >= 0) and np.all(cdf_values <= 1)):
        raise ValueError("CDF values are not within the range [0, 1].")
    
    # Check limits should be zero or above and one or below
    if not np.isclose(cdf_values.iloc[0], 0, atol=1e-5) or not np.isclose(cdf_values.iloc[-1], 1):
        raise ValueError("CDF does not start at zero and end at one.")
    
    # Check proper normalization
    if not np.isclose(cdf_values.diff().fillna(cdf_values.iloc[0]).sum(), 1):
        raise ValueError("CDF is not properly normalized.")
    
    # Check proper length
    if len(cdf_values) != len(feature_values.unique()):
        raise ValueError("The length of the CDF does not match the number of unique values in the input data.")
        



def calculate_cumulative_distribution(df, value_col):
    """
    Calculate the cumulative distribution of values across all voxels.

    Parameters:
    df (pd.DataFrame): The dataframe containing voxel data.
    value_col (str): The name of the column containing voxel values.

    Returns:
    pd.Series: A series representing the cumulative distribution.

    Raises:
    ValueError: If the DataFrame is empty.
    KeyError: If the specified column does not exist in the DataFrame.
    TypeError: If the specified column does not contain numeric values.
    """

    # Perform pre-tests
    calculate_cumulative_distribution_pretest(df, value_col)
    
    # Calculate the frequency of each unique value
    value_counts = df[value_col].value_counts().sort_index(ascending=False)
    
    # Compute the cumulative distribution
    cumulative_distribution = value_counts.cumsum()

    # Normalize the cumulative distribution to get the CDF
    cdf = cumulative_distribution / cumulative_distribution.iloc[-1]

    # Perform post-tests
    calculate_cumulative_distribution_posttest(cdf, df[value_col])

    return cdf


