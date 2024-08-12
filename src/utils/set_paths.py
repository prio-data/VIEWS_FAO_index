import sys
from pathlib import Path

def setup_root_paths(PATH) -> Path:
    """
    Extracts and returns the root path (pathlib path object) up to and including the "VIEWS_FAO_index" directory from any given path.
    This function identifies the "VIEWS_FAO_index" directory within the provided path and constructs a new path up to and including this directory. 
    This is useful for setting up root paths for project-wide resources and utilities.

    Args:
        PATH (Path): The base path, typically the path of the script invoking this function (e.g., `PATH = Path(__file__)`).

    Returns:
        PATH_ROOT: The root path (pathlib path object) including the "VIEWS_FAO_index" directory.
    """
    try:
        parts = PATH.parts
        index = parts.index("VIEWS_FAO_index")
        PATH_ROOT = Path(*parts[:index+1]) # The +1 is to include the "VIEWS_FAO_index" part in the path

    except ValueError:
        # If "VIEWS_FAO_index" is not found in the parts, check parent directories
        current_path = PATH.resolve()
        while current_path != current_path.parent:
            if current_path.name == "VIEWS_FAO_index":
                return current_path
            current_path = current_path.parent
        raise ValueError("The provided path does not contain 'VIEWS_FAO_index' directory.")
    return PATH_ROOT



def setup_project_paths(PATH) -> None:
    """
    Configures project-wide access to common utilities, configurations, and model-specific paths by adjusting `sys.path`.

    This function should be called at the start of a script to ensure consistent and machine-agnostic path resolution throughout the project. It dynamically sets up paths relative to the specified base path, facilitating access to shared resources located in `common_utils` and `common_configs`, as well as model-specific directories within `models`.

    Args:
        PATH (Path): The base path, typically the path of the script invoking this function (i.e., `Path(__file__)`).
        Following the usage example below, this is automatically passed to the function by the script.

    Usage:
        To ensure all necessary project paths are accessible, add the following to the start of each project script:

        ```python
            import sys
            from pathlib import Path

            PATH = Path(__file__)
            sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "common_utils")) # PATH_COMMON_UTILS  

            from set_path import setup_project_paths
            setup_project_paths(PATH)
        ```

    Note: Paths are only added to sys.path if they exist and are not already included `(e.g. PATH_COMMON_UTILS), to avoid redundancy.
    Disclaimer: A solution that avoids the insertion of the code above would be preferred.
    """
    PATH_ROOT = setup_root_paths(PATH)

    # Define configs paths
    PATH_COMMON_CONFIGS = PATH_ROOT / "configs"
    PATH_SRC = PATH_ROOT / "src"
    PATH_RAW_VIEWSER = PATH_ROOT / "data" / "raw_viewser"
    PATH_RAW_EXTERNAL = PATH_ROOT / "data" / "raw_external"
    PATH_PROCESSED = PATH_ROOT / "data" / "processed"
    PATH_GENERATED = PATH_ROOT / "data" / "generated"

    # Define src-specific paths
    PATH_UTILS = PATH_SRC / "utils"
    PATH_MANAGEMENT = PATH_SRC / "management" # added to keep the management scripts in a separate folder the utils according to Sara's point
    PATH_ARCHITECTURES = PATH_SRC / "architectures"
    PATH_TRAINING = PATH_SRC / "training"
    PATH_FORECASTING = PATH_SRC / "forecasting"
    PATH_OFFLINE_EVALUATION = PATH_SRC / "offline_evaluation"
    PATH_DATALOADERS = PATH_SRC / "dataloaders"

    paths_to_add = [
        PATH_ROOT, PATH_COMMON_CONFIGS, PATH_UTILS, PATH_MANAGEMENT, PATH_ARCHITECTURES, 
        PATH_TRAINING, PATH_FORECASTING, PATH_OFFLINE_EVALUATION, PATH_DATALOADERS,
        PATH_RAW_VIEWSER, PATH_RAW_EXTERNAL, PATH_PROCESSED, PATH_GENERATED
    ]

    for path in paths_to_add:
        path_str = str(path)

        # if path does not exist, make it
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        if path.exists() and path_str not in sys.path:
            sys.path.insert(0, path_str)

import unittest
import sys
from pathlib import Path
from set_paths import setup_root_paths, setup_project_paths

class TestSetupPaths(unittest.TestCase):
    def setUp(self):
        self.base_path = Path("/home/simon/Documents/scripts/VIEWS_FAO_index/subdir/script.py")

    def test_setup_root_paths(self):
        expected_root_path = Path("/home/simon/Documents/scripts/VIEWS_FAO_index")
        result = setup_root_paths(self.base_path)
        self.assertEqual(result, expected_root_path)

    def test_setup_root_paths_no_views_fao_index(self):
        with self.assertRaises(ValueError):
            setup_root_paths(Path("/home/simon/Documents/scripts/subdir/script.py"))

    def test_setup_project_paths(self):
        initial_sys_path = sys.path.copy()
        setup_project_paths(self.base_path)
        expected_paths = [
            "/home/simon/Documents/scripts/VIEWS_FAO_index",
            "/home/simon/Documents/scripts/VIEWS_FAO_index/configs",
            "/home/simon/Documents/scripts/VIEWS_FAO_index/src/utils",
            "/home/simon/Documents/scripts/VIEWS_FAO_index/src/management",
            "/home/simon/Documents/scripts/VIEWS_FAO_index/src/architectures",
            "/home/simon/Documents/scripts/VIEWS_FAO_index/src/training",
            "/home/simon/Documents/scripts/VIEWS_FAO_index/src/forecasting",
            "/home/simon/Documents/scripts/VIEWS_FAO_index/src/offline_evaluation",
            "/home/simon/Documents/scripts/VIEWS_FAO_index/src/dataloaders",
            "/home/simon/Documents/scripts/VIEWS_FAO_index/data/raw_viewser",
            "/home/simon/Documents/scripts/VIEWS_FAO_index/data/raw_external",
            "/home/simon/Documents/scripts/VIEWS_FAO_index/data/processed",
            "/home/simon/Documents/scripts/VIEWS_FAO_index/data/generated"
        ]
        for path in expected_paths:
            self.assertIn(path, sys.path)

        sys.path = initial_sys_path  # Reset sys.path after test

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)