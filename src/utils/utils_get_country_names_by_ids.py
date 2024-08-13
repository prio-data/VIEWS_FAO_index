import pandas as pd

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths, setup_root_paths, get_logo_path, get_data_paths
setup_project_paths(PATH)

from utils_country_id_csv_to_json import country_id_csv_to_json

def get_country_names_by_ids(country_ids, PATH = PATH):
    """
    Matches a list of country IDs to the country IDs in the DataFrame and returns a dictionary
    with the country name as the value and the country ID as the key.
    
    Parameters:
    - df: pd.DataFrame, the DataFrame containing country IDs and names.
    - country_ids: list, a list of country IDs to match.
    
    Returns:
    - dict: a dictionary with country IDs as keys and country names as values.
    """

    # get the data paths
    PATH_RAW_VIEWSER, PATH_RAW_EXTERNAL, PATH_PROCESSED, PATH_GENERATED = get_data_paths(PATH)


    # check if the json exists
    PATH_JSON = PATH_PROCESSED / "MatchingTable_VIEWS_Country_IDs.json"

    if not PATH_JSON.exists():
        # convert the csv to json
        country_id_csv_to_json()

    # load the json file as a dataframe
    df_country_index = pd.read_json(PATH_JSON, lines=True)

    # check that the df is not empty and rais an error otherwise
    if df_country_index.empty:
        raise ValueError("The MatchingTable_VIEWS_Country_IDs DataFrame is empty.")

    # Filter the DataFrame to only include rows with the specified country IDs
    filtered_df = df_country_index[df_country_index['country_id'].isin(country_ids)]
    
    # Create a dictionary with country IDs as keys and country names as values
    country_dict = filtered_df.set_index('country_id')['name'].to_dict()

    # check that all country IDs were found and that the dict is not empty
    if len(country_dict) != len(country_ids):
        print(f"Warning: Not all country IDs were found in the DataFrame. Missing country IDs: {set(country_ids) - set(country_dict)}")
    
    return country_dict

# Example usage
#country_dict = get_country_names_by_ids(country_list[0:12])
#print(country_dict)