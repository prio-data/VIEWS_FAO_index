import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
#import cartopy.crs as ccrs
#import cartopy.feature as cfeature

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("VIEWS_FAO_index")+1]]) / "src/utils"))  

from set_paths import setup_project_paths, setup_root_paths
setup_project_paths(PATH)

def plot_time_series_data(df, time_ids, time_id_name, columns, figsize=(18, 25), cmap="rainbow", alpha=0.6, marker='.', s=6):
    """
    Plots a grid of scatter plots for specified time_ids and columns.

    Parameters:
    - df: pandas DataFrame containing the data
    - time_ids: list of time_ids to plot (e.g., months, years, weeks)
    - time_id_name: name of the time_id column (e.g 'month_id', 'year_id', 'week_id')
    - columns: list of columns to plot
    - figsize: tuple specifying the figure size
    - cmap: colormap for the scatter plots
    - alpha: transparency level of the markers
    - marker: marker style for the scatter plots
    - s: size of the markers
    """
    
    # Create a subplot grid
    fig, axes = plt.subplots(nrows=len(columns), ncols=len(time_ids), figsize=figsize)

    # Iterate over the rows and columns to create each subplot
    for i, col in enumerate(columns):

        # if the columns name includes "likelihood" we the reverse the colormap
        if "likelihood" in col:
            cmap_suffix = "_r"

        else:
            cmap_suffix = ""

        for j, time_id in enumerate(time_ids):
            ax = axes[i, j]
            filtered_df = df[df[time_id_name] == time_id]
            scatter = ax.scatter(filtered_df["col"], filtered_df["row"], c=filtered_df[col], cmap=f'{cmap}{cmap_suffix}', alpha=alpha, marker=marker, s=s)
            
            # Add a color bar if the value is a float
            if filtered_df[col].dtype == "float64":
                cbar = plt.colorbar(scatter, ax=ax)
                cbar.set_label(col)
            
            # Add labels and title
            ax.set_xlabel('Column')
            ax.set_ylabel('Row')
            ax.set_title(f'{col} for Time ID {time_id}')
            
            # Add grid
            ax.grid(True, linestyle='--', alpha=0.5)

    # Adjust layout
    plt.tight_layout()

    # Show the plot
    plt.show()


def plot_random_monthly_and_yearly_data(df_monthly, df_yearly, feature, year=None, lock_first_month=False, edge_alpha=0.001, cmap_alpha=1, edge_color=None, edge_width=0.4, save_plot=False, title_fontsize=18, label_fontsize=16, tick_fontsize=16):
    """
    Plots random monthly and yearly data from the provided DataFrames.
    """
    # Select a specific year if provided, otherwise select a random year
    selected_year = year if year is not None else np.random.choice(df_yearly['year_id'].unique())
    if year is not None and year not in df_yearly['year_id'].unique():
        raise ValueError(f"Year {year} is not available in the yearly data.")

    # Select the first month if lock_first_month is True and year is provided, otherwise select a random month
    selected_month = df_monthly[df_monthly['year_id'] == selected_year]['month_id'].min() if lock_first_month and year is not None else np.random.choice(df_monthly[df_monthly['year_id'] == selected_year]['month_id'].unique())

    # Set the style
    sns.set(style="whitegrid")

    # Load country borders
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Size the plot
    fig, axs = plt.subplots(1, 2, figsize=(22, 10))

    # Set the color map
    cmap = 'rainbow_r' if 'likelihood' in feature else 'rainbow'

    # Plot monthly data
    monthly_data = df_monthly[df_monthly['month_id'] == selected_month]
    sc1 = axs[0].scatter(monthly_data['col'], monthly_data['row'], c=monthly_data[feature], cmap=cmap, marker='s', s=12, edgecolor=edge_color, linewidth=edge_width, alpha=cmap_alpha)
    axs[0].scatter(monthly_data['col'], monthly_data['row'], facecolors='none', edgecolors=edge_color, s=12, linewidth=edge_width, alpha=edge_alpha)
    axs[0].set_title(f'Monthly Data for Month {selected_month}', fontsize=title_fontsize)
    fig.colorbar(sc1, ax=axs[0], orientation='vertical', label=feature)
    
    # no ticklabels but still the grid
    axs[0].set_xticklabels([])
    axs[0].set_yticklabels([])

    # Plot yearly data
    yearly_data = df_yearly[df_yearly['year_id'] == selected_year]
    sc2 = axs[1].scatter(yearly_data['col'], yearly_data['row'], c=yearly_data[feature], cmap=cmap, marker='s', s=12, edgecolor=edge_color, linewidth=edge_width, alpha=cmap_alpha)
    axs[1].scatter(yearly_data['col'], yearly_data['row'], facecolors='none', edgecolors=edge_color, s=12, linewidth=edge_width, alpha=edge_alpha)
    axs[1].set_title(f'Yearly Data for Year {selected_year}', fontsize=title_fontsize)
    fig.colorbar(sc2, ax=axs[1], orientation='vertical', label=feature)

    # no ticklabels but still the grid
    axs[1].set_xticklabels([])
    axs[1].set_yticklabels([])

    # Add a super title
    plt.suptitle(f'{feature} for Month {selected_month} and Year {selected_year}', fontsize=title_fontsize)

    # Set font sizes for tick labels
    for ax in axs:
        ax.tick_params(axis='both', which='major', labelsize=tick_fontsize)

    # Improve layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Save the plot if save_plot is True
    if save_plot:
        plt.savefig(f'{feature}_month_{selected_month}_year_{selected_year}.png', dpi=300, bbox_inches='tight')

    # Show the plot
    plt.show()
#
#def plot_random_monthly_and_yearly_data(df_monthly, df_yearly, feature, year=None, lock_first_month=False, edge_alpha=0.001, cmap_alpha=1, edge_color='k', edge_width=0.4, save_plot=False, title_fontsize=18, label_fontsize=16, tick_fontsize=16):
#    """
#    Plots random monthly and yearly data from the provided DataFrames.
#
#    Parameters:
#    df_monthly (pd.DataFrame): DataFrame containing monthly data.
#    df_yearly (pd.DataFrame): DataFrame containing yearly data.
#    feature (str): The feature to be plotted.
#    year (int, optional): The specific year to plot. Defaults to None, which selects a random year.
#    lock_first_month (bool, optional): If True and year is provided, locks the month to the first month of the year. Defaults to False.
#    edge_alpha (float, optional): Alpha value for the edge color of the markers. Defaults to 0.001.
#    cmap_alpha (float, optional): Alpha value for the color map of the markers. Defaults to 1.
#    edge_color (str, optional): Color of the edge of the markers. Defaults to 'gray'.
#    edge_width (float, optional): Width of the edge of the markers. Defaults to 0.5.
#    save_plot (bool, optional): If True, saves the plot to a file. Defaults to False.
#    title_fontsize (int, optional): Font size for the plot titles. Defaults to 16.
#    label_fontsize (int, optional): Font size for the axis labels. Defaults to 14.
#    tick_fontsize (int, optional): Font size for the tick labels. Defaults to 12.
#    """
#    # Select a specific year if provided, otherwise select a random year
#    if year is not None:
#        if year not in df_yearly['year_id'].unique():
#            raise ValueError(f"Year {year} is not available in the yearly data.")
#        selected_year = year
#    else:
#        selected_year = np.random.choice(df_yearly['year_id'].unique())
#
#    # Select the first month if lock_first_month is True and year is provided, otherwise select a random month
#    if lock_first_month and year is not None:
#        selected_month = df_monthly[df_monthly['year_id'] == selected_year]['month_id'].min()
#    else:
#        selected_month = np.random.choice(df_monthly[df_monthly['year_id'] == selected_year]['month_id'].unique())
#
#    # Set the style
#    sns.set(style="whitegrid")
#
#    # Size the plot
#    fig, axs = plt.subplots(1, 2, figsize=(22, 10))
#
#    # if the feature name contains "likelihood", set the color map to 'viridis'
#    cmap = 'rainbow_r' if 'likelihood' in feature else 'rainbow'
#
#    # Plot monthly data
#    sc1 = axs[0].scatter(df_monthly[df_monthly['month_id'] == selected_month]['col'], 
#                         df_monthly[df_monthly['month_id'] == selected_month]['row'], 
#                         c=df_monthly[df_monthly['month_id'] == selected_month][feature], cmap=cmap, marker='o', s=12, edgecolor=edge_color, linewidth=edge_width, alpha=cmap_alpha)
#    
#    axs[0].scatter(df_monthly[df_monthly['month_id'] == selected_month]['col'], 
#                   df_monthly[df_monthly['month_id'] == selected_month]['row'], 
#                   facecolors='none', edgecolors=edge_color, s=12, linewidth=edge_width, alpha=edge_alpha)
#    
#    axs[0].set_title(f'Monthly Data for Month {selected_month}', fontsize=title_fontsize)
#    axs[0].set_aspect('equal', 'box')
#
#    fig.colorbar(sc1, ax=axs[0], orientation='vertical', label=feature)
#
#    # Plot yearly data
#    sc2 = axs[1].scatter(df_yearly[df_yearly['year_id'] == selected_year]['col'], 
#                         df_yearly[df_yearly['year_id'] == selected_year]['row'], 
#                         c=df_yearly[df_yearly['year_id'] == selected_year][feature], cmap=cmap, marker='o', s=12, edgecolor=edge_color, linewidth=edge_width, alpha=cmap_alpha)
#    
#    axs[1].scatter(df_yearly[df_yearly['year_id'] == selected_year]['col'], 
#                   df_yearly[df_yearly['year_id'] == selected_year]['row'], 
#                   facecolors='none', edgecolors=edge_color, s=12, linewidth=edge_width, alpha=edge_alpha)
#    
#    axs[1].set_title(f'Yearly Data for Year {selected_year}', fontsize=title_fontsize)
#    axs[1].set_aspect('equal', 'box')
#
#    fig.colorbar(sc2, ax=axs[1], orientation='vertical', label=feature)
#
#    # Add a super title
#    plt.suptitle(f'{feature} for Month {selected_month} and Year {selected_year}', fontsize=title_fontsize)
#
#    # Set font sizes for tick labels
#    for ax in axs:
#        ax.tick_params(axis='both', which='major', labelsize=tick_fontsize)
#
#    # Improve layout
#    plt.tight_layout(rect=[0, 0, 1, 0.95])
#
#    # Save the plot if save_plot is True
#    if save_plot:
#        PATH_ROOT = setup_root_paths(PATH)
#        plt.savefig(f'{PATH_ROOT}/reports/plots/{feature}_month_{selected_month}_year_{selected_year}.png', dpi=300, bbox_inches='tight')
#
#    # Show the plot
#    plt.show()
#
#def plot_random_monthly_and_yearly_data(df_monthly, df_yearly, feature, year=None, lock_first_month=False, save_plot=False):
#    """
#    Plots random monthly and yearly data from the provided DataFrames.
#
#    Parameters:
#    df_monthly (pd.DataFrame): DataFrame containing monthly data.
#    df_yearly (pd.DataFrame): DataFrame containing yearly data.
#    feature (str): The feature to be plotted.
#    year (int, optional): The specific year to plot. Defaults to None, which selects a random year.
#    lock_first_month (bool, optional): If True and year is provided, locks the month to the first month of the year. Defaults to False.
#    """
#    # Select a specific year if provided, otherwise select a random year
#    if year is not None:
#        if year not in df_yearly['year_id'].unique():
#            raise ValueError(f"Year {year} is not available in the yearly data.")
#        selected_year = year
#    else:
#        selected_year = np.random.choice(df_yearly['year_id'].unique())
#
#    # Select the first month if lock_first_month is True and year is provided, otherwise select a random month
#    if lock_first_month and year is not None:
#        selected_month = df_monthly[df_monthly['year_id'] == selected_year]['month_id'].min()
#    else:
#        selected_month = np.random.choice(df_monthly[df_monthly['year_id'] == selected_year]['month_id'].unique())
#
#    # Size the plot
#    fig, axs = plt.subplots(1, 2, figsize=(20, 7))
#
#    # if the feature name contains "likelihood", set the color map to 'rainbow_r'
#    suffix = '' if 'likelihood' not in feature else '_r'
#
#    # Plot monthly data
#    sc1 = axs[0].scatter(df_monthly[df_monthly['month_id'] == selected_month]['col'], 
#                         df_monthly[df_monthly['month_id'] == selected_month]['row'], 
#                         c=df_monthly[df_monthly['month_id'] == selected_month][feature], cmap=f'rainbow{suffix}', marker='.', s=10)
#    axs[0].set_title(f'Monthly Data for Month {selected_month}')
#    axs[0].set_xlabel('Column')
#    axs[0].set_ylabel('Row')
#    fig.colorbar(sc1, ax=axs[0], orientation='vertical', label=feature)
#
#    # Plot yearly data
#    sc2 = axs[1].scatter(df_yearly[df_yearly['year_id'] == selected_year]['col'], 
#                         df_yearly[df_yearly['year_id'] == selected_year]['row'], 
#                         c=df_yearly[df_yearly['year_id'] == selected_year][feature], cmap=f'rainbow{suffix}', marker='.', s=10)
#    axs[1].set_title(f'Yearly Data for Year {selected_year}')
#    axs[1].set_xlabel('Column')
#    axs[1].set_ylabel('Row')
#    fig.colorbar(sc2, ax=axs[1], orientation='vertical', label=feature)
#
#    # a super title
#    plt.suptitle(f'{feature} for Month {selected_month} and Year {selected_year}')
#
#    # Save the plot if save_plot is True
#    if save_plot:
#        PATH_ROOT = setup_root_paths(PATH)
#        plt.savefig(f'{PATH_ROOT}reports/plots/{feature}_month_{selected_month}_year_{selected_year}.png') # use path lib insted... 
#
#    # Show the plot
#    plt.show()