import pandas as pd
import unittest
import numpy as np

def calculate_return_periods_precheck(df_probabilities):
    """
    Pre-checks for the calculate_return_periods function.

    Parameters:
    df_probabilities (pd.DataFrame): A DataFrame containing the probabilities.

    Returns:
    bool: True if all pre-checks pass, raises ValueError otherwise.
    """
    # Check if the DataFrame is empty
    if df_probabilities.empty:
        raise ValueError("The input DataFrame is empty.")
    
    # Check if the required columns are present
    required_columns = ['p_i', 'P_i']
    for column in required_columns:
        if column not in df_probabilities.columns:
            raise ValueError(f"Missing required column: {column}")
    
    # Check if the probabilities are within the valid range (0, 1]
    if not ((df_probabilities['p_i'] > 0) & (df_probabilities['p_i'] <= 1)).all():
        raise ValueError("Values in 'p_i' must be within the range (0, 1].")
    if not ((df_probabilities['P_i'] > 0) & (df_probabilities['P_i'] <= 1)).all():
        raise ValueError("Values in 'P_i' must be within the range (0, 1].")
    
    return True

def calculate_return_periods_postcheck(df_probabilities):
    """
    Post-checks for the calculate_return_periods function.

    Parameters:
    df_probabilities (pd.DataFrame): A DataFrame containing the probabilities and return periods.

    Returns:
    bool: True if all post-checks pass, raises ValueError otherwise.
    """
    # Check if the return periods are positive
    if not (df_probabilities['e_i'] > 0).all():
        raise ValueError("Values in 'e_i' must be positive.")
    if not (df_probabilities['E_i'] > 0).all():
        raise ValueError("Values in 'E_i' must be positive.")
    
    return True

def calculate_return_periods(probabilities_df):
    """
    Calculate return periods for given probabilities.

    This function calculates the return periods for individual probabilities (p_i) and cumulative probabilities (P_i).
    The return period is defined as the inverse of the probability.

    Parameters:
    probabilities_df (pd.DataFrame): A DataFrame containing the probabilities with columns 'p_i' and 'P_i'.

    Returns:
    pd.DataFrame: The input DataFrame updated with return periods 'e_i' and 'E_i'.
                  'e_i' is the return period for individual probabilities.
                  'E_i' is the return period for cumulative probabilities.
    """
    
    # Perform pre-checks
    calculate_return_periods_precheck(probabilities_df)

    # Extract individual and cumulative probabilities from the DataFrame
    p_i = probabilities_df['p_i']
    P_i = probabilities_df['P_i']

    # Calculate return periods as the inverse of the probabilities
    e_i = 1 / p_i
    E_i = 1 / P_i

    # Update the DataFrame with the calculated return periods
    probabilities_df['e_i'] = e_i
    probabilities_df['E_i'] = E_i

    # Perform post-checks
    calculate_return_periods_postcheck(probabilities_df)

    # Return the updated DataFrame
    return probabilities_df