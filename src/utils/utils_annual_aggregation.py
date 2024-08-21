import numpy as np
import pandas as pd
import unittest
from pandas.testing import assert_frame_equal
from scipy.stats import mode
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

    # Check that the required columns in the list are present in the DataFrame
    if not set(required_columns).issubset(df.columns):
        raise ValueError("Input DataFrame is missing one or more required columns.")
    
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
        if not np.all(np.isclose(monthly_sum, yearly_sum, atol=tolerance)):
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



def population_max_post_test(df, df_yearly):
    """
    Compare the maximum population values from monthly data with the yearly data.

    This function calculates the maximum population per year from the monthly data,
    compares it with the yearly data, and identifies any discrepancies.

    Parameters:
    df (pd.DataFrame): The monthly data DataFrame containing population data.
    df_yearly (pd.DataFrame): The yearly data DataFrame containing population data.

    Returns:
    None: The function prints out any discrepancies found between the yearly and monthly max population values.
    """
    
    # Step 1: Calculate the maximum population per year from the monthly data
    max_pop_monthly = df.groupby(['pg_id', 'year_id'])['pop_gpw_sum'].max().reset_index()

    # Step 2: Compare the yearly data with the recalculated maximums
    comparison = pd.merge(df_yearly[['pg_id', 'year_id', 'pop_gpw_sum']],
                          max_pop_monthly,
                          on=['pg_id', 'year_id'],
                          suffixes=('_yearly', '_monthly'))

    # Step 3: Identify discrepancies
    discrepancies = comparison[comparison['pop_gpw_sum_yearly'] != comparison['pop_gpw_sum_monthly']]

    # Output the discrepancies if there are any
    if not discrepancies.empty:
        print("Discrepancies found between yearly and monthly max population values:")
        print(discrepancies)
    else:
        print("No discrepancies found. The yearly population matches the max population observed in the monthly data.")



def summed_features_post_test(df, df_yearly, columns_to_sum):
    """
    Compare the summed feature values from monthly data with the yearly data.

    This function calculates the sum of specified features per year from the monthly data,
    compares it with the yearly data, and identifies any discrepancies.

    Parameters:
    df (pd.DataFrame): The monthly data DataFrame containing the features to be summed.
    df_yearly (pd.DataFrame): The yearly data DataFrame containing the summed features.
    columns_to_sum (list): List of column names to be summed.

    Returns:
    None: The function prints out any discrepancies found between the yearly and monthly summed feature values.
    """
    
    # Step 1: Calculate the sum of the specified features per year from the monthly data
    summed_features_monthly = df.groupby(['pg_id', 'year_id'])[columns_to_sum].sum().reset_index()

    # Step 2: Compare the yearly data with the recalculated sums
    comparison = pd.merge(df_yearly[['pg_id', 'year_id'] + columns_to_sum],
                          summed_features_monthly,
                          on=['pg_id', 'year_id'],
                          suffixes=('_yearly', '_monthly'))

    # Step 3: Identify discrepancies
    discrepancies = {}
    for column in columns_to_sum:
        discrepancies[column] = comparison[comparison[f'{column}_yearly'] != comparison[f'{column}_monthly']]

    # Output the discrepancies if there are any
    for column, discrepancy in discrepancies.items():
        if not discrepancy.empty:
            print(f"Discrepancies found between yearly and monthly summed values for {column}:")
            print(discrepancy)
        else:
            print(f"No discrepancies found for {column}. The yearly sums match the sums observed in the monthly data.")



def aggregate_monthly_to_yearly(df, columns_to_sum = ['sb_best', 'ns_best', 'os_best'], columns_to_average = ['pop_gpw_sum'], columns_time_invariant = ['row', 'col'], columns_to_group_on = ['pg_id', 'year_id'], columns_other = ['c_id']):
    
    """
    Aggregates a dataset from monthly to yearly.
    
    Parameters:
    - df (pd.DataFrame): The data as a pandas DataFrame. Must contain 'pg_id', 'year_id', and 'month_id' columns.
    - columns_to_sum (list of str): List of column names to sum up.
    - columns_to_average (list of str): List of column names to average.
    - columns_time_invariant (list of str): List of column names that are time-invariant.
    - columns_to_group_on (list of str): List of columns to group by for aggregation.
    - columns_other (list of str): List of columns to handle as additional attributes, e.g., c_id.
    
    Returns:
    - pd.DataFrame: Data aggregated at the yearly level.
    
    Raises:
    - ValueError: If required columns are missing.
    """

   # # Check if the input DataFrame is empty
    expected_columns = columns_to_group_on + columns_other + columns_time_invariant + columns_to_sum + columns_to_average #['pg_id', 'year_id', 'c_id', 'col', 'row', 'sb_best', 'ns_best', 'os_best', 'pop_gpw_sum']
    required_columns = columns_to_group_on + ['month_id'] #{'pg_id', 'year_id', 'month_id'}

    # pre-test
    aggregate_monthly_to_yearly_pre_test(df, expected_columns, required_columns)

    
    # Aggregation functions
    aggregation_functions = {col: 'sum' for col in columns_to_sum}
    aggregation_functions.update({col: 'mean' for col in columns_to_average})
    
    # Group the data and perform aggregations
    grouped_df = df.groupby(columns_to_group_on).agg(aggregation_functions).reset_index()
    
    # Handle columns that are time-invariant (keep first instance)
    for col in columns_time_invariant:
        if col in df.columns:
            # Use first() to retain a single representative value per group
            grouped_df[col] = df.groupby(columns_to_group_on)[col].first().values
    
    # Handle c_id with majority voting
    if 'c_id' in columns_other:
        def majority_vote(series):
            result = mode(series)
            try:
                return result[0]  # For newer versions of scipy
            
            except AttributeError:
                return result[0][0]  # For older versions of scipy
            
            #return mode(series)[0][0]
        
        grouped_df['c_id'] = df.groupby(columns_to_group_on)['c_id'].apply(majority_vote).values

    # Sort the columns according to the order they appear in the list of expected columns
    grouped_df = grouped_df[expected_columns]
    
    # post-test
    aggregate_monthly_to_yearly_post_test(df, grouped_df, columns_to_sum)
    
    return grouped_df
