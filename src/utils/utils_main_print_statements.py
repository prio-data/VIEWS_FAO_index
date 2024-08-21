import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths, get_data_paths
setup_project_paths(PATH)



def print_main_title_head(version="0.1.0", last_update="2024-20-08"):
    pattern = f"""

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

██    ██ ██ ███████ ██     ██ ███████       ███████  █████   ██████  
██    ██ ██ ██      ██     ██ ██            ██      ██   ██ ██    ██ 
██    ██ ██ █████   ██  █  ██ ███████ █████ █████   ███████ ██    ██ 
 ██  ██  ██ ██      ██ ███ ██      ██       ██      ██   ██ ██    ██ 
  ████   ██ ███████  ███ ███  ███████       ██      ██   ██  ██████ 

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

----------------- Welcome to the VIEWS-FAO project! ----------------

Version: {version}
Last update: {last_update}

You are now in the main script (main.py). 
This script is the entry point to the project.

The script is currrntlly under delopment and it's functionality is limited.

For now the script simply: 

1) Prints the contents of the data directories
2) Prompts the user regarding whether they want to download and process data

If the data directories are empty, or the user knows/suspects that the data is outdated, 
the user should choose (Y) to download and process the data.

For any questions, issues, or suggestions, please contact the project maintainer at: simmaa@prio.org
Or submit an issue on the project's GitHub page: https://github.com/prio-data/VIEWS_FAO_index

Note that is you are not able to run this script and optain the data, 
you can download the data directly from google cloude storage.
Link at the project's GitHub page.

---------------------------------------------------------------------

"""
    print(pattern)


def list_directory_contents(path, title):
    """
    Lists the contents of a directory with a given title.

    Args:
        path (Path): The path to the directory.
        title (str): The title to be printed above the directory contents.
    """
    print(f"\n{title}:")
    print("=" * len(title))
    for item in path.iterdir():
        
        # not gitkeep or gitignore or readme
        if item.name not in [".gitkeep", ".gitignore", "README.md"]: 
            print(f"- {item.name}")
    print("\n")


def print_directory_contents():
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
#    print("\nEnd of main.py")