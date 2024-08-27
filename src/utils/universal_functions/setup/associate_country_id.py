import pandas as pd

def associate_country_years(df,country):

    # """
    # 1. This gives us a dictionary connecting the country id for the inserted country (variable 2) with country start and end ranges. 
    # """
    # filtered__country = df.loc[(df['country_name']==country)]
    # filtered__country = filtered__country.rename(columns={'country_id':'c_id'})
    # country_and_year = filtered__country.groupby(['c_id', 'country_name', 'C_start_year', 'C_end_year']).size().to_frame().iloc[:, :-1].reset_index()
    # cids = list(pd.unique(country_and_year['c_id']))

    # length_of_cids = len(cids)
    # print(f'the length of country_ids for the selected country is: {length_of_cids}')
    # country_and_year_sorted=country_and_year.sort_values(by=['C_start_year'],ascending=False)

    # country_and_year_sorted['Year_range'] = list(zip(country_and_year_sorted["C_start_year"], country_and_year_sorted["C_end_year"]))
    # d = dict(zip(country_and_year_sorted['c_id'], country_and_year_sorted['Year_range']))


    # return(d)

    filtered__country = df.loc[(df['country_name']==country)]
    
    filtered__country = filtered__country.rename(columns={'country_id':'c_id'})
    country_and_year = filtered__country.groupby(['c_id', 'country_name', 'C_start_year', 'C_end_year']).size().to_frame().reset_index()


    # Step 1: Get the number of unique values in c_id
    unique_cid_count = country_and_year['c_id'].nunique()

    # Step 2: Sort the DataFrame by c_id and the last column (in descending order)
    df_sorted = country_and_year.sort_values(by=country_and_year.columns[-1], ascending=False)


    # Step 3: Subset the top 'unique_cid_count' rows per c_id based on the highest values in the last column
    result = df_sorted.head(unique_cid_count).reset_index(drop=True)
    print(result)


    cids = list(pd.unique(country_and_year['c_id']))

    length_of_cids = len(cids)
    print(f'the length of country_ids for the selected country is: {length_of_cids}')
    country_and_year_sorted=country_and_year.sort_values(by=['C_start_year'],ascending=False)

    result['Year_range'] = list(zip(result["C_start_year"], result["C_end_year"]))
    d = dict(zip(result['c_id'], result['Year_range']))

    return(d)

def pull_from_c_y_dictionary(country_year_dictionary):
    first_key = list(country_year_dictionary.keys())[0]
    return(first_key)