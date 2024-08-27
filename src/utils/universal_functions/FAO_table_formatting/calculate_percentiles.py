import pandas as pd
import numpy as np

def format_stats(table_to_describe, field_to_describe='percapita_100k'):
    
    lowpercentile = 0

    p = np.array(np.arange(lowpercentile, 100.1, 0.1))
    divisor = 100
    p_div = p/divisor
    l = p_div.tolist()
    l_3dec = [round(elem, 3) for elem in l]

    SummaryField = field_to_describe
    data = pd.DataFrame({SummaryField: table_to_describe[SummaryField].describe(percentiles=l_3dec)})
    return(data)

def clean_percentile_table(df):

    new_x = df.reset_index()
    filtered_x = new_x[~new_x['index'].isin(['count', 'mean', 'std', 'min', 'max'])]
    filtered_x = filtered_x.rename(columns={'index': 'percentile'})
    filtered_x['percentile'] = filtered_x['percentile'].str.replace('%', '')
    filtered_x['percentile'] = filtered_x['percentile'].astype('string')
    return(filtered_x)

def convert_to_float_or_null(column):
    return pd.to_numeric(column, errors='coerce')