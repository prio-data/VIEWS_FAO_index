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


def plot_time_series(df, country_ids, feature, time_periods=None, figsize=(12, 8)):
    """
    Plots time series data for a given feature and multiple countries.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    country_ids (list): List of country IDs to filter the data.
    feature (str): The feature/column to plot.
    time_periods (list, optional): List of time periods to plot. Defaults to all periods.
    figsize (tuple, optional): Figure size for the plot. Defaults to (12, 8).

    Returns:
    None
    """

    # Check that df is a pandas DataFrame and that it is not empty
    if not isinstance(df, pd.DataFrame) or df.empty:
        raise ValueError('Input data is not a valid DataFrame or is empty.')
    
    # Check that data has the country ID column
    if 'c_id' not in df.columns:
        raise ValueError('Country ID column not found in the data. Please check the data.')

    # Ensure country_ids is a list
    if not isinstance(country_ids, list):
        raise ValueError('Country IDs should be provided as a list.')

    # Check that all country_ids are in the data
    missing_ids = [cid for cid in country_ids if cid not in df['c_id'].unique()]
    if missing_ids:
        raise ValueError(f'Country IDs not found in the data: {missing_ids}')

    # Check which time unit is used in the data by seeing if month_id or year_id is in the columns
    if 'month_id' in df.columns:
        time_period = 'month_id'
    elif 'year_id' in df.columns:
        time_period = 'year_id'
    else:
        raise ValueError('Time unit not found in the data. Please check the data.')

    plt.figure(figsize=figsize)
    sns.set(style="whitegrid")

    # Define a color palette
    palette = sns.color_palette("tab10", len(country_ids))
    markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h']

    # Plot each country's time series
    for idx, country_id in enumerate(country_ids):
        # Filter by country_id
        df_filtered = df[df['c_id'] == country_id]

        # Filter by time_periods if provided
        if time_periods is not None:
            df_filtered = df_filtered[df_filtered[time_period].isin(time_periods)]

        # Aggregate data by summing the feature over time periods
        df_aggregated = df_filtered.groupby(time_period)[feature].sum().reset_index()

        # Assert that the contry-time_period data hase been summed correctly (approximate equality)
        assert np.allclose(df_filtered[feature].sum(), df_aggregated[feature].sum(), rtol=1e-5), 'Data aggregation failed.'


        # Plotting
        plt.plot(df_aggregated[time_period], df_aggregated[feature], marker=markers[idx % len(markers)], linestyle='-', 
                 label=f'Country ID: {country_id}', color=palette[idx])

    plt.title(f'Time Series Plot for {feature}', fontsize=16)
    plt.xlabel('Time Period', fontsize=14)
    plt.ylabel(feature, fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='upper left', bbox_to_anchor=(0.85, 1), fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

     # If monthly time period, get all month ids and change them using the calculate_date_from_index function
    if time_period == 'month_id':
        # Calculate the dates from the month_id
        month_dates = [calculate_date_from_index(i) for i in df_aggregated[time_period]]
    
        # Check if they start with '01' and use these for the x-tick labels
        months_labels = [month_label if month_label[:2] == '01' else '' for month_label in month_dates]
    
        # Filter the positions for the x-ticks
        labeled_positions = [pos for pos, label in zip(df_aggregated[time_period], months_labels) if label]
    
        # Set the x-ticks and their labels
        plt.xticks(labeled_positions, [label for label in months_labels if label], rotation=45)

    # for year_id only have the full year on x-axis
    if time_period == 'year_id':
        plt.xticks(df_aggregated[time_period], [i for i in df_aggregated[time_period]], rotation=45)
        

    # now insert our logo under the legende - first check the path if 
    PATH_logo = get_logo_path(PATH) / "VIEWS_logo.png"

    #only plot if logo is available other wise just show the plot but print a warning
    if not Path(PATH_logo).is_file():

        print("Logo not found, please make sure the logo is available in the logos folder")

    else:

        # Load the image
        image = plt.imread(PATH_logo)

        # Create OffsetImage and AnnotationBbox
        imagebox = OffsetImage(image, zoom=0.3, alpha=0.7)
        ab = AnnotationBbox(imagebox, (0.8, 0.87), frameon=False, xycoords='axes fraction', zorder=3)

    # Add AnnotationBbox to the plot
    plt.gca().add_artist(ab)

    plt.tight_layout()
    plt.show()



def plot_feature_histograms(df, country_ids, feature, figsize=(16, 8)):
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
    num_cols = min(4, num_countries)
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

        # Create the histogram plot
        sns.histplot(sub_df, bins=50, kde=True, color=palette[idx], ax=axes[idx], alpha=0.6)

        # Add titles and labels
        axes[idx].set_title(f'Country ID: {country_id}', fontsize=14)
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



# 
# 
# def plot_time_series_data(df, time_ids, time_id_name, columns, figsize=(18, 25), cmap="rainbow", alpha=0.6, marker='.', s=6):
#     """
#     Plots a grid of scatter plots for specified time_ids and columns.
# 
#     Parameters:
#     - df: pandas DataFrame containing the data
#     - time_ids: list of time_ids to plot (e.g., months, years, weeks)
#     - time_id_name: name of the time_id column (e.g 'month_id', 'year_id', 'week_id')
#     - columns: list of columns to plot
#     - figsize: tuple specifying the figure size
#     - cmap: colormap for the scatter plots
#     - alpha: transparency level of the markers
#     - marker: marker style for the scatter plots
#     - s: size of the markers
#     """
#     
#     # Create a subplot grid
#     fig, axes = plt.subplots(nrows=len(columns), ncols=len(time_ids), figsize=figsize)
# 
#     # Iterate over the rows and columns to create each subplot
#     for i, col in enumerate(columns):
# 
#         # if the columns name includes "likelihood" we the reverse the colormap
#         if "likelihood" in col:
#             cmap_suffix = "_r"
# 
#         else:
#             cmap_suffix = ""
# 
#         for j, time_id in enumerate(time_ids):
#             ax = axes[i, j]
#             filtered_df = df[df[time_id_name] == time_id]
#             scatter = ax.scatter(filtered_df["col"], filtered_df["row"], c=filtered_df[col], cmap=f'{cmap}{cmap_suffix}', alpha=alpha, marker=marker, s=s)
#             
#             # Add a color bar if the value is a float
#             if filtered_df[col].dtype == "float64":
#                 cbar = plt.colorbar(scatter, ax=ax)
#                 cbar.set_label(col)
#             
#             # Add labels and title
#             ax.set_xlabel('Column')
#             ax.set_ylabel('Row')
#             ax.set_title(f'{col} for Time ID {time_id}')
#             
#             # Add grid
#             ax.grid(True, linestyle='--', alpha=0.5)
# 
#     # Adjust layout
#     plt.tight_layout()
# 
#     # Show the plot
#     plt.show()
# 

#def plot_random_monthly_and_yearly_data(df_monthly, df_yearly, feature, year=None, lock_first_month=False, edge_alpha=0.001, cmap_alpha=1, edge_color=None, edge_width=0.4, save_plot=False, title_fontsize=18, label_fontsize=16, tick_fontsize=16):
#    """
#    Plots random monthly and yearly data from the provided DataFrames.
#    """
#    # Select a specific year if provided, otherwise select a random year
#    selected_year = year if year is not None else np.random.choice(df_yearly['year_id'].unique())
#    if year is not None and year not in df_yearly['year_id'].unique():
#        raise ValueError(f"Year {year} is not available in the yearly data.")
#
#    # Select the first month if lock_first_month is True and year is provided, otherwise select a random month
#    selected_month = df_monthly[df_monthly['year_id'] == selected_year]['month_id'].min() if lock_first_month and year is not None else np.random.choice(df_monthly[df_monthly['year_id'] == selected_year]['month_id'].unique())
#
#    # Set the style
#    sns.set(style="whitegrid")
#
#    # Load country borders
#    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
#
#    # Size the plot
#    fig, axs = plt.subplots(1, 2, figsize=(22, 10))
#
#    # Set the color map
#    cmap = 'rainbow_r' if 'likelihood' in feature else 'rainbow'
#
#    # Plot monthly data
#    monthly_data = df_monthly[df_monthly['month_id'] == selected_month]
#    sc1 = axs[0].scatter(monthly_data['col'], monthly_data['row'], c=monthly_data[feature], cmap=cmap, marker='s', s=12, edgecolor=edge_color, linewidth=edge_width, alpha=cmap_alpha)
#    axs[0].scatter(monthly_data['col'], monthly_data['row'], facecolors='none', edgecolors=edge_color, s=12, linewidth=edge_width, alpha=edge_alpha)
#    axs[0].set_title(f'Monthly Data for Month {selected_month}', fontsize=title_fontsize)
#    fig.colorbar(sc1, ax=axs[0], orientation='vertical', label=feature)
#    
#    # no ticklabels but still the grid
#    axs[0].set_xticklabels([])
#    axs[0].set_yticklabels([])
#
#    # Plot yearly data
#    yearly_data = df_yearly[df_yearly['year_id'] == selected_year]
#    sc2 = axs[1].scatter(yearly_data['col'], yearly_data['row'], c=yearly_data[feature], cmap=cmap, marker='s', s=12, edgecolor=edge_color, linewidth=edge_width, alpha=cmap_alpha)
#    axs[1].scatter(yearly_data['col'], yearly_data['row'], facecolors='none', edgecolors=edge_color, s=12, linewidth=edge_width, alpha=edge_alpha)
#    axs[1].set_title(f'Yearly Data for Year {selected_year}', fontsize=title_fontsize)
#    fig.colorbar(sc2, ax=axs[1], orientation='vertical', label=feature)
#
#    # no ticklabels but still the grid
#    axs[1].set_xticklabels([])
#    axs[1].set_yticklabels([])
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
#
#    # Show the plot
#    plt.show()
#

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