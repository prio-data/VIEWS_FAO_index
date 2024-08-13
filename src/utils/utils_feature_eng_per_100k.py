import numpy as np
import pandas as pd
import unittest

def feature_eng_fat_per_100k_precheck(df):

    # check if datafram is empty
    if df.empty:
        raise ValueError("Input DataFrame is empty")
    
    # Check if the required columns are present
    required_columns = ['sb_best', 'ns_best', 'os_best', 'pop_gpw_sum']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Column {col} is missing from the DataFrame")
        
    # Check for the correct data types
    for col in required_columns:
        if not np.issubdtype(df[col].dtype, np.number):
            raise ValueError(f"Column {col} does not have a numeric data type")
        
    # Check for NaN values
    if df[required_columns].isnull().values.any():
        raise ValueError("Input DataFrame contains NaN values")
    
    # Check for negative values
    if (df[required_columns] < 0).values.any():
        raise ValueError("Input DataFrame contains negative values")
    
    # check is either month_id or year_id is present
    if 'month_id' not in df.columns and 'year_id' not in df.columns:
        raise ValueError("Either 'month_id' or 'year_id' column is required in the DataFrame")

    # check for other relevant columns
    additional_columns = ['c_id', 'pg_id', 'row', 'col']
    for col in additional_columns:
        if col not in df.columns:
            raise ValueError(f"Column {col} is missing from the DataFrame")



def feature_eng_fat_per_100k_postcheck(df, new_columns):

    # check if datafram is empty
    if df.empty:
        raise ValueError("The generated DataFrame is empty")
                        
    # Check for the existence of the new columns
    for col in new_columns:
        if col not in df.columns:
            raise ValueError(f"New column {col} is missing from the DataFrame")

    # Check for the correct data types
    for col in new_columns:
        if not np.issubdtype(df[col].dtype, np.number):
            raise ValueError(f"Column {col} does not have a numeric data type")

    # Check for the correct number of rows
    if len(df) != len(df.dropna()):
        raise ValueError("The number of rows in the DataFrame has changed")

    # Above 0
    for col in new_columns:
        if (df[col] < 0).values.any():
            raise ValueError(f"Column {col} has negative values")

    # Not NaN, Inf or -Inf
    for col in new_columns:
        if df[col].isnull().values.any():
            raise ValueError(f"Column {col} contains NaN values")
        if np.isinf(df[col]).values.any():
            raise ValueError(f"Column {col} contains Inf values")
        if np.isneginf(df[col]).values.any():
            raise ValueError(f"Column {col} contains -Inf values")

    return df


def feature_eng_fat_per_100k(df):
    """
    Perform feature engineering to calculate fatalities per 100,000 population.

    Parameters:
    df (pd.DataFrame): Input DataFrame containing conflict data.

    Returns:
    pd.DataFrame: Modified DataFrame with new features.
    """

    # Checks
    feature_eng_fat_per_100k_precheck(df)

    # Total fatalities
    df['total_best'] = df['sb_best'] + df['ns_best'] + df['os_best']

    # Population normalization counts
    n_pop = 100000

    # Replace zero population values with NaN using the recommended method
    df.replace({'pop_gpw_sum': {0: np.nan}}, inplace=True)

    # Fatalities per 100,000 population for each type of conflict
    df['fatalities_per_100k'] = (df['total_best'] / df['pop_gpw_sum']) * n_pop
    df['sb_per_100k'] = (df['sb_best'] / df['pop_gpw_sum']) * n_pop
    df['ns_per_100k'] = (df['ns_best'] / df['pop_gpw_sum']) * n_pop
    df['os_per_100k'] = (df['os_best'] / df['pop_gpw_sum']) * n_pop

    # Fill NaNs with 0 - NaN values are created when dividing by 0 population, so it makes sense to fill them with 0
    df.fillna(0, inplace=True)

    # Test that all the new columns are created and have valid values:
    new_columns = ['fatalities_per_100k', 'sb_per_100k', 'ns_per_100k', 'os_per_100k']
    
    # Checks
    feature_eng_fat_per_100k_postcheck(df, new_columns)

    return df




class TestFeatureEngFatPer100k(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        data = {
            'sb_best': [10, 20, 30],
            'ns_best': [5, 15, 25],
            'os_best': [2, 12, 22],
            'pop_gpw_sum': [1000, 0, 3000]
        }
        self.df = pd.DataFrame(data)

    def test_feature_eng_fat_per_100k(self):
        # Apply the feature engineering function
        result_df = feature_eng_fat_per_100k(self.df.copy())

        # Check if new columns are created
        new_columns = ['fatalities_per_100k', 'sb_per_100k', 'ns_per_100k', 'os_per_100k']
        for col in new_columns:
            self.assertIn(col, result_df.columns)

        # Check if the values are correct
        expected_fatalities_per_100k = [1700.0, 0.0, 2566.6666666666665]
        actual_fatalities_per_100k = result_df['fatalities_per_100k'].values

        # Print actual values for debugging
        print("Actual fatalities_per_100k:", actual_fatalities_per_100k)

        # Use a tolerance level for floating-point comparison
        np.testing.assert_almost_equal(actual_fatalities_per_100k, expected_fatalities_per_100k, decimal=5)

        # Check if NaNs are filled with 0
        self.assertEqual(result_df['fatalities_per_100k'].iloc[1], 0)

        # Check for non-negative values
        for col in new_columns:
            self.assertTrue((result_df[col] >= 0).all())

        # Check for no NaN, Inf, or -Inf values
        for col in new_columns:
            self.assertFalse(result_df[col].isnull().values.any())
            self.assertFalse(np.isinf(result_df[col]).values.any())
            self.assertFalse(np.isneginf(result_df[col]).values.any())

if __name__ == '__main__':
    unittest.main()