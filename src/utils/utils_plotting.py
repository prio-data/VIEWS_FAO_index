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



def plot_country_time_series(df, country_ids, feature, time_periods=None, figsize=(12, 8), PATH=PATH, logo_placement = (0.9, 0.85), legend_placement=(0.8, 1), force_color = None, save_plot = False, PATH_PLOT = None):

    print("WARINING: This function is deprecated, please use the function plot_country_time_series from the utils_plotting_country_time_series.py instead")
    print("E.i. from utils_plotting_country_time_series import plot_country_time_series")


def plot_feature_histograms(df, country_ids, feature, figsize=(16, 8), PATH=PATH):
    """
    Plots histograms of a specified feature for multiple countries in subplots.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    country_ids (list): List of country IDs to filter the data.
    feature (str): The feature/column to plot.
    logo_path (str): Path to the logo image file.
    figsize (tuple, optional): Figure size for the plot. Defaults to (16, 8).

    Returns:
    None
    """
    
    # Ensure country_ids is a list
    if not isinstance(country_ids, list):
        raise ValueError('Country IDs should be provided as a list.')

    # Determine the number of rows and columns for subplots
    num_countries = len(country_ids)
    num_cols = min(3, num_countries)
    num_rows = (num_countries + num_cols - 1) // num_cols

    # check that wither month_id or year_id is in the columns
    if 'month_id' in df.columns:
        time_period = 'monthly'
    
    elif 'year_id' in df.columns:
        time_period = 'yearly'

    else:
        raise ValueError('Time unit not found in the data. Please check the data.')

    # Set the figure size
    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    axes = axes.flatten()  # Flatten the axes array for easy iteration

    # Set the style
    sns.set(style="whitegrid")

    # Define a color palette
    palette = sns.color_palette("tab10", num_countries)

    # Plot each country's histogram in a subplot
    for idx, country_id in enumerate(country_ids):
        # Filter the data for the specified country and feature
        sub_df = df[df['c_id'] == country_id][feature]

        # Remove zero values
        sub_df = sub_df[sub_df != 0]

        # if the feature name contains "return_period", remove 1 values
        if 'return_period' in feature:
            sub_df = sub_df[sub_df != 1]

        # Create the histogram plot
        sns.histplot(sub_df, bins=50, kde=True, color=palette[idx], ax=axes[idx], alpha=0.6)

            # country name:
        country_dict = get_country_names_by_ids([country_id])
        country_name = list(country_dict.values())[0]

        # Add titles and labels
        axes[idx].set_title(f'Country: {country_name} (ID: {country_id})', fontsize=14)
        axes[idx].set_xlabel(feature.replace("_", " ").title(), fontsize=12)
        axes[idx].set_ylabel('Frequency', fontsize=12)

        # Customize the grid
        axes[idx].grid(True, linestyle='--', alpha=0.7)

    # Remove any unused subplots
    for j in range(idx + 1, len(axes)):
        fig.delaxes(axes[j])

    # Add a super title
    fig.suptitle(f'Histogram of {feature.replace("_", " ").title()} for Selected Countries ({time_period})', fontsize=16)

    # Add a logo next to the super title if available
    PATH_logo = get_logo_path(PATH) / 'VIEWS_logo.png'
    if not PATH_logo.is_file():
        print("Logo not found, please make sure the logo is available in the logos folder")
    else:
        # Load the image
        image = plt.imread(PATH_logo)

        # Create OffsetImage and AnnotationBbox
        imagebox = OffsetImage(image, zoom=0.3, alpha=0.7)
        ab = AnnotationBbox(imagebox, (0.95, 0.96), frameon=False, xycoords='figure fraction', zorder=3)
        fig.add_artist(ab)

    # Adjust layout and show the plot
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust rect to make space for the super title
    plt.show()


def plot_contry_period_map(df, country_id, feature, periods, figsize=(16, 8), marker_size=64, PATH=PATH):

    print("WARINING: This function is deprecated, please use the function plot_country_period_map from the utils_plotting_country_period_map.py instead")
    print("E.i. from utils_plotting_country_period_map import plot_country_period_map")



def plot_random_monthly_and_yearly_data(df_monthly, df_yearly, feature, year=None, lock_first_month=False, edge_alpha=0.001, cmap_alpha=1, edge_color=None, edge_width=0.4, save_plot=False, title_fontsize=18, label_fontsize=16, tick_fontsize=16):
    """
    Plots random monthly and yearly data from the provided DataFrames.

    Parameters:
    df_monthly (pd.DataFrame): DataFrame containing monthly data.
    df_yearly (pd.DataFrame): DataFrame containing yearly data.
    feature (str): The feature to be plotted.
    year (int, optional): The specific year to plot. Defaults to None, which selects a random year.
    lock_first_month (bool, optional): If True and year is provided, locks the month to the first month of the year. Defaults to False.
    edge_alpha (float, optional): Alpha value for the edge color of the markers. Defaults to 0.001.
    cmap_alpha (float, optional): Alpha value for the color map of the markers. Defaults to 1.
    edge_color (str, optional): Color of the edge of the markers. Defaults to 'gray'.
    edge_width (float, optional): Width of the edge of the markers. Defaults to 0.5.
    save_plot (bool, optional): If True, saves the plot to a file. Defaults to False.
    title_fontsize (int, optional): Font size for the plot titles. Defaults to 16.
    label_fontsize (int, optional): Font size for the axis labels. Defaults to 14.
    tick_fontsize (int, optional): Font size for the tick labels. Defaults to 12.
    """
    # Select a specific year if provided, otherwise select a random year
    if year is not None:
        if year not in df_yearly['year_id'].unique():
            raise ValueError(f"Year {year} is not available in the yearly data.")
        selected_year = year
    else:
        selected_year = np.random.choice(df_yearly['year_id'].unique())

    # Select the first month if lock_first_month is True and year is provided, otherwise select a random month
    if lock_first_month and year is not None:
        selected_month = df_monthly[df_monthly['year_id'] == selected_year]['month_id'].min()
    else:
        selected_month = np.random.choice(df_monthly[df_monthly['year_id'] == selected_year]['month_id'].unique())

    # Set the style
    sns.set(style="whitegrid")

    # Size the plot
    fig, axs = plt.subplots(1, 2, figsize=(22, 10))

    # if the feature name contains "likelihood", set the color map to 'viridis'
    cmap = 'rainbow_r' if 'likelihood' in feature else 'rainbow'

    # Plot monthly data
    sc1 = axs[0].scatter(df_monthly[df_monthly['month_id'] == selected_month]['col'], 
                         df_monthly[df_monthly['month_id'] == selected_month]['row'], 
                         c=df_monthly[df_monthly['month_id'] == selected_month][feature], cmap=cmap, marker='s', s=12, edgecolor=edge_color, linewidth=edge_width, alpha=cmap_alpha)
    
    axs[0].scatter(df_monthly[df_monthly['month_id'] == selected_month]['col'], 
                   df_monthly[df_monthly['month_id'] == selected_month]['row'], 
                   facecolors='none', edgecolors=edge_color, s=12, linewidth=edge_width, alpha=edge_alpha)
    
    axs[0].set_title(f'Monthly Data for Month {selected_month}', fontsize=title_fontsize)
    axs[0].set_aspect('equal', 'box')

    fig.colorbar(sc1, ax=axs[0], orientation='vertical', label=feature)

    # Plot yearly data
    sc2 = axs[1].scatter(df_yearly[df_yearly['year_id'] == selected_year]['col'], 
                         df_yearly[df_yearly['year_id'] == selected_year]['row'], 
                         c=df_yearly[df_yearly['year_id'] == selected_year][feature], cmap=cmap, marker='s', s=12, edgecolor=edge_color, linewidth=edge_width, alpha=cmap_alpha)
    
    axs[1].scatter(df_yearly[df_yearly['year_id'] == selected_year]['col'], 
                   df_yearly[df_yearly['year_id'] == selected_year]['row'], 
                   facecolors='none', edgecolors=edge_color, s=12, linewidth=edge_width, alpha=edge_alpha)
    
    axs[1].set_title(f'Yearly Data for Year {selected_year}', fontsize=title_fontsize)
    axs[1].set_aspect('equal', 'box')

    # remove the tick labels but keep the grid
    axs[0].set_xticklabels([])
    axs[0].set_yticklabels([])
    axs[1].set_xticklabels([])
    axs[1].set_yticklabels([])

    fig.colorbar(sc2, ax=axs[1], orientation='vertical', label=feature)

    # Add a super title
    plt.suptitle(f'{feature} for Month {selected_month} and Year {selected_year}', fontsize=title_fontsize)

    # Set font sizes for tick labels
    for ax in axs:
        ax.tick_params(axis='both', which='major', labelsize=tick_fontsize)

    # Improve layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Save the plot if save_plot is True
    if save_plot:
        PATH_ROOT = setup_root_paths(PATH)
        plt.savefig(f'{PATH_ROOT}/reports/plots/{feature}_month_{selected_month}_year_{selected_year}.png', dpi=300, bbox_inches='tight')

    # Show the plot
    plt.show()


