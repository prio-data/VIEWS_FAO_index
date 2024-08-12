import numpy as np
import os

report_inf = os.getcwd() + '/Report_Checks/Report_inf_values/'

def views_month_id_to_year(month_id: int) -> int:
    """Converts a month_id to the calendar year of the month_id. Works on vectors/columns of month_ids.

    Parameters
    ----------
    month_id : int
        A count of months starting (from 1) on January 1980.

    Returns
    -------
    int
        The calendar year of the month_id.
    """
    return 1980 + (month_id - 1) // 12


def PGM_preprocess(table):

    #replace NA Population values with 0
    table['pop_gpw_sum'] = table['pop_gpw_sum'].replace({np.nan:0})

    table['Fatalities_Sum'] = table['ged_sb'] + table['ged_ns'] + table['ged_os']
    table['PerCapitaFatalities'] = table['Fatalities_Sum'] / table['pop_gpw_sum']
    table['PerCapitaFatalities'] = table['PerCapitaFatalities'].replace({np.nan:0})

    table = table.drop(['ged_sb','ged_ns','ged_os'], axis = 1)

    return(table)

def report_infinity_values(base_table,CM__or__PG, resolution=0):

    if resolution == 0:
        res = '_'
    else:
        res = resolution

    CM__or__PGstr = CM__or__PG+'_'

    base_table['PerCapitaFatalities'] = base_table['PerCapitaFatalities'].replace([np.inf, -np.inf], np.nan)
    Anamoly = base_table[base_table['PerCapitaFatalities'].isna()]
    #Anamoly.to_csv(f'/Users/gbenz/Documents/Food Security and Conflict/{CM__or__PGstr}{res}Fatality_NoPop.csv')
    Anamoly.to_csv(f'{report_inf}{CM__or__PGstr}{res}Fatality_NoPop.csv')

    base_table['PerCapitaFatalities'] = base_table['PerCapitaFatalities'].replace({np.nan:0})

    return(base_table)