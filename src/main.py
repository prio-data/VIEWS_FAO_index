import sys
from pathlib import Path
import subprocess

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths, get_data_paths
setup_project_paths(PATH)

from utils_main_print_statements import print_main_title_head, print_directory_contents, print_library_versions
# from utils_main_prompts import prompt_user
from utils_main_prompts_dynamic import prompt_user_dynamic

def main():

    # Print the main title head
    print_main_title_head(version="0.1.0", last_update="15-08-2024")

    while True:
        print("\nPlease choose an option:")
        print("1. Print the contents of the data directories")
        print("2. Download and process data")
        print("3. Print tested library versions")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            print_directory_contents()
        elif choice == '2':
            prompt_user_dynamic()
        elif choice == '3':
            print_library_versions()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()