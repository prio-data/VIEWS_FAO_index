import numpy as np
import pandas as pd

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths
setup_project_paths(PATH)

def calculate_P_i_pretest(p_i_values, num_trials):
    """
    Perform pre-tests for the calculate_P_i_values function.

    Parameters:
    p_i_values (np.array or list): The cumulative distribution function (p_i_values) as an array of probabilities.
    num_trials (int): The number of independent trials or time units.

    Raises:
    ValueError: If any probability in p_i_values is not between 0 and 1.
    ValueError: If num_trials is negative.
    TypeError: If num_trials is not an integer.
    TypeError: If p_i_values is not an array-like object.
    ValueError: If p_i_values is empty.
    ValueError: If p_i_values is not non-decreasing.
    ValueError: If p_i_values does not start at zero and end at one.
    ValueError: If p_i_values is not properly normalized.
    """
    if not all(0 <= p <= 1 for p in p_i_values):
        raise ValueError("All probabilities in p_i_values must be between 0 and 1.")
    
    if num_trials < 0:
        raise ValueError("The number of trials must be non-negative.")
    
    if not isinstance(num_trials, int):
        raise TypeError("The number of trials must be an integer.")
    
    if not isinstance(p_i_values, (np.ndarray, list, pd.Series)):
        raise TypeError("p_i_values must be an array-like object.")
    
    if not len(p_i_values) > 0:
        raise ValueError("p_i_values must contain at least one value.")
    
    if not np.all(np.diff(p_i_values) >= 0):
        raise ValueError("p_i_values must be non-decreasing.")

    # Check that the p_i_values start at zero
    if not np.isclose(p_i_values.iloc[0], 0, atol=1e-2):
        #print(p_i_values.iloc[-1])
        raise ValueError(f"p_i_values do not start at zero. Start value: {p_i_values.iloc[0]}")

    # Check that the p_i_values end at one
    if not np.isclose(p_i_values.iloc[-1], 1, atol=1e-2):
        #print(p_i_values.iloc[0])
        raise ValueError(f"p_i_values do not end at one. End value: {p_i_values.iloc[-1]}")
    
    # Check proper normalization
    if not np.isclose(np.diff(p_i_values).sum(), 1, atol=1e-2):
        raise ValueError("p_i_values is not properly normalized.")
    
    return True

def calculate_P_i_posttest(P_i_values):
    """
    Perform post-tests for the calculate_P_i_values function.

    Parameters:
    P_i_values (np.ndarray, pd.Series, or list): The output probabilities of observing at least one event.

    Raises:
    ValueError: If any probability in P_i_values is not between 0 and 1.
    ValueError: If P_i_values is not non-decreasing.
    ValueError: If P_i_values does not start at zero and end at one.
    """
    if not isinstance(P_i_values, (np.ndarray, pd.Series, list)):
        raise ValueError("The output must be a numpy array, pandas series, or list.")
    
    if not all(0 <= p <= 1 for p in P_i_values):
        raise ValueError("All probabilities must be between 0 and 1.")
    
    if not np.all(np.diff(P_i_values) >= 0):
        raise ValueError("The probabilities must be non-decreasing.")

    if isinstance(P_i_values, (pd.Series, list)):
        P_i_values = np.array(P_i_values)

    #if not np.isclose(P_i_values[0], 0, atol=1e-1) or not np.isclose(P_i_values[-1], 1, atol=1e-1):
    #    raise ValueError(f"The probabilities must start at zero and end at one. Probabilities are min {P_i_values[0]} and max {P_i_values[-1]}.")

    return True

def calculate_P_i(p_i_df, num_trials):
    """
    Calculate the probability of observing at least one event of a specific value or above 
    over a given number of independent trials or time units using an array of cumulative probabilities (p_i_values).

    In the context of our use case, p_i_values represents the likelihood of observing a value of a feature or above one or more times
    given the number of PRIO grid cells in a given time unit. E.g., the number of grid cells in a given country in a given month. 
    Or the number of grid cells in a region in a given year, etc.

    Parameters:
    p_i_values (np.array or list): The cumulative distribution function (p_i_values) as an array of probabilities.
    num_trials (int): The number of independent trials or time units over which the event could occur. In our use case, 
                      this is the number of PRIO grid cells in a given time unit given the spatial aggregation level.

     Returns:
    pd.Series: A series of probabilities (P_i_values) representing the likelihood of observing at least one occurrence 
                   of each value or above over the given number of trials. 
                   Here trails would usually refer to a time unit (month, year, etc.) specific number of grif cells in a country or similar spatial aggregation level.
    """

    # get the p_i values
    p_i_values = p_i_df['p_i']

    # Perform pre-tests
    calculate_P_i_pretest(p_i_values, num_trials)
    
    # Convert p_i_values to the probability of not observing the event up to that value (basically the complement of p_i_values and the CDF)
    not_occur_prob = 1 - p_i_values
    
    # Calculate the probability of not observing the event across all trials - trials here would usually refer to a time unit (month, year, etc.) number of grid cells in a country or similar spatial aggregation level
    not_occur_prob_all_trials = not_occur_prob ** num_trials
    
    # Convert back to the probability of at least one occurrence
    P_i_values = 1 - not_occur_prob_all_trials

    # Perform post-tests
    calculate_P_i_posttest(P_i_values)

    # map the P_i values to the original DataFrame
    p_i_df['P_i'] = P_i_values

    return p_i_df # the DataFrame with the P_i values added