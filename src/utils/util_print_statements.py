def print_main_title_head(version="1.0.0", last_update="2023-10-01"):
    pattern = f"""

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

██    ██ ██ ███████ ██     ██ ███████       ███████  █████   ██████  
██    ██ ██ ██      ██     ██ ██            ██      ██   ██ ██    ██ 
██    ██ ██ █████   ██  █  ██ ███████ █████ █████   ███████ ██    ██ 
 ██  ██  ██ ██      ██ ███ ██      ██       ██      ██   ██ ██    ██ 
  ████   ██ ███████  ███ ███  ███████       ██      ██   ██  ██████ 

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

----------------- Welcome to the VIEWS-FAO project! ----------------

You are now in the main script (main.py). 
This script is the entry point to the project.

Version: {version}
Last update: {last_update}

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