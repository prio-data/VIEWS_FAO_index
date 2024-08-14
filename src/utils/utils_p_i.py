import numpy as np 
import pandas as pd
import unittest

def calculate_p_i_pretest(df, value_col):
    """
    Perform pre-tests for the calculate_p_i function.

    This function checks the validity of the input DataFrame and the specified column
    before proceeding with further calculations. It ensures that the input is a pandas
    DataFrame, the DataFrame is not empty, the specified column exists, and the column
    contains numeric values.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the data.
    value_col (str): The name of the column in the DataFrame to be checked.

    Raises:
    ValueError: If the input is not a pandas DataFrame.
    ValueError: If the input DataFrame is empty.
    KeyError: If the specified column does not exist in the DataFrame.
    TypeError: If the specified column does not contain numeric values.
    """
    
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


def calculate_p_i_posttest(p_i_values, feature_values):
    """
    Perform post-tests for the calculate_p_i function.

    This function checks the validity of the output p_i values
    after the calculation. It ensures that the p_i values are a pandas
    Series, are not empty, do not contain NaN values, are non-decreasing,
    strictly increasing, within the range [0, 1], start at zero, end at one,
    are properly normalized, and have the correct length.

    Parameters:
    p_i_values (pd.Series): The output p_i values to be checked.
    feature_values (pd.Series): The original feature values used to calculate the p_i values.

    Raises:
    ValueError: If the output is not a pandas Series.
    ValueError: If the output Series is empty.
    ValueError: If the p_i values contain NaN values.
    ValueError: If the p_i values are not non-decreasing.
    ValueError: If the p_i values are not strictly increasing.
    ValueError: If the p_i values are not within the range [0, 1].
    ValueError: If the p_i values do not start at zero.
    ValueError: If the p_i values do not end at one.
    ValueError: If the p_i values are not properly normalized.
    ValueError: If the length of the p_i values does not match the number of unique values in the input data.
    """
    
    # Check if a Series is returned
    if not isinstance(p_i_values, pd.Series):
        raise ValueError("The output is not a pandas Series.")
    
    # Check that it is not empty
    if p_i_values.empty:
        raise ValueError("The output Series is empty.")
    
    # Check for NaN values
    if p_i_values.isna().any():
        raise ValueError("The p_i values contain NaN values.")
    
    # Check non-decreasing property
    if not np.all(np.diff(p_i_values) >= 0):
        raise ValueError("p_i values are not non-decreasing.")
    
    # Check for strict monotonicity
    if not np.all(np.diff(p_i_values) > 0):
        raise ValueError("p_i values are not strictly increasing.")
    
    # Check range
    if not (np.all(p_i_values >= 0) and np.all(p_i_values <= 1)):
        raise ValueError("p_i values are not within the range [0, 1].")
    
    # Check that the p_i values start at zero
    if not np.isclose(p_i_values.iloc[0], 0, atol=1e-5):
        print(p_i_values.iloc[-1])
        raise ValueError(f"p_i values do not start at zero. Start value: {p_i_values.iloc[0]}")

    # Check that the p_i values end at one
    if not np.isclose(p_i_values.iloc[-1], 1, atol=1e-5):
        print(p_i_values.iloc[0])
        raise ValueError(f"p_i values do not end at one. End value: {p_i_values.iloc[-1]}")
    
    # Check proper normalization
    if not np.isclose(p_i_values.diff().fillna(p_i_values.iloc[0]).sum(), 1):
        raise ValueError("p_i values are not properly normalized.")
    
    # Check proper length
    if len(p_i_values) != len(feature_values.unique()):
        raise ValueError("The length of the p_i values does not match the number of unique values in the input data.")


def calculate_p_i(df, value_col):
    """
    Calculate the cumulative distribution of values across all voxels.

    This function calculates the probability p of seeing the individual values i or a larger value
    given all values. Usually, the CDF is the probability of seeing a smaller value, but here p_i
    represents 1 - CDF.

    Parameters:
    df (pd.DataFrame): The dataframe containing voxel data.
    value_col (str): The name of the column containing grid cell values.

    Returns:
    pd.Series: A series representing the cumulative distribution (p_i), which is the probability
               of seeing the individual values i or a larger value.

    """

    # Perform pre-tests
    calculate_p_i_pretest(df, value_col)
    
    # Calculate the frequency of each unique value
    value_counts = df[value_col].value_counts().sort_index(ascending=False)
    
    # Compute the cumulative distribution
    p_i_unnormed = value_counts.cumsum()

    # Normalize the cumulative distribution to get p_i
    p_i = p_i_unnormed / p_i_unnormed.iloc[-1]

    # Perform post-tests
    calculate_p_i_posttest(p_i, df[value_col])

    return p_i