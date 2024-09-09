"""
specify the field that you want to derive per capita fatalities from: this is using the total of sb, os, and ns for the application with FAO
 but could be replicated with any one or combination of these UCDP catagories.

 also accepts a population field, the default is = 'pop_gpw_sum'

is going to look for a year column as year this should be noted as viewser might supply year_id in which case the column name should be changed.

"""
import pandas as pd

def native_per_capita_fatalities(df, pg_field='pg_id',year_field='year',fatality_field='fatalities_sum', population_field='pop_gpw_sum'):
    
    # columns to group by
    grouping_columns = [pg_field, year_field]
    annual_fatalities = df.groupby(grouping_columns)[fatality_field].sum().reset_index()
    # Gives the population value from the last month. This is expected to be the same as the first month
    #   however, in case population data becomes more temporally granular (World Pop is improving) we want a value
    #   that closest resembles the 'net' population from that year.
    annual_population = df.groupby(grouping_columns)[population_field].last().reset_index()
    
    # Merge the summed monthly data with the yearly data
    df_annual = pd.merge(annual_fatalities, annual_population, on=grouping_columns)
    

    df_annual['percapita_100k'] = (df_annual[fatality_field] / df_annual[population_field]) * 100000
    return df_annual