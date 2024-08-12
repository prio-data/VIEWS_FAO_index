import numpy as np
import pandas as pd
def Format_summary_stats(PG_or_CM, table_to_describe,field_to_describe,zero__or__non_zero):
    
    if PG_or_CM == 'PG':
        lowpercentile = 0
    else:
        lowpercentile = 0

    p = np.array(np.arange(lowpercentile, 100.1, 0.1))
    divisor = 100
    p_div = p/divisor
    l = p_div.tolist()
    l_3dec = [round(elem, 3) for elem in l ]

    if field_to_describe == 'Fatalities_Sum':
        SummaryField = 'Fatalities'

    elif field_to_describe == 'PerCapitaFatalities':
        SummaryField = 'Fatalities Per Capita'

    if zero__or__non_zero == 'zero' and PG_or_CM == 'PG':
        #percentile = [.5,.7,.8,.85,.9,.95,.98,.99,.991,.992,.993,.994,.995,.996,.997,.998,.999,1]
        data = pd.DataFrame({SummaryField: table_to_describe[field_to_describe].describe(percentiles=l_3dec)})

    elif zero__or__non_zero == 'zero' and PG_or_CM == 'CM':
        #percentile = [.5,.7,.8,.81,.82,.83,.84,.85,.86,.87,.88,.89,.9,.95,.98,.99,.991,.992,.993,.994,.995,.996,.997,.998,.999,1]
        data = pd.DataFrame({SummaryField: table_to_describe[field_to_describe].describe(percentiles=l_3dec)})

    elif zero__or__non_zero == 'non-zero':
        check_length_nonzero = len(table_to_describe[table_to_describe[field_to_describe]>0.0])
        if check_length_nonzero == 0:
            return(0, 0, 0)
        attribute_nozero=table_to_describe[table_to_describe[field_to_describe]!= 0]
        length_of_attribute_nozero = len(attribute_nozero)
        percentile = [0,.25,.5,.75,.8,.85,.9,.95,.99,.995,1]
        data = pd.DataFrame({SummaryField: attribute_nozero[field_to_describe].describe(percentiles=percentile)})

    #data = pd.DataFrame({SummaryField: table_to_describe[field_to_describe].describe(percentiles=percentile)})
    data = data.reset_index()
    data = data.rename(columns={'index':'Percentile'})
    data = data.iloc[4:][:-1]
    data['Percentile'] = data['Percentile'].str[:-1]

    if field_to_describe == 'Fatalities_Sum' and zero__or__non_zero == 'non-zero':
        data['Fatalities'] = (data['Fatalities']).astype(int)
        #attribute_nozero=table_to_describe[table_to_describe['Fatalities_Sum']!= 0]
        return(attribute_nozero, data, length_of_attribute_nozero)

    elif field_to_describe == 'Fatalities_Sum' and zero__or__non_zero == 'zero':
        data['Fatalities'] = (data['Fatalities']).astype(int)
        return(data)

    elif field_to_describe == 'PerCapitaFatalities' and zero__or__non_zero == 'non-zero':
        #attribute_nozero=table_to_describe[table_to_describe['PerCapitaFatalities']!= 0]
        return(attribute_nozero, data, length_of_attribute_nozero)
    


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