import sys
from pathlib import Path
import subprocess

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths, setup_root_paths
setup_project_paths(PATH)

def prompt_user_dynamic_precheck():
    """
    Checks if the paths to specific scripts are dynamically constructed and exist.

    This function assumes that the PATH variable is previously defined and points to the current file's location.
    It dynamically constructs the paths to two scripts located in the project directory:
    - "src/dataloaders/get_full_base.py"
    - "src/management/process_raw_viewser_data.py"

    The function then checks if these paths exist. If any of the paths do not exist, it prints detailed information
    about which path is missing and suggests that the paths might be hard-coded. If both paths exist, it confirms
    that the paths are dynamic.

    Returns:
        None
    """
    # Assuming PATH is previously defined 
    PATH = Path(__file__)

    # Dynamically construct the paths
    project_root = setup_root_paths(PATH)
    first_script = project_root / "src/dataloaders/get_full_base.py"
    second_script = project_root / "src/management/process_raw_viewser_data.py"

    # Check if the constructed paths exist
    paths_exist = first_script.exists() and second_script.exists()

    if not paths_exist:
        # check and print detailed information about the paths
        if not first_script.exists():
            print(f"Path to first script is not dynamic and is hard-coded: {first_script}")
        if not second_script.exists():
            print(f"Path to second script is not dynamic and is hard-coded: {second_script}")

        # summary message
        print("One or more paths are not dynamic and might be hard-coded. Please check your setup.")
        return
    
    # confirming that paths are dynamic
    if paths_exist:
        # check if the paths are dynamic
        print("Paths to the scripts are dynamic.")
    else:
        print("Paths to the scripts are not dynamic and might be hard-coded.")
        return      


def prompt_user_dynamic():

        # Prompt the user for input
    user_response = input("Do you want to download and process some data? (Y/n): ").strip().lower()

    # Check the user's response
    if user_response == 'y' or user_response == 'yes':
        print("Running the scripts to download and process data...")

        # Dynamically construct the paths
        project_root = setup_root_paths(PATH)
        first_script = project_root / "src/dataloaders/get_full_base.py"
        second_script = project_root / "src/management/process_raw_viewser_data.py"

        # Checking that the paths are dynamic
        if not prompt_user_dynamic_precheck():
            print("Paths are not dynamic. Exiting the program.")
            return
        else:
            print("Paths are dynamic. Proceeding with script execution.")

        # Run the first script using subprocess
        subprocess.run([sys.executable, str(first_script)])
        
        # Run the second script using subprocess
        subprocess.run([sys.executable, str(second_script)])
        
    else:
        print("Exiting the program. No data will be processed.")
        return
    

