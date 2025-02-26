import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

def generate_linear_gradient(start_color, end_color, steps):
    """
    Generates a list of hex color values that transition smoothly from start_color to end_color
    over a given number of steps.

    Parameters:
    - start_color (str): The starting color in HEX format or named color.
    - end_color (str): The ending color in HEX format or named color.
    - steps (int): The number of intermediate steps in the transition.

    Returns:
    - DataFrame with 'Step' and 'hex_value' columns.
    """
    cmap = LinearSegmentedColormap.from_list("gradient", [start_color, end_color], N=steps)
    step_values = np.linspace(0, 1, steps)
    hex_colors = [mcolors.to_hex(cmap(i)) for i in step_values]
    
    return pd.DataFrame({'Step': range(steps), 'hex_value': hex_colors})

def generate_dynamic_percentile_colormap_custom(
    thresholds=[1, 85, 90, 92, 93, 95, 97, 99.5, 100],
    colors=['cyan', 'turquoise', 'blue', 'green', 'yellow', 'pink','purple', 'red', 'black'],
    percentile_for_detailed_increase=85
):
    """
    Generates a DataFrame mapping a smooth range of percentile values to a color scale dynamically,
    allowing the user to specify multiple thresholds with associated colors.

    Parameters:
    - left_extreme (str): Color for values from 1 up to the first threshold.
    - thresholds (list): Percentile breakpoints where colors change.
    - colors (list): Colors assigned to each threshold in order.

    Returns:
    - DataFrame with 'Percentile' and 'hex_value' columns.
    """
    # Ensure thresholds and colors have the same length
    if len(thresholds) != len(colors):
        raise ValueError("The number of thresholds must match the number of colors.")

    # Sort thresholds and colors together to maintain correct mapping
    sorted_indices = np.argsort(thresholds)
    thresholds = np.array(thresholds)[sorted_indices]
    colors = np.array(colors)[sorted_indices]

    # Generate color mappings dynamically
    color_mappings = []
    for i in range(len(thresholds) - 1):
        start, end = thresholds[i], thresholds[i + 1]
        start_color, end_color = colors[i], colors[i + 1]
        
        # Ensure values increase by 1.0 until reaching 90, then by 0.1
        if start < percentile_for_detailed_increase:
            step_size = 1.0
        else:
            step_size = 0.1
        
        steps_required = len(np.arange(start, end + step_size, step_size))
        
        # Generate color gradient
        gradient_df = generate_linear_gradient(start_color, end_color, steps_required)
        gradient_df["Percentile"] = np.arange(start, end + step_size, step_size)[:steps_required]
        color_mappings.append(gradient_df)

    # Combine all parts into a single DataFrame
    full_colormap_df = pd.concat(color_mappings, ignore_index=True)
    
    # Reorder columns for clarity
    full_colormap_df = full_colormap_df[['Percentile', 'hex_value']]

    return full_colormap_df

def user_defined_colormap():
    """
    Interactive function that prompts the user to enter custom thresholds, colors, and the percentile where the step size changes.
    Includes a predefined list of color options for reference.

    Returns:
    - dynamic_colormap_df: A DataFrame containing the generated colormap.
    """
    # Predefined list of named colors
    standard_colors = [
        "black", "white", "gray", "silver", "lightgray", "darkgray",
        "red", "darkred", "lightcoral", "indianred", "salmon", "darksalmon",
        "tomato", "orangered", "firebrick", "brown", "maroon",
        "orange", "darkorange", "gold", "yellow", "lightyellow", "khaki",
        "olive", "darkolivegreen", "green", "darkgreen", "forestgreen",
        "lime", "limegreen", "lightgreen", "palegreen", "springgreen",
        "seagreen", "mediumseagreen", "mediumspringgreen", "teal",
        "darkcyan", "cyan", "lightcyan", "aqua", "aquamarine", "turquoise",
        "mediumturquoise", "darkturquoise", "steelblue", "deepskyblue",
        "dodgerblue", "blue", "mediumblue", "darkblue", "navy",
        "royalblue", "cornflowerblue", "skyblue", "lightskyblue",
        "slateblue", "mediumslateblue", "darkslateblue",
        "purple", "mediumorchid", "darkorchid", "darkviolet",
        "violet", "blueviolet", "indigo", "magenta", "darkmagenta",
        "fuchsia", "plum", "orchid", "thistle", "pink", "lightpink",
        "hotpink", "deeppink", "mediumvioletred"
    ]
    
    # Step 1: Prompt user to enter thresholds
    thresholds_input = input("Enter thresholds as comma-separated values (e.g., 1,80,90,92.5,95,97.5,99,99.5,100):\n")
    thresholds = [float(x.strip()) for x in thresholds_input.split(",")]

    # Step 2: Display available colors and prompt for user input
    print("\nAvailable Colors:")
    print(", ".join(standard_colors))
    
    print(f"\nYou entered {len(thresholds)} thresholds. Now, enter {len(thresholds)} colors corresponding to them.")
    colors_input = input(f"Enter {len(thresholds)} colors from the list above, separated by commas:\n")
    colors = [x.strip() for x in colors_input.split(",")]

    # Ensure number of colors matches number of thresholds
    if len(colors) != len(thresholds):
        print("Error: The number of colors must match the number of thresholds.")
        return None

    # Step 3: Prompt user to enter the percentile where step increase switches to 0.1
    percentile_for_detailed_increase = float(input(f"Enter the percentile where detailed steps (0.1 increments) should start (e.g., 80):\n"))

    # Create a dictionary mapping percentiles to colors
    percentile_color_mapping = dict(zip(thresholds, colors))
    
    # Print the mapping
    print("\nPercentile to Color Mapping:")
    for percentile, color in percentile_color_mapping.items():
        print(f"  {percentile}: {color}")

    # Generate the colormap using user inputs
    dynamic_colormap_df = generate_dynamic_percentile_colormap_custom(
        thresholds=thresholds,
        colors=colors,
        percentile_for_detailed_increase=percentile_for_detailed_increase
    )

    return dynamic_colormap_df

def display_percentile_color_table(df):
    """
    Displays a table where each row is colored according to the assigned hex_value.
    
    Parameters:
    - df (DataFrame): DataFrame containing 'Percentile' and 'hex_value' columns.
    """
    fig, ax = plt.subplots(figsize=(6, len(df) // 10))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(df))

    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    # Display each row as a colored bar
    for i, row in enumerate(df.itertuples()):
        ax.add_patch(plt.Rectangle((0, i), 1, 1, color=row.hex_value))

        # Add text labels
        ax.text(0.5, i + 0.5, f"{row.Percentile:.2f} - {row.hex_value}",
                va='center', ha='center', fontsize=8, color="white" if i % 2 == 0 else "black")

    plt.gca().invert_yaxis()  # Flip order so lowest percentile is at the top
    plt.show()

def assign_color_to_zero_values(df, zero_value_color_name):
    """
    - Retains only rows where fatalities_sum > 0 and the last row that contains zero fatalities.
    - Assigns a user-specified color name to the last zero-value row and converts it to HEX.
    - Sorts the DataFrame by Percentile in ascending order.
    - Removes duplicate rows to ensure unique combinations.
    - Returns the modified DataFrame.
    """
    # Convert color name to HEX using matplotlib
    if zero_value_color_name in mcolors.CSS4_COLORS:
        zero_value_color_hex = mcolors.to_hex(mcolors.CSS4_COLORS[zero_value_color_name])
    else:
        print(f"Invalid color name '{zero_value_color_name}'. Using default gray.")
        zero_value_color_hex = mcolors.to_hex(mcolors.CSS4_COLORS["gray"])

    # Identify the last row that contains zero fatalities
    last_zero_fatalities_row = df[df["fatalities_sum"] == 0].iloc[-1:]

    # Filter to retain only non-zero rows and the last zero-fatalities row
    df_filtered = pd.concat([df[df["fatalities_sum"] > 0], last_zero_fatalities_row]).copy()

    # Overwrite hex_value for the last zero-fatalities row with the converted color
    df_filtered.loc[df_filtered["fatalities_sum"] == 0, "hex_value"] = zero_value_color_hex

    # Ensure Percentile remains numeric where applicable and sort by Percentile
    df_filtered["Percentile"] = pd.to_numeric(df_filtered["Percentile"], errors="coerce")
    df_filtered = df_filtered.sort_values(by="Percentile", ascending=True).reset_index(drop=True)

    # Remove duplicate rows based on all column values
    df_filtered = df_filtered.drop_duplicates()

    return df_filtered

def process_and_merge_return_periods(df_return_period, dynamic_colormap_df_corrected):
    """
    Processes and merges return period data with a dynamic colormap based on Percentile values.
    
    Steps:
    1. Replaces 'max' in the Percentile column of df_return_period with 100.
    2. Converts Percentile columns to float and rounds to one decimal place.
    3. Merges df_return_period with dynamic_colormap_df_corrected on Percentile.
    4. Prompts the user to enter a color name for zero values.
    5. Assigns the user-defined color to zero values using `assign_color_to_zero_values`.
    
    Parameters:
    - df_return_period (pd.DataFrame): DataFrame containing return period data with a 'Percentile' column.
    - dynamic_colormap_df_corrected (pd.DataFrame): DataFrame containing colormap mappings with a 'Percentile' column.
    
    Returns:
    - pd.DataFrame: The merged and updated dataframe with the assigned zero-value color.
    """

    # Ensure "max" is replaced with 100 in Percentile column
    df_return_period["Percentile"] = df_return_period["Percentile"].replace("max", 100)
    
    # Convert Percentile column to float and round to one decimal place
    df_return_period["Percentile"] = df_return_period["Percentile"].astype(float).round(1)
    dynamic_colormap_df_corrected["Percentile"] = dynamic_colormap_df_corrected["Percentile"].astype(float).round(1)

    # Perform the join based on the shared Percentile column
    df_merged = df_return_period.merge(dynamic_colormap_df_corrected, on="Percentile", how="left")

    # Prompt user to enter a color name for zero values
    zero_value_color_name = input("Enter the color name to assign to zero values (e.g., 'blue', 'red', 'green'): ").strip().lower()

    # Apply the function with user input
    df_updated = assign_color_to_zero_values(df_merged, zero_value_color_name)

    return df_updated