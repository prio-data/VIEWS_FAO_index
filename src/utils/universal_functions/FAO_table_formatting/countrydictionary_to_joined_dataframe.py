
import pandas as pd

def merge_countrydictionary_tables(country_data, table_type):
    """
    Merges the specified table (if available) across all countries in country_data.
    
    Parameters:
      - country_data: dict
          A dictionary where keys are country names and values are dicts containing
          various tables (e.g., 'annual summary report', 'return period table').
      - table_type: str
          The type of table to merge. Must be one of:
          'return period table', 'annual summary report'
    
    Returns:
      A merged pandas DataFrame of the selected table type, merged on the appropriate key.
    """
    # Define merge keys for each table type
    merge_keys = {
        'return period table': 'Percentile',
        'annual summary report': 'year',
    }
    
    if table_type not in merge_keys:
        raise ValueError("Invalid table_type. Must be one of: 'return period table', 'annual summary report', or 'PGY dataframe'")
    
    merge_key = merge_keys[table_type]
    merged_df = None
    
    for country, data in country_data.items():
        # Check if the country has the table of interest
        if table_type in data:
            # Get a copy of the DataFrame
            df = data[table_type].copy()
            # Rename all columns (except the merge key) to include the country name as a suffix
            new_cols = {col: f"{col}_{country}" for col in df.columns if col != merge_key}
            df.rename(columns=new_cols, inplace=True)
            
            # Merge with the aggregated DataFrame
            if merged_df is None:
                merged_df = df
            else:
                merged_df = pd.merge(merged_df, df, on=merge_key, how='outer')
                
    return merged_df