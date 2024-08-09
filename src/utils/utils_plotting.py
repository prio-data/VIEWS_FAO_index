import numpy as np
import matplotlib.pyplot as plt

def plot_random_monthly_and_yearly_data(df_monthly, df_yearly, feature, year=None):
    """
    Plots random monthly and yearly data from the provided DataFrames.

    Parameters:
    df_monthly (pd.DataFrame): DataFrame containing monthly data.
    df_yearly (pd.DataFrame): DataFrame containing yearly data.
    feature (str): The feature to be plotted.
    year (int, optional): The specific year to plot. Defaults to None, which selects a random year.
    """
    # Select a specific year if provided, otherwise select a random year
    if year is not None:
        if year not in df_yearly['year_id'].unique():
            raise ValueError(f"Year {year} is not available in the yearly data.")
        selected_year = year
    else:
        selected_year = np.random.choice(df_yearly['year_id'].unique())

    # Select a random month within the selected year
    random_month = np.random.choice(df_monthly[df_monthly['year_id'] == selected_year]['month_id'].unique())

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
    sc2 = axs[1].scatter(df_yearly[df_yearly['year_id'] == selected_year]['col'], 
                         df_yearly[df_yearly['year_id'] == selected_year]['row'], 
                         c=df_yearly[df_yearly['year_id'] == selected_year][feature], cmap=f'rainbow{suffix}', marker='.', s=10)
    axs[1].set_title(f'Yearly Data for Year {selected_year}')
    axs[1].set_xlabel('Column')
    axs[1].set_ylabel('Row')
    fig.colorbar(sc2, ax=axs[1], orientation='vertical', label=feature)

    # Show the plot
    plt.show()