import pandas as pd

def represent_zero_percentiles(insert_percentile):
    
    float_percentile_at_1 = float(insert_percentile)
    
    if float_percentile_at_1 == 100:
        sub_perc = [100]
        #sub_perc.insert(0, float_percentile_at_1)
        return(sub_perc)
    
    if float_percentile_at_1 <= 99.9 and float_percentile_at_1 >= 99.5:
        sub_perc = [100]
        sub_perc.insert(0, float_percentile_at_1)
        return(sub_perc)

    #if float_percentile_at_1 < 99.7 and float_percentile_at_1 >= 99.5:
    #    sub_perc = [99.7, 99.9, 100]
    #    sub_perc.insert(0, float_percentile_at_1)
    #    return(sub_perc)

    elif float_percentile_at_1 < 99.5 and float_percentile_at_1 >= 99:
        sub_perc = [99.5, 99.9, 100]
        sub_perc.insert(0, float_percentile_at_1)
        return(sub_perc)

    elif float_percentile_at_1 < 99 and float_percentile_at_1 >= 98:
        sub_perc = [99, 99.5, 100]
        sub_perc.insert(0, float_percentile_at_1)
        return(sub_perc)

    elif float_percentile_at_1 < 98 and float_percentile_at_1 >= 95:
        sub_perc = [99, 99.5, 100]
        sub_perc.insert(0, float_percentile_at_1)
        return(sub_perc)

    elif float_percentile_at_1 < 95 and float_percentile_at_1 >= 90:
        sub_perc = [95, 99, 99.5, 100]
        sub_perc.insert(0, float_percentile_at_1)
        return(sub_perc)

    elif float_percentile_at_1 < 90 and float_percentile_at_1 >= 85:
        sub_perc = [90, 95, 99, 100]
        sub_perc.insert(0, float_percentile_at_1)
        return(sub_perc)

    elif float_percentile_at_1 < 85 and float_percentile_at_1 >= 80:
        sub_perc = [85, 90, 95, 99, 100]
        sub_perc.insert(0, float_percentile_at_1)
        return(sub_perc)

    elif float_percentile_at_1 < 80 and float_percentile_at_1 >= 70:
        sub_perc = [80, 85, 90, 95, 99, 100]
        sub_perc.insert(0, float_percentile_at_1)
        return(sub_perc)
    
    elif float_percentile_at_1 < 70 and float_percentile_at_1 >= 50:
        sub_perc = [70, 80, 85, 90, 95, 99, 100]
        sub_perc.insert(0, float_percentile_at_1)
        return(sub_perc)
    
    elif float_percentile_at_1 <50:
        sub_perc = [50, 75, 80, 85, 90, 95, 99, 100]
        sub_perc.insert(0, float_percentile_at_1)
        return(sub_perc)


def check_for_nonzero(check_this):
    return any(check_this != 0.0)

def correct_definition_df__v2(definition_dataframe,original_dataframe, list_of_unique_fatality_values, zero__or__nonzero,single_cell_analysis,PG__or__CM='PG',single_cell_analysis_percentiles=[99,95]):

    check_list = list(definition_dataframe)
    PCF_multiplier = 100000
#--------------------------------------------

#--------------------------------------------
#check first that there is some value other than 0 present otherwise stop the Pantaleon function and report this:

    list_of_unique_fatality_values__series = pd.Series(list_of_unique_fatality_values)

    check = check_for_nonzero(list_of_unique_fatality_values__series)

    if check == False:
        ohboy = 'There are no nonzero values'
        return(ohboy)

    # else:
    #     sort_list_with_nonzero_fatalities = list_of_unique_fatality_values__series.sort_values()
    #     retrieve_nonzero_value = next(value for value in sort_list_with_nonzero_fatalities if value != 0)

    #     #using the 'retrieve_nonzero_value' we need to know whether this value matches
    #         #any number within the 'definition_dataframe'. The reason it might not is because
    #         # for countries with very few fatalities or large but infrequent fatalities
    #         #the definition function will interpret values between the percentiles. Example:
    #         #if the first reported fatality total is 20 and this occured once along with just two other events 
    #         #in the countries history these values will beyond the accuracy of .1 which is being measured.

    #     #1 If retrieve_nonzero_value is exactly matched to a value in 'definition_dataframe':
    #     from_fatalities_interp = list(unique(definition_dataframe['Fatalities']))
    #     t_of_f = retrieve_nonzero_value in from_fatalities_interp
    #     if t_of_f == True:
    #         approved_retrieve_nonzero_value = retrieve_nonzero_value
    #         print('approved_retrieve_nonzero_value')
    #         print(approved_retrieve_nonzero_value)
    #     else:
    #         from_fatalities_interp.append(retrieve_nonzero_value)

    #         sort_from_fatalities_interp = sorted(from_fatalities_interp)
    #         target_index = sort_from_fatalities_interp.index(retrieve_nonzero_value)
    #         return_previous_val = sort_from_fatalities_interp[target_index -1]
    #         approved_retrieve_nonzero_value = return_previous_val
    #         print('approved_retrieve_nonzero_value')
    #         print(approved_retrieve_nonzero_value)

#----------------------------------------------------------------------------
    if 'Fatalities' in check_list:
        #attribute_nozero=original_dataframe[original_dataframe['Fatalities_Sum']!= 0]
        #return(Fatalities_nozero)

        if zero__or__nonzero == 'zero' and check == True:

            #----
            #Get the length of non-zero values from the 'list_of_unique_fatality_values' list:
            len_nonzero = [value for value in list_of_unique_fatality_values if value != 0]
            len_filtered = len(len_nonzero)
#Get length of the original (aggregated DF):
            len_df_ag = len(original_dataframe)

#If this result is greater than 99.9 it will create issues because the true first non-zero value 
    #will have been obscured (somewhere between 99.9xx and 100.0)
            Actual_P = (len_filtered / len_df_ag) * 100
            Percentage_Real_NonZero = 100 - Actual_P
#print(percentage)
            check_if_greater_than_99_9 = Percentage_Real_NonZero > 99.9000000000000000

            #----

            sort_list_with_nonzero_fatalities = list_of_unique_fatality_values__series.sort_values()
            retrieve_nonzero_value = next(value for value in sort_list_with_nonzero_fatalities if value != 0)
            print()
            print('the accepted retrieve_nonzero_value is....')
            print(retrieve_nonzero_value)
        #using the 'retrieve_nonzero_value' we need to know whether this value matches
            #any number within the 'definition_dataframe'. The reason it might not is because
            # for countries with very few fatalities or large but infrequent fatalities
            #the definition function will interpret values between the percentiles. Example:
            #if the first reported fatality total is 20 and this occured once along with just two other events 
            #in the countries history these values will beyond the accuracy of .1 which is being measured.

        #1 If retrieve_nonzero_value is exactly matched to a value in 'definition_dataframe':
            from_fatalities_interp = list(unique(definition_dataframe['Fatalities']))
            print('Here is a list of unique fatalities from the definition DF')
            print(from_fatalities_interp)
            t_of_f = retrieve_nonzero_value in from_fatalities_interp
            print(str(t_of_f) + 'The retrieve_nonzero_value is in the definition dataframe')

            if t_of_f == True:
                approved_retrieve_nonzero_value = retrieve_nonzero_value
                print('approved_retrieve_nonzero_value')
                print(approved_retrieve_nonzero_value)
                
            else:

                if check_if_greater_than_99_9 == True:
                    #change 99.9 Percentile value to equal the approved_retrieve_nonzero_value:
                    definition_dataframe.loc[definition_dataframe['Percentile'] == '99.9', 'Fatalities'] = retrieve_nonzero_value
                    approved_retrieve_nonzero_value = retrieve_nonzero_value

                else:
                    from_fatalities_interp.append(retrieve_nonzero_value)

                    sort_from_fatalities_interp = sorted(from_fatalities_interp)
                    target_index = sort_from_fatalities_interp.index(retrieve_nonzero_value)
                    return_previous_val = sort_from_fatalities_interp[target_index -1]
                    approved_retrieve_nonzero_value = return_previous_val
                    print('approved_retrieve_nonzero_value')
                    print(approved_retrieve_nonzero_value)

            definition_dataframe = definition_dataframe.reset_index()
                #if 1 not in definition_dataframe['Fatalities'].values:
                #      return(0)
            percentile_at_1 = list(definition_dataframe.loc[definition_dataframe['Fatalities'] == approved_retrieve_nonzero_value, 'Percentile'])[0]
            print('percentile_at_1')
            print(percentile_at_1)
            sub_perc=represent_zero_percentiles(percentile_at_1)
            print('sub_perc')
            print(sub_perc)
            search_P = list(map(str, sub_perc))
                #print(search_P)
            definition_dataframe['Percentile'] = definition_dataframe['Percentile'].astype('string')
            from_sub_perc = definition_dataframe[definition_dataframe['Percentile'].isin(search_P)]
                #sub_perc = ['84','90','95','99','99.5','100']
                #definition_dataframe['Percentile'] = definition_dataframe['Percentile'].astype('string')
                #from_sub_perc = definition_dataframe[definition_dataframe['Percentile'].isin(sub_perc)]
                #from_sub_perc = definition_dataframe[definition_dataframe['Percentile'] in sub_perc]
                #match_p = definition_dataframe.loc[definition_dataframe['Percentile'] == i]
            def_values = from_sub_perc['Percentile'].unique()
                #print(def_values)

        else:
            def_values = definition_dataframe['Percentile'].unique()
        id_fatality = []
        id_triggers = []
        id_p = []
            
    if 'Fatalities Per Capita' in check_list:
        def_values = definition_dataframe['Percentile'].unique()
        id_percapita = []
        id_triggers = []
        id_p = []

    collected = pd.DataFrame()

    if single_cell_analysis == 'Yes':
        def_values = single_cell_analysis_percentiles

    for i in def_values:
                            #if 'Fatalities' in check_list and i == 0.0:
                                #if i == 0.0:
                                #continue
                            #elif 'Fatalities' in check_list and i != 0.0:
                            if 'Fatalities' in check_list:

                                get_row = definition_dataframe.loc[definition_dataframe['Percentile'] == i]
                                fatality = get_row.at[get_row.index[0], 'Fatalities']
                                limit = original_dataframe.loc[original_dataframe['Fatalities_Sum'] >= fatality]
                                triggers = len(limit.index)
                                percentile = i

                                id_p.append(percentile)
                                id_fatality.append(fatality)
                                id_triggers.append(triggers)

                                Out_Percentile = pd.DataFrame(list(zip(id_p, id_fatality, id_triggers)),
                                    columns=['Percentile','Fatalities','Occurrence'])
                                
                            if 'Fatalities Per Capita' in check_list:
                                get_row = definition_dataframe.loc[definition_dataframe['Percentile'] == i]
                                fpc = get_row.at[get_row.index[0], 'Fatalities Per Capita']
                                limit = original_dataframe.loc[original_dataframe['PerCapitaFatalities'] >= fpc]
                                triggers = len(limit.index)
                                percentile = i                        

                                id_p.append(percentile)
                                id_percapita.append(fpc)
                                id_triggers.append(triggers)

                                Out_Percentile = pd.DataFrame(list(zip(id_p, id_percapita, id_triggers)),
                                    columns=['Percentile','Fatalities Per Capita','Occurrence'])
                            
    if zero__or__nonzero == 'zero' or single_cell_analysis == 'Yes':
           
        collected = pd.concat([collected, Out_Percentile], ignore_index=True) 
        return(collected)
    
    elif zero__or__nonzero == 'non-zero'and 'Fatalities Per Capita' in check_list:
        collected = pd.concat([collected, Out_Percentile], ignore_index=True) 
        collected['Fatalities Per Capita'] = collected['Fatalities Per Capita']*PCF_multiplier
        collected['Fatalities Per Capita'] = collected['Fatalities Per Capita'].round(1)
        collected = collected.rename(columns={'Fatalities Per Capita':'Per Capita'})
        Transpose_desc=collected.transpose()
        new_header = Transpose_desc.iloc[0] #grab the first row for the header
        Transpose_desc_less = Transpose_desc[1:] #take the data less the header row
        Transpose_desc_less.columns = new_header
        Transpose_desc_less = Transpose_desc_less.reset_index()
        Transpose_desc_less = Transpose_desc_less.rename(columns={'index':'Percentile'})

        return(Transpose_desc_less)

    elif zero__or__nonzero == 'non-zero' and 'Fatalities' in check_list:
        collected = pd.concat([collected, Out_Percentile], ignore_index=True) 
        Transpose_desc=collected.transpose()
        new_header = Transpose_desc.iloc[0] #grab the first row for the header
        Transpose_desc_less = Transpose_desc[1:] #take the data less the header row
        Transpose_desc_less.columns = new_header
        Transpose_desc_less = Transpose_desc_less.reset_index()
        Transpose_desc_less = Transpose_desc_less.rename(columns={'index':'Percentile'})

        return(Transpose_desc_less)

    #elif zero__or__nonzero != 'zero' or zero__or__nonzero != 'non-zero':
        #print('This parameter was incorrectly named. Select from zero or non-zero') 