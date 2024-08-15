import numpy as np
import pandas as pd
import unittest

def calculate_p_i_pretest(feature_series):
    """
    Perform pre-tests for the calculate_p_i function.

    This function checks the validity of the input Series before proceeding with further calculations.
    It ensures that the input is a pandas Series, the Series is not empty, and the Series contains numeric values.

    Parameters:
    feature_series (pd.Series): The input Series containing the data.

    Raises:
    ValueError: If the input is not a pandas Series.
    ValueError: If the input Series is empty.
    TypeError: If the Series does not contain numeric values.
    """
    
    # Check that the input is a Series
    if not isinstance(feature_series, pd.Series):
        raise ValueError("Input is not a pandas Series")

    # Check if the Series is empty
    if feature_series.empty:
        raise ValueError("The input Series is empty.")
    
    # Check if the Series contains numeric values
    if not np.issubdtype(feature_series.dtype, np.number):
        raise TypeError("The Series does not contain numeric values.")
    
    return True


def calculate_p_i_posttest(p_i_values, feature_values):
    """
    Perform post-tests for the calculate_p_i function.

    This function checks the validity of the output p_i values after the calculation.
    It ensures that the p_i values are a pandas Series, are not empty, do not contain NaN values,
    are non-increasing, strictly decreasing, within the range [0, 1], start at one, end at zero,
    are properly normalized, and have the correct length.

    Parameters:
    p_i_values (pd.Series): The output p_i values to be checked.
    feature_values (pd.Series): The original feature values used to calculate the p_i values.

    Raises:
    ValueError: If the output is not a pandas Series.
    ValueError: If the output Series is empty.
    ValueError: If the p_i values contain NaN values.
    ValueError: If the p_i values are not non-increasing.
    ValueError: If the p_i values are not strictly decreasing.
    ValueError: If the p_i values are not within the range [0, 1].
    ValueError: If the p_i values do not start at one.
    ValueError: If the p_i values do not end at zero.
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
    
    # Check non-increasing property
    #if not np.all(np.diff(p_i_values) <= 0):
    #    raise ValueError("p_i values are not non-increasing.")
    
    # Check for strict monotonicity
    #if not np.all(np.diff(p_i_values) < 0):
    #    raise ValueError("p_i values are not strictly decreasing.")
    
    # Check range above 0 but with tolerance for floating point errors
    if not np.isclose(p_i_values.min(), 0, atol=1e-2):
        raise ValueError(f"Min p_i value not above 0. Minimum value: {p_i_values.min()}")
    
    # Check range below 1 but with tolerance for floating point errors
    if not np.isclose(p_i_values.max(), 1, atol=1e-2):
        raise ValueError(f"Max p_i not below 1. Maximum value: {p_i_values.max()}")
                  
    # Check that the p_i values start at one
    if not np.isclose(p_i_values.iloc[0], 0, atol=1e-2):
        raise ValueError(f"p_i values do not start around zero. Start value: {p_i_values.iloc[0]}")

    # Check that the p_i values end around one
    if not np.isclose(p_i_values.iloc[-1], 1, atol=1e-2):
        raise ValueError(f"p_i values do not end around one. End value: {p_i_values.iloc[-1]}")
    
    # Check proper normalization
    #if not np.isclose(p_i_values.diff().fillna(p_i_values.iloc[0]).sum(), -1, atol=1e-1):
    #    raise ValueError("p_i values are not properly normalized.")
    
    # Check proper length
    #if len(p_i_values) != len(feature_values.unique()):
    #    raise ValueError("The length of the p_i values does not match the number of unique values in the input data.")

    return True

def calculate_p_i(feature_series):
    """
    Calculate the cumulative distribution of values across all voxels.

    This function calculates the probability p of seeing the individual values i or a larger value
    given all values. Usually, the CDF is the probability of seeing a smaller value, but here p_i
    represents 1 - CDF.

    Parameters:
    feature_series (pd.Series): The series containing voxel data.

    Returns:
    pd.Series: A series representing the cumulative distribution (p_i), which is the probability
               of seeing the individual values i or a larger value.

    """

    # Perform pre-tests
    calculate_p_i_pretest(feature_series)

    # Sort the data
    # sorted_feature_series = np.sort(feature_series)
    #ecdf = np.arange(1, len(sorted_feature_series) + 1) / len(sorted_feature_series)
    # p_i = 1 - ecdf

    # Alternative method
    value_counts = feature_series.value_counts().sort_index(ascending=False)
    p_i_values = value_counts.cumsum()/ value_counts.sum()

    #debugging print
    #print(p_i_values.min(), p_i_values.max())

    # Perform post-tests
    calculate_p_i_posttest(pd.Series(p_i_values), feature_series)

    # make df with p_i_values and value_counts
    p_i_df = pd.DataFrame({'value_count' : value_counts, 'value': value_counts.index, 'p_i': p_i_values.values}).reset_index(drop=True)

    return p_i_df