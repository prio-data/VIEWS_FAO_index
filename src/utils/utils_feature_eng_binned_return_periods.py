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


def feature_eng_binned_return_periods_pretest(series, bins_types= 'auto', num_bins = 10, rounding_decimals = 0):
    
    """
    Pre-test the input parameters for the feature_eng_binned_return_periods function.

    This function checks the validity of the input parameters before they are used in the
    feature_eng_binned_return_periods function. It ensures that the series is a non-empty
    pandas Series, contains no NaNs, infinities, or negative values, and that the minimum
    value is 1. It also checks that num_bins and rounding_decimals are integers and that
    bins_types is a valid string, list, or numpy array.

    Parameters:
    -----------
    series : pd.Series
        The input data series to be checked.
    bins_types : str or list or np.ndarray, optional
        The type of bins to use. If 'auto', bins are created based on the logarithm of the series.
        Other valid string values are 'monthly_e_i', 'yearly_e_i', 'monthly_E_i', 'yearly_E_i'.
        Custom bins can also be provided as a list or numpy array. Default is 'auto'.
    num_bins : int, optional
        The number of bins to create if bins_types is 'auto'. Default is 10.
    rounding_decimals : int, optional
        The number of decimals to round the bins to if bins_types is 'auto'. Default is 0.

    Returns:
    --------
    bool
        Returns True if all checks pass, otherwise raises a ValueError with an appropriate message.

    Raises:
    -------
    ValueError
        If the series is not a pandas Series, is empty, contains NaNs, negative values, or zero values,
        or if num_bins or rounding_decimals are not integers, or if bins_types is not a valid value.

    Notes:
    ------
    - The function prints warnings if the series contains zero values or if the minimum value is not 1.
    - The function raises errors for invalid input types and values.

    """

    
    # test that the input is a pandas series
    if not isinstance(series, pd.Series):
        raise ValueError("Please provide a pandas Series as input.")
    
    #check that the series is not empty
    if series.empty:
        raise ValueError("The input series is empty. Please provide a non-empty series.")
    
    #check for nans, infs, and negative values
    if series.isnull().sum() > 0:
        raise ValueError("The input series contains NaN values. Please remove or replace them.")
    
    if (series < 0).sum() > 0:
        raise ValueError("The input series contains negative values. That does not make sense for return periods. Please remove or replace them.")
    
    # check for zero values
    if (series == 0).sum() > 0:
        print("The input series contains zero values. That does not make sense for return periods where minimum is 1. Please remove or replace them.")

    # check that the minimum value is 1
    if series.min() != 1:
        print("The minimum value in the series is not 1. We would expect a minmum value of 1 for return periods. Please check the input data.")

    # ceck num of bins is an integer
    if not isinstance(num_bins, int):
        raise ValueError("Please provide an integer value for num_bins.")
    
    # check rounding_decimals is an integer
    if not isinstance(rounding_decimals, int):
        raise ValueError("Please provide an integer value for rounding_decimals.")
    
    # check that num_bins is greater than 1
    if num_bins < 2:
        raise ValueError("Please provide a value greater than 1 for num_bins.")
    
    # check that the bins_types is a valid string or list or numpy array
    if not isinstance(bins_types, (str, list, np.ndarray)):
        raise ValueError("Please provide a valid bins_types value. Valid values are 'auto', 'monthly_e_i', 'yearly_e_i', 'monthly_E_i', 'yearly_E_i' or a list/np.array of costume values.")

    return True



def feature_eng_binned_return_periods_posttest(series, binned_series, bins_types, num_bins):


    """
    Post-test the output of the feature_eng_binned_return_periods function.

    This function checks the validity of the output from the feature_eng_binned_return_periods function.
    It ensures that the binned series is the same length as the input series, is a pandas Series, contains
    no NaNs or infinity values, and has more than one unique value. It also checks that the number of bins
    is correct and that there are values in each bin.

    Parameters:
    -----------
    series : pd.Series
        The original input data series that was binned.
    binned_series : pd.Series
        The binned series output from the feature_eng_binned_return_periods function.
    bins_types : str
        The type of bins used. Valid values are 'auto', 'monthly_e_i', 'yearly_e_i', 'monthly_E_i', 'yearly_E_i'.
    num_bins : int
        The number of bins created if bins_types is 'auto'.

    Returns:
    --------
    bool
        Returns True if all checks pass, otherwise raises a ValueError with an appropriate message.

    Raises:
    -------
    ValueError
        If the binned series is not the same length as the input series, is not a pandas Series, contains NaNs,
        infinity values, or only one unique value, or if the number of bins is incorrect, or if there are no
        values in one or more bins.

    Notes:
    ------
    - The function prints a warning if the number of bins is incorrect when bins_types is 'auto'.
    - The function raises errors for invalid output types and values.

    """


    # check if the binned series is the same length as the input series
    if len(binned_series) != len(series):
        raise ValueError("The binned series is not the same length as the input series. Please check the input parameters")

    # check that the binned series is a pandas series
    if not isinstance(binned_series, pd.Series):
        raise ValueError("The binned series is not a pandas Series. Please check the input parameters")

    # check that there are no NaNs of infinities in the binned series
    if binned_series.isnull().sum() > 0:
        raise ValueError("The binned series contains NaN values. Please check the input parameters")

    if np.isinf(binned_series).sum() > 0:
        raise ValueError("The binned series contains infinity values. Please check the input parameters")
    
    # Check that thare more than one unique value in the binned series
    if len(binned_series.unique()) < 2:
        raise ValueError("The binned series contains only one unique value. Please check the input parameters")
    
    # check if number of bins is correct
    if bins_types == 'auto' and len(binned_series.unique()) != (num_bins-1): # -1 because we have one more bin edge than bins
        print("WARNING: The number of bins is not correct. Please check the input parameters. You are not using a costume bins list and you have like set the number of bins to a value that is too high or the rounding_decimals to a value that is too high.")

    # check that there are values in each bin
    if not all(binned_series.value_counts()):
        raise ValueError("There are no values in one or more bins. Please check the input parameters")

    return True

def feature_eng_binned_return_periods(series, bins_types= 'auto', num_bins = 10, rounding_decimals = 0):


    """
    Bin a pandas Series into specified bins and return the binned series along with the bins used.

    Parameters:
    -----------
    series : pd.Series representing the return periods E_i or e_i
        The input data series to be binned.

    bins_types : str or list or np.ndarray, optional
        The type of bins to use. If 'auto', bins are created based on the logarithm of the series.
        Other valid string values are 'monthly_e_i', 'yearly_e_i', 'monthly_E_i', 'yearly_E_i'.
        Custom bins can also be provided as a list or numpy array.

    num_bins : int, optional
        The number of bins to create if bins_types is 'auto'. Default is 10.

    rounding_decimals : int, optional
        The number of decimals to round the bins to if bins_types is 'auto'. Default is 0.

    Returns:
    --------
    binned_series : pd.Series
        The series with values binned according to the specified bins.

    bins : np.ndarray
        The bins used for binning the series.

    Raises:
    -------
    ValueError
        If an invalid bins_types value is provided.

    Notes:
    ------
    - If bins_types is 'auto', the bins are created based on the logarithm of the series values.
    - If bins_types is 'monthly_e_i', 'yearly_e_i', 'monthly_E_i', or 'yearly_E_i', predefined bins are used.
    - If bins_types is a list or numpy array, those bins are used directly.
    - The function checks if the number of bins created is correct and if there are values in each bin.
    - The function extends the bins to infinity to ensure all values are binned.

    Examples:
    ---------
    >>> series = pd.Series(np.arange(0, 1000, 1))
    >>> binned_series, bins = feature_eng_binned_return_periods(series, bins_types='auto', num_bins=10, rounding_decimals=0)
    >>> print(binned_series)
    >>> print(bins)
    """    """
    
    """

    # pre-test
    feature_eng_binned_return_periods_pretest(series, bins_types, num_bins, rounding_decimals)


    if bins_types == 'auto':

        log_series = np.log1p(series)
        log_bins = np.linspace(log_series.min(), log_series.max(), num_bins)

        bins = np.expm1(log_bins)

        # Round bins and ensure they are unique
        bins = np.round(bins, rounding_decimals)
        bins = np.unique(bins)

    elif bins_types == 'monthly_e_i':
        bins = np.array([0, 100, 1000, 5000, 10000, 50000, 100000])

    elif bins_types == 'yearly_e_i':
        bins = np.array([0, 100, 400, 1200, 3600, 10000])

    elif bins_types == 'monthly_E_i':
        bins = np.array([0, 3, 6, 12, 24, 48, 72, 120, 240])

    elif bins_types == 'yearly_E_i':
        bins = np.array([0, 2, 4, 6, 10, 16, 24, 32])

    elif isinstance(bins_types, (list, np.ndarray)):
        bins = np.array(bins_types)

    else:
        raise ValueError("Please provide a valid bins_types value. Valid values are 'inferred', 'monthly_e_i', 'yearly_e_i', 'monthly_E_i', 'yearly_E_i'.")

    # Extend bins to infinity
    bins_extended = np.append(bins, np.inf)

    # Use the lower bounds as labels, excluding the last bin (inf)
    labels = bins

    # Bin the series
    binned_series = pd.cut(series, bins=bins_extended, labels=labels, right=False, include_lowest=True).astype(int)

    # post test
    feature_eng_binned_return_periods_posttest(series, binned_series, bins_types, num_bins)

    return binned_series, bins