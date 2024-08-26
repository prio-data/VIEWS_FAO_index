import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import seaborn as sns
#import geopandas as gpd
#import cartopy.crs as ccrs
#import cartopy.feature as cfeature

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths, setup_root_paths, get_logo_path
setup_project_paths(PATH)

from utils_date_index import calculate_date_from_index 
from utils_get_country_names_by_ids import get_country_names_by_ids
from utils_get_time_period import get_time_period


def plot_contry_period_map(df, country_id, feature, periods, figsize=(16, 8), marker_size=64, PATH=PATH):

    # Determine the number of rows and columns for subplots
    num_periods = len(periods)
    num_cols = min(3, num_periods)
    num_rows = (num_periods + num_cols - 1) // num_cols

    # check that wither month_id or year_id is in the columns
    if 'month_id' in df.columns:
        time_period = 'month_id'
        time_period_name = 'monthly'
    
    elif 'year_id' in df.columns:
        time_period = 'year_id'
        time_period_name = 'yearly'

    else:
        raise ValueError('Time unit not found in the data. Please check the data.')
    
    # adjust marker size
    base_marker_size = marker_size  # Base marker size
    num_unique_prio_grids_in_country = len(df[(df['c_id'] == country_id) & (df[time_period].isin(periods))]['pg_id'].unique())
    marker_size = ((base_marker_size / num_unique_prio_grids_in_country)*1000) / len(periods)**0.18  # Adjust marker size based on the number of periods
    
    # Set the figure size
    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    axes = axes.flatten()  # Flatten the axes array for easy iteration

    # Set the style
    sns.set(style="whitegrid")

    # Plot each country's histogram in a subplot
    for idx, periode in enumerate(periods):
        
        # Filter the data for the specified country and feature
        sub_df =  df[(df['c_id'] == country_id) & (df[time_period] == periode)][['row', 'col', feature, time_period]]

        # get the min and max values of the feature for that contry over all the periods
        unique_values = df[(df['c_id'] == country_id) & (df[time_period].isin(periods))][feature].unique()

        vmin = df[(df['c_id'] == country_id) & (df[time_period].isin(periods))][feature].min()
        vmax = df[(df['c_id'] == country_id) & (df[time_period].isin(periods))][feature].max()

        print(f"unique_values: {unique_values}")
        print(f"vmin: {vmin}, vmax: {vmax}")


        # is the data frame empty?
        if sub_df.empty:
            print(f"No data found for country {country_id}, {feature} and {time_period} {periode}")
            continue

        # create the scatter
            # if the feature name contains "likelihood", set the color map to 'viridis'
        cmap = 'rainbow_r' if 'likelihood' in feature else 'rainbow'

        # Plot monthly data
        sc1 = axes[idx].scatter(sub_df[sub_df[time_period] == periode]['col'], 
                        sub_df[sub_df[time_period] == periode]['row'], 
                        c=sub_df[sub_df[time_period] == periode][feature], 
                        cmap=cmap, marker='s', 
                        s=marker_size, edgecolor=None, linewidth=None, alpha=1, vmin= vmin, vmax= vmax)
    

        axes[idx].set_title(f'{time_period_name} Data for {periode}', fontsize=16)
        axes[idx].set_aspect('equal', 'box')

    cbar = fig.colorbar(sc1, ax=axes, orientation='horizontal', pad=0.2, aspect=50)
    cbar.set_label(feature)

    # Remove any unused subplots
    for j in range(idx + 1, len(axes)):
        fig.delaxes(axes[j])

    # country name:
    country_dict = get_country_names_by_ids([country_id])
    country_name = list(country_dict.values())[0]

    # Add a super title
    fig.suptitle(f'Map of {feature.replace("_", " ").title()} in country {country_name} (ID: {country_id}), ({time_period_name} data)', fontsize=16, y = 1)

    # Add a logo next to the super title if available
    PATH_logo = get_logo_path(PATH) / 'VIEWS_logo.png'
    
    if not PATH_logo.is_file():
        print("Logo not found, please make sure the logo is available in the logos folder")
    else:
        # Load the image
        image = plt.imread(PATH_logo)

        # Create OffsetImage and AnnotationBbox
        imagebox = OffsetImage(image, zoom=0.2, alpha=0.7)
        ab = AnnotationBbox(imagebox, (0.7, 0.82), frameon=False, xycoords='figure fraction', zorder=3)
        fig.add_artist(ab)

    # Adjust layout and show the plot
    #plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust rect to make space for the super title

    # Adjust layout to make space for the colorbar
    fig.subplots_adjust(bottom=0.35, top= 0.9, hspace=0.5, wspace=0.2)

    if save_plot:
        plt.savefig(f'{PATH}.png', dpi=300, bbox_inches='tight')

    plt.show()


