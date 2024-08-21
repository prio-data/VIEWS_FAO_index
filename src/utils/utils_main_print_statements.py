import sys
from pathlib import Path
import subprocess

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

# would also be nice to list the versions of the various packages used in the project

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


def print_library_versions():

    """
    This script checks the versions of various libraries used in the project.
    
    It attempts to import each library and prints the version if the import is successful.
    If the import fails, it prints an error message and indicates that the library is uninstalled.
    
    Libraries checked:
    - sys
    - pandas
    - numpy
    - scipy
    - pathlib
    - matplotlib
    - seaborn
    - fuzzywuzzy
    - viewser
    
    Usage:
    Run this script to see the versions of the installed libraries.
    """

    try:
        import sys
        sys_version = sys.version
    except ImportError as e:
        sys_version = "uninstalled"
        print(f"Failed to import sys: {e}")
    
    try:
        import pandas as pd
        pd_version = pd.__version__
    except ImportError as e:
        pd_version = "uninstalled"
        print(f"Failed to import pandas: {e}")
    
    try:
        import numpy as np
        np_version = np.__version__
    except ImportError as e:
        np_version = "uninstalled"
        print(f"Failed to import numpy: {e}")
    
    try:
        import scipy
        scipy_version = scipy.__version__
    except ImportError as e:
        scipy_version = "uninstalled"
        print(f"Failed to import scipy: {e}")
    
    try:
        from pathlib import Path
        pathlib_version = "installed"
    except ImportError as e:
        pathlib_version = "uninstalled"
        print(f"Failed to import pathlib: {e}")
    
    try:
        import matplotlib
        matplotlib_version = matplotlib.__version__
    except ImportError as e:
        matplotlib_version = "uninstalled"
        print(f"Failed to import matplotlib: {e}")
    
    try:
        import seaborn
        seaborn_version = seaborn.__version__
    except ImportError as e:
        seaborn_version = "uninstalled"
        print(f"Failed to import seaborn: {e}")
    
    try:
        import fuzzywuzzy
        fuzzywuzzy_version = fuzzywuzzy.__version__
    except ImportError as e:
        fuzzywuzzy_version = "uninstalled"
        print(f"Failed to import fuzzywuzzy: {e}")
    
    try:
        import viewser
        try:
            viewser_version = subprocess.check_output(["viewser", "--version"], text=True).strip()
        except subprocess.CalledProcessError as e:
            viewser_version = "installed, but failed to get version"
            print(f"Failed to get viewser version: {e}")
    except ImportError as e:
        viewser_version = "uninstalled"
        print(f"Failed to import viewser: {e}")
    
    print(f"viewser version: {viewser_version}")
    
    # Print the versions of the libraries used in the project
    print("\nYour library versions versus tested library versions known to work:")
    print("=================")
    print(f"Python version: {sys_version} (Tested: 3.11.7)")
    print(f"pandas version: {pd_version} (Tested: 2.2.2)")
    print(f"numpy version: {np_version} (Tested: 1.26.4)")
    print(f"scipy version: {scipy_version} (Tested: 1.12.0)")
    print(f"pathlib version: {pathlib_version} (Tested: installed)")
    print(f"matplotlib version: {matplotlib_version} (Tested: 3.8.0)")
    print(f"seaborn version: {seaborn_version} (Tested: 0.13.2)")
    print(f"fuzzywuzzy version: {fuzzywuzzy_version} (Tested: 0.18.0)")
    print(f"viewser version: {viewser_version} (Tested: 6.5.2)")
    print("=================")


