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

def plot_country_time_series_precheck(df, country_ids):

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


def place_logo(logo_placement, logo_size, PATH):

    """
    Places a logo on a given axis in a plot.

    Parameters:
    ax (matplotlib.axes.Axes): The axis on which to place the logo.
    logo_placement (tuple): Coordinates for logo placement in the axis, specified as a fraction of the axis size (e.g., (0.9, 0.85)).
    logo_size (float): The size of the logo, specified as a zoom factor.
    PATH (str): Path to the directory containing the logo.

    Raises:
    FileNotFoundError: If the logo file is not found in the specified PATH.

    Returns:
    None
    """

    # now insert our logo under the legende - first check the path if 
    PATH_logo = get_logo_path(PATH) / "VIEWS_logo.png"

    #only plot if logo is available other wise just show the plot but print a warning
    if not Path(PATH_logo).is_file():

        print("Logo not found, please make sure the logo is available in the logos folder")

    else:

        # Load the image
        image = plt.imread(PATH_logo)

        # Create OffsetImage and AnnotationBbox
        imagebox = OffsetImage(image, zoom=logo_size, alpha=0.7)
        ab = AnnotationBbox(imagebox, logo_placement, frameon=False, xycoords='axes fraction', zorder=3)

    # Add AnnotationBbox to the plot
    plt.gca().add_artist(ab)


def plot_country_time_series(df, country_ids, feature, time_periods=None, manual_title = None, manual_ylabel = None, figsize=(12, 8), PATH=PATH, logo_placement = (0.9, 0.85), logo_size = 0.6, legend_placement=(0.8, 1), force_color = None, save_plot = False, PATH_PLOT = None):
    """
    Plots time series data for a given feature and multiple countries.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    country_ids (list): List of country IDs to filter the data.
    feature (str): The feature/column to plot.
    time_periods (list, optional): List of time periods to plot. Defaults to all periods.
    manual_title (str, optional): Manual title for the plot. Defaults to None in which case the title is generated automatically.
    figsize (tuple, optional): Figure size for the plot. Defaults to (12, 8).

    Returns:
    None
    """
    # This is a pre-test ----------------------------------------------------------------------
    plot_country_time_series_precheck(df, country_ids)

    time_period = get_time_period(df)

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

        # if the feature contains per_100k_pop, average the feature
        if 'per_100k' in feature:
            if not '_country' in feature:
                print(f"This plot aggregates data by either averaging or summing the country-specific feature (in this case {feature}) over the given time period (in this case {time_period}).")
                print(f"For features normalized per 100k population, ensure you use the country-specific version of the feature to get accurate data in the plot.")
                print(f"Summing or averaging the pg (PRIO grid) level feature '{feature}' (e.i. the one without '_country' in the name) will not give accurate results in this plot.")
                print(f"Feature '{feature}' should end with '_country' to ensure correct plotting. If this feature is not in your data,, please download the data again.")
                return

            else:
                df_aggregated = df_aggregated = df_filtered.groupby(time_period)[feature].mean().reset_index()

                # Assert that the contry-time_period data hase been averaged correctly (approximate equality)
                assert np.allclose(df_filtered[feature].mean(), df_aggregated[feature].mean(), rtol=1e-5), 'Data aggregation failed.'

        # Aggregate data by summing the feature over time periods
        else:
            df_aggregated = df_filtered.groupby(time_period)[feature].sum().reset_index()

            # Assert that the contry-time_period data hase been summed correctly (approximate equality)
            assert np.allclose(df_filtered[feature].sum(), df_aggregated[feature].sum(), rtol=1e-5), 'Data aggregation failed.'

        # country name:
        country_dict = get_country_names_by_ids([country_id])
        country_name = list(country_dict.values())[0]

        # if force color is provided, use this color for all countries
        if force_color:
            color = force_color

        else:
            color = palette[idx]

        # Plotting
        plt.plot(df_aggregated[time_period], df_aggregated[feature], marker=markers[idx % len(markers)], linestyle='-', 
                 label=f'Country: {country_name} (ID: {country_id})', color=color)


    if manual_title:
        plt.title(manual_title, fontsize=16)

    else:
        plt.title(f'Time Series ({time_period.split("_")[0]}ly) Plot for {feature}', fontsize=16)
    
    if manual_ylabel:
        plt.ylabel(manual_ylabel, fontsize=14)

    else:
        plt.ylabel(feature, fontsize=14)

    plt.xlabel('Time Period', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='upper left', bbox_to_anchor=legend_placement, fontsize=12)
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
        

    place_logo(logo_placement, logo_size, PATH)
    
    plt.tight_layout()

    if save_plot:
        if PATH_PLOT:
            plt.savefig(f'{PATH_PLOT}.png', dpi=300, bbox_inches='tight')
        else:
            raise ValueError("Please provide a path to save the plot")

    plt.show()
