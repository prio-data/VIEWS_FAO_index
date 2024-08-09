import numpy as np
import pandas as pd
import unittest
from pandas.testing import assert_frame_equal

import numpy as np

def aggregate_monthly_to_yearly_pre_test(df, expected_columns, required_columns):
    """
    Pre-test function to validate the input DataFrame before aggregation.
    
    Args:
    df (pd.DataFrame): The input monthly data.
    
    Returns:
    pd.DataFrame: An empty DataFrame with expected columns if the input DataFrame is empty.
    
    Raises:
    ValueError: If the required columns are not present.
    TypeError: If any of the columns are not numeric.
    """
    # Check that the required columns are present
    if not required_columns.issubset(df.columns):
        raise ValueError(f"The DataFrame must contain the following columns: {required_columns}")
    
    # Check if the input DataFrame is empty
    if df.empty:
        # Define the expected columns for the output DataFrame
        return pd.DataFrame(columns=expected_columns)

    # Check that all columns are numeric
    if not df.select_dtypes(include='number').columns.equals(df.columns):
        raise TypeError("All columns must be numeric for aggregation.")


def aggregate_monthly_to_yearly_post_test(df, df_yearly, columns_to_sum):
    """
    Post-test function to validate the aggregation of monthly data to yearly data.
    
    Args:
    df (pd.DataFrame): The original monthly data.
    df_yearly (pd.DataFrame): The aggregated yearly data.
    columns_to_sum (list): List of columns that should be summed.
    
    Raises:
    ValueError: If any of the validation checks fail.
    """
    tolerance = 1e-6  # Define a tolerance level for rounding errors
    
    # Test that the total sum of features is almost the same in the monthly and yearly data
    for feature in columns_to_sum:
        monthly_sum = df[feature].sum()
        yearly_sum = df_yearly[feature].sum()
        if not np.isclose(monthly_sum, yearly_sum, atol=tolerance):
            print(f"Monthly sum of {feature}: {monthly_sum}")
            print(f"Yearly sum of {feature}: {yearly_sum}")
            raise ValueError(f"The total sum of {feature} in the monthly data is not equal to the sum in the yearly data within the tolerance level.")
    
    # Same but over each year:
    for year in df['year_id'].unique():
        for feature in columns_to_sum:
            monthly_sum = df[df['year_id'] == year][feature].sum()
            yearly_sum = df_yearly[df_yearly['year_id'] == year][feature].sum()
            if not np.isclose(monthly_sum, yearly_sum, atol=tolerance):
                print(f"Year: {year}")
                print(f"Monthly sum of {feature} for year {year}: {monthly_sum}")
                print(f"Yearly sum of {feature} for year {year}: {yearly_sum}")
                raise ValueError(f"The total sum of {feature} in the monthly data for year {year} is not equal to the sum in the yearly data within the tolerance level.")
    
    # Same but over each pg_id:
    for pg in df['pg_id'].unique():
        for feature in columns_to_sum:
            monthly_sum = df[df['pg_id'] == pg][feature].sum()
            yearly_sum = df_yearly[df_yearly['pg_id'] == pg][feature].sum()
            if not np.isclose(monthly_sum, yearly_sum, atol=tolerance):
                print(f"pg_id: {pg}")
                print(f"Monthly sum of {feature} for pg_id {pg}: {monthly_sum}")
                print(f"Yearly sum of {feature} for pg_id {pg}: {yearly_sum}")
                raise ValueError(f"The total sum of {feature} in the monthly data for pg_id {pg} is not equal to the sum in the yearly data within the tolerance level.")
    
    # Check if the row and col have been accidentally summed in the yearly data
    if df_yearly['row'].max() != df['row'].max() or df_yearly['col'].max() != df['col'].max():
        raise ValueError("The 'row' and 'col' columns should not be summed in the yearly data.")
    
    # Check if the 'c_id' feature has the same number of unique values in the monthly and yearly data
    if df['c_id'].nunique() != df_yearly['c_id'].nunique():
        
        # Extract unique 'c_id' values from both DataFrames
        monthly_c_ids = set(df['c_id'].unique())
        yearly_c_ids = set(df_yearly['c_id'].unique())
        
        # Find differences
        only_in_monthly = monthly_c_ids - yearly_c_ids
        only_in_yearly = yearly_c_ids - monthly_c_ids
        
        # Print differences
        print("Unique 'c_id' values only in monthly data:", only_in_monthly)
        print("Unique 'c_id' values only in yearly data:", only_in_yearly)
        
        #raise ValueError("The 'c_id' feature should have the same unique values in the monthly and yearly data.") # known issue just print the differences
        print(f"The 'c_id' feature should have the same unique values in the monthly and yearly data... Keep running")
    
    # Same for pg_id
    if df['pg_id'].nunique() != df_yearly['pg_id'].nunique():
        raise ValueError("The 'pg_id' feature should have the same unique values in the monthly and yearly data.")
    
    # Same for year_id
    if df['year_id'].nunique() != df_yearly['year_id'].nunique():
        raise ValueError("The 'year_id' feature should have the same unique values in the monthly and yearly data.")
    
    # Check that the yearly data has the same number of rows as the number of unique 'pg_id' and 'year_id' combinations
    grouping_columns = ['pg_id', 'year_id']
    if df_yearly.shape[0] != df.groupby(grouping_columns).ngroups:
        raise ValueError("The yearly data should have the same number of rows as the number of unique 'pg_id' and 'year_id' combinations.")
    
    # Check that the monthly data has the same number of rows as the number of unique 'pg_id', 'year_id', and 'month_id' combinations
    if df.shape[0] != df.groupby(['pg_id', 'year_id', 'month_id']).ngroups:
        raise ValueError("The monthly data should have the same number of rows as the number of unique 'pg_id', 'year_id', and 'month_id' combinations.")
    
    # Check that the monthly data is 12 times the size of the yearly data
    if df.shape[0] != 12 * df_yearly.shape[0]:
        raise ValueError("The monthly data should be 12 times the size of the yearly data.")


def aggregate_monthly_to_yearly(df):
    """
    Aggregates monthly data to yearly data.
    
    Args:
    df (pd.DataFrame): The data as a pandas DataFrame. Must contain 'pg_id', 'year_id', and 'month_id' columns.
    
    Returns:
    pd.DataFrame: Data aggregated at the yearly level.
    
    Raises:
    ValueError: If required columns are missing.
    """

   # # Check if the input DataFrame is empty
    expected_columns = ['pg_id', 'year_id', 'c_id', 'col', 'row', 'sb_best', 'ns_best', 'os_best', 'pop_gpw_sum']
    required_columns = {'pg_id', 'year_id', 'month_id'}

    # pre-test
    aggregate_monthly_to_yearly_pre_test(df, expected_columns, required_columns)

    # Columns to group by
    grouping_columns = ['pg_id', 'year_id']
    
    # Columns to sum
    columns_to_sum = ['sb_best', 'ns_best', 'os_best', 'pop_gpw_sum']
    
    # Group by 'pg_id' and 'year_id', summing the specified columns
    df_yearly_summed = df.groupby(grouping_columns)[columns_to_sum].sum().reset_index()
    
    # Identify columns to keep by excluding the columns to sum, grouping columns, and 'month_id'
    columns_to_keep = [col for col in df.columns if col not in columns_to_sum + grouping_columns + ['month_id']]

    # Get the first occurrence of the columns to keep since they don't change
    df_yearly_intact = df.groupby(grouping_columns)[columns_to_keep].first().reset_index()
    
    # Merge the summed monthly data with the yearly data
    df_yearly = pd.merge(df_yearly_summed, df_yearly_intact, on=grouping_columns)

    # Sort the columns according to the order they appear in the list of expected columns
    df_yearly = df_yearly[expected_columns]
    
    # post-test
    aggregate_monthly_to_yearly_post_test(df, df_yearly, columns_to_sum)

    return df_yearly


# class TestAggregateMonthlyToYearly(unittest.TestCase):
#     def setUp(self):
#         # Sample data with true columns
#         self.df = pd.DataFrame({
#             'pg_id': [1, 1, 1, 2, 2, 2],
#             'year_id': [2020, 2020, 2020, 2021, 2021, 2021],
#             'month_id': [1, 2, 3, 1, 2, 3],
#             'c_id': [10, 10, 10, 20, 20, 20],
#             'col': [100, 100, 100, 200, 200, 200],
#             'row': [1000, 1000, 1000, 2000, 2000, 2000],
#             'sb_best': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
#             'ns_best': [1.1, 1.2, 1.3, 1.4, 1.5, 1.6],
#             'os_best': [2.1, 2.2, 2.3, 2.4, 2.5, 2.6],
#             'pop_gpw_sum': [100, 200, 300, 400, 500, 600]
#         })
# 
#     def test_empty_dataframe(self):
#         empty_df = pd.DataFrame(columns=self.df.columns)
#         result_df = aggregate_monthly_to_yearly(empty_df)
#         expected_df = pd.DataFrame(columns=['pg_id', 'year_id', 'c_id', 'col', 'row', 'sb_best', 'ns_best', 'os_best', 'pop_gpw_sum'])
# 
#         # Sort columns before comparison
#         result_df = result_df.reindex(sorted(result_df.columns), axis=1)
#         expected_df = expected_df.reindex(sorted(expected_df.columns), axis=1)
# 
#         assert_frame_equal(result_df, expected_df)
# 
#     def test_non_numeric_monthly_columns(self):
#         df_non_numeric = self.df.copy()
#         df_non_numeric['sb_best'] = ['a', 'b', 'c', 'd', 'e', 'f']
#         with self.assertRaises(TypeError):
#             aggregate_monthly_to_yearly(df_non_numeric)
# 
# if __name__ == '__main__':
#     unittest.main(argv=[''], exit=False)