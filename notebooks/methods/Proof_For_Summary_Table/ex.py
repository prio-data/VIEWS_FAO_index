population_sum = x[(x['year'] == 2020) & 
                               (x[value_field] >= 31.0) & 
                               (x[value_field] < 100000)]['pop_gpw_sum'].sum()
print(population_sum)

info_df_to_save = info_df.drop('Color', axis=1)


#Example dataset ()
x_year = x[x['year'] == 2020]


x_20yr_events = x_year[(x_year['fatalities_sum'] >= 1.0) & 
                (x_year['fatalities_sum'] < 8.0)]


display(x_20yr_events)

