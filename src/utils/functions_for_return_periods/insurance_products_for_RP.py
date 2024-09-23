import os
import sys

# Get the current working directory
current_directory = os.getcwd()

# Print the current working directory
print("The current Working Directory is:", current_directory)

# Get the path to the base directory (VIEWS_FAO_index)
base_dir = os.path.abspath(os.path.join(os.getcwd(), '..', '..'))
print(f'The base directory will be set to: {base_dir}')

# Add the base directory to sys.path
sys.path.insert(0, base_dir)

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

#Functions necessary for all methods:
from src.utils.universal_functions.setup.generate_base_file import give_primary_frame
from src.utils.universal_functions.setup.associate_country_id import associate_country_years, pull_from_c_y_dictionary
from src.utils.universal_functions.setup.build_directory import ensure_directory_exists


#Functions to generate the insurance table requested by FAO partners:
from src.utils.universal_functions.FAO_table_formatting.calculate_percentiles import format_stats, clean_percentile_table
from src.utils.universal_functions.FAO_table_formatting.generate_output_tables import insurance_table, annual_summary_table

#Functions bespoke to standard method:
from src.utils.functions_for_method_standard.standard_per_capita_fatalities import native_per_capita_fatalities

#Functions bespoke to aggregation method:
from src.utils.functions_for_method_aggregation.generate_aggregate_dataframe import aggregate_priogrid_for_country, map_c_y_dictionary_to_data, map_c_id_to_aggregations

#Function for Event-Year Return Period process:
from src.utils.functions_for_single_cell_return_period.cell_return_period import calculate_cumulative_distribution, calculate_probabilities, calculate_expected_time_periods, calculate_expected_voxels, compare_empirical_vs_expected
from src.utils.functions_for_single_cell_return_period.Ei_insurance_table_setup import insurance_table_for_E_i

#Functions necessary for all methods:
from src.utils.universal_functions.setup.generate_base_file import give_primary_frame
from src.utils.universal_functions.setup.associate_country_id import associate_country_years, pull_from_c_y_dictionary
from src.utils.universal_functions.setup.build_directory import ensure_directory_exists

#Functions to generate the insurance table requested by FAO partners:
from src.utils.universal_functions.FAO_table_formatting.calculate_percentiles import format_stats, clean_percentile_table
from src.utils.universal_functions.FAO_table_formatting.generate_output_tables import insurance_table, annual_summary_table

#Functions bespoke to smoothing method:
from src.utils.functions_for_method_smoothing.generate_smoothing_dataframe import smoothed_dataframe

def standard_Country_Year_files(data, country_name, eval_field):

    country_and_year_dictionary = associate_country_years(data, country_name)
    print('printing he country and year dictionary:')
    print(country_and_year_dictionary)
#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
#   Second:
#       1. Subset designated country in list. This requires examining country_id information and corresponding start and end years. 
#   Some countries contain more than one country_id. The functions employed in this section identify the most recent country range and 
#   subset the neccesary temporal ranges.
#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
    cid_int = pull_from_c_y_dictionary(country_and_year_dictionary)
    subset_to_country = data[data['country_id'] == cid_int]
    conflict_profile = {col: subset_to_country[col].sum() for col in ['ged_sb', 'ged_ns', 'ged_os', 'fatalities_sum']}

    df_annual = native_per_capita_fatalities(subset_to_country, pg_field='pg_id', year_field='year', fatality_field=eval_field, population_field='pop_gpw_sum')
    df_annual['percapita_100k'] = df_annual['percapita_100k'].round(1)

    percentile_df = format_stats(df_annual, field_to_describe=eval_field)
    filtered_x = clean_percentile_table(percentile_df)
    insurance_table_df = insurance_table(filtered_x, df_annual, ['90','95','98','99','100'], attribute_to_explore=eval_field) #uses the default attribute = percapita_100k and appened_1_value = yes
    annual_summary = annual_summary_table(df_annual, 'standard', fat_or_pcf=eval_field)
#-----------------------------------------------------------------------------------------------------------------------------------
#----- SET DIRECTORIES 
#-----------------------------------------------------------------------------------------------------------------------------------
#----- THIS SETS A DIRECTORY THAT IS UNIQUE UNIQUE STANDARD METHOD ----
#-----------------------------------------------------------------------------------------------------------------------------------
#----- <<< working just with the 'Cell Year' Return Period Process >>>-
    output_path = base_dir + '/notebooks/methods/Country_Results/' + country_name + f'/Standard/Country Year/FAO tables/'
    ensure_directory_exists(output_path)
#-----------------------------------------------------------------------------------------------------------------------------------
    annual_summary_file_path = output_path + country_name + ' annual summary.csv'
    print(f'saving annual_summary table to: {annual_summary_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
    insurance_table_file_path = output_path + country_name + ' insurance table.csv'
    print(f'saving insurance table to: {insurance_table_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
    main_dataframe_file_path = output_path + country_name + ' main dataframe.csv'
    print(f'saving main dataframe table to: {main_dataframe_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
#----- NOW WE WRITE TO THE FOLDERS. -----------------------------------
    annual_summary.to_csv(annual_summary_file_path)
    insurance_table_df.to_csv(insurance_table_file_path)
    df_annual.to_csv(main_dataframe_file_path)

    return(conflict_profile, df_annual, annual_summary, insurance_table_df)

def smoothing_Country_Year_files(data, country_name):
    country_and_year_dictionary = associate_country_years(data, country_name)
#-----------------------------------------------------------------------------------------------------------------------------------
#   Second:
#       1. Subset designated country in list. This requires examining country_id information and corresponding start and end years. 
#   Some countries contain more than one country_id. The functions employed in this section identify the most recent country range and 
#   subset the neccesary temporal ranges.
#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
    cid_int = pull_from_c_y_dictionary(country_and_year_dictionary)
    subset_to_country = data[data['country_id'] == cid_int]
    conflict_profile = {col: subset_to_country[col].sum() for col in ['ged_sb', 'ged_ns', 'ged_os', 'fatalities_sum']}

    #concludes the AOI subsetting parameters----
    smoothed_dataframe_file = base_dir + '/data/generated/Smoothing/' + 'pgy_smoothing.csv'
    
    df_annual_cleaned = smoothed_dataframe(smoothed_dataframe_file, subset_to_country, df_pg_column='pg_id', df_year_column='year', smooth_pg_column='gid', smooth_year_column='year_id', smoothing_column='perca_Mean')
    df_annual_cleaned['perca_Mean'] = df_annual_cleaned['perca_Mean'].round(1)

    percentile_df = format_stats(df_annual_cleaned, 'perca_Mean')
    filtered_x = clean_percentile_table(percentile_df)
    insurance_table_df = insurance_table(filtered_x, df_annual_cleaned, ['90','95','98','99','100'], 'perca_Mean') #uses the default attribute = percapita_100k and appened_1_value = yes
    annual_summary = annual_summary_table(df_annual_cleaned, 'smoothing', 'perca_Mean')
#-----------------------------------------------------------------------------------------------------------------------------------
#----- SET DIRECTORIES 
#-----------------------------------------------------------------------------------------------------------------------------------
#----- THIS SETS A DIRECTORY THAT IS UNIQUE FOR AGGREGATION METHOD ----
#-----------------------------------------------------------------------------------------------------------------------------------
#----- <<< working just with the 'Cell Year' Return Period Process >>>-
    output_path = base_dir + '/notebooks/methods/Country_Results/' + country_name + '/Smoothing/Cell Year/FAO tables/'
    ensure_directory_exists(output_path)
#-----------------------------------------------------------------------------------------------------------------------------------
    annual_summary_file_path = output_path + country_name + ' annual summary.csv'
    print(f'saving annual_summary table to: {annual_summary_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
    insurance_table_file_path = output_path + country_name + ' insurance table.csv'
    print(f'saving insurance table to: {insurance_table_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
    main_dataframe_file_path = output_path + country_name + ' main dataframe.csv'
    print(f'saving main dataframe table to: {main_dataframe_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
#----- NOW WE WRITE TO THE FOLDERS. -----------------------------------
    annual_summary.to_csv(annual_summary_file_path)
    insurance_table_df.to_csv(insurance_table_file_path)
    df_annual_cleaned.to_csv(main_dataframe_file_path)
#-----------------------------------------------------------------------------------------------------------------------------------
    return(conflict_profile, df_annual_cleaned, annual_summary, insurance_table_df)

def aggregation_Country_Year_files(data, country_name, aggregation_unit, eval_field):
#-----------------------------------------------------------------------------------------------------------------------------------
    country_and_year_dictionary = associate_country_years(data, country_name)
    cid_int = pull_from_c_y_dictionary(country_and_year_dictionary)
    subset_to_country = data[data['country_id'] == cid_int]
    conflict_profile = {col: subset_to_country[col].sum() for col in ['ged_sb', 'ged_ns', 'ged_os', 'fatalities_sum']}
#-----------------------------------------------------------------------------------------------------------------------------------
# First:
#   1. Aggregate the standard PRIO-Grid scale to a courser resolution
    aggregated_cells = aggregate_priogrid_for_country(data, aggregation_unit)
#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
# Second:
#   1. Subset designated country in list. This requires examining country_id information and corresponding start and end years. 
#   Some countries contain more than one country_id. The functions employed in this section identify the most recent country range and 
#   subset the neccesary temporal ranges.
#-----------------------------------------------------------------------------------------------------------------------------------
    country_and_year_dictionary = associate_country_years(aggregated_cells, country_name)
    print('printing the country id and year dictionary for reference:')
    print(country_and_year_dictionary)

    aggregated_cells_filtered_cid_year, cid = map_c_y_dictionary_to_data(country_and_year_dictionary,aggregated_cells)
    cid = str(cid)

    #print(aggregated_cells_filtered_cid_year)
    print(cid)

    aggregated_cells_filtered_cid_year = aggregated_cells_filtered_cid_year.rename(columns={'country_id':'c_id'})
    aggregated_cells_added_cid = map_c_id_to_aggregations(aggregated_cells_filtered_cid_year)
    #This process is specific to Aggregation Method: 
    columns_to_group = ['pg_id', 'year']
    columns_to_keep = ['pg_id', 'year', 'GIS__Index', 'scale_cid_list', 'most_common_cid']
    df_annual = aggregated_cells_added_cid[columns_to_keep]
    max_year = max(df_annual['year'])
    min_year = min(df_annual['year'])
    print(f'The max year in the dataframe (max_year): {max_year}')
    print(f'The min year in the dataframe (max_year): {min_year}')

    sum_fatalities_annual = aggregated_cells_added_cid.groupby(columns_to_group)['fatalities_sum'].sum().reset_index()
    print('the fields in sum_fatalities_annual:')
    print(list(sum_fatalities_annual))

    population_to_annual = aggregated_cells_added_cid.groupby(columns_to_group)['pop_gpw_sum'].last().reset_index()
    print('population_to_annual:')
    print(list(population_to_annual))

    base_annual = pd.merge(sum_fatalities_annual, population_to_annual, on=['pg_id', 'year'])
    all_annual = pd.merge(base_annual,df_annual, on=['pg_id', 'year'])

    #Now we summarize to get to the aggregation level -- dropping the PG level --
    agg_index_columns = ['year', 'GIS__Index', 'most_common_cid']

    aggregation_annual = all_annual.groupby(agg_index_columns).agg({
        'fatalities_sum': 'sum',
        'pop_gpw_sum': 'sum'
    }).reset_index()

    aggregation_annual['percapita_100k'] = ((aggregation_annual['fatalities_sum'] / aggregation_annual['pop_gpw_sum'])) * 100000
    aggregation_annual['percapita_100k'] = aggregation_annual['percapita_100k'].fillna(0)

    aggregation_annual__country = aggregation_annual[aggregation_annual['most_common_cid'] == cid]
    aggregation_annual__country['percapita_100k'] = aggregation_annual__country['percapita_100k'].round(1)

    percentile_df = format_stats(aggregation_annual__country, field_to_describe=eval_field)
    filtered_x = clean_percentile_table(percentile_df)
    insurance_table_df = insurance_table(filtered_x, aggregation_annual__country, ['90','95','98','99','100'], eval_field, 'yes')
    annual_summary = annual_summary_table(aggregation_annual__country, 'aggregation', eval_field)

#-----------------------------------------------------------------------------------------------------------------------------------
#----- SET DIRECTORIES 
#-----------------------------------------------------------------------------------------------------------------------------------
#----- THIS SETS A DIRECTORY THAT IS UNIQUE FOR AGGREGATION METHOD ----
#-----------------------------------------------------------------------------------------------------------------------------------
#----- <<< working just with the 'Cell Year' Return Period Process >>>-
    output_path = base_dir + '/notebooks/methods/Country_Results/' + country_name + '/Aggregation/Cell Year/FAO tables/'
    ensure_directory_exists(output_path)
#-----------------------------------------------------------------------------------------------------------------------------------
    annual_summary_file_path = output_path + country_name + ' annual summary.csv'
    print(f'saving annual_summary table to: {annual_summary_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
    insurance_table_file_path = output_path + country_name + ' insurance table.csv'
    print(f'saving insurance table to: {insurance_table_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
    main_dataframe_file_path = output_path + country_name + ' main dataframe.csv'
    print(f'saving main dataframe table to: {main_dataframe_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
#----- NOW WE WRITE TO THE FOLDERS. -----------------------------------
    annual_summary.to_csv(annual_summary_file_path)
    insurance_table_df.to_csv(insurance_table_file_path)
    aggregation_annual__country.to_csv(main_dataframe_file_path)
#-----------------------------------------------------------------------------------------------------------------------------------
    return(conflict_profile, aggregation_annual__country, annual_summary, insurance_table_df)


def standard_Event_Year_files(data, country_name, method, return_period_type, eval_field):

    conflict_profile, df_annual, annual_summary, insurance_table_df = standard_Country_Year_files(data, country_name, eval_field)

    df_annual = df_annual.rename(columns={'GIS__Index': 'priogrid_gid'})
    cumulative_distribution = calculate_cumulative_distribution(df_annual, eval_field)

    #calculate_probabilities(cumulative_distribution, data, id_column='percapita_100k'):
    probabilities = calculate_probabilities(cumulative_distribution, df_annual, 'pg_id')
    #print(probabilities)
    probabilities['E_i'] = calculate_expected_time_periods(probabilities['P_i'])
    # Calculate E_i^voxels
    probabilities['E_i_voxels'] = calculate_expected_voxels(probabilities['p_i'])
    probabilities_renamed = probabilities.rename(columns={'value': eval_field})
    print(probabilities_renamed.head(100))

    probabilities_with_empirical = compare_empirical_vs_expected(df_annual, probabilities_renamed, time_column='year', value_column=eval_field)
    probabilities_with_empirical_sorted = probabilities_with_empirical.sort_values(by='E_i_value')
    subset_E_i = probabilities_with_empirical_sorted[probabilities_with_empirical_sorted['E_i_value'] >= 4.0]
    insurance_from_E_i = insurance_table_for_E_i([5,10,20,30], subset_E_i, df_annual, value_field=eval_field)
    insurance_from_E_i = insurance_from_E_i.round({
        'closest r.p.': 1,
        eval_field: 1,
    })
#-----------------------------------------------------------------------------------------------------------------------------------
#----- SET DIRECTORIES 
#-----------------------------------------------------------------------------------------------------------------------------------
#----- THIS SETS A DIRECTORY THAT IS UNIQUE FOR AGGREGATION METHOD ----
#-----------------------------------------------------------------------------------------------------------------------------------
#----- <<< working just with the 'Cell Year' Return Period Process >>>-
    output_path = base_dir + '/notebooks/methods/Country_Results/' + country_name + f'/{method}/{return_period_type}/FAO tables/'
    ensure_directory_exists(output_path)
#-----------------------------------------------------------------------------------------------------------------------------------
    E_i_insurance_table_file_path = output_path + country_name + f'{return_period_type} insurance table.csv'
    print(f'saving insurance table to: {E_i_insurance_table_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
    event_year_probabilities_file_path = output_path + ' Event year probabilities.csv'
    print(f'saving main dataframe table to: {event_year_probabilities_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
#----- NOW WE WRITE TO THE FOLDERS. -----------------------------------
    insurance_from_E_i.to_csv(E_i_insurance_table_file_path)
    probabilities_with_empirical_sorted.to_csv(event_year_probabilities_file_path)

    return(conflict_profile, df_annual, annual_summary, insurance_from_E_i)

def smoothing_Event_Year_files(data, country_name, method, return_period_type):

    conflict_profile, df_annual_cleaned, annual_summary, insurance_table_df = smoothing_Country_Year_files(data, country_name)

    #This cell is exclusively working with E_i values (Return Period by Cell)
    cumulative_distribution = calculate_cumulative_distribution(df_annual_cleaned, 'perca_Mean')
    #calculate_probabilities(cumulative_distribution, data, id_column='percapita_100k'):
    probabilities = calculate_probabilities(cumulative_distribution, df_annual_cleaned, 'pg_id')
    #print(probabilities)
    probabilities['E_i'] = calculate_expected_time_periods(probabilities['P_i'])
    # Calculate E_i^voxels
    probabilities['E_i_voxels'] = calculate_expected_voxels(probabilities['p_i'])
    probabilities_renamed = probabilities.rename(columns={'value': 'perca_Mean'})
    print(probabilities_renamed.head(100))

    probabilities_with_empirical = compare_empirical_vs_expected(df_annual_cleaned, probabilities_renamed, time_column='year', value_column = 'perca_Mean')

    probabilities_with_empirical_sorted = probabilities_with_empirical.sort_values(by='E_i_value')
    subset_E_i = probabilities_with_empirical_sorted[probabilities_with_empirical_sorted['E_i_value'] >= 4.0]
    insurance_from_E_i = insurance_table_for_E_i( [5,10,20,30], subset_E_i, df_annual_cleaned, value_field='perca_Mean')
    insurance_from_E_i = insurance_from_E_i.round({
        'closest r.p.': 1,
        'perca_Mean': 1,
    })
#-----------------------------------------------------------------------------------------------------------------------------------
#----- SET DIRECTORIES 
#-----------------------------------------------------------------------------------------------------------------------------------
#----- THIS SETS A DIRECTORY THAT IS UNIQUE FOR AGGREGATION METHOD ----
#-----------------------------------------------------------------------------------------------------------------------------------
#----- <<< working just with the 'Cell Year' Return Period Process >>>-
    output_path = base_dir + '/notebooks/methods/Country_Results/' + country_name + f'/{method}/{return_period_type}/FAO tables/'
    ensure_directory_exists(output_path)
#-----------------------------------------------------------------------------------------------------------------------------------
    E_i_insurance_table_file_path = output_path + country_name + f'{return_period_type} insurance table.csv'
    print(f'saving insurance table to: {E_i_insurance_table_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
    event_year_probabilities_file_path = output_path + ' Event year probabilities.csv'
    print(f'saving main dataframe table to: {event_year_probabilities_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
#----- NOW WE WRITE TO THE FOLDERS. -----------------------------------
    insurance_from_E_i.to_csv(E_i_insurance_table_file_path)
    probabilities_with_empirical_sorted.to_csv(event_year_probabilities_file_path)

    return(conflict_profile, df_annual_cleaned, annual_summary, insurance_from_E_i)

def aggregation_Event_Year_files(data, country_name, method, aggregation_unit, eval_field):

    conflict_profile, aggregation_annual__country, annual_summary, insurance_table_df = aggregation_Country_Year_files(data, country_name, aggregation_unit, eval_field)

    #This cell is exclusively working with E_i values (Return Period by Cell)
    aggregation_annual__country_renamed = aggregation_annual__country.rename(columns={'GIS__Index': 'priogrid_gid'})
    cumulative_distribution = calculate_cumulative_distribution(aggregation_annual__country_renamed, eval_field)

    #calculate_probabilities(cumulative_distribution, data, id_column='percapita_100k'):
    probabilities = calculate_probabilities(cumulative_distribution, aggregation_annual__country_renamed, 'priogrid_gid')
    #print(probabilities)
    probabilities['E_i'] = calculate_expected_time_periods(probabilities['P_i'])
    # Calculate E_i^voxels
    probabilities['E_i_voxels'] = calculate_expected_voxels(probabilities['p_i'])
    probabilities_renamed = probabilities.rename(columns={'value': eval_field})
    print(probabilities_renamed.head(100))

    probabilities_with_empirical = compare_empirical_vs_expected(aggregation_annual__country_renamed, probabilities_renamed, time_column='year', value_column=eval_field)
    probabilities_with_empirical_sorted = probabilities_with_empirical.sort_values(by='E_i_value')
    subset_E_i = probabilities_with_empirical_sorted[probabilities_with_empirical_sorted['E_i_value'] >= 4.0]
    insurance_from_E_i = insurance_table_for_E_i([5,10,20,30], subset_E_i, aggregation_annual__country_renamed, value_field=eval_field)
    insurance_from_E_i = insurance_from_E_i.round({
        'closest r.p.': 1,
        eval_field: 1,
    })
    #-----------------------------------------------------------------------------------------------------------------------------------
#----- SET DIRECTORIES 
#-----------------------------------------------------------------------------------------------------------------------------------
#----- THIS SETS A DIRECTORY THAT IS UNIQUE FOR AGGREGATION METHOD ----
#-----------------------------------------------------------------------------------------------------------------------------------
#----- <<< working just with the 'Cell Year' Return Period Process >>>-
    output_path = base_dir + '/notebooks/methods/Country_Results/' + country_name + f'/{method}/Event year/FAO tables/'
    ensure_directory_exists(output_path)
#-----------------------------------------------------------------------------------------------------------------------------------
    E_i_insurance_table_file_path = output_path + country_name + 'Event year insurance table.csv'
    print(f'saving insurance table to: {E_i_insurance_table_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
    event_year_probabilities_file_path = output_path + country_name + ' Event year probabilities.csv'
    print(f'saving main dataframe table to: {event_year_probabilities_file_path}')
#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
#----- NOW WE WRITE TO THE FOLDERS. -----------------------------------
    insurance_from_E_i.to_csv(E_i_insurance_table_file_path)
    probabilities_with_empirical_sorted.to_csv(event_year_probabilities_file_path)

    return(conflict_profile, aggregation_annual__country_renamed, annual_summary, insurance_from_E_i)

def insurance_files(data, country_name, method, return_period_process, aggregation_unit='0', eval_field='percapita_100k'):
    if method == 'smoothing' and return_period_process == 'Event year':
        conflict_profile, df_annual_cleaned, annual_summary, insurance_from_E_i =  smoothing_Event_Year_files(data, country_name, method, return_period_process)
        return(conflict_profile, df_annual_cleaned, annual_summary, insurance_from_E_i)
    
    if method == 'aggregation' and return_period_process == 'Event year':
        conflict_profile, df_annual_cleaned, annual_summary, insurance_from_E_i = aggregation_Event_Year_files(data, country_name, method, aggregation_unit, eval_field)
        return(conflict_profile, df_annual_cleaned, annual_summary, insurance_from_E_i)

    if method == 'standard' and return_period_process == 'Event year':
        conflict_profile, df_annual_cleaned, annual_summary, insurance_from_E_i = standard_Event_Year_files(data, country_name, method, return_period_process, eval_field)
        return(conflict_profile, df_annual_cleaned, annual_summary, insurance_from_E_i)

    if method == 'smoothing' and return_period_process == 'Country year':
        conflict_profile, df_annual_cleaned, annual_summary, insurance_table_df = smoothing_Country_Year_files(data, country_name)
        return(conflict_profile, df_annual_cleaned, annual_summary, insurance_table_df)

    if method == 'aggregation' and return_period_process == 'Country year':
        conflict_profile, df_annual_cleaned, annual_summary, insurance_table_df = aggregation_Country_Year_files(data, country_name, aggregation_unit, eval_field)
        return(conflict_profile, df_annual_cleaned, annual_summary, insurance_table_df)
    
    if method == 'standard' and return_period_process == 'Country year':
        conflict_profile, df_annual_cleaned, annual_summary, insurance_table_df = standard_Country_Year_files(data, country_name, eval_field)
        return(conflict_profile, df_annual_cleaned, annual_summary, insurance_table_df)

