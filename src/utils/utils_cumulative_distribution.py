import numpy as np 
import pandas as pd
import unittest

def calculate_global_cumulative_distribution(df, value_col):
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
    # Check if the DataFrame is empty
    if df.empty:
        raise ValueError("The input DataFrame is empty.")
    
    # Check if the column exists in the DataFrame
    if value_col not in df.columns:
        raise KeyError(f"The column '{value_col}' does not exist in the DataFrame.")
    
    # Check if the column contains numeric values
    if not np.issubdtype(df[value_col].dtype, np.number):
        raise TypeError(f"The column '{value_col}' does not contain numeric values.")
    
    # Calculate the frequency of each unique value
    value_counts = df[value_col].value_counts().sort_index(ascending=False)
    
    # Compute the cumulative distribution
    cumulative_distribution = value_counts.cumsum()
    
    # Check if the cumulative distribution is correctly calculated
    if cumulative_distribution.empty:
        raise ValueError("The cumulative distribution calculation resulted in an empty series.")
    
    return cumulative_distribution


# class TestCalculateCumulativeDistribution(unittest.TestCase):
# 
#     def test_empty_dataframe(self):
#         df = pd.DataFrame()
#         with self.assertRaises(ValueError):
#             calculate_cumulative_distribution(df, 'value')
# 
#     def test_column_not_exist(self):
#         df = pd.DataFrame({'value': [1, 2, 3]})
#         with self.assertRaises(KeyError):
#             calculate_cumulative_distribution(df, 'non_existent_column')
# 
#     def test_non_numeric_column(self):
#         df = pd.DataFrame({'value': ['a', 'b', 'c']})
#         with self.assertRaises(TypeError):
#             calculate_cumulative_distribution(df, 'value')
# 
#     def test_correct_cumulative_distribution(self):
#         df = pd.DataFrame({'value': [1, 2, 2, 3, 3, 3]})
#         expected_result = pd.Series([3, 5, 6], index=[3, 2, 1])
#         result = calculate_cumulative_distribution(df, 'value')
#         pd.testing.assert_series_equal(result, expected_result)
# 
#     def test_single_value_column(self):
#         df = pd.DataFrame({'value': [1]})
#         expected_result = pd.Series([1], index=[1])
#         result = calculate_cumulative_distribution(df, 'value')
#         pd.testing.assert_series_equal(result, expected_result)
# 
#     def test_all_same_values(self):
#         df = pd.DataFrame({'value': [2, 2, 2, 2]})
#         expected_result = pd.Series([4], index=[2])
#         result = calculate_cumulative_distribution(df, 'value')
#         pd.testing.assert_series_equal(result, expected_result)
# 
# if __name__ == '__main__':
#     unittest.main()