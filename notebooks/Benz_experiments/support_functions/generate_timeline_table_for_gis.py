from ingester3.extensions import *
import os

Timeline_tables_dir = os.getcwd() + '/Tables_For_Timeline_Maps/'

def Save_for_timeline_generation(yes_or_no, gisfile, pg_or_cm, temporal, resolution, country):
    
    if yes_or_no == 'yes':

#1. create month field --
#2. convert to string
        m_list = ['1','2','3','4','5','6','7','8','9']
    #subset all that fit the prior def
    #mask = df['Subscription'].isin(active_statuses)

        gisfile['month'] = gisfile.m.month.astype(str)
        #gisfile['month'] = np.where(gisfile['month'].isin(m_list),gisfile['month'].str.zfill(1),gisfile['month'].str.zfill(0))
        gisfile['month'] = gisfile['month'].astype(str).str.zfill(2)
        gisfile['year'] = gisfile.m.year.astype(str)
        gisfile['date'] = gisfile['year'] + '-' + gisfile['month']

        gisfile = gisfile.drop(['month','year'], axis=1)

        print(gisfile.head(3))
    #All_country_zero.loc[mask, 'Percentile_of_1'] = 100

        gisfile.to_csv(f'{Timeline_tables_dir}{pg_or_cm}_{temporal}_{resolution}_{country}.csv')