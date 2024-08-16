import numpy as np
import pandas as pd

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths
setup_project_paths(PATH)

def get_time_period(df):
    
    if 'month_id' in df.columns:
        return 'month_id'
    
    elif 'year_id' in df.columns:
        return 'year_id'
    
    else:
        print(df.columns)
        raise ValueError('Time period not found')