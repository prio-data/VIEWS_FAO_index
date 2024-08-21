import sys
from pathlib import Path
import subprocess

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths
setup_project_paths(PATH)


def prompt_user():

        # Prompt the user for input
    user_response = input("Do you want to download and process some data? (Y/n): ").strip().lower()

    # Check the user's response
    if user_response == 'y' or user_response == 'yes':
        print("Running the scripts to download and process data...")
        
        # Run the first script using subprocess
        subprocess.run([sys.executable, "script1.py"])

        # Run the second script using subprocess
        subprocess.run([sys.executable, "script2.py"])
        
    else:
        print("Exiting the program. No data will be processed.")
        return