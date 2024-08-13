import numpy as np
import pandas as pd
from multiprocessing import Pool

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths
setup_project_paths(PATH)

def calculate_likelihood_of_at_least_one_event_pretest(cdf, num_trials):

    if not all(0 <= p <= 1 for p in cdf):
        raise ValueError("All probabilities in the CDF must be between 0 and 1.")
    
    if num_trials < 0:
        raise ValueError("The number of trials must be non-negative.")
    
    if not isinstance(num_trials, int):
        raise TypeError("The number of trials must be an integer.")
    
    if not isinstance(cdf, (np.ndarray, list, pd.Series)):
        raise TypeError("The CDF must be an array-like object.")
    
    if not len(cdf) > 0:
        raise ValueError("The CDF must contain at least one value.")
    
    if not np.all(np.diff(cdf) >= 0):
        raise ValueError("The CDF must be non-decreasing.")

    # Check limits should be zero or above and one or below
    if not np.isclose(cdf.iloc[0], 0, atol=1e-5) or not np.isclose(cdf.iloc[-1], 1):
        raise ValueError("CDF does not start at zero and end at one.")
    
    # Check proper normalization
    if not np.isclose(cdf.diff().fillna(cdf.iloc[0]).sum(), 1):
        raise ValueError("CDF is not properly normalized.")
    


def calculate_likelihood_of_at_least_one_event_posttest(at_least_one_occurrence_prob):

    if not isinstance(at_least_one_occurrence_prob, np.ndarray):
        raise ValueError("The output must be a numpy array.")
    
    if not all(0 <= p <= 1 for p in at_least_one_occurrence_prob):
        raise ValueError("All probabilities must be between 0 and 1.")
    
    if not np.all(np.diff(at_least_one_occurrence_prob) >= 0):
        raise ValueError("The probabilities must be non-decreasing.")

    if not np.isclose(at_least_one_occurrence_prob[0], 0, atol=1e-1) or not np.isclose(at_least_one_occurrence_prob[-1], 1):
        raise ValueError("The probabilities must start at zero and end at one.")
    
    # Check if the array is strictly increasing
    #if not np.all(np.diff(at_least_one_occurrence_prob) > 1e-1):
    #    raise ValueError("The probabilities must be strictly increasing.")
    
    if not all(0 <= p <= 1 for p in at_least_one_occurrence_prob):
        raise ValueError("All probabilities must be between 0 and 1.")



def calculate_likelihood_of_at_least_one_event(cdf, num_trials):
    """
    Calculate the probability of observing at least one event of a specific value or above 
    over a given number of independent trials or time units using an array of cumulative probabilities (CDF).

    In the context of our use case, the CDF represents the likelihood of observing a value of a feature or above one or more times
    given the number of PRIO grid cells in a given time unit. E.g the number of grid cells in a given country in a given month. Or the number of grid cells in a region in a given year. Etc.

    Parameters:
    cdf (np.array or list): The cumulative distribution function (CDF) as an array of probabilities.
    num_trials (int): The number of independent trials or time units over which the event could occur. In our use case, this is the number of PRIO grid cells in a given time unit given the spatial aggregation level.

    Returns:
    np.array: An array of probabilities representing the likelihood of observing at least one occurrence 
              of each value or above over the given number of trials.
    """

    # perform pre-tests
    calculate_likelihood_of_at_least_one_event_pretest(cdf, num_trials)
    
    # Convert CDF to the probability of not observing the event up to that value
    not_occur_prob = 1 - np.array(cdf)
    
    # Calculate the probability of not observing the event across all trials
    not_occur_prob_all_trials = not_occur_prob ** num_trials
    
    # Convert back to the probability of at least one occurrence
    at_least_one_occurrence_prob = 1 - not_occur_prob_all_trials

    # perform post-tests
    calculate_likelihood_of_at_least_one_event_posttest(at_least_one_occurrence_prob)

    # merge with the original CDF
    df_at_least_one_occurrence_prob = pd.DataFrame({'cdf': cdf, 'likelihood': at_least_one_occurrence_prob})
    
    return df_at_least_one_occurrence_prob