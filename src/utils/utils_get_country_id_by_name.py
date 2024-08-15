import pandas as pd
from fuzzywuzzy import process # install with conda install conda-forge::fuzzywuzzy


import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths, setup_root_paths, get_logo_path, get_data_paths
setup_project_paths(PATH)

from utils_country_id_csv_to_json import country_id_csv_to_json


def get_country_id_by_name(country_name, PATH=PATH, threshold=80):
    """
    Performs a fuzzy search given a country name and finds relevant country IDs.
    
    Parameters:
    - country_name: str, the country name to search for.
    - PATH: Path, the path to the data directory.
    - threshold: int, the minimum score for a match to be considered relevant.
    
    Returns:
    - list: a list of tuples with country IDs and their corresponding names.
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

    # check that the df is not empty and raise an error otherwise
    if df_country_index.empty:
        raise ValueError("The MatchingTable_VIEWS_Country_IDs DataFrame is empty.")
    
    # Perform fuzzy search
    matches = process.extract(country_name, df_country_index['name'], limit=None)
    
    # Filter matches based on the threshold
    relevant_matches = [(df_country_index.iloc[idx]['country_id'], name) for name, score, idx in matches if score >= threshold]
    
    return relevant_matches

# Example usage
#country_ids = get_country_id_by_name("ghana")
#print(country_ids)