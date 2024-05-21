import glob
import numpy as np
import pandas as pd
import os
from support_functions.setup_general import report_infinity_values

aggregation_tables_dir = os.getcwd() + '/Aggregation_Key_Tables/'

def DOBY(n):
    n['Year_range'] = list(zip(n["C_start_year"], n["C_end_year"]))
    d = dict(zip(n['C_id'], n['Year_range']))
    return(d)

#boundaries = 'first'

def setup_DOBY(df, country, boundary_requirement):

    filtered__country = df.loc[(df['country_name']==country)]
    filtered__country = filtered__country.rename(columns={'country_id':'C_id'})
    country_and_year = filtered__country.groupby(['C_id', 'country_name', 'C_start_year', 'C_end_year']).size().to_frame().iloc[:, :-1].reset_index()
    cids = list(unique(country_and_year['C_id']))

    length_of_cids = len(cids)
    country_and_year_sorted=country_and_year.sort_values(by=['C_start_year'],ascending=False)
    if length_of_cids > 1 and boundary_requirement == 'recent':
        country_head=country_and_year_sorted.head(1)
        year_dictionary = DOBY(country_head)
        return(year_dictionary)

    else:
        year_dictionary = DOBY(country_and_year_sorted)
        return(year_dictionary)


def scale_and_countryid(dictionary_input, table_input, scale):
        
        year_len_dictionary=len(dictionary_input)

        if year_len_dictionary > 1:
                #if running for 'all'
                print('multiple dictionary keys')
                join_multi_country_ID = pd.DataFrame()

                for index, (key, value) in enumerate(dictionary_input.items()):
                        print(index)
                        key = str(key)
                        print(key)
                        start = value[0]
                        print(start)
                        end = value[1]
                        print(end)
                        if index == 0:
                                print('index 0:', index, ' includes start value: ', start, 'and end value: ',end)
                                #--
                                if scale != '1x1': #because this field is a list
                                        selected_country = table_input.loc[table_input['Included_Countries'].explode().eq(key).loc[lambda x: x].index]
                                else: #because this field is just a value
                                        #going to have to convert this field to a string type
                                        selected_country = table_input.loc[table_input['country_id']==key]
                                #---
                                selected_filtered_country = selected_country.loc[(selected_country['year_id']>=start) & (selected_country['year_id']<= end)]
                                
                                if scale != '1x1':
                                        selected_filtered_country = selected_filtered_country.drop(['country_id', 'Included_Countries','C_start_year','C_end_year'], axis = 1)
                                else:
                                        selected_filtered_country = selected_filtered_country.drop(['country_id', 'C_start_year','C_end_year'], axis = 1)

                                selected_filtered_country.drop_duplicates()
                                print(selected_filtered_country.tail(5))

                                chckPG = len(unique(selected_filtered_country['priogrid_gid']))
                                print(chckPG)
                                chckmonth = len(unique(selected_filtered_country['month_id']))
                                print(chckmonth)
                                all =len(selected_filtered_country)
                                print(all)
                                #---
                                df_2022_grouped = selected_filtered_country.groupby(['month_id','year_id','Scale_ID']).agg({'PerCapitaFatalities':'sum','Fatalities_Sum':'sum'}).reset_index()
                                #append to empty dataframe
                                df_2022_grouped['Applied_cid'] = key
                                print('dataframe for:', key)
                                print(df_2022_grouped.tail(3))
                                join_multi_country_ID = join_multi_country_ID.append(df_2022_grouped)
                        else:
                                print('index should be other than 0:', index, ' includes start value: ', start, 'and end value: ',end)
                                if scale != '1x1': #because this field is a list
                                        selected_country = table_input.loc[table_input['Included_Countries'].explode().eq(key).loc[lambda x: x].index]
                                else: #because this field is just a value
                                        #going to have to convert this field to a string type
                                        selected_country = table_input.loc[table_input['country_id']==key]

                                selected_filtered_country = selected_country.loc[(selected_country['year_id']>=start) & (selected_country['year_id'] < end)]
                                #---
                                if scale != '1x1':
                                        selected_filtered_country = selected_filtered_country.drop(['country_id', 'Included_Countries','C_start_year','C_end_year'], axis = 1)
                                else:
                                        selected_filtered_country = selected_filtered_country.drop(['country_id', 'C_start_year','C_end_year'], axis = 1)                                
                                
                                selected_filtered_country.drop_duplicates()
                                print(selected_filtered_country.tail(5))

                                chckPG = len(unique(selected_filtered_country['priogrid_gid']))
                                print('length of PG: ',chckPG)
                                chckmonth = len(unique(selected_filtered_country['month_id']))
                                print('length of monthid: ',chckmonth)
                                all =len(selected_filtered_country)
                                print('total; ',all)
                            #---
                                df_2022_grouped = selected_filtered_country.groupby(['month_id','year_id','Scale_ID']).agg({'PerCapitaFatalities':'sum','Fatalities_Sum':'sum'}).reset_index()
                                df_2022_grouped['Applied_cid'] = key
                                print('dataframe for:', key)
                                print(df_2022_grouped.tail(3))
                                join_multi_country_ID = join_multi_country_ID.append(df_2022_grouped)

                return(join_multi_country_ID)

        else:
                for key, value in dictionary_input.items():
                        key = str(key)
                        print(key)
                        start = value[0]
                        print(start)
                        end = value[1]
                        print(end)
                        if scale != '1x1': #because this field is a list
                                selected_country = table_input.loc[table_input['Included_Countries'].explode().eq(key).loc[lambda x: x].index]
                        else: #because this field is just a value
                                        #going to have to convert this field to a string type
                                selected_country = table_input.loc[table_input['country_id']==key]

                        selected_filtered_country = selected_country.loc[(selected_country['year_id']>=start) & (selected_country['year_id']<= end)]
                        if scale != '1x1':
                                selected_filtered_country = selected_filtered_country.drop(['country_id', 'Included_Countries','C_start_year','C_end_year'], axis = 1)
                        else:
                                selected_filtered_country = selected_filtered_country.drop(['country_id', 'C_start_year','C_end_year'], axis = 1)                          
                        
                        selected_filtered_country.drop_duplicates()
                        #print(selected_filtered_country.tail(5))

                        chckPG = len(unique(selected_filtered_country['priogrid_gid']))
                        print(chckPG)
                        chckmonth = len(unique(selected_filtered_country['month_id']))
                        print(chckmonth)
                        all =len(selected_filtered_country)
                        print(all)

                        df_2022_grouped = selected_filtered_country.groupby(['month_id','year_id','Scale_ID']).agg({'PerCapitaFatalities':'sum','Fatalities_Sum':'sum'}).reset_index()
                        df_2022_grouped['Applied_cid'] = key
                        return(df_2022_grouped)
                
def map_c_id_to_aggregations(x):       
        withcountry = x.groupby(['Scale_ID','country_id']).size().to_frame().iloc[:, :-1].reset_index()
                #This is exactly the problem ------^
        withcountry['country_id'] = withcountry['country_id'].astype(str)

        withcountry['Country_id_present'] = withcountry.groupby(['Scale_ID'])['country_id'].transform(lambda x : '___'.join(x))
        withcountry = withcountry.drop(['country_id'], axis=1).drop_duplicates()

        withcountry__dic = dict(zip(withcountry.Scale_ID, withcountry.Country_id_present))
        #print(withcountry)

        x['Countries_In_AG_Unit']= x['Scale_ID'].map(withcountry__dic)
        x['Included_Countries'] = x['Countries_In_AG_Unit'].str.split('___')
        return(x)

    
def PRIO_Agg_serious(table,time,CMorPG,scale=0,country=0,recent_or_all='recent'):
    
    CM_or_PG = CMorPG
    c = np.isinf(table['PerCapitaFatalities']).values.sum() 

    if c > 0:    
        table=report_infinity_values(table,CM_or_PG)

    if time == 'monthly':
        time_attribute = 'month_id'
    elif time == 'annual':
        time_attribute = 'year_id'

    if CM_or_PG == 'CM':
        if country == 0:
            table = table.rename(columns={'country_id':'Scale_ID'})
            table = table.rename(columns={'country_name':'Included_Countries'})
            table = table.drop(['year_id', 'pop_gpw_sum'], axis=1)
            return(table)
        elif country !=0:
            table = table.rename(columns={'country_id':'Scale_ID'})
            table = table.rename(columns={'country_name':'Included_Countries'})
            table = table.drop(['year_id', 'pop_gpw_sum'], axis=1)
            selected_country=table[table['Included_Countries'].isin([country])]
            return(selected_country, selected_country)

    elif CM_or_PG == 'PG': 
        if scale == '1x1':

            if country == 0:
                table = table.rename(columns={'priogrid_gid':'Scale_ID'})
                table = table.drop(['year_id', 'pop_gpw_sum'], axis=1)
                #table = table.rename(columns={'country_name':'Included_Countries'})
                table = table.drop(['country_id','C_start_year','C_end_year'], axis = 1)
                table.drop_duplicates()
                return(table, table)
            else:
#FIX 02-18--------------------------------------------------------------------------------------------------------------------
#Need to reflect consistent changes to the aggregation functions applied below
#Must map to the Country ID 

#NEED TO ADD the function to map only recent boundaries--
                #selected_country = table[table['Included_Countries'].isin([country])]
#What fields does setupDOBY need:
#just country_name
                #table['Included_Countries'] = table['country_id']
                table['Scale_ID'] = table['priogrid_gid']
                table['country_id'] = table['country_id'].astype(str)

#------^is a matter of formatted so field names match what the definition is looking for rather 
#   than add a series of if statements
                year_dictionary = setup_DOBY(table, country, recent_or_all)
                xx = scale_and_countryid(year_dictionary, table, scale)

                #xx = xx.drop(['country_id','C_start_year','C_end_year'], axis = 1)
                xx.drop_duplicates()
                return(xx, xx)    
        #--------------------------------------------------
        else:
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

            table['Scale_ID'] = table.priogrid_gid.map({item: k for k, v in pg__AG__dic.items() for item in v})
            df_2022 = table.sort_values(by=['Scale_ID','priogrid_gid'], ascending=[False,True])
#----------------------------------------------------------------------------------------------------------------------------------------------------
        #changes here --
        #This is exactly the problem ------^

            if country == 0:
                df_2022 = df_2022.drop(['country_id','C_start_year','C_end_year'], axis = 1)
                df_2022.drop_duplicates()

                print(df_2022.tail(5))

                chckPG = len(unique(df_2022['priogrid_gid']))
                print(chckPG)
                chckmonth = len(unique(df_2022['month_id']))
                print(chckmonth)
                all =len(df_2022)
                print(all)
                #---
                df_2022_grouped = df_2022.groupby(['month_id','year_id','Scale_ID']).agg({'PerCapitaFatalities':'sum','Fatalities_Sum':'sum'}).reset_index()
                #append to empty dataframe
                df_2022_grouped['Applied_cid'] = 'None'

                #print('dataframe for:', key)
                df_2022_grouped['GIS__Index'] = df_2022_grouped['Scale_ID'].map(GIS_dic)
                for_GIS = df_2022_grouped.drop(['Scale_ID'], axis=1)
                df_2022_grouped = df_2022_grouped.drop(['GIS__Index'], axis=1)

                return(df_2022_grouped, for_GIS)
            else:

                df_22 = map_c_id_to_aggregations(df_2022)
                year_dictionary = setup_DOBY(table, country, recent_or_all)
                xx = scale_and_countryid(year_dictionary, df_22, scale)

                
                xx['GIS__Index'] = xx['Scale_ID'].map(GIS_dic)
                for_GIS = xx.drop(['Scale_ID'], axis=1)
                xx = xx.drop(['GIS__Index'], axis=1)

                return(xx, for_GIS)