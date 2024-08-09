import numpy as np
from matplotlib import pyplot as plt

def plot_time_series_data(df, time_ids, columns, figsize=(18, 25), cmap="rainbow", alpha=0.6, marker='.', s=6):
    """
    Plots a grid of scatter plots for specified time_ids and columns.

    Parameters:
    - df: pandas DataFrame containing the data
    - time_ids: list of time_ids to plot (e.g., months, years, weeks)
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
        for j, time_id in enumerate(time_ids):
            ax = axes[i, j]
            filtered_df = df[df["time_id"] == time_id]
            scatter = ax.scatter(filtered_df["col"], filtered_df["row"], c=filtered_df[col], cmap=cmap, alpha=alpha, marker=marker, s=s)
            
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


def plot_random_monthly_and_yearly_data(df_monthly, df_yearly, feature):
    """
    Plots random monthly and yearly data from the provided DataFrames.

    Parameters:
    df_monthly (pd.DataFrame): DataFrame containing monthly data.
    df_yearly (pd.DataFrame): DataFrame containing yearly data.
    feature (str): The feature to be plotted.
    """
    # Select a random year and a random month within that year
    random_year = np.random.choice(df_yearly['year_id'].unique())
    random_month = np.random.choice(df_monthly[df_monthly['year_id'] == random_year]['month_id'].unique())

    # Size the plot
    fig, axs = plt.subplots(1, 2, figsize=(20, 7))

    # if the feature name contains "likelihood", set the color map to 'rainbow_r'
    suffix = '' if 'likelihood' not in feature else '_r'

    # Plot monthly data
    sc1 = axs[0].scatter(df_monthly[df_monthly['month_id'] == random_month]['col'], 
                         df_monthly[df_monthly['month_id'] == random_month]['row'], 
                         c=df_monthly[df_monthly['month_id'] == random_month][feature], cmap=f'rainbow{suffix}', marker='.', s=10)
    axs[0].set_title(f'Monthly Data for Month {random_month}')
    axs[0].set_xlabel('Column')
    axs[0].set_ylabel('Row')
    fig.colorbar(sc1, ax=axs[0], orientation='vertical', label=feature)

    # Plot yearly data
    sc2 = axs[1].scatter(df_yearly[df_yearly['year_id'] == random_year]['col'], 
                         df_yearly[df_yearly['year_id'] == random_year]['row'], 
                         c=df_yearly[df_yearly['year_id'] == random_year][feature], cmap=f'rainbow{suffix}', marker='.', s=10)
    axs[1].set_title(f'Yearly Data for Year {random_year}')
    axs[1].set_xlabel('Column')
    axs[1].set_ylabel('Row')
    fig.colorbar(sc2, ax=axs[1], orientation='vertical', label=feature)

    # Show the plot
    plt.show()