import pandas as pd
import os

def smoothed_dataframe(location_of_smoothed_df, df, df_pg_column = 'pg_id', df_year_column = 'year', smooth_pg_column = 'pg_id', smooth_year_column = 'year', smoothing_column='Annual_Percapita_Fatalities_PopNet'):

#If the prio grid id columns between the 'df' and 'smooth' dataframe do not match then we will set it to the name consistent with the df dataframe

    smoothed_df = pd.read_csv(location_of_smoothed_df)

    smoothed_columns = list(smoothed_df)
    print(f'The smoothed dataframe contains the following columns: {smoothed_columns}')

    if df_pg_column != smooth_pg_column:
        smoothed_df.rename(columns={smooth_pg_column: df_pg_column}, inplace=True)

    if df_year_column != smooth_year_column:
        smoothed_df.rename(columns={smooth_year_column: df_year_column}, inplace=True)

    # Remove any leading or trailing whitespace (including tabs) from column names in both DataFrames
    df.columns = df.columns.str.strip()
    smoothed_df.columns = smoothed_df.columns.str.strip()

    columns_to_keep = [df_pg_column, df_year_column]
    df_annual = df[columns_to_keep]
    df_unique_combinations = df_annual.drop_duplicates()
    print(f'the length of the smoothed country priogrid dataframe is: {len(df_unique_combinations)}')

    # # # Rename 'gid' to 'priogrid_gid' and drop the 'Annual_Percapita_Fatalities_PopNet' column if it exists
    # if 'gid' in smoothed_df.columns:
    #     smoothed_df = smoothed_df.rename(columns={'gid': 'priogrid_gid', 'year_id': 'year'}) #if this gets ingested to viewser this will become obsolete
    #     if 'Annual_Percapita_Fatalities_PopNet' in smoothed_df.columns:
    #         smoothed_df = smoothed_df.drop(columns=['Annual_Percapita_Fatalities_PopNet'])

    # # Perform the merge
    df_to_format_stats = df_unique_combinations.merge(smoothed_df, on=[df_pg_column, df_year_column], how='left')
    print(f'After joining...the length of the country priogrid dataframe is: {len(df_to_format_stats)}')

    after_join_columns_to_keep = [df_pg_column, df_year_column, smoothing_column]
    df_annual_cleaned = df_to_format_stats[after_join_columns_to_keep]

    #The Percapita_PopNet_Smoothed was NOT PRE-PROCESSED to include per capita fatalities per 100,000 the values are the true decimal values.
    
    #df_annual_cleaned['percapita_100k'] = df_annual_cleaned[smoothing_column]*100000
    # # Print the first 5 rows of the resulting dataframe
    return(df_annual_cleaned)