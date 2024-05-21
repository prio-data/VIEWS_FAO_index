import pandas as pd
from collections import Counter
import numpy as np
from ingester3.extensions import *
from collections import Counter

def params_for_graphs(description, original_df, a, b, c,):

    a=str(a)
    b=str(b)
    c=str(c)

    desc_attribute = description.at[0, 'Percentile']
    if desc_attribute == 'Fatalities':
        attribute = 'Fatalities_Sum'
    elif desc_attribute == 'Fatalities Per Capita':
        attribute = 'PerCapitaFatalities'

    f_fpc=original_df[attribute]
    #fpc=df_109_516___Fatalities['PerCapitaFatalities']

    #print('trying to now select 85th percentile value')
    Select_a_Percentile = description.at[0,a]
    Select_b_Percentile = description.at[0,b]
    Select_c_Percentile = description.at[0,c]

#print(Select_95_Percentile)

#print()
    Fatalities_a = f_fpc[f_fpc <= Select_a_Percentile]
    Fatalities_a_b = f_fpc[(f_fpc > Select_a_Percentile) & (f_fpc <= Select_b_Percentile)]
    Fatalities_b_c = f_fpc[(f_fpc > Select_b_Percentile) & (f_fpc <= Select_c_Percentile)]
    Fatalities_c = f_fpc[(f_fpc > Select_c_Percentile)]

    Fatalities_a = np.sort(Fatalities_a)
    cdf_a = 1.0 * np.arange(len(Fatalities_a)) / float(len(Fatalities_a) - 1)
    Fatalities_a_b = np.sort(Fatalities_a_b)
    cdf_a_b = 1.0 * np.arange(len(Fatalities_a_b)) / float(len(Fatalities_a_b) - 1)
    Fatalities_b_c = np.sort(Fatalities_b_c)
    cdf_b_c = 1.0 * np.arange(len(Fatalities_b_c)) / float(len(Fatalities_b_c) - 1)
    Fatalities_c = np.sort(Fatalities_c)
    cdf_c = 1.0 * np.arange(len(Fatalities_c)) / float(len(Fatalities_c) - 1)
    return((Fatalities_a,cdf_a), (Fatalities_a_b,cdf_a_b), (Fatalities_b_c,cdf_b_c), (Fatalities_c,cdf_c))

def single_hist_params (hist):
    xlim_max = max(hist)+1
    xlim_min = min(hist)-1 # for x limit min

    x_ticks = linspace(xlim_min,xlim_max,5)
    x_int_list = [int(item) for item in x_ticks]

    x_tick_labels = [str(item) for item in x_int_list]
    x_tick_labels[1] = ''
    x_tick_labels[3] = ''

    num_most_common = Counter(hist).most_common(1)[0][1]
    ylim_max=num_most_common + 3 #for y limit max

    ylim_min = 0

    y_ticks = linspace(ylim_min,ylim_max,3)
    y_int_list = [int(item) for item in y_ticks]

    y_tick_labels = [str(item) for item in y_int_list]
    return(xlim_max, xlim_min, x_int_list, x_tick_labels, ylim_max, ylim_min, y_int_list, y_tick_labels)

def summarytextline (cm_or_pg, total_events, perc_nonzero, total_nonzero, fpc_99th_nz, fpc_99th_nz_occurance, month_or_annual='monthly', resolution=0, country=0):

    if cm_or_pg == 'PG' and country != 0:
        text = f'In {country}, employing a unit of analysis that considers a {resolution} priogrid at a {month_or_annual} temporal resolution, yields {total_events} total events.\nFrom this value, just less than {perc_nonzero}% report zero fatalities. Among a subset data frame, consisting of {total_nonzero} non-zero events,\nthe 99th percentile reports {fpc_99th_nz} fatalities per capita (per 10,000 individuals), a threshold experienced {fpc_99th_nz_occurance} times.'
        return(text)
    
    if cm_or_pg == 'PG' and country == 0:
        text = f'Across Africa and the Middle East, employing a unit of analysis that considers a {resolution} priogrid at a {month_or_annual} temporal resolution,\nyields {total_events} total events. From this value, just less than {perc_nonzero}% report zero fatalities. Among a subset data frame,\nconsisting of {total_nonzero} non-zero events, the 99th percentile reports {fpc_99th_nz} fatalities per capita (per 10,000 individuals), a threshold experienced {fpc_99th_nz_occurance} times.'
        return(text)

    if cm_or_pg == 'CM' and country == 0:
        text = f'Globally, employing a unit of analysis that considers each county boundary at a {month_or_annual} temporal resolution,\nyields {total_events} total events. From this value, just less than {perc_nonzero}% report zero fatalities. Among a subset data frame,\nconsisting of {total_nonzero} non-zero events, the 99th percentile reports {fpc_99th_nz} fatalities per capita (per 10,000 individuals), a threshold experienced {fpc_99th_nz_occurance} times.'
        return(text)

    if cm_or_pg and country != 0:
        text = f'In {country}, employing a unit of analysis that exclusively considers this county boundary at a {month_or_annual} temporal resolution,\nyields {total_events} total events. From this value, just less than {perc_nonzero}% report zero fatalities. Among a subset data frame, consisting\nof {total_nonzero} non-zero events, the 99th percentile reports {fpc_99th_nz} fatalities per capita (per 10,000 individuals),\na threshold experienced {fpc_99th_nz_occurance} times.'
        return(text)

def format_for_summarytextline(cm_or_pg,A,B,C,D,month_or_annual='monthly',resolution=0, country=0):

    cm__or__pg = cm_or_pg
    mora = month_or_annual
    r = resolution
    c = country

    total_events = len(A)
    Percentage_non_zero = B.loc[0, 'Percentile']
    total_nonzero = C.loc[1, '0']
    PCF_Occurance = D.loc[1, '99']
    PCF_total = D.loc[0, '99']
        
    txt = summarytextline(cm__or__pg, total_events, Percentage_non_zero, total_nonzero, PCF_total, PCF_Occurance, mora, r, c)
    return(txt)
        
def timeline_x_axes_params(start,end):
        start_month = start
        end_month = end
        up_by = 6
        givemevalues = list(range(start_month, end_month+1, up_by))

        every_12th_value_list = givemevalues[::4]

        test__df = pd.DataFrame({'original_column': givemevalues})
        joining_df = pd.DataFrame({'joining_column': every_12th_value_list})

        # Merge the DataFrames with an outer join
        result_df = pd.merge(test__df, joining_df, left_on='original_column', right_on='joining_column', how='outer')
        result_df = result_df.rename(columns={'original_column': 'month_id'})
        #column_types = result_df.dtypes

        #result_df = result_df.fillna(0)
        result_df['month_id'] = result_df['month_id'].astype(int)
        #print(result_df)
        result_df['month'] = result_df.m.month.astype(str)
        #gisfile['month'] = np.where(gisfile['month'].isin(m_list),gisfile['month'].str.zfill(1),gisfile['month'].str.zfill(0))
        result_df['month'] = result_df['month'].astype(str).str.replace(r'\.0$', '').str.zfill(2)

        #result_df['month'] = result_df['month'].astype(str).str.zfill(2)
        result_df['year'] = result_df.m.year.astype(str)
        result_df['date'] = result_df['year'] + ', ' + result_df['month']

        result_df.loc[result_df['joining_column'].isna(), 'year'] = np.nan
        x_labels = result_df['year'].fillna('').tolist()
        x_ticks = result_df['month_id'].tolist()
        return(x_ticks, x_labels)

