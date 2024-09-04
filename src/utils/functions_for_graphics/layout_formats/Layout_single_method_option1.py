import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont

from support_functions.universal_functions.setup.build_directory import ensure_directory_exists

def find_file_with_string(folder_path, search_string):
    # Loop through all files in the directory
    for filename in os.listdir(folder_path):
        # Check if the search_string is in the filename
        if search_string in filename:
            return filename
    return None

def mapped_option1(country, method, returnperiodmethod, aggregation=0): 


    base_directory = os.getcwd()

    if aggregation == 0:
        map_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'map_png/'
        print(map_path)
        annual_table_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'table_png/'
        print(annual_table_path)
        return_period_table_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'table_png/percentile and payout table/'
        print(return_period_table_path)
        return_period_lineplot_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'plot_png/'
        print(return_period_lineplot_path)
        #---
        output_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'layout/Individual Method/'

    else:
        aggregation_string = aggregation + 'x' + aggregation

        map_path = base_directory + '/files/' + country + '/' + method + '/' + aggregation_string + '/' + returnperiodmethod  + '/' + 'map_png/'
        print(map_path)
        annual_table_path = base_directory + '/files/' + country + '/' + method + '/' + aggregation_string + '/' + returnperiodmethod  + '/' + 'table_png/'
        print(annual_table_path)
        return_period_table_path = base_directory + '/files/' + country + '/' + method + '/' + aggregation_string + '/' + returnperiodmethod  + '/' + 'table_png/percentile and payout table/'
        print(return_period_table_path)
        return_period_lineplot_path = base_directory + '/files/' + country + '/' + method + '/' + aggregation_string + '/' + returnperiodmethod  + '/' + 'plot_png/'
        print(return_period_lineplot_path)
        #---
        output_path = base_directory + '/files/' + country + '/' + method + '/' + aggregation_string + '/' + returnperiodmethod  + '/' + 'layout/Individual Method/'

    ensure_directory_exists(output_path)


#look for the graphic with the appropriate dimensions:
    map_filename = find_file_with_string(map_path, '3_5x3_5') # looking for a 3.5 x 3.5 map
    print(map_filename)
    annual_table_filename = find_file_with_string(annual_table_path, '4.0x5.5') #  looking for a 2.5 x 1.75 map 4_0x5_5
    print(annual_table_filename)
    return_period_table_fileneame = find_file_with_string(return_period_table_path, '2.5x1.8')
    print(return_period_table_fileneame)
    return_period_lineplot_fileneame = find_file_with_string(return_period_lineplot_path, '6.0x3.0')
    print(return_period_lineplot_fileneame)

    # Load the template image
    template_path = '/Users/gbenz/Desktop/Screenshot 2024-07-20 at 06.33.22.png'
    template_image = Image.open(template_path)
    draw = ImageDraw.Draw(template_image)

    # Define grid parameters
    grid_spacing = 50  # Adjust the spacing as needed
    grid_color = "blue"
    grid_width = 1

    # Define the font for the grid labels
    font = ImageFont.load_default()

    # Get the dimensions of the template image
    width, height = template_image.size

    # Draw the grid
    for x in range(0, width, grid_spacing):
         draw.line([(x, 0), (x, height)], fill=grid_color, width=grid_width)
         draw.text((x, 0), str(x), fill=grid_color, font=font)
    for y in range(0, height, grid_spacing):
         draw.line([(0, y), (width, y)], fill=grid_color, width=grid_width)
         draw.text((0, y), str(y), fill=grid_color, font=font)

    # Define the positions, sizes, and paths for placeholders
    positions = [
        {'position': (800, 200), 'size': (350, 350), 'label': 'Main Map', 'filename': map_filename, 'folder': map_path},      # Main Map
        {'position': (1175, 250), 'size': (400, 550), 'label': 'Annual Summary', 'filename': annual_table_filename, 'folder': annual_table_path},         # Annual Summary
        {'position': (800, 625), 'size': (350, 175), 'label': 'Payout Legend', 'filename': return_period_table_fileneame, 'folder': return_period_table_path},    # Payout Legend
        {'position': (75, 500), 'size': (600, 300), 'label': 'Line Plot', 'filename': return_period_lineplot_fileneame, 'folder':return_period_lineplot_path},   # Payout line graph
    ]

    # Define the positions and sizes for text boxes
    text_boxes = [
        {'position': (1175, 215), 'size': (400, 50), 'label': 'Annual Title'},
        {'position': (800, 575), 'size': (350, 50), 'label': 'Legend'},
    ]

    # # Load and paste the images onto the template
    for pos in positions:
         img_path = os.path.join(pos['folder'], pos['filename'])
         if os.path.exists(img_path):
             img = Image.open(img_path)
             img = img.resize(pos['size'], Image.Resampling.LANCZOS)
             template_image.paste(img, pos['position'])
         else:
             print(f"Image {pos['filename']} not found in {pos['folder']}")

    # Add text boxes
    for box in text_boxes:
        x, y = box['position']
        w, h = box['size']
        label = box['label']

    #     Draw a rectangle around the text box area with a dark grey background
        draw.rectangle([x, y, x + w, y + h], fill="darkgrey", outline="black", width=2)

    #     # Calculate the bounding box of the text
        text_bbox = draw.textbbox((0, 0), label, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

         # Calculate the position to center the text
        text_x = x + (w - text_width) / 2
        text_y = y + (h - text_height) / 2

    #     # Draw the text centered in the box with white color
        draw.text((text_x, text_y), label, fill="white", font=font)

    # Save and show the template with overlaid images and text boxes
    layout_path = output_path + country + ' ' + method + ' ' + 'style A.png'
    template_image.save(layout_path)
    template_image.show()