import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont

import os
import sys

# Get the current working directory
current_directory = os.getcwd()

# Print the current working directory
print("The current Working Directory is:", current_directory)

# Get the path to the base directory (VIEWS_FAO_index)
base_dir = os.path.abspath(os.path.join(os.getcwd(), '..', '..'))
print(f'The base directory will be set to: {base_dir}')

# Add the base directory to sys.path
sys.path.insert(0, base_dir)

from src.utils.universal_functions.setup.build_directory import ensure_directory_exists

def find_file_with_string(folder_path, search_string):
    # Loop through all files in the directory
    for filename in os.listdir(folder_path):
        # Check if the search_string is in the filename
        if search_string in filename:
            return filename
    return None


"""
This gives the formatting criteria for OPTION 2 Slides (1 & 2)
"""

def map_top_years(country, method, returnperiodmethod, summary_text, aggregation='0'): 

    base_directory = os.getcwd()
    font_path = base_dir + '/src/utils/functions_for_graphics/layout_formats/OpenSans-VariableFont.ttf'
    template_path = base_dir + '/src/utils/functions_for_graphics/layout_formats/PRIO Layout A Sept2.png'
    template_image = Image.open(template_path)

    if aggregation == '1':
        map_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'map_png/'
        print(map_path)
        annual_table_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'table_png/'
        print(annual_table_path)
        return_period_table_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'table_png/percentile and payout table/'
        print(return_period_table_path)
        return_period_lineplot_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'plot_png/'
        print(return_period_lineplot_path)
        #---
        output_path = base_directory + '/files/Layouts/' + country + '/' 

    else:
        aggregation_string = aggregation + 'x' + aggregation

        map_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod + '/' + aggregation_string   + '/' + 'map_png/'
        print(map_path)
        annual_table_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod + '/' + aggregation_string  + '/' + 'table_png/'
        print(annual_table_path)
        return_period_table_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod + '/' + aggregation_string  + '/' + 'table_png/percentile and payout table/'
        print(return_period_table_path)
        return_period_lineplot_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod + '/' + aggregation_string  + '/' + 'plot_png/'
        print(return_period_lineplot_path)
        #---
        output_path = base_directory + '/files/Layouts/' + country + '/' 


    ensure_directory_exists(output_path)

    #look for the graphic with the appropriate dimensions:
    #Map 1
    map_filename_0 = find_file_with_string(map_path, 'conflict year 0 ') # looking for a 3.5 x 3.5 map 
    print(map_filename_0)
    #Map 2
    map_filename_1 = find_file_with_string(map_path, 'conflict year 1 ') # looking for a 3.5 x 3.5 map
    print(map_filename_1)
    #Map 3
    map_filename_2 = find_file_with_string(map_path, 'conflict year 2 ') # looking for a 3.5 x 3.5 map
    print(map_filename_2)
    #Map 4
    map_filename_3 = find_file_with_string(map_path, 'conflict year 3 ') # looking for a 3.5 x 3.5 map
    print(map_filename_3)
    #Map 5
    map_filename_4 = find_file_with_string(map_path, 'conflict year 4 ') # looking for a 3.5 x 3.5 map
    print(map_filename_4)
    #Map 6
    map_filename_5 = find_file_with_string(map_path, 'conflict year 5 ') # looking for a 3.5 x 3.5 map
    print(map_filename_5)
    #Map 7
    map_filename_6 = find_file_with_string(map_path, 'conflict year 6 ') # looking for a 3.5 x 3.5 map
    print(map_filename_6)
    #Map 8
    map_filename_7 = find_file_with_string(map_path, 'conflict year 7 ') # looking for a 3.5 x 3.5 map
    print(map_filename_7)
    #Map 9
    map_filename_8 = find_file_with_string(map_path, 'conflict year 8 ') # looking for a 3.5 x 3.5 map
    print(map_filename_8)
    #Map 10
    map_filename_9 = find_file_with_string(map_path, 'conflict year 9 ') # looking for a 3.5 x 3.5 map
    print(map_filename_9)

    annual_table_filename = find_file_with_string(annual_table_path, 'annual_count') #  looking for a 2.5 x 1.75 map 4_0x5_5
    print(annual_table_filename)
    return_period_table_fileneame = find_file_with_string(return_period_table_path, '2.5x1.8')
    print(return_period_table_fileneame)
    return_period_lineplot_fileneame = find_file_with_string(return_period_lineplot_path, '6.0x3.0')
    print(return_period_lineplot_fileneame)



    # Load the template image
    #template_path = 'Slide 1 Option B Template.png'

    template_image = template_image.resize((1620, 915), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(template_image)

    #template_image = Image.open(template_path)
    #draw = ImageDraw.Draw(template_image)

    # # Define grid parameters
    # grid_spacing = 50  # Adjust the spacing as needed
    # grid_color = "blue"
    # grid_width = 1

    # # Define the font for the grid labels
    # font = ImageFont.load_default()

    # # Get the dimensions of the template image
    # width, height = template_image.size

    # # Draw the grid
    # for x in range(0, width, grid_spacing):
    #     draw.line([(x, 0), (x, height)], fill=grid_color, width=grid_width)
    #     draw.text((x, 0), str(x), fill=grid_color, font=font)
    # for y in range(0, height, grid_spacing):
    #     draw.line([(0, y), (width, y)], fill=grid_color, width=grid_width)
    #     draw.text((0, y), str(y), fill=grid_color, font=font)

    # Define the positions and sizes for placeholders
    positions = [

        {'position': (425, 200), 'size': (400, 350), 'label': 'Rank 1','filename': map_filename_0, 'folder': map_path, 'font_size':9},      # Main Map

        {'position': (925, 175), 'size': (200, 200), 'label': 'Rank 2','filename': map_filename_1, 'folder': map_path, 'font_size': 9},       # Year 1
        {'position': (925, 400), 'size': (200, 200), 'label': 'Rank 5','filename': map_filename_4, 'folder': map_path, 'font_size':9},       # Year 1
        {'position': (925, 625), 'size': (200, 200), 'label': 'Rank 8','filename': map_filename_7, 'folder': map_path, 'font_size':9},       # Year 1
        {'position': (1150, 175), 'size': (200, 200), 'label': 'Rank 3','filename': map_filename_2, 'folder': map_path, 'font_size':9},       # Year 1
        {'position': (1150, 400), 'size': (200, 200), 'label': 'Rank 6','filename': map_filename_5, 'folder': map_path, 'font_size':9},       # Year 1
        {'position': (1150, 625), 'size': (200, 200), 'label': 'Rank 9','filename': map_filename_8, 'folder': map_path, 'font_size':9},       # Year 1
        {'position': (1375, 175), 'size': (200, 200), 'label': 'Rank 4','filename': map_filename_3, 'folder': map_path, 'font_size':9},       # Year 1
        {'position': (1375, 400), 'size': (200, 200), 'label': 'Rank 7','filename': map_filename_6, 'folder': map_path, 'font_size':9},       # Year 1
        {'position': (1375, 625), 'size': (200, 200), 'label': 'Rank 10','filename': map_filename_9, 'folder': map_path, 'font_size':9},       # Year 1

        {'position': (425, 625), 'size': (400, 200), 'label': '','filename': return_period_table_fileneame, 'folder': return_period_table_path,'font_size':1},     # Payout Legend 
       
        #{'position': (425, 575), 'size': (400, 50), 'label': 'Legend'},     # Payout Legend Title
        #{'position': (925, 100), 'size': (650, 50), 'label': 'Legend'},     # Payout Legend Title

    ]

        # Define the positions and sizes for text boxes
    text_boxes = [
        #{'position': (425, 575), 'size': (400, 50), 'label': 'Payout Legend','font_size': 24},     # Payout Legend Title
        #{'position': (925, 100), 'size': (650, 50), 'label': 'Top Conflict Years','font_size': 32},     # Payout Legend Title
        {'position': (65, 215), 'size': (270, 325), 'label':  summary_text,'font_size': 15}
    ]

    title = [
        #{'position': (425, 575), 'size': (400, 50), 'label': 'Payout Legend','font_size': 24},     # Payout Legend Title
        #{'position': (925, 100), 'size': (650, 50), 'label': 'Top Conflict Years','font_size': 32},     # Payout Legend Title
        {'position': (50, 25), 'size': (600, 125), 'label':  country, 'font_size': 92}
    ]

    title_boxes = [
        {'position': (425, 575), 'size': (400, 50), 'label': 'Payout Legend','font_size': 24},     # Payout Legend Title
        {'position': (925, 100), 'size': (650, 50), 'label': 'Top Conflict Years','font_size': 32},     # Payout Legend Title
        {'position': (50, 200), 'size': (300, 350), 'label': '','font_size': 32},     # empty text box

        #{'position': (50, 175), 'size': (300, 500), 'label':  summary_text,'font_size': 14}
    ]

        # # Load and paste the images onto the template
    for pos in positions:
        if 'folder' in pos and 'filename' in pos:
                img_path = os.path.join(pos['folder'], pos['filename'])
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img = img.resize(pos['size'], Image.Resampling.LANCZOS)
                    template_image.paste(img, pos['position'])
                else:
                    print(f"Image {pos['filename']} not found in {pos['folder']}")
        else:
                print(f"Missing 'folder' or 'filename' in: {pos}")

# Add text boxes
    # Add text boxes
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------         
    for title_b in title_boxes:
        x, y = title_b['position']
        w, h = title_b['size']
        label = title_b['label']
        font_size = title_b['font_size']  # Get the font size from the dictionary

            # Create a font object with the specified size
        try:
            font = ImageFont.truetype(font_path, font_size)  # Use a valid font on your system
        except IOError:
            font = ImageFont.load_default()

    #     Draw a rectangle around the text box area with a dark grey background
        draw.rectangle([x, y, x + w, y + h], fill="darkgrey", outline="black", width=2)

    #     # Calculate the bounding box of the text
        text_bbox = draw.textbbox((0, 0), label, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

         # Calculate the position to center the text
        text_x = x + (w - text_width) / 2
        text_y = y + (h - text_height) / 3

    #     # Draw the text centered in the box with white color
        draw.text((text_x, text_y), label, fill="white", font=font)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    for t in title:
        x, y = t['position']
        w, h = t['size']
        label = t['label']
        font_size = t['font_size']  # Get the font size from the dictionary

        # Create a font object with the specified size
        try:
            font = ImageFont.truetype(font_path, font_size)  # Use a valid font on your system
        except IOError:
            font = ImageFont.load_default()

        # Draw a rectangle around the text box area with a dark grey background
        #draw.rectangle([x, y, x + w, y + h], fill="grey", outline="white", width=2)
        #draw.rectangle([x, y, x + w, y + h])

        # Wrap the text to fit inside the box
        wrapped_text = []
        words = label.split()
        line = ""

        for word in words:
            # Add the word to the line and check if it fits
            test_line = line + word + " "
            text_bbox = draw.textbbox((0, 0), test_line, font=font)
            test_width = text_bbox[2] - text_bbox[0]

            if test_width <= w:
                line = test_line
            else:
                # If the line is too long, add the current line to wrapped_text and start a new line
                wrapped_text.append(line.strip())
                line = word + " "

        # Add the last line
        wrapped_text.append(line.strip())

        # Draw the text line by line, adjusting the position
        current_y = y
        for line in wrapped_text:
            draw.text((x, current_y), line, fill="black", font=font)
            current_y += font_size  # Move to the next line

        # Ensure that the text doesn't overflow the box height
        if current_y > y + h:
            print("Warning: Text overflow in the box. Consider reducing the font size or the amount of text.")
#-------------------------------------------------------------------------------------------------------------------------------------------------------         
#-------------------------------------------------------------------------------------------------------------------------------------------------------         
    for box in text_boxes:
        x, y = box['position']
        w, h = box['size']
        label = box['label']
        font_size = box['font_size']  # Get the font size from the dictionary

        # Create a font object with the specified size
        try:
            font = ImageFont.truetype(font_path, font_size)  # Use a valid font on your system
        except IOError:
            font = ImageFont.load_default()

        # Draw a rectangle around the text box area with a dark grey background
        #draw.rectangle([x, y, x + w, y + h], fill="white", outline="white", width=2)
        #draw.rectangle([x, y, x + w, y + h])

        # Wrap the text to fit inside the box
        wrapped_text = []
        words = label.split()
        line = ""

        for word in words:
            # Add the word to the line and check if it fits
            test_line = line + word + " "
            text_bbox = draw.textbbox((0, 0), test_line, font=font)
            test_width = text_bbox[2] - text_bbox[0]

            if test_width <= w:
                line = test_line
            else:
                # If the line is too long, add the current line to wrapped_text and start a new line
                wrapped_text.append(line.strip())
                line = word + " "

        # Add the last line
        wrapped_text.append(line.strip())

        # Draw the text line by line, adjusting the position
        current_y = y
        for line in wrapped_text:
            draw.text((x, current_y), line, fill="black", font=font)
            current_y += font_size  # Move to the next line

        # Ensure that the text doesn't overflow the box height
        if current_y > y + h:
            print("Warning: Text overflow in the box. Consider reducing the font size or the amount of text.")

#-------------------------------------------------------------------------------------------------------------------------------------------------------         
#-------------------------------------------------------------------------------------------------------------------------------------------------------         

    # Draw rectangles at specified positions
    for pos in positions:
        x, y = pos['position']
        w, h = pos['size']
        draw.rectangle([x, y, x + w, y + h], outline="black", width=3)
        draw.text((x, y - 20), pos['label'], fill="black")
        font_size = pos['font_size']  # Get the font size from the dictionary

        try:
            font = ImageFont.truetype(font_path, font_size)  # Use a valid font on your system
        except IOError:
            font = ImageFont.load_default()

    # Save and show the template with marked positions
    #marked_template_path = '/Users/gbenz/Desktop/tmp.png'
            
        # Save the final image with a specified filename
            

    output_filename = os.path.join(output_path, f'{country}_{method}_{returnperiodmethod}_{aggregation}x{aggregation}.png')
    template_image.save(output_filename)
    template_image.show()