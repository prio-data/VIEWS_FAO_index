import pandas as pd

import pandas as pd

def get_extended_feature_list_pretest(df, feature):
    """
    Pre-test the DataFrame to ensure it meets the requirements for processing.

    Parameters:
    df (pd.DataFrame): The DataFrame to be tested.
    feature (str): The feature column to be checked.

    Raises:
    TypeError: If the DataFrame is not a pandas DataFrame.
    ValueError: If the DataFrame is empty.
    ValueError: If the DataFrame has less than 2 columns.
    ValueError: If the feature column is not found in the DataFrame.
    ValueError: If the feature column is empty.
    ValueError: If the feature column has less than 2 unique values.
    ValueError: If the feature column contains NaNs, Infs, or -Infs.

    Returns:
    bool: True if all checks pass.
    """

    # Check that the df is a pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError('df is not a pandas DataFrame')
    
    # Check that the df is not empty
    if df.empty:
        raise ValueError('df is empty')
    
    # Check that the df has more than one column
    if df.shape[1] < 2:
        raise ValueError('df has less than 2 columns...')
    
    # Check that it has the feature
    if feature not in df.columns:
        raise ValueError(f'Feature {feature} not found in df')
    
    # Check that the feature is not empty
    if df[feature].isnull().all():
        raise ValueError(f'Feature {feature} is empty')
    
    # Check that the feature has more than one unique value
    if df[feature].nunique() < 2:
        raise ValueError(f'Feature {feature} has less than 2 unique values')
    
    return True


def get_extended_feature_list_posttest(df, feature, feature_list):
    """
    Post-test the DataFrame to ensure the extended feature list meets the requirements.

    Parameters:
    df (pd.DataFrame): The DataFrame to be tested.
    feature (str): The original feature column.
    feature_list (list): The list of extended features to be checked.

    Raises:
    ValueError: If any feature in the feature_list is not found in the DataFrame.
    ValueError: If any feature in the feature_list contains NaNs, Infs, or -Infs.
    ValueError: If any feature in the feature_list has less than 2 unique values.
    ValueError: If any new feature is equal to the original feature.
    ValueError: If any new feature contains NaNs, Infs, or -Infs.
    ValueError: If any new feature is equal to another new feature.

    Returns:
    bool: True if all checks pass.
    """

    # Check that the feature is present in the df
    if not all(feature in df.columns for feature in feature_list):
        raise ValueError(f'Feature {feature} not found in df')
    
    # Check that none of the features are empty
    if not all(df[feature].notnull().all() for feature in feature_list):
        raise ValueError(f'Feature {feature} contains NaNs, Infs, or -Infs')
    
    # Check that the features have more than one unique value
    if not all(df[feature].nunique() > 1 for feature in feature_list):
        raise ValueError(f'Feature {feature} has less than 2 unique values')
    
    # Check that none of the new features are equal to the original feature
    if not all(feature != f'{feature}_{suffix}' for suffix in ['p_i', 'P_i', 'e_i', 'E_i', 'b_i', 'B_i']):
        raise ValueError(f'Feature {feature} is equal to one of the new features')
    
    return True


def get_extended_feature_list(df, feature, base_feature=True, p_i=True, P_i=True, e_i=True, E_i=True, b_i=True, B_i=True):
    """
    Generate an extended feature list based on the given feature and options.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the feature.
    feature (str): The original feature column.
    base_feature (bool): Whether to include the base feature in the list. Default is True.
    p_i (bool): Whether to include the p_i feature in the list. Default is True.
    P_i (bool): Whether to include the P_i feature in the list. Default is True.
    e_i (bool): Whether to include the e_i feature in the list. Default is True.
    E_i (bool): Whether to include the E_i feature in the list. Default is True.
    b_i (bool): Whether to include the b_i feature in the list. Default is True.
    B_i (bool): Whether to include the B_i feature in the list. Default is True.

    Raises:
    ValueError: If any of the pre-tests or post-tests fail.

    Returns:
    list: The extended feature list.
    """

    # Pre-test the DataFrame
    get_extended_feature_list_pretest(df, feature)
    
    feature_list = []

    if base_feature:
        feature_list.append(feature)

    if p_i:
        feature_list.append(f'{feature}_p_i')

    if P_i:
        feature_list.append(f'{feature}_P_i')

    if e_i:
        feature_list.append(f'{feature}_e_i')

    if E_i:
        feature_list.append(f'{feature}_E_i')

    if b_i:
        feature_list.append(f'{feature}_b_i')

    if B_i:
        feature_list.append(f'{feature}_B_i')

    # Post-test the extended feature list
    get_extended_feature_list_posttest(df, feature, feature_list)

    return feature_list