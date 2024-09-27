import pandas as pd
import re

def append_return_periods_to_annual_table(x, y, z, filtered_info, value_field, population_field):
    # Calculate the total population for percentage calculation

    # Initialize the results dictionary for storing year, label, count, population sum, and percentage
    results = {
        'year': [], 
        'Label': [], 
        'count': [], 
        'pop sum': [], 
        'pop prop': []
    }

    # Loop over each unique year in the dataset 'x'
    for year in x['year'].unique():
        for _, row in filtered_info.iterrows():
            range_start, range_end = map(float, row['Range'].split(' - '))
            label = row['Label']

            #subset by year and sum by population so pop sum is specific to that year
            total_population = x[(x['year'] == year)][population_field].sum()

            # Count occurrences within the range for the current year
            count = x[(x['year'] == year) & 
                      (x[value_field] >= range_start) & 
                      (x[value_field] < range_end)].shape[0]

            # Sum the population within the range for the current year
            population_sum = x[(x['year'] == year) & 
                               (x[value_field] >= range_start) & 
                               (x[value_field] < range_end)][population_field].sum()

            # Calculate the population percentage relative to the total population
            pop_perc = population_sum / total_population

            # Append the year, label, count, population sum, and percentage to the results dictionary
            results['year'].append(year)
            results['Label'].append(label)
            results['count'].append(count)
            results['pop sum'].append(population_sum)
            results['pop prop'].append(pop_perc)

    # Convert the results to a DataFrame
    results_df = pd.DataFrame(results)

    # Pivot the DataFrame to get counts and population sums for each 'Return Period'
    pivoted_df = results_df.pivot_table(index='year', columns='Label', values=['count', 'pop sum', 'pop prop'], fill_value=0)

    # Reset the index to make 'year' a column, and flatten the column MultiIndex
    pivoted_df.columns = ['_'.join(col).strip() for col in pivoted_df.columns.values]
    pivoted_df = pivoted_df.reset_index()

    # Reformat the annual summary table to only contain the max event and average event
    annual_summary_df = y.drop(columns=['second_value', 'third_value'])

    # Merge the count of Return Period events with the annual summary table on the field 'year'
    merged_annual_summary = pd.merge(annual_summary_df, pivoted_df, on='year')

    # Check to make sure none of the columns refer to 'Below X Return Period'
    columns_to_drop = merged_annual_summary.filter(like='Below', axis=1).columns

    # Drop the identified columns
    merged_annual_summary = merged_annual_summary.drop(columns=columns_to_drop)

    fixed_order = ['year', 'first_value', 'average_value']
    
    #incorporating the population weigthed columns in order to define a total payout value----------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------------------------
            
    #Right now there is no PAYOUT SCHEME defined for the big p return period so this calculation can only be developed for little p (Country year)
    if return_period == 'Country year':
        return_period_to_payout_rate = dict(zip(z['Return Period'], z['Payout Rate']))

    if return_period == 'Event year':
        return_period_to_payout_rate = dict.fromkeys(z['return period'], '100%')

    filtered_dict = {
            int(k) if k != '--' and '.' in str(k) and float(k).is_integer() else k: v.rstrip('%')
            for k, v in return_period_to_payout_rate.items()
            if 'undefined' not in str(k) and '--' not in str(k) and 'undefined' not in str(v) and '--' not in str(v)
        }

    transformed_dict = {
            str(k): int(v) for k, v in filtered_dict.items()
        }

    for key, value in transformed_dict.items():
            column_name = f'pop prop_1 in {key} year'
            new_column_name = f'pay weight {key}'
        
            # Check if the column exists in the DataFrame
            if column_name in merged_annual_summary.columns:
                merged_annual_summary[new_column_name] = merged_annual_summary[column_name] * value

    merged_annual_summary['payout rate (%)'] = merged_annual_summary.filter(like='pay weight').sum(axis=1)
    merged_annual_summary['Total Payout'] = (merged_annual_summary['payout rate (%)'] * .01) * 1000000

#Drop the '1 in <year> year' in field names:----------------------------------------------------------------------------------------------------------

    merged_annual_summary.columns = merged_annual_summary.columns.str.replace(r'1 in (\d+) year', r'\1', regex=True)

#Re organize the field structure:---------------------------------------------------------------------------------------------------------------------
    columns = list(merged_annual_summary.columns)
    # Extract columns that contain "in " followed by a number
    numeric_columns = [col for col in columns if re.search(r'\d+', col)]
    print(numeric_columns)
    # Sort the numeric columns by the number that comes after "in "
    sorted_numeric_columns = sorted(numeric_columns, key=lambda x: int(re.search(r'\d+', x).group(0)), reverse=True)
    print(sorted_numeric_columns)

    # Combine the fixed columns with the sorted numeric columns
    new_column_order = fixed_order + sorted_numeric_columns

    # Reorder the DataFrame columns based on the new order
    merged_annual_summary = merged_annual_summary[new_column_order]

        # Initialize a new column with zeros to accumulate the weighted sum
    merged_annual_summary['weight_rp'] = 0

#restrict columns to only the fields that are counting the number of occurrences for each conflict return period:
    count_columns = [col for col in sorted_numeric_columns if 'count' in col]

        # Loop through each column in sorted_numeric_columns_dropbottom
    for col in count_columns:
            # Extract the numerical part of the column name (assumes the pattern '1 in X year')
            numeric_value = int(re.search(r'count_(\d+)', col).group(1))
            
            # Multiply the entire column by the extracted numeric value and accumulate the result
            merged_annual_summary['weight_rp'] += merged_annual_summary[col] * numeric_value

    merged_annual_summary['payout rate (%)'] = merged_annual_summary.filter(like='pay weight').sum(axis=1)
    merged_annual_summary['Total Payout'] = (merged_annual_summary['payout rate (%)'] * .01) * 1000000

    return merged_annual_summary