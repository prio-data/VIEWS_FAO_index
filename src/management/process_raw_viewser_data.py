import numpy as np
import pandas as pd

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths, get_data_paths
setup_project_paths(PATH)
PATH_RAW_VIEWSER, PATH_RAW_EXTERNAL, PATH_PROCESSED, PATH_GENERATED = get_data_paths(PATH)


from utils_annual_aggregation import aggregate_monthly_to_yearly
from utils_feature_eng_per_100k import feature_eng_fat_per_100k
from utils_process_data_country_wise import process_data_country_wise
from utils_feature_eng_per_100k_country_wise import get_per_100k_features_country_wise

if __name__ == '__main__':

    # # load the data from pkl
    print("Loading the data")
    df_monthly = pd.read_pickle(PATH_RAW_VIEWSER / "full_base_01_viewser_df.pkl")
    
    print("Aggregating the data to yearly")
    df_yearly = aggregate_monthly_to_yearly(df_monthly)
    
    # Feature engineering
    print("Feature engineering - pg wise")
    df_monthly = feature_eng_fat_per_100k(df_monthly)
    df_yearly = feature_eng_fat_per_100k(df_yearly)

    # contry wise
    print("Feature engineering - country wise")
    df_monthly = get_per_100k_features_country_wise(df_monthly, post_test = True)
    df_yearly = get_per_100k_features_country_wise(df_yearly, post_test = True)

    # save the data
    #df_monthly.to_pickle(PATH_PROCESSED / "df_monthly.pkl")  
    #df_yearly.to_pickle(PATH_PROCESSED / "df_yearly.pkl")

    fatality_features = ['sb_best', 'ns_best', 'os_best', 'total_best']
    
    # monthly data    
    # Initialize the DataFrame
    print("Creating the monthly dataframes for the return periods")
    df_monthly_global_country_level = df_monthly.copy()
    
    print("Processing the monthly data for the return periods")
    for feature in fatality_features:
        df_monthly_global_country_level = process_data_country_wise(df_monthly_global_country_level, feature)

    
    # yearly data 
    # Initialize the DataFrame  
    print("Creating the yearly dataframes for the return periods")
    df_yearly_global_country_level = df_yearly.copy()
     
    print("Processing the yearly data for the return periods") 
    for feature in fatality_features:
        df_yearly_global_country_level = process_data_country_wise(df_yearly_global_country_level, feature)
    

    # save the data
    print("Saving the data as pkl and csv")
    df_monthly_global_country_level.to_pickle(PATH_GENERATED / "df_monthly_country_return_periods.pkl")
    df_monthly_global_country_level.to_csv(PATH_GENERATED / "df_monthly_country_return_periods.csv")

    df_yearly_global_country_level.to_pickle(PATH_GENERATED / "df_yearly_country_return_periods.pkl")
    df_yearly_global_country_level.to_csv(PATH_GENERATED / "df_yearly_country_return_periods.csv")
 
    print("Done")

