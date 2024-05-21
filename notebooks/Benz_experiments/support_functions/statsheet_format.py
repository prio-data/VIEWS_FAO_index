import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
from notebooks.Benz_experiments.support_functions.statsheet_input import single_hist_params, timeline_x_axes_params


#import matplotlib. image as image

compare_countries = os.getcwd() + '/Country_Comparisons/'

def annotate_axes(ax, text, fontsize=18):
        ax.text(0.5, 0.5, text, transform=ax.transAxes,
                ha="center", va="center", fontsize=fontsize, color="darkgrey")

    #def statsheet(zerotable, nonzerotable_Fatality, nonzerotable_fpc, hist1, cdf1, hist2, cdf2, hist3, cdf3, hist4, cdf4, timeseries):    
def statsheet_v3(zerotable, textsummary, nonzerotable_Fatality, nonzerotable_fpc, hist1, cdf1, hist2, cdf2, hist3, cdf3, hist4, cdf4, timeline, PG_or_CM, month_or_annual, country=0, resolution=0):    


    comb_nz_Fatality__nz_PCF = pd.concat([nonzerotable_Fatality, nonzerotable_fpc], axis=0)

    #nonzerotable_fpc['Fatalities Per Capita'] = nonzerotable_fpc['Fatalities Per Capita']*10000
    #nonzerotable_fpc['Fatalities Per Capita'] = nonzerotable_fpc['Fatalities Per Capita'].round(1)
    Unit_of_analysis = PG_or_CM
    mora = month_or_annual 
    r = resolution
    c = country
    if resolution != 0:
        res = resolution
    else:
        res = ''

    if country != 0:
        cntry = country
    else:
         cntry = 'Global'
    
    Title = cntry +' ' + mora + ' ' + res + ' ' + Unit_of_analysis + ' ' + 'Stat Sheet'

    #if resolution != 0:

    #For timeline--------------------------v
    timeline_month_fatalitytotal = timeline.groupby(["month_id"]).Fatalities_Sum.sum().reset_index().reset_index()

    timeline_month_fatalities20000 = timeline_month_fatalitytotal.loc[timeline_month_fatalitytotal['Fatalities_Sum']>20000]

    index_to_color = timeline_month_fatalities20000['index']
    #--------------------------------------^

    units_of_analysis = '13000'
    percent_zero_fromtable = '99.3%'
    percent_nonzero_fromtable ='.6%'
    total_nonzero_fromtable = '1300'
    inf_total = '7'
    MissingData1 ='Y# occurances of 2 or less# fatalities and Y# occurances of 3-5 fatalities.'
    MissingData2 = 'Y# counts of fatalities between n and n'
    MissingData3 = 'XXXXXXX# fatalities were recorded between XX and XX of XXXX, XXXXXX in XX-XX, XXXXXXXX# in XX-XX, and XXXXX# in XX-XX'
    #inputtext = 'In this text I want to summarize:\nalso, the per capita row reflects 1/10,000 individuals 1. The definition of event in this iteration 2.The total number of Events.\n Including how many months and the month ranges. Describe the graphs \n why do the total fatalities not match the total PCF (becuse 7 events in area with no population\n This is the last line that you have room for!'
    #inputtext = f'Defining an event, summarizing fatalities, as a 1x1 standard PRIO Grid across a monthly temporal resolution produced {units_of_analysis} units of analysis. Summary tables\n discriminate between events reflecting zero and non-zero fatality results. At the employed unit scale, zero fatalities account for {percent_zero_fromtable} of all events. The remaining\n tables and graphics are constituent to that remaining {percent_nonzero_fromtable} ({total_nonzero_fromtable}) fatalities. Non-zero results from the Per Capita table reflect a unique total from the reported fatalities,\n {inf_total} events contained fatalities in units with no expected population values. Several graphics host data that is not completely visualized with extreme values exceeding\n the Y-axis; These locations are indicated by a prominent red bar. The following relationships uncover the obscured information. 1st-85th Percentile: There were\n {MissingData1} ; 99.5-100th Percentile: {MissingData2}'
    inputtext = 'This is incomplete for now but statistics are generated to insert in next push...'
    fig = plt.figure(figsize=(11, 8.5), constrained_layout = True)
    spec = fig.add_gridspec(7, 4)

#Zero table
    ax0 = fig.add_subplot(spec[0:3, :-3])

    # exaggerate_x = 3
    # exaggerate_y = 2
    #ax0.set_facecolor((0.9, 0.9, 1.0))
    #rect = patches.Rectangle((-0.5, 0), 2, 1, transform=ax0.transFigure, color='#D3D3D3', alpha=0.5)
    #rect.set_width(1.75)

    #rect.set_width(rect.get_width() * exaggerate_x)   # Scaling factor for x-direction
    #rect.set_height(rect.get_height() * exaggerate_y)  # Scaling factor for y-direction

    #ax0.add_patch(rect)
    len_of_zero_df = len(zerotable)
    if len_of_zero_df >= 8:
        exaggerate = 1.5
    elif len_of_zero_df >= 6:
        exaggerate = 1.85
    elif len_of_zero_df < 6:
        exaggerate = 2.25

    #annotate_axes(ax0, 'ax0')
    table_ax0 = ax0.table(cellText=zerotable.values,
                    colLabels=zerotable.columns,
                    loc='center',
                    cellLoc='center',
                    rowLoc='center',
                    )
    
    FirstFatality = table_ax0[1,0]
    FirstFatality.set_edgecolor('#e34a33')
    FirstFatality.set_linewidth(2)

    ax0.add_patch(FirstFatality)
    table_ax0.auto_set_font_size(False)  # Turn off automatic font size adjustment


    firstline = 0
    for col_index in range(len(zerotable.columns)):
        table_ax0[firstline, col_index].set_text_props(color='white', weight='bold')
        table_ax0.set_fontsize(0.05) 
        table_ax0[firstline, col_index].set_facecolor('#36454F')  # Use any valid color code or name

    fontprops = fm.FontProperties(weight='bold')
    for i, cell in enumerate(table_ax0.get_children()):
        if i % len(zerotable.columns) == 0:  # Check if it's the first column
            cell.set_text_props(fontproperties=fontprops)
            #table_ax0.set_fontsize(3.5) 

    table_ax0.set_fontsize(7)
    ax0.axis('off')
    table_ax0.scale(1.35, exaggerate)

    ax0.set_title('Distribution of Fatalities\nAll zero and non-zero events', size=10)

# Summary Text
    
    #summarytext = summarytextline (Unit_of_analysis, total_events, perc_nonzero, total_nonzero, fpc_99th_nz, fpc_99th_nz_occurance, mora, r, c)

    ax1 = fig.add_subplot(spec[0, -3:])
    #annotate_axes(ax1, 'ax1')
    ax1.text(0, 0.5,textsummary, fontsize=8, va='top',wrap='True',
                      bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'))
    ax1.axis('off')
    ax1.set_title(Title, size=14, fontweight="bold")

    #ax1.margins(x=-.25)
    #text_ax1.scale(-.25, 1)

#plt.text(5, 5, input_text, fontsize=10, style='oblique', ha='center', va='top', wrap=True, rotation=-30)

#Non-Zero Fatalities
    ax2 = fig.add_subplot(spec[1:3, -3:])
    #annotate_axes(ax1, 'ax1')
    table_ax2 = ax2.table(cellText=comb_nz_Fatality__nz_PCF.values,
                     colLabels=comb_nz_Fatality__nz_PCF.columns,
                     loc='center',
                     cellLoc='center',
                     rowLoc='center')

    charcoal_row = 0
    for col_index in range(len(comb_nz_Fatality__nz_PCF.columns)):
        table_ax2[charcoal_row, col_index].set_facecolor('#36454F')  # Use any valid color code or name

    bold_titleline = 0
    for col_index in range(len(comb_nz_Fatality__nz_PCF.columns)):
        table_ax2[bold_titleline, col_index].set_text_props(color='white', weight='bold')

    lightgrey_row = 3
    for col_index in range(len(comb_nz_Fatality__nz_PCF.columns)):
        table_ax2[lightgrey_row, col_index].set_facecolor('#F2F2F2')

    lightgrey_row2 = 4
    for col_index in range(len(comb_nz_Fatality__nz_PCF.columns)):
        table_ax2[lightgrey_row2, col_index].set_facecolor('#F2F2F2')

    #-----FF4B4B
    fatality_cell_colors = {(1, 1): ('#ECF4FF'),  # Red for cell in row 0, column 0
                            (1, 2): ('#ECF4FF'),  # Red for cell in row 1, column 1
                            (1, 3): ('#ECF4FF'),  # Red for cell in row 2, column 2
                            (1, 4): ('#ECF4FF'),  # Red for cell in row 2, column 2
                            (1, 5): ('#ECF4FF'),  # Red for cell in row 2, column 2
                            #(1, 6): ('#ECF4FF'),  # Red for cell in row 2, column 2
                            (2, 1): ('#ECF4FF'),  # Red for cell in row 1, column 1
                            (2, 2): ('#ECF4FF'),  # Red for cell in row 1, column 1
                            (2, 3): ('#ECF4FF'),  # Red for cell in row 2, column 2
                            (2, 4): ('#ECF4FF'),  # Red for cell in row 2, column 2
                            (2, 5): ('#ECF4FF'),  # Red for cell in row 2, column 2
                            #(2, 6): ('#ECF4FF'),  # Red for cell in row 2, column 2
                            (1, 6): ('#FFD2D2'),  # Red for cell in row 2, column 2
                            (1, 7): ('#FFD2D2'),  # Red for cell in row 2, column 2
                            (2, 6): ('#FFD2D2'),  # Red for cell in row 2, column 2
                            (2, 7): ('#FFD2D2'),  # Red for cell in row 2, column 2
                            (1, 8): ('#FF7878'),  # Red for cell in row 2, column 2
                            (1, 9): ('#FF7878'),  # Red for cell in row 2, column 2
                            (2, 8): ('#FF7878'),  # Red for cell in row 2, column 2
                            (2, 9): ('#FF7878'),  # Red for cell in row 2, column 2
                            (1, 10): ('#FF3434'),  # Red for cell in row 2, column 2
                            (1, 11): ('#FF3434'),  # Red for cell in row 2, column 2
                            (2, 10): ('#FF3434'),  # Red for cell in row 2, column 2
                            (2, 11): ('#FF3434')}  # Red for cell in row 2, column 2
                            
    for (row, col), color in fatality_cell_colors.items():
         table_ax2[row, col].set_facecolor(color)

# Change the background color of the second row (index 1)
    #table_ax2[0, 0:9].set_facecolor('#FFFF00')  # Use any valid color code or name

    
    # FPC_99_val = table_ax2[1,9]
    # FPC_99_val.set_edgecolor('#e34a33')
    # FPC_99_val.set_linewidth(2.5)

    # FPC_99_occ = table_ax2[2,9]
    # FPC_99_occ.set_edgecolor('#e34a33')
    # FPC_99_occ.set_linewidth(2.5)

    # ax2.add_patch(FPC_99_val)
    # ax2.add_patch(FPC_99_occ)

    table_ax2.auto_set_font_size(False)
    table_ax2.set_fontsize(6)
    ax2.axis('off')
    table_ax2.scale(1.0, 1.45)

#Non-Zero Fatalities
    # ax3 = fig.add_subplot(spec[2, -3:])

    # cellcolours_array = [[ '#ffffff', '#fef0d9', '#fef0d9', '#fef0d9', '#fef0d9', '#fef0d9','#fef0d9', '#fdcc8a', '#fdcc8a', '#fc8d59', '#fc8d59', '#e34a33'],
    #                     ['#ffffff', '#fef0d9', '#fef0d9', '#fef0d9', '#fef0d9', '#fef0d9', '#fef0d9', '#fdcc8a', '#fdcc8a', '#fc8d59', '#fc8d59', '#e34a33']]

    # table_ax3 = ax3.table(cellText=nonzerotable_Fatality.values,
    #                 colLabels=nonzerotable_Fatality.columns,
    #                 cellColours=cellcolours_array,
    #                 loc='upper center',
    #                 cellLoc='center',
    #                 rowLoc='center')
    # table_ax3.auto_set_font_size(False)
    # table_ax3.set_fontsize(6)
    # ax3.axis('off')
    # table_ax3.scale(1, 1.45)

    #ax4_set_ylim_max,ax4_set_xlim_max,ax4_set_xticks = ax4_params(res)
    ax4xlim_max, ax4xlim_min, ax4x_int_list, ax4x_tick_labels, ax4ylim_max, ax4ylim_min, ax4y_int_list, ax4y_tick_labels = single_hist_params (hist1)
    #Histogram 1-85
    ax4 = fig.add_subplot(spec[3, -2])
    #annotate_axes(ax4, 'ax4')
    ax4.hist(hist1, bins=100, color='black')
    ax4.set_title("1-85th Percentile")
    #for i in range(0,10):
    #    patches_ax4[i].set_facecolor('red')
    #ax4.set_xlabel("Fatalities")
    ax4.set_ylabel("Frequency", fontsize = 7)

    ax4.set_ylim(ax4ylim_min, ax4ylim_max)
    ax4.set_yticks(ticks=ax4y_int_list, labels=ax4y_tick_labels)

    ax4.set_xlim(ax4xlim_min, ax4xlim_max)
    ax4.set_xticks(ticks=ax4x_int_list, labels=ax4x_tick_labels)

    #ax4.set_yticks((0,500,1000,1500,2000))
    #ax4.set_yticks(ticks=[0,500,1000,1500,2000],labels=['0',' ','1000','','2000'])

    #for label in ax4.xaxis.get_ticklabels()[::2]:
    #    label.set_visible(False)
    ax4.tick_params(axis='x', labelsize=6.5)
    ax4.tick_params(axis='y', labelsize=6.5)
    ax4.set_facecolor('#ECF4FF')

    
    #ax6_set_xticks, ax6_set_xticks_labels, ax6_set_yticks, ax6_set_yticks_labels = ax6_params(res)
    ax6xlim_max, ax6xlim_min, ax6x_int_list, ax6x_tick_labels, ax6ylim_max, ax6ylim_min, ax6y_int_list, ax6y_tick_labels = single_hist_params(hist2)

    #Histogram 85-95
    ax6 = fig.add_subplot(spec[3, -1])
    #annotate_axes(ax6, 'ax6')
    ax6.hist(hist2, bins=100, color='black')
    ax6.set_title("85-95th Percentile")
    #ax6.tick_params(axis='x', labelcolor='white')

    ax6.set_xlim(ax6xlim_min, ax6xlim_max)
    ax6.set_xticks(ticks=ax6x_int_list, labels=ax6x_tick_labels)
    #for label in ax6.xaxis.get_ticklabels()[::2]:
    #    label.set_visible(False)
    ax6.set_ylim(ax6ylim_min, ax6ylim_max)
    ax6.set_yticks(ticks=ax6y_int_list,labels=ax6y_tick_labels)
    ax6.tick_params(axis='x', labelsize=6.5)
    ax6.tick_params(axis='y', labelsize=6.5)

    ax6.set_facecolor('#FFD2D2')

    #CDF 85-95


    #ax8_set_xticks, ax8_set_xticks_labels, ax8_set_yticks, ax8_set_yticks_labels = ax8_params(res)
    ax8xlim_max, ax8xlim_min, ax8x_int_list, ax8x_tick_labels, ax8ylim_max, ax8ylim_min, ax8y_int_list, ax8y_tick_labels = single_hist_params(hist3)

    #Histogram 95-99.5
    ax8 = fig.add_subplot(spec[4, -2])
    #annotate_axes(ax8, 'ax8')
    ax8.hist(hist3, bins=100, color='black')
    ax8.set_title("95-99.5 Percentile")
    #ax8.tick_params(axis='x', labelcolor='white')
    
    ax8.set_xlim(ax8xlim_min, ax8xlim_max)
    ax8.set_xticks(ticks=ax8x_int_list, labels=ax8x_tick_labels)

    ax8.set_ylim(ax8ylim_min, ax8ylim_max)
    ax8.set_yticks(ticks=ax8y_int_list,labels=ax8y_tick_labels)
    ax8.set_ylabel("Frequency", fontsize = 7)

    ax8.set_xlabel("Fatalities", fontsize = 7)
    ax8.tick_params(axis='x', labelsize=6.5)
    ax8.tick_params(axis='y', labelsize=6.5)

    ax8.set_facecolor('#FF7878')



    #ax10_set_xticks, ax10_set_xticks_labels, ax10_set_yticks, ax10_set_yticks_labels, ylim = ax10_params(res)
    ax10xlim_max, ax10xlim_min, ax10x_int_list, ax10x_tick_labels, ax10ylim_max, ax10ylim_min, ax10y_int_list, ax10y_tick_labels = single_hist_params(hist4)

    #Histogram 99.5-100
    ax10 = fig.add_subplot(spec[4, -1])
    #annotate_axes(ax10, 'ax10')
    N, bins, patches_ax10=ax10.hist(hist4, bins=100, color='black')
    ax10.set_title("99.5-100th Percentile")
    #ax10.tick_params(axis='x', labelcolor='white')
    
    ax10.set_ylim(ax10ylim_min, ax10ylim_max)
    ax10.set_yticks(ticks=ax10y_int_list,labels=ax10y_tick_labels)

    ax10.set_xticks(ticks=ax10x_int_list, labels=ax10x_tick_labels)
    ax10.set_xlabel("Fatalities", fontsize=7)  # Adjust the fontsize as needed

    ax10.tick_params(axis='x', labelsize=6.5)
    ax10.tick_params(axis='y', labelsize=6.5)


    #for i in range(0,2):
    #    patches_ax10[i].set_edgecolor('white')
    #    patches_ax10[i].set_facecolor('red')

    #for label in ax10.xaxis.get_ticklabels()[::1]:
    #    label.set_visible(False)
    ax10.set_facecolor('#FF3434')

#Read the image from file into an array of binary format
#READ FILE TO COMPARE CURRENT COUNTRY TO ALL COUNTRIES:

    # PG_CM__ = 'PG'
    # Scale = resolution
    All_country_REPORT = pd.read_csv(compare_countries + PG_or_CM +'_'+ resolution + '.csv')
    All_country_REPORT__onlyhasvalues = All_country_REPORT[All_country_REPORT['Percentile_of_1'] != 9999.0]
    All_country_REPORT__onlyhasvalues = All_country_REPORT[All_country_REPORT['Fatality_95_Percentile'] != 9999.0]
    All_country_REPORT__onlyhasvalues['Percentile_of_1'] = 100 - All_country_REPORT['Percentile_of_1']

    #----Select country--------
    if country != 0:
        highlight_country = country
        highlight_row = All_country_REPORT__onlyhasvalues[All_country_REPORT__onlyhasvalues['Country'] == highlight_country]
        highlight_Percentile_of_1 = highlight_row['Percentile_of_1'].values[0]
        highlight_Fatality_95_Percentile = highlight_row['Fatality_95_Percentile'].values[0]
    #----Select country--------


    # fig, ax = plt.subplots()
    ax11 = fig.add_subplot(spec[3:5, 0:2])

    ax11.set_title('Global Per Capita Fatality (PCF) Country Metrics')
    if PG_or_CM == 'PG':
        ax11.set_xlabel('PCF (100,000) Associated With the '+ PG_or_CM + '(' +resolution + ')' +' 95th Percentile', fontsize = 7)
    else:
        ax11.set_xlabel('PCF (100,000) Associated With the '+ PG_or_CM +' 95th Percentile', fontsize = 7)

    ax11.set_ylabel('Percentage of Events With at Least 1 Fatality', fontsize = 7)
    # plt.axvline(x=250, color='black', ls='--', lw=1,)
    # plt.vlines(x=500, ymin=0, ymax=100, colors='black', ls='--', lw=.75)
    # plt.vlines(x=1000, ymin=0, ymax=100, colors='black', ls='--', lw=.25)

    # plt.hlines(y=50, xmin=0, xmax=6000, colors='black', ls='--', lw=1)
    # plt.hlines(y=75, xmin=0, xmax=6000, colors='black', ls='--', lw=.25)

    ax11.scatter(All_country_REPORT__onlyhasvalues['Fatality_95_Percentile'], All_country_REPORT__onlyhasvalues['Percentile_of_1'], marker='.', s=50, alpha=.25, color='red')
    if country != 0:
        ax11.scatter(highlight_Fatality_95_Percentile, highlight_Percentile_of_1, marker='*', color='black', label=highlight_country)

    # file = (os.getcwd()+"/Map_Input_for_Statsheet/PRIO_logo_2010.png")
    # prio_logo = image. imread (file)
    #print (prio_logo. shape); print (prio_logo)

    #ax11.imshow(prio_logo)

    if country == 0:
        ax12lim_max = 17500
        ax12y_int_list = [0,1000,5000, 7500, 10000, 1250, 15000, 17500]
        ax12y_tick_labels = ['0','1000','5000', '', '10000','', '15000', '17500']
    
    else:
        ax12lim_max = 2000
        ax12y_int_list = [0, 100, 150, 200, 250, 500, 750, 1000, 1250, 1500, 2000]
        ax12y_tick_labels = ['0','100', '', '', '250', '500', '', '1000', '', '1500', '2000']

    x12_tick, x12_label = timeline_x_axes_params(109,517)

    normalize = plt.Normalize(min(timeline_month_fatalitytotal['Fatalities_Sum']), max(timeline_month_fatalitytotal['Fatalities_Sum']))
    colors = [(0.8, 0.8, .8), (1, 0, 0)]  # Blue to Red
    cmap = LinearSegmentedColormap.from_list('custom_colormap', colors)

    ax12 = fig.add_subplot(spec[5:, :])
    #annotate_axes(ax12, 'ax12')
    bars=ax12.bar(timeline_month_fatalitytotal['month_id'],timeline_month_fatalitytotal['Fatalities_Sum'], 
        color=cmap(normalize(timeline_month_fatalitytotal['Fatalities_Sum'])),
        align='center') # A bar chart
    ax12.set_xlabel('Month')
    ax12.set_ylabel('Total Fatalities', fontsize = 8)
    ax12.set_ylim(0, ax12lim_max)
    ax12.set_yticks(ticks=ax12y_int_list,labels=ax12y_tick_labels)
    ax12.set_xticks(ticks=x12_tick,labels=x12_label)
    ax12.tick_params(axis='x', labelsize=7)
    ax12.tick_params(axis='y', labelsize=7)  # Adjust the labelsize parameter

    for col in index_to_color:
        # That's it!
        bars[col].set_color('white')

    fig.align_ylabels()
    plt.show()

    #fig.tight_layout()
    return()
