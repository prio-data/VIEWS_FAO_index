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

#Function for Event-Year Return Period process:
from src.utils.functions_for_single_cell_return_period.cell_return_period import calculate_cumulative_distribution, calculate_probabilities, calculate_expected_time_periods, calculate_expected_voxels, compare_empirical_vs_expected
from src.utils.functions_for_single_cell_return_period.Ei_insurance_table_setup import insurance_table_for_E_i

#Functions necessary for all methods:
from src.utils.universal_functions.setup.associate_country_id import associate_country_years, pull_from_c_y_dictionary
from src.utils.universal_functions.setup.build_directory import ensure_directory_exists

#Functions to generate the insurance table requested by FAO partners:
from src.utils.universal_functions.FAO_table_formatting.calculate_percentiles import format_stats, clean_percentile_table
from src.utils.universal_functions.FAO_table_formatting.generate_output_tables import insurance_table, annual_summary_table


def standard_Country_Year_files(data, country_name, attribute):

    country_and_year_dictionary = associate_country_years(data, country_name)
    print('printing he country and year dictionary:')
    print(country_and_year_dictionary)
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

    df_annual = native_per_capita_fatalities(subset_to_country)
    df_annual['percapita_100k'] = df_annual['percapita_100k'].round(1)

    percentile_df = format_stats(df_annual, field_to_describe=attribute)
    filtered_x = clean_percentile_table(percentile_df)
    insurance_table_df = insurance_table(filtered_x, df_annual, ['90','95','98','99','100'], attribute_to_explore=attribute) #uses the default attribute = percapita_100k and appened_1_value = yes
    annual_summary = annual_summary_table(df_annual, 'standard', fat_or_pcf=attribute)
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

def standard_Event_Year_files(data, country_name, method, return_period_type, attribute):

    conflict_profile, df_annual, annual_summary, insurance_table_df = standard_Country_Year_files(data, country_name, attribute)

    df_annual = df_annual.rename(columns={'GIS__Index': 'priogrid_gid'})
    cumulative_distribution = calculate_cumulative_distribution(df_annual, attribute)

    #calculate_probabilities(cumulative_distribution, data, id_column='percapita_100k'):
    probabilities = calculate_probabilities(cumulative_distribution, df_annual, 'pg_id')
    #print(probabilities)
    probabilities['E_i'] = calculate_expected_time_periods(probabilities['P_i'])
    # Calculate E_i^voxels
    probabilities['E_i_voxels'] = calculate_expected_voxels(probabilities['p_i'])
    probabilities_renamed = probabilities.rename(columns={'value': attribute})
    print(probabilities_renamed.head(100))

    probabilities_with_empirical = compare_empirical_vs_expected(df_annual, probabilities_renamed, value_column=attribute)
    probabilities_with_empirical_sorted = probabilities_with_empirical.sort_values(by='E_i_value')
    subset_E_i = probabilities_with_empirical_sorted[probabilities_with_empirical_sorted['E_i_value'] >= 4.0]
    insurance_from_E_i = insurance_table_for_E_i([5,10,20,30], subset_E_i, df_annual, value_field=attribute)
    insurance_from_E_i = insurance_from_E_i.round({
        'closest r.p.': 1,
        attribute: 1,
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
