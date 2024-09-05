import pandas as pd
import os

def smoothed_dataframe(location_of_smoothed_df, df, smoothing_column='Annual_Percapita_Fatalities_PopNet'):

    base_directory = os.getcwd()
    smoothing_file_location = base_directory + location_of_smoothed_df
    print(smoothing_file_location)

    smoothed_df = pd.read_csv(smoothing_file_location)

    print(len(smoothed_df['gid']))

    # Remove any leading or trailing whitespace (including tabs) from column names in both DataFrames
    df.columns = df.columns.str.strip()
    smoothed_df.columns = smoothed_df.columns.str.strip()

    columns_to_keep = ['priogrid_gid', 'year']
    df_annual = df[columns_to_keep]
    df_unique_combinations = df_annual.drop_duplicates()
    print(f'the length of the country priogrid dataframe is: {len(df_unique_combinations)}')

    # # Rename 'gid' to 'priogrid_gid' and drop the 'Annual_Percapita_Fatalities_PopNet' column if it exists
    if 'gid' in smoothed_df.columns:
        smoothed_df = smoothed_df.rename(columns={'gid': 'priogrid_gid', 'year_id': 'year'}) #if this gets ingested to viewser this will become obsolete
        if 'Annual_Percapita_Fatalities_PopNet' in smoothed_df.columns:
            smoothed_df = smoothed_df.drop(columns=['Annual_Percapita_Fatalities_PopNet'])

    # # Perform the merge
    df_to_format_stats = df_unique_combinations.merge(smoothed_df, on=['priogrid_gid', 'year'], how='left')
    print(f'After joining...the length of the country priogrid dataframe is: {len(df_to_format_stats)}')

    after_join_columns_to_keep = ['priogrid_gid', 'year', smoothing_column]
    df_annual_cleaned = df_to_format_stats[after_join_columns_to_keep]

    #The Percapita_PopNet_Smoothed was NOT PRE-PROCESSED to include per capita fatalities per 100,000 the values are the true decimal values.
    
    #df_annual_cleaned['percapita_100k'] = df_annual_cleaned[smoothing_column]*100000
    # # Print the first 5 rows of the resulting dataframe
    return(df_annual_cleaned)