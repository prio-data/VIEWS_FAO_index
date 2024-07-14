
import sys
import os
import numpy as np
import pandas as pd

from viewser import Queryset, Column

def get_input_data_config():
    """
    Contains the configuration for the input data in the form of a viewser queryset. 
    This configuration is "behavioral" so modifying it will affect the model's runtime behavior 
    and integration into the deployment system. There is no guarantee that the model will work 
    if the input data configuration is changed here without changing the model settings and architecture accordingly.

    Returns:
    queryset_base (Queryset): A queryset containing the base data for the model training.
    """

    queryset_base = (Queryset("FAO_simon_experiments", "priogrid_month")
        .with_column(Column("sb_best", from_loa = "priogrid_month", from_column = "ged_sb_best_count_nokgi").transform.missing.replace_na())
        .with_column(Column("ns_best", from_loa = "priogrid_month", from_column = "ged_ns_best_count_nokgi").transform.missing.replace_na())
        .with_column(Column("os_best", from_loa = "priogrid_month", from_column = "ged_os_best_count_nokgi").transform.missing.replace_na())
        .with_column(Column("pop_gpw_sum", from_loa="priogrid_year", from_column="pop_gpw_sum").transform.missing.fill().transform.missing.replace_na())
        .with_column(Column("month", from_loa = "month", from_column = "month"))
        .with_column(Column("year_id", from_loa = "country_year", from_column = "year_id"))
        .with_column(Column("c_id", from_loa = "country_year", from_column = "country_id"))
        .with_column(Column("col", from_loa = "priogrid", from_column = "col"))
        .with_column(Column("row", from_loa = "priogrid", from_column = "row")))

    return queryset_base

def fetch_data_from_viewser():
    """
    Fetches and prepares the initial DataFrame from viewser.

    Returns:
        pd.DataFrame: The prepared DataFrame with initial processing done.
    """
    print(f'Beginning file download through viewser')
    queryset_base = get_input_data_config()

    df = queryset_base.publish().fetch()
    
    # Print the size of the DataFrame to see if it is empty
    print(f'Size of DataFrame: {df.shape}')
    
    df.reset_index(inplace=True)

    # Rename and add columns specific to HydraNet or vol specific
    df.rename(columns={'priogrid_gid': 'pg_id'}, inplace=True)
    
    return df

def get_year_range():
    """
    Gets the year range for the data as specified in Håvard's mail.

    Returns:
        tuple: A tuple containing the first and last years.
    """
    year_first = 1989
    year_last = 2023

    return year_first, year_last

def get_country_id():
    """
    Gets the country ID for Mali.

    Returns:
        int: The country ID for Mali.
    """
    country_id = 50

    return country_id


def filter_dataframe_by_year_range(df, year_first, year_last): # NOT USING THIS YET
    """
    Filters the DataFrame to include only the specified year range.

    Args:
        df (pd.DataFrame): The input DataFrame to be filtered.
        year_first (int): The first year ID to include.
        year_last (int): The last year ID to include.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    year_range = np.arange(year_first, year_last + 1)  # Adding 1 to include year_last in the range
    new_df = df[df['year_id'].isin(year_range)].copy()

    # chek if the size of the new DataFrame is empty
    print(f'Size of new DataFrame: {new_df.shape}')

    return new_df


def get_views_df():
    """
    Fetches and returns the DataFrame from viewser.

    Returns:
        pd.DataFrame: The DataFrame fetched from viewser.
    """
    df = fetch_data_from_viewser()

    return df


def fetch_views_df(PATH_RAW):
    """
    Fetches or loads the views DataFrame and saves it to a pickle file.

    Args:
        partition (str): The partition type (e.g., 'calibration').
        PATH_RAW (str): The path to the directory where raw data is stored.

    Returns:
        pd.DataFrame: The fetched or loaded DataFrame.
    """
    path_viewser_df = os.path.join(PATH_RAW, f'simon_mali_01_viewser_df.pkl') 

    # Create the folders if they don't exist
    os.makedirs(PATH_RAW, exist_ok=True)

    print('Fetching file...')
    df = get_views_df()  # Removed partition argument, as it is not used in get_views_df

    # get the year range 
    year_first, year_last = get_year_range()

    # Filter the DataFrame by the year range
    df = filter_dataframe_by_year_range(df, year_first, year_last)

    # get the country ID
    country_id = get_country_id()

    # Filter the DataFrame by the country ID
    df = df[df['c_id'] == country_id].copy()
    
    # Save the DataFrame to a pickle file
    print(f'Saving file to {path_viewser_df}')
    df.to_pickle(path_viewser_df)

    # print the final size of the DataFrame
    print(f'Final size of DataFrame: {df.shape}')

    return df

if __name__ == "__main__":
    PATH_RAW = '/home/simon/Documents/scripts/VIEWS_FAO_index/data/raw_viewser'
    df_cal = fetch_views_df(PATH_RAW)






























# import sys
# import os
# import numpy as np
# import pandas as pd
# 
# from viewser import Queryset, Column
# from ingester3.ViewsMonth import ViewsMonth
# 
# 
# def get_input_data_config():
# 
#     """
#     Contains the configuration for the input data in the form of a viewser queryset. That is the data from viewser that is used to train the model.
#     This configuration is "behavioral" so modifying it will affect the model's runtime behavior and integration into the deployment system.
#     There is no guarantee that the model will work if the input data configuration is changed here without changing the model settings and architecture accordingly.
# 
#     Returns:
#     queryset_base (Queryset): A queryset containing the base data for the model training.
#     """
# 
#     queryset_base = (Queryset("FAO_simon_experiments", "priogrid_year")
#         .with_column(Column("sb_best", from_loa = "priogrid_year", from_column = "ged_sb_best_count_nokgi").transform.missing.replace_na())
#         .with_column(Column("ln_pop_gpw_sum", from_loa="priogrid_year", from_column="pop_gpw_sum").transform.missing.fill().transform.missing.replace_na())
#         .with_column(Column("year_id", from_loa = "country_year", from_column = "year_id"))
#         .with_column(Column("year", from_loa = "country_year", from_column = "year"))
#         .with_column(Column("c_id", from_loa = "country_year", from_column = "country_id"))
#         .with_column(Column("col", from_loa = "priogrid", from_column = "col"))
#         .with_column(Column("row", from_loa = "priogrid", from_column = "row")))
# 
#     return queryset_base
# 
# 
# def fetch_data_from_viewser(year_first, year_last):
#     """
#     Fetches and prepares the initial DataFrame from viewser.
# 
#     Returns:
#         pd.DataFrame: The prepared DataFrame with initial processing done.
#     """
#     print(f'Beginning file download through viewser with year range {year_first},{year_last}')
#     queryset_base = get_input_data_config()
# 
#     df = queryset_base.publish().fetch()
# 
#     df.reset_index(inplace=True)
# 
#     df.rename(columns={'priogrid_gid': 'pg_id'}, inplace=True) # arguably HydraNet or at lest vol specific
# 
#     df['in_viewser'] = True  # arguably HydraNet or at lest vol specific
#     
#     return df
# 
# 
# def get_year_range():
#     """
#     ...
#     """
# 
#     # as specific in Håvard's mail
#     year_first = 1989
#     year_last = 2023
# 
# 
#     return year_first, year_last
# 
# 
# def filter_dataframe_by_year_range(df, year_first, year_last):
#     """
#     Filters the DataFrame to include only the specified year range.
# 
#     Args:
#         df (pd.DataFrame): The input DataFrame to be filtered.
#         year_first (int): The first year ID to include.
#         year_last (int): The last year ID to include.
# 
#     Returns:
#         pd.DataFrame: The filtered DataFrame.
#     """
#     month_range = np.arange(year_first, year_last)
#     return df[df['month_id'].isin(month_range)].copy()
# 
# 
# def get_views_df():
#     """
#     ...
#     """
# 
#     year_first, year_last = get_year_range()
# 
#     df = fetch_data_from_viewser(year_first, year_last)
# 
#     return df
# 
# 
# def fetch_or_load_views_df(partition, PATH_RAW):
# 
#     """
#     ...
#     """
# 
#     path_viewser_df = os.path.join(str(PATH_RAW), f'{"simons_mali_01"}_viewser_df.pkl') 
# 
#     # Create the folders if they don't exist
#     os.makedirs(str(PATH_RAW), exist_ok=True)
# 
#     print(f'Fetching file...')
#     df = get_views_df(partition) # which is then used here
#     
#     print(f'Saving file to {path_viewser_df}')
#     df.to_pickle(path_viewser_df)
# 
# 
#     return df
# 
# 
# if __name__ == "__main__":
# 
#     PATH_RAW = 'data/raw'
#     df_cal = fetch_or_load_views_df('calibration', PATH_RAW)
# 
# 
# 