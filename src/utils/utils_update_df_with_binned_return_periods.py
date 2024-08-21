import numpy as np
import pandas as pd

import os
from pathlib import Path
import sys

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths
setup_project_paths(PATH)

from utils_get_time_period import get_time_period
from utils_feature_eng_binned_return_periods import feature_eng_binned_return_periods

def process_binning_pretest(df):

    """
     Preprocess and validate the input DataFrame for binning.

    This function performs several checks on the input DataFrame to ensure it is suitable for binning operations.
    It verifies that the input is a pandas DataFrame, is not empty, contains the expected columns based on the time period,
    and that these columns are not empty, do not contain NaNs or infinities, and have more than one unique value.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame to be validated.

    Returns:
    --------
    bool
        Returns True if all checks pass.

    Raises:
    -------
    ValueError
        If the input is not a pandas DataFrame.
        If the input DataFrame is empty.
        If the input DataFrame does not contain the expected columns.
        If any expected column is empty.
        If any expected column contains NaNs or infinities.
        If any expected column has less than two unique values.
    """


    # check that the input is a padas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    
    # check that the input DataFrame is not empty
    if df.empty:
        raise ValueError("Input DataFrame is empty.")
    
    # check that the input DataFrame has the expected columns
    time_period = get_time_period(df)

    if time_period == 'year_id':

        expected_columns = ['pg_id', 'year_id', 'c_id', 'row', 'col', 'sb_best', 'ns_best',
       'os_best', 'pop_gpw_sum', 'total_best', 'fatalities_per_100k',
       'sb_per_100k', 'ns_per_100k', 'os_per_100k',
       'total_best_per_100k_country', 'sb_best_per_100k_country',
       'os_best_per_100k_country', 'ns_best_per_100k_country',
       'sb_best_value_count', 'sb_best_p_i', 'sb_best_P_i', 'sb_best_e_i',
       'sb_best_E_i', 'ns_best_value_count', 'ns_best_p_i', 'ns_best_P_i',
       'ns_best_e_i', 'ns_best_E_i', 'os_best_value_count', 'os_best_p_i',
       'os_best_P_i', 'os_best_e_i', 'os_best_E_i', 'total_best_value_count',
       'total_best_p_i', 'total_best_P_i', 'total_best_e_i', 'total_best_E_i']
        
    elif time_period == 'month_id':

        expected_columns = ['month_id', 'pg_id', 'year_id', 'c_id', 'col', 'row', 'sb_best',
       'ns_best', 'os_best', 'pop_gpw_sum', 'month', 'total_best',
       'fatalities_per_100k', 'sb_per_100k', 'ns_per_100k', 'os_per_100k',
       'total_best_per_100k_country', 'sb_best_per_100k_country',
       'os_best_per_100k_country', 'ns_best_per_100k_country',
       'sb_best_value_count', 'sb_best_p_i', 'sb_best_P_i', 'sb_best_e_i',
       'sb_best_E_i', 'ns_best_value_count', 'ns_best_p_i', 'ns_best_P_i',
       'ns_best_e_i', 'ns_best_E_i', 'os_best_value_count', 'os_best_p_i',
       'os_best_P_i', 'os_best_e_i', 'os_best_E_i', 'total_best_value_count',
       'total_best_p_i', 'total_best_P_i', 'total_best_e_i', 'total_best_E_i',]
        
    else:
        raise ValueError("Time period not recognized.")
    
    for column in expected_columns:
        if column not in df.columns:
            raise ValueError(f"Expected column '{column}' not found in input DataFrame.")
        
        # see if the column is empty
        if df[column].isnull().all():
            raise ValueError(f"Column '{column}' is empty.")
        
        # see if the column has any nans or infs
        if df[column].isnull().any() or df[column].isin([np.inf, -np.inf]).any():
            raise ValueError(f"Column '{column}' contains NaNs or infinities.")
        
        # see if the column have more than one unique value
        if df[column].nunique() < 2:
            raise ValueError(f"Column '{column}' has less than two unique values.")

    return True


def process_binning_posttest(df, new_feature_name_list):

    """
    Post-process and validate the input DataFrame after binning.

    This function performs several checks on the input DataFrame to ensure it is suitable after binning operations.
    It verifies that the input is a pandas DataFrame, is not empty, contains the expected columns (including new features),
    and that these columns are not empty, do not contain NaNs or infinities, and have more than one unique value.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame to be validated.
    new_feature_name_list : list
        A list of new feature names that should be included in the DataFrame after binning.

    Returns:
    --------
    bool
        Returns True if all checks pass.

    Raises:
    -------
    ValueError
        If the input is not a pandas DataFrame.
        If the input DataFrame is empty.
        If the input DataFrame does not contain the expected columns (including new features).
        If any expected column is empty.
        If any expected column contains NaNs or infinities.
        If any expected column has less than two unique values.
    """

    # check that the input is a padas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    
    # check that the input DataFrame is not empty
    if df.empty:
        raise ValueError("Input DataFrame is empty.")
    
    # check that the input DataFrame has the expected columns now including the new features
    time_period = get_time_period(df)

    if time_period == 'year_id':

        expected_columns = ['pg_id', 'year_id', 'c_id', 'row', 'col', 'sb_best', 'ns_best',
       'os_best', 'pop_gpw_sum', 'total_best', 'fatalities_per_100k',
       'sb_per_100k', 'ns_per_100k', 'os_per_100k',
       'total_best_per_100k_country', 'sb_best_per_100k_country',
       'os_best_per_100k_country', 'ns_best_per_100k_country',
       'sb_best_value_count', 'sb_best_p_i', 'sb_best_P_i', 'sb_best_e_i',
       'sb_best_E_i', 'ns_best_value_count', 'ns_best_p_i', 'ns_best_P_i',
       'ns_best_e_i', 'ns_best_E_i', 'os_best_value_count', 'os_best_p_i',
       'os_best_P_i', 'os_best_e_i', 'os_best_E_i', 'total_best_value_count',
       'total_best_p_i', 'total_best_P_i', 'total_best_e_i', 'total_best_E_i'] + new_feature_name_list
        
    elif time_period == 'month_id':

        expected_columns = ['month_id', 'pg_id', 'year_id', 'c_id', 'col', 'row', 'sb_best',
       'ns_best', 'os_best', 'pop_gpw_sum', 'month', 'total_best',
       'fatalities_per_100k', 'sb_per_100k', 'ns_per_100k', 'os_per_100k',
       'total_best_per_100k_country', 'sb_best_per_100k_country',
       'os_best_per_100k_country', 'ns_best_per_100k_country',
       'sb_best_value_count', 'sb_best_p_i', 'sb_best_P_i', 'sb_best_e_i',
       'sb_best_E_i', 'ns_best_value_count', 'ns_best_p_i', 'ns_best_P_i',
       'ns_best_e_i', 'ns_best_E_i', 'os_best_value_count', 'os_best_p_i',
       'os_best_P_i', 'os_best_e_i', 'os_best_E_i', 'total_best_value_count',
       'total_best_p_i', 'total_best_P_i', 'total_best_e_i', 'total_best_E_i'] + new_feature_name_list
        
    else:
        raise ValueError("Time period not recognized.")
    
    for column in expected_columns:
        if column not in df.columns:
            raise ValueError(f"Expected column '{column}' not found in input DataFrame.")
        
        # see if the column is empty
        if df[column].isnull().all():
            raise ValueError(f"Column '{column}' is empty.")
        
        # see if the column has any nans or infs
        if df[column].isnull().any() or df[column].isin([np.inf, -np.inf]).any():
            raise ValueError(f"Column '{column}' contains NaNs or infinities.")
        
        # see if the column have more than one unique value
        if df[column].nunique() < 2:
            raise ValueError(f"Column '{column}' has less than two unique values.")

    return True


def process_binning(df):
    """
    Processes binning for the given DataFrame based on the time period and feature engineering function.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame containing the data to be processed.

    Returns:
    --------
    pd.DataFrame
        The DataFrame with new binned features added.
    list
        A list of bins used for each feature.
    """

    process_binning_pretest(df)

    time_period = get_time_period(df)
    bins_list = []

    new_feature_name_list = []

    for feature in df.columns:
        if 'e_i' in feature:
            bin_types = f'{time_period.split("_")[0]}ly_e_i'
            new_feature_name = feature.replace('e_i', 'b_i')
            df[new_feature_name], bins = feature_eng_binned_return_periods(df[feature], bin_types)
            new_feature_name_list.append(new_feature_name)
            print(f"Processed feature '{feature}' into '{new_feature_name}' with bin types '{bin_types}'")
            bins_list.append(bins)
            print(f"Processed feature '{feature}' into '{new_feature_name}' with bin types '{bin_types}'")

        elif 'E_i' in feature:
            bin_types = f'{time_period.split("_")[0]}ly_E_i'
            new_feature_name = feature.replace('E_i', 'B_i')
            df[new_feature_name], bins = feature_eng_binned_return_periods(df[feature], bin_types)
            new_feature_name_list.append(new_feature_name)
            print(f"Processed feature '{feature}' into '{new_feature_name}' with bin types '{bin_types}'")
            bins_list.append(bins)
            print(f"Processed feature '{feature}' into '{new_feature_name}' with bin types '{bin_types}'")

        else:
            pass

    process_binning_posttest(df, new_feature_name_list)

    return df, bins_list