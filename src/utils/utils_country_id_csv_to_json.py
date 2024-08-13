import pandas as pd
import os
from pathlib import Path

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths, setup_root_paths, get_data_paths
setup_project_paths(PATH)


def country_id_csv_to_json(delimiter=';', quotechar='"', PATH = PATH):
    """
    Converts a CSV file to a JSON file with specified parameters.
    The if not in the raw_external folder, the csv can be downloaded from the following link: https://viewsforecasting.org/gis-resources/
    
    Parameters:
    - PATH: str or Path, root path to the data directories.
    - delimiter: str, delimiter used in the CSV file (default is ';').
    - quotechar: str, character used to quote fields in the CSV file (default is '"').
    """

    PATH_ROOT = setup_root_paths(PATH)  

    print(PATH_ROOT) 

    # set path to point to the data
    _, PATH_RAW_EXTERNAL, PATH_PROCESSED, _ = get_data_paths(PATH_ROOT)

    print(PATH_RAW_EXTERNAL)
    print(PATH_PROCESSED)

    # check if the path exists and raise an error otherwise
    if not os.path.exists(PATH_PROCESSED):
        raise ValueError(f"Path does not exist: {PATH_PROCESSED}")

    PATH_DF = PATH_RAW_EXTERNAL / "MatchingTable_VIEWS_Country_IDs.csv"
    print(PATH_DF)

    try:
        # Attempt to read the CSV file with additional parameters
        df_contry_index = pd.read_csv(str(PATH_DF), delimiter=delimiter, quotechar=quotechar, on_bad_lines='skip')
    except pd.errors.ParserError as e:
        print(f"ParserError: {e}")
        return False
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

    PATH_JSON = PATH_PROCESSED / "MatchingTable_VIEWS_Country_IDs.json"

    try:
        # Save DataFrame to JSON
        df_contry_index.to_json(str(PATH_JSON), orient='records', lines=True)
    except Exception as e:
        print(f"An error occurred while saving to JSON: {e}")
        return False

    print(f"CSV file successfully converted to JSON and saved to {PATH_JSON}")
    return True

# Example usage
# Ensure PATH is defined before calling the function
# country_id_csv_to_json(PATH)