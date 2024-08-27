import pandas as pd
import glob
import os
from collections import Counter

def aggregate_priogrid_for_country(table,scale=0,country=0,recent_or_all='recent'):

    """
    1. Maps individual priogrid id to an aggregate cell 
    
    """
    base_dir = os.path.abspath(os.path.join(os.getcwd(), '..', '..'))

    aggregation_tables_dir = base_dir + '/data/generated/Aggregation_Key_Tables/'

            #source_PG_aggregation_dir = '/Users/gbenz/Documents/Common Data/PG Aggregation/'
    allFiles = glob.glob(aggregation_tables_dir + "/*.csv")

    for filename in allFiles:
        if scale in filename:
                        #print(filename)
            break
    Aggregation_file = filename

    single_res = int(scale.split('x')[0])

    Expected = single_res ** 2

    pg_AG = pd.read_csv(Aggregation_file)

    pg_AG['gid'] = pg_AG['gid'].astype(str)
    pg_AG['Id'] = pg_AG['Id'].astype(str)

    pg_AG['Scale_ID'] = pg_AG.groupby(['Id'])['gid'].transform(lambda x : '_'.join(x))

    pg_AG['gid'] = pg_AG['gid'].astype('int64')
    pg_AG['Id'] = pg_AG['Id'].astype('int64')

        #A method to get rows that communicate 1. Each indivdiual geospatial abstract id and corresponding PRIOgrid ID 
    pg_AG__FOR_VALIDATE = pg_AG.groupby(['Id','Scale_ID']).size().to_frame().iloc[:, :-1].reset_index()
    pg_AG__FOR_VALIDATE = pg_AG__FOR_VALIDATE.sort_values(by='Scale_ID')

            #pg_AG__FOR_VALIDATE['liststring'] = pg_AG__FOR_VALIDATE['lists'].apply(lambda x: ','.join(map(str, x)))
    GIS_dic = dict(zip(pg_AG__FOR_VALIDATE['Scale_ID'], pg_AG__FOR_VALIDATE['Id']))

    pg__AG = pg_AG.groupby('Scale_ID')['gid'].apply(list)
    pg__AG__dic = pg__AG.to_dict()

    table['Scale_ID'] = table.pg_id.map({item: k for k, v in pg__AG__dic.items() for item in v})
    df_2022 = table.sort_values(by=['Scale_ID','pg_id'], ascending=[False,True])
#----------------------------------------------------------------------------------------------------------------------------------------------------
    df_2022['GIS__Index'] = df_2022['Scale_ID'].map(GIS_dic)

    return(df_2022)

def map_c_y_dictionary_to_data(country_year_dictionary, df):

    """
    filters dataframe by the most recent year range, those associated with the first country id

    returns a filtered dataset and a variable containing the desired country id
    """

    first_key = list(country_year_dictionary.keys())[0]
    start_date, end_date = country_year_dictionary[first_key]


    df_return = df[(df['year'] >= start_date) & (df['year'] <= end_date)]

    return(df_return, first_key)
    #query on new dates

def concatenate_countryids(group):
        concat_countryids = '__'.join(group['c_id'].astype(str))
        return pd.Series({'scale_cid':concat_countryids})

def most_common_value(c_id_list):
    counter = Counter(c_id_list)
    most_common = counter.most_common(1)[0][0]  # Get the most common value
    return most_common

def map_c_id_to_aggregations(df):       
        #withcountry = df.groupby(['Scale_ID','c_id']).size().to_frame().iloc[:, :-1].reset_index()
        grouped = df.groupby(['Scale_ID','year']).apply(concatenate_countryids).reset_index()
        grouped['scale_cid_list'] = grouped['scale_cid'].str.split('__')

        grouped['most_common_cid'] = grouped['scale_cid_list'].apply(most_common_value)
        grouped.drop(columns=['scale_cid'], inplace=True)

        df_merged = pd.merge(df, grouped, on=['Scale_ID', 'year'])
        return(df_merged)