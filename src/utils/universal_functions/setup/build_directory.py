import os
import pandas as pd

# def float_to_custom_string(value):
#     # Convert float to string
#     value_str = str(value)
#     # Replace the decimal point with an underscore
#     custom_str = value_str.replace('.', '_')
#     return custom_str

def float_to_custom_string(value):
    return f"{value:.1f}"

def ensure_directory_exists(full_directory_path):
    # Normalize the path to handle different OS path separators
    normalized_path = os.path.normpath(full_directory_path)
    
    if not os.path.exists(normalized_path):
        os.makedirs(normalized_path)
        print(f"Directory '{normalized_path}' created.")
    else:
        print(f"Directory '{normalized_path}' already exists.")

