import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths, get_data_paths
setup_project_paths(PATH)

from util_print_statements import print_main_title_head, list_directory_contents

if __name__ == '__main__':
    

    print_main_title_head(version="0.1.0", last_update="15-08-2024")

    # then print what files are in the varios data directories
    PATH_RAW_VIEWSER, PATH_RAW_EXTERNAL, PATH_PROCESSED, PATH_GENERATED = get_data_paths(PATH)


    # but rally this should also just print the agrparse help message


    
    # Print the contents of the data directories
    print("\nContents of the data directories:")
    print("=================================")
    
    # and then somethign about these functions returning somethign regarding if the path exists or not
    # and ask if stuff should be downloaded or created or whatnot

    list_directory_contents(PATH_RAW_VIEWSER, "Raw Viewser data directory")
    list_directory_contents(PATH_RAW_EXTERNAL, "Raw External data directory")
    list_directory_contents(PATH_PROCESSED, "Processed data directory")
    list_directory_contents(PATH_GENERATED, "Generated data directory")
    
    print("=================================")
    print("\nEnd of main.py")


