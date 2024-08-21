import numpy as np
import pandas as pd

import os
from pathlib import Path
import sys

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths
setup_project_paths(PATH)

from utils_get_time_period import get_time_period

def get_per_100k_features_country_wise_test(df, df_new, features , n_pop, time_period):

    print("Running tests for get_per_100k_features_country_wise - this may take a while (approx. 7-9 minutes)")

    for feature in features:

        exemple_c_ids = [47, 57, 237, 161, 50, 244, 162, 78, 120, 242, 235, 124, 158]

        for e_c_id in exemple_c_ids:

            # get the periods for the c_id
            all_periods = df_new[df_new['c_id'] == e_c_id][time_period].unique()

            for period in all_periods:

                exemple_pop = df[(df['c_id'] == e_c_id) & (df[time_period] == period)]['pop_gpw_sum'].sum()
                #print(sum_monthly_jan_2023_pop_bf)

                sum_monthly_jan_2023_fatalities_bf = df[(df['c_id'] == e_c_id) & (df[time_period] == period)][feature].sum()
                #print(sum_monthly_jan_2023_fatalities_bf)

                fatalities_per_100k_country = (sum_monthly_jan_2023_fatalities_bf / exemple_pop) * n_pop
                #print(fatalities_per_100k_country)


                exemple = df_new[(df_new['c_id'] == e_c_id) & (df_new[time_period] == period)][f'{feature}_per_100k_country'].unique()

                # check if there is any nans, inf or -inf in the exemple
                if np.isnan(exemple).any() or np.isinf(exemple).any() or np.isneginf(exemple).any():
                    raise ValueError(f"Error: {e_c_id} - {period} - There is a nan, inf or -inf in the exemple")

                # if there is no element in the list
                if len(exemple) == 0:
                    raise ValueError(f"Error: {e_c_id} - {period} - The list is empty")

                if exemple[0] != fatalities_per_100k_country:
                    raise ValueError(f"Error: {e_c_id} - {period} - The values are not equal (value test 1). Expected: {fatalities_per_100k_country}, Actual: {exemple[0]}")
                
                # reverse the calculation appoximately
                if not np.allclose((exemple[0] / n_pop) * exemple_pop, sum_monthly_jan_2023_fatalities_bf, rtol=1e-05, atol=1e-08):
                    raise ValueError(f"Error: {e_c_id} - {period} - The values are not equal (value test 2). Expected: {sum_monthly_jan_2023_fatalities_bf}, Actual: {(exemple[0] / n_pop) * exemple_pop}")


def get_per_100k_features_country_wise(df, features = ['total_best','sb_best', 'os_best', 'ns_best'], n_pop=100000, post_test = True):

    time_period = get_time_period(df)
    df_new = df.copy() # is this necessary?

    # Country, year, and month specific population normalization
    country_period_pop = df_new.groupby(['c_id', time_period])['pop_gpw_sum'].transform('sum')

    for feature in features:
        country_period_feature = df_new.groupby(['c_id', time_period])[feature].transform('sum')
        df_new[f"{feature}_per_100k_country"] = (country_period_feature / country_period_pop) * n_pop


    if post_test:
        # test the function'
        get_per_100k_features_country_wise_test(df, df_new, features, n_pop, time_period)

    return df_new