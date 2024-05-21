from support_functions.setup_general import PGM_preprocess
from support_functions.setup_aggregation import PRIO_Agg_serious
from support_functions.fatality_statistics_reformat import correct_definition_df__v2
from support_functions.fatality_statistics_generate import Format_summary_stats

from support_functions.statsheet_input import params_for_graphs, format_for_summarytextline
from support_functions.statsheet_format import statsheet_v3

import numpy as np

def Empowered_Pantaleon(PG_or_CM, d_pg, d_cm, monthly_or_annual, resolution=0, country=0, recent_or_all=0):

    pg__or__cm = PG_or_CM
    res = resolution
    cntry = country
    m_or_a = monthly_or_annual
    
    if PG_or_CM == 'PG':
        #df_pg = queryset_base_PG.publish().fetch()
    #Reset index in order to access 'month_id' and 'priogrid_gid' columns
        #d_pg = d_pg.reset_index()
        df_109_516 = d_pg.loc[(d_pg['month_id']>=109) & (d_pg['month_id']<= 516)]

    else:
        #df_cm = queryset_base_CM.publish().fetch()
        #d_cm = d_cm.reset_index()
        df_109_516 = d_cm.loc[(d_cm['month_id']>=109) & (d_cm['month_id']<= 516)]

    df__PP=PGM_preprocess(df_109_516)
    df_ag, gis=PRIO_Agg_serious(df__PP, monthly_or_annual,pg__or__cm, res, cntry, recent_or_all)

    #total_events = report_length(df_ag, PG_or_CM,'Global', monthly_or_annual,res)
    #print(total_events)
    list_of_fatality_values__ = list(unique(df_ag['Fatalities_Sum']))

    format_fatalities_zero=Format_summary_stats(PG_or_CM,df_ag,'Fatalities_Sum','zero')
    #print(format_fatalities_zero.dtypes)

    described_fatalities_zero = correct_definition_df__v2(format_fatalities_zero,df_ag,list_of_fatality_values__,'zero','No',pg__or__cm)
    if type(described_fatalities_zero) == str:
        return(described_fatalities_zero,described_fatalities_zero)
    fatalities_nonzero, described_fatalities_nonzero,len_fat = Format_summary_stats(PG_or_CM,df_ag,'Fatalities_Sum','non-zero')
    Fatalities_nonzero_cordef = correct_definition_df__v2(described_fatalities_nonzero, fatalities_nonzero, list_of_fatality_values__, 'non-zero','No')
    #print(len_fat)
    
    pcf_nonzero, described_pcf_nonzero, len_fpc = Format_summary_stats(PG_or_CM,df_ag,'PerCapitaFatalities','non-zero')
    pcf_nonzero_cordef = correct_definition_df__v2(described_pcf_nonzero, pcf_nonzero,list_of_fatality_values__, 'non-zero','No')
    
    #print(len_fpc)
    a, b, c, d=params_for_graphs(Fatalities_nonzero_cordef,fatalities_nonzero,85,95,99.5)

    #print('type of A:')
    a_dic = a[0]
    a_cdf = a[1]
    b_dic = b[0]
    b_cdf = b[1]
    c_dic = c[0]
    c_cdf = c[1]
    d_dic = d[0]
    d_cdf = d[1]
    #def statsheet(zerotable, nonzerotable_Fatality, nonzerotable_fpc, hist1, cdf1, hist2, cdf2, hist3, cdf3, hist4, cdf4, timeline, PG_or_CM, month_or_annual, country=0, resolution=0):    
    
    txt = format_for_summarytextline(pg__or__cm,df_ag,described_fatalities_zero,Fatalities_nonzero_cordef,pcf_nonzero_cordef,m_or_a,res, cntry)
    x = statsheet_v3(described_fatalities_zero, txt, Fatalities_nonzero_cordef, pcf_nonzero_cordef, a_dic, a_cdf, b_dic, b_cdf, c_dic, c_cdf, d_dic, d_cdf, fatalities_nonzero, pg__or__cm, m_or_a, cntry, res)    
    return(x,gis)
    #return(described_fatalities_zero, Fatalities_nonzero_cordef, pcf_nonzero_cordef, a_dic, a_cdf, b_dic, b_cdf, c_dic, c_cdf, d_dic, d_cdf, fatalities_nonzero,)
