from viewser import Queryset, Column
import pandas as pd

from ingester3.extensions import *


def give_primary_frame(queryset_name, cm_queryset, start, end):

    """"
    1. retrieves base queryset
    2.assigns a year field from Ingester3 functions
    3. trims to defined intervals
    4. sum fatalities

    """

    queryset_base_PG= (Queryset(queryset_name, ''))
    df = queryset_base_PG.fetch()
    df = df.reset_index()

    queryset_cm= (Queryset(cm_queryset, ''))
    cm_properties = queryset_cm.fetch()
    cm_properties = cm_properties.reset_index()    

    df['year'] = df.m.year

    df_trimmed = df[(df['year'] > start) & (df['year'] < end)]
    df_trimmed['fatalities_sum'] = df_trimmed['ged_sb'] + df_trimmed['ged_ns'] + df_trimmed['ged_os']


    merged_cid = pd.merge(df_trimmed, cm_properties[['month_id', 'country_name', 'country_id']], on=['month_id', 'country_name'], how='left')
    #print(merged_cid)
    df_pg = merged_cid

    df_pg = df_pg.rename(columns={'priogrid_gid':'pg_id'})
    #df_pg['year_id'] = df_pg['month_id'].apply(views_month_id_to_year)

    print(list(df_pg))
    return(df_pg)
