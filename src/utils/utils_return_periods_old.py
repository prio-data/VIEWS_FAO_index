import pandas as pd
import unittest

def calculate_return_periods(df, p_i_col, P_i_col):
    """
    Calculate the expected number of time periods and voxels to survey to find at least one voxel with a value greater than or equal to i.

    Parameters:
    df (pd.DataFrame): Dataframe containing values, p_i, and P_i.
    p_i_col (str): The name of the column containing unit likelihoods (p_i).
    P_i_col (str): The name of the column containing time unit likelihoods (P_i).

    Returns:
    pd.DataFrame: The original dataframe with added columns for time unit return periods (E_i) and unit return periods (E_{i}^{voxels}).
    """
    # Check if required columns exist in the dataframe
    if p_i_col not in df.columns or P_i_col not in df.columns:
        raise ValueError(f"Columns {p_i_col} and/or {P_i_col} not found in dataframe")

    # Infer value_col by removing the '_unit_likelihood' suffix from p_i_col
    value_col = p_i_col.replace("_unit_likelihood", "")

    # If the value_col ends on "_country" we need to remove that as well
    if value_col.endswith("_country"):
        value_col = value_col.replace("_country", "")
        suffix = "_country"
    else:
        suffix = ""

    # Calculate E_i = 1 / P_i
    df[f'{value_col}_time_unit_return_period{suffix}'] = df[P_i_col].apply(lambda x: 1 / x if x != 0 else float('inf'))
    
    # Calculate E_{i}^{voxels} = 1 / p_i
    df[f'{value_col}_unit_return_period{suffix}'] = df[p_i_col].apply(lambda x: 1 / x if x != 0 else float('inf'))
    
    return df

#
#class TestCalculateReturnPeriods(unittest.TestCase):
#
#    def setUp(self):
#        # Sample dataframe for testing
#        self.df = pd.DataFrame({
#            'value_unit_likelihood': [0.1, 0.2, 0.0, 0.5],
#            'value_time_unit_likelihood': [0.05, 0.1, 0.2, 0.0]
#        })
#
#    def test_calculate_return_periods(self):
#        result_df = calculate_return_periods(self.df, 'value_unit_likelihood', 'value_time_unit_likelihood')
#        expected_time_unit_return_period = [20.0, 10.0, 5.0, float('inf')]
#        expected_unit_return_period = [10.0, 5.0, float('inf'), 2.0]
#        
#        self.assertTrue((result_df['value_time_unit_return_period'] == expected_time_unit_return_period).all())
#        self.assertTrue((result_df['value_unit_return_period'] == expected_unit_return_period).all())
#
#    def test_missing_columns(self):
#        with self.assertRaises(ValueError):
#            calculate_return_periods(self.df, 'missing_col', 'value_time_unit_likelihood')
#
#    def test_zero_values(self):
#        result_df = calculate_return_periods(self.df, 'value_unit_likelihood', 'value_time_unit_likelihood')
#        self.assertEqual(result_df['value_time_unit_return_period'][3], float('inf'))
#        self.assertEqual(result_df['value_unit_return_period'][2], float('inf'))
#
#if __name__ == '__main__':
#    unittest.main()