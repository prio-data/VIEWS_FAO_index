import pandas as pd
import unittest
from pandas.testing import assert_frame_equal

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

    # Check that the required columns are present
    required_columns = {'pg_id', 'year_id', 'month_id'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"The DataFrame must contain the following columns: {required_columns}")
    
    # Check if the input DataFrame is empty
    expected_columns = ['pg_id', 'year_id', 'c_id', 'col', 'row', 'sb_best', 'ns_best', 'os_best', 'pop_gpw_sum']
    if df.empty:
        # Define the expected columns for the output DataFrame
        return pd.DataFrame(columns=expected_columns)

    # Check that all columns are numeric
    if not df.select_dtypes(include='number').columns.equals(df.columns):
        raise TypeError("All columns must be numeric for aggregation.")

    # Columns to group by
    grouping_columns = ['pg_id', 'year_id']
    
    # Identify monthly columns by excluding the grouping columns and 'month_id'
    monthly_columns = [col for col in df.columns if col not in grouping_columns + ['month_id']]
    
    # Group by 'pg_id' and 'year_id', summing the monthly columns
    df_yearly_summed = df.groupby(grouping_columns)[monthly_columns].sum().reset_index()
    
    # Identify yearly columns by excluding the monthly columns and grouping columns
    yearly_columns = [col for col in df.columns if col not in monthly_columns + grouping_columns + ['month_id']]

    # Get the first occurrence of the yearly columns since they don't change
    df_yearly_intact = df.groupby(grouping_columns)[yearly_columns].first().reset_index()
    
    # Merge the summed monthly data with the yearly data
    df_yearly = pd.merge(df_yearly_summed, df_yearly_intact, on=grouping_columns)

    # Sort the columns according to the order they appear in the list of expected columns
    df_yearly = df_yearly[expected_columns]

    return df_yearly

class TestAggregateMonthlyToYearly(unittest.TestCase):
    def setUp(self):
        # Sample data with true columns
        self.df = pd.DataFrame({
            'pg_id': [1, 1, 1, 2, 2, 2],
            'year_id': [2020, 2020, 2020, 2021, 2021, 2021],
            'month_id': [1, 2, 3, 1, 2, 3],
            'c_id': [10, 10, 10, 20, 20, 20],
            'col': [100, 100, 100, 200, 200, 200],
            'row': [1000, 1000, 1000, 2000, 2000, 2000],
            'sb_best': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            'ns_best': [1.1, 1.2, 1.3, 1.4, 1.5, 1.6],
            'os_best': [2.1, 2.2, 2.3, 2.4, 2.5, 2.6],
            'pop_gpw_sum': [100, 200, 300, 400, 500, 600]
        })

    def test_empty_dataframe(self):
        empty_df = pd.DataFrame(columns=self.df.columns)
        result_df = aggregate_monthly_to_yearly(empty_df)
        expected_df = pd.DataFrame(columns=['pg_id', 'year_id', 'c_id', 'col', 'row', 'sb_best', 'ns_best', 'os_best', 'pop_gpw_sum'])

        # Sort columns before comparison
        result_df = result_df.reindex(sorted(result_df.columns), axis=1)
        expected_df = expected_df.reindex(sorted(expected_df.columns), axis=1)

        assert_frame_equal(result_df, expected_df)

    def test_non_numeric_monthly_columns(self):
        df_non_numeric = self.df.copy()
        df_non_numeric['sb_best'] = ['a', 'b', 'c', 'd', 'e', 'f']
        with self.assertRaises(TypeError):
            aggregate_monthly_to_yearly(df_non_numeric)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)