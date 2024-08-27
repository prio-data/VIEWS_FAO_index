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


def plot_country_period_map_precheck(df, country_id, features, time_period, time_period_ids):

    """
    Performs pre-checks on the input data and parameters for plotting country period maps.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data to be plotted. Must include columns for country ID, time period, and features.
    country_id (int): The ID of the country to be plotted.
    features (list of str): List of feature names to be plotted.
    time_period (str): The name of the column representing the time period in the DataFrame.
    time_period_ids (list of int): List of time period IDs to be plotted.

    Raises:
    ValueError: If any of the following conditions are met:
        - df is not a pandas DataFrame.
        - df is empty.
        - 'c_id' column is not found in df.
        - country_id is not an integer.
        - country_id is not found in the 'c_id' column of df.
        - features is not a list.
        - Any element in features is not a string.
        - Any feature in features is not found in the columns of df.
        - time_period is not found in the columns of df.
        - time_period_ids is not a list.
        - Any element in time_period_ids is not an integer.
        - Any time period ID in time_period_ids is not found in the time_period column of df.

    Returns:
    None
    """

    # Check that df is a pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError('Input is not a valid DataFrame.')
    
    # check thath the data is not empty
    if df.empty:
        raise ValueError('Input dataframe is empty.')
    
    # Check that data has the country ID column
    if 'c_id' not in df.columns:
        raise ValueError('Country ID column not found in the data. Please check the data.')
    
    # check that the country_id is an integer
    if not isinstance(country_id, int):
        raise ValueError('Country ID should be an integer.')

    # check that the country_id is in the country column
    if country_id not in df['c_id'].unique():
        raise ValueError('Country ID not found in the data. Please check the data.')

    # check that features is a list
    if not isinstance(features, list):
        raise ValueError('Feature should be a list of strings - if only one feature is needed, it should still be in a list. E.g. [feature].')
    
    # check taht each feature in the list is a string
    if not all(isinstance(f, str) for f in features):
        raise ValueError('All elements in the feature list should be strings.')

    # check that each feature in the list is in the columns of the data frame
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        raise ValueError(f'Feature(s) not found in the data: {missing_features }')
    
    # Check if any feature string contains the word "country"
    for f in features:
        if 'country' in f:
            print(f"WARNING: The feature '{f}' you are plotting is a country-level feature. This will result in a map with the same color for all the cells in the country.")

    # Check that the time_period is in the data
    if time_period not in df.columns:
        raise ValueError('Time period not found in the data. Please check the data.')
    

    # check that the time_period_ids is a list
    if not isinstance(time_period_ids, list):
        raise ValueError('Time period IDs should be provided as a list - even if only one time period is needed. E.g. [time_period_id].')
    
    # check that each element in the time_period_ids list is an integer
    if not all(isinstance(tp, int) for tp in time_period_ids):
        raise ValueError('All elements in the time period ID list should be integers.')

    # check that all the time_period_id are within the range of the time_period feature
    if not all(tp in df[time_period].unique() for tp in time_period_ids):
        raise ValueError('Time period IDs not found in the data. Please check the data.')


def place_logo(ax, logo_placement, logo_size, PATH):

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
    #plt.gca().add_artist(ab)
    ax.add_artist(ab)


def plot_country_period_map(df, country_id, features, time_period_ids, shared_feature_min_max = False, manual_title = None, figsize=(16, 8), PATH=PATH, logo_placement = (0.9, 0.85), logo_size = 0.6, save_plot = False, PATH_PLOT = None):

    """
    Plots a grid of maps for a given country over specified time periods and features.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data to be plotted. Must include columns for country ID, time period, row, col, and features.
    country_id (int): The ID of the country to be plotted.
    features (list of str): List of feature names to be plotted.
    time_period_ids (list of int): List of time period IDs to be plotted.
    shared_feature_min_max (bool, optional): If True, all subplots of the same feature will share the same color scale. Defaults to False.
    manual_title (str, optional): Title for the plot. Defaults to None in which case a title will be generated automatically.
    figsize (tuple, optional): Size of the figure. Defaults to (16, 8).
    PATH (str, optional): Path to the directory containing the logo. Defaults to PATH.
    logo_placement (tuple, optional): Coordinates for logo placement in each subplot. Defaults to (0.9, 0.85).
    logo_size (float, optional): Size of the logo. Defaults to 0.6.
    save_plot (bool, optional): If True, the plot will be saved to the specified path. Defaults to False.
    PATH_PLOT (str, optional): Path to save the plot if save_plot is True. Defaults to None.

    Raises:
    ValueError: If shared_min_max is not a boolean.
    ValueError: If save_plot is True and PATH_PLOT is not provided.

    Returns:
    None
    """

    time_period = get_time_period(df)

    plot_country_period_map_precheck(df, country_id, features, time_period, time_period_ids)

    # set style
    sns.set(style="whitegrid")
    
    # this will be infered soon enough 
    num_rows = len(time_period_ids)
    num_cols = len(features)

    # make the plot
    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    
    # Handle different cases for axes
    if num_rows == 1 and num_cols == 1:
        axes = np.array([[axes]])  # Single Axes object to 2D array
    elif num_rows == 1:
        axes = np.array([axes])  # 1D array to 2D array with one row
    elif num_cols == 1:
        axes = np.array([[ax] for ax in axes])  # 1D array to 2D array with one column

    # Iterate over time periods and features
    for row_idx, time_period_id in enumerate(time_period_ids):
        for col_idx, feature in enumerate(features):

            if 'P_i' in feature:
                cmap = 'rainbow_r'

            elif 'p_i' in feature:
                cmap = 'rainbow_r'

            else:
                cmap = 'rainbow'

            ax = axes[row_idx, col_idx]

            sub_df = df[(df['c_id'] == country_id) & (df[time_period] == time_period_id)][['row', 'col', feature, time_period]]
            
            if not shared_feature_min_max:
                vmin = sub_df[feature].min()
                vmax = sub_df[feature].max()

            elif shared_feature_min_max:
                vmin = df[(df['c_id'] == country_id) & (df[time_period].isin(time_period_ids))][feature].min()
                vmax = df[(df['c_id'] == country_id) &(df[time_period].isin(time_period_ids))][feature].max()

            else:
                raise ValueError('shared_min_max should be a boolean.')

            country_name = list(get_country_names_by_ids([country_id]).values())[0]

            if time_period == 'year_id':
                title = f'{feature} in {country_name} (country id: {country_id}) for {time_period} {time_period_id}'

            elif time_period == 'month_id':
                date = calculate_date_from_index(time_period_id)
                title = f'{feature} in {country_name} (country id: {country_id}) for {date} ({time_period}: {time_period_id})'

            # Assuming sub_df is your DataFrame and feature is the column name for pixel intensity
            pivot_table = sub_df.pivot(index='row', columns='col', values=feature)

            im = ax.imshow(pivot_table, cmap=cmap, vmin=vmin, vmax=vmax, origin='lower')

            # Add title
            ax.set_title(title, fontsize=16)

            # Add the colorbar to the same axis, ensuring it has the same height
            fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

            # Just get rid of the ticks
            ax.set_xticks([])
            ax.set_yticks([])

            place_logo(ax, logo_placement, logo_size, PATH)

    # Add a super title
    if manual_title:
        fig.suptitle(manual_title, fontsize=16, y = 1)
    else:
        fig.suptitle(f'Map of feature(s) {features} in country {country_name} (ID: {country_id})', fontsize=16, y = 1)

    plt.tight_layout()

    if save_plot:
        if PATH_PLOT:
            plt.savefig(f'{PATH_PLOT}.png', dpi=300, bbox_inches='tight')
        else:
            raise ValueError("Please provide a path to save the plot")

    plt.show()

