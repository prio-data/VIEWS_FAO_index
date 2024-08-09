import pandas as pd

def check_expected_features(df):
    """
    Check that all the expected columns are present in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to check.
    expected_columns (list): A list of expected column names.

    Raises:
    AssertionError: If any expected column is missing from the DataFrame.
    """

    expected_features = [
        'total_best', 'fatalities_per_100k', 'sb_per_100k', 'ns_per_100k', 'os_per_100k',
        'fatalities_per_100k_unit_likelihood', 'fatalities_per_100k_time_unit_likelihood',
        'sb_per_100k_unit_likelihood', 'sb_per_100k_time_unit_likelihood',
        'ns_per_100k_unit_likelihood', 'ns_per_100k_time_unit_likelihood',
        'os_per_100k_unit_likelihood', 'os_per_100k_time_unit_likelihood',
        'total_best_unit_likelihood', 'total_best_time_unit_likelihood',
        'fatalities_per_100k_unit_return_period', 'fatalities_per_100k_time_unit_return_period',
        'sb_per_100k_unit_return_period', 'sb_per_100k_time_unit_return_period',
        'ns_per_100k_unit_return_period', 'ns_per_100k_time_unit_return_period',
        'os_per_100k_unit_return_period', 'os_per_100k_time_unit_return_period',
        'total_best_unit_return_period', 'total_best_time_unit_return_period',
        'fatalities_per_100k_unit_likelihood_country', 'fatalities_per_100k_time_unit_likelihood_country',
        'sb_per_100k_unit_likelihood_country', 'sb_per_100k_time_unit_likelihood_country',
        'ns_per_100k_unit_likelihood_country', 'ns_per_100k_time_unit_likelihood_country',
        'os_per_100k_unit_likelihood_country', 'os_per_100k_time_unit_likelihood_country',
        'total_best_unit_likelihood_country', 'total_best_time_unit_likelihood_country',
        'fatalities_per_100k_unit_return_period_country', 'fatalities_per_100k_time_unit_return_period_country',
        'sb_per_100k_unit_return_period_country', 'sb_per_100k_time_unit_return_period_country',
        'ns_per_100k_unit_return_period_country', 'ns_per_100k_time_unit_return_period_country',
        'os_per_100k_unit_return_period_country', 'os_per_100k_time_unit_return_period_country',
        'total_best_unit_return_period_country', 'total_best_time_unit_return_period_country'
    ]

    for col in expected_features:
        assert col in df.columns, f"Column {col} is missing from the DataFrame"

