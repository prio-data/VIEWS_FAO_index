import sys
from pathlib import Path
import subprocess

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths, get_data_paths
setup_project_paths(PATH)

from utils_main_print_statements import print_main_title_head, print_directory_contents
from utils_main_prompts import prompt_user


# The main issue right now is that m computer I use two differant conda environments, one for the viewser dataloader and one process the data.
# And there is an issue if I try to use the VIEWSER environment for both
# The issue pops up doing the yearly aggreation and has somethign to do with the mode used to decided which country a pgm belongs to in years where the country has changed.
# I suspect that the issue pertains to pandas since it is a groupby stituation where it happens.
# Or scipy as that is were I get the mode from. 

# base conda environment: 
# pandas 2.2.1
# scipy 1.10.1

# viewser_2024 conda environment:
# pandas 1.5.3
# scipy 1.11.4

def main():

    # Print the main title head
    print_main_title_head(version="0.1.0", last_update="15-08-2024")


    # Print the contents of the data directories
    print_directory_contents()


    # Prompt the user for input
    prompt_user()


if __name__ == '__main__':
    main()