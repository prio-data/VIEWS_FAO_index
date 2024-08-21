import sys
from pathlib import Path
import subprocess

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths, get_data_paths
setup_project_paths(PATH)

from utils_main_print_statements import print_main_title_head, print_directory_contents
from utils_main_prompts import prompt_user
    
def main():

    # Print the main title head
    print_main_title_head(version="0.1.0", last_update="15-08-2024")


    # Print the contents of the data directories
    print_directory_contents()


    # Prompt the user for input
    prompt_user()


if __name__ == '__main__':
    main()