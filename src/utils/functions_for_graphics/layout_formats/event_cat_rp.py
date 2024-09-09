import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont
import re

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

def map_event_cat_rp(country, method, returnperiodmethod, year_datastart, year_dataend, aggregation='0', gridlines='no'): 

    base_directory = os.getcwd()
    font_path = base_dir + '/src/utils/functions_for_graphics/layout_formats/OpenSans-VariableFont.ttf'
    template_path = base_dir + '/src/utils/functions_for_graphics/layout_formats/event_cat_rd_template.png'
    template_image = Image.open(template_path)


    if aggregation == '1':
        aggregation_string = aggregation + 'x' + aggregation

        map_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'map_png/'
        print(map_path)
        annual_table_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + aggregation_string + '/table_png/'
        print(annual_table_path)
        return_period_table_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/table_png/percentile and payout table/'
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

    output_path = base_directory + '/files/Layouts/event_cat_rd/' 

    ensure_directory_exists(output_path)

    #look for the graphic with the appropriate dimensions:
    #Map 1
    map_filename_0 = find_file_with_string(map_path, 'conflict year 0') # looking for a 3.5 x 3.5 map 
    print(f'located map rank1: {map_filename_0}')

    year__0 = re.search(r"\b\d{4}\b", map_filename_0)

    # Convert the match to an integer and print
    if year__0:
        year__0 = str(int(year__0.group()))
        print(year__0)

    #Map 2
    map_filename_1 = find_file_with_string(map_path, 'conflict year 1 ') # looking for a 3.5 x 3.5 map
    print(f'located map rank 2: {map_filename_1}')

    year__1 = re.search(r"\b\d{4}\b", map_filename_1)

    # Convert the match to an integer and print
    if year__1:
        year__1 = str(int(year__1.group()))
        print(year__1)

    map_filename_2 = find_file_with_string(map_path, 'conflict year 2 ') # looking for a 3.5 x 3.5 map
    print(f'located map rank 3: {map_filename_2}')

    year__2 = re.search(r"\b\d{4}\b", map_filename_2)

    # Convert the match to an integer and print
    if year__2:
        year__2 = str(int(year__2.group()))
        print(year__2)

    #Map 3
    map_filename_2010 = find_file_with_string(map_path, '2010') # looking for a 3.5 x 3.5 map
    print(map_filename_2010)
    #Map 4
    map_filename_2020 = find_file_with_string(map_path, '2020') # looking for a 3.5 x 3.5 map
    print(map_filename_2020)

    map_filename_2000 = find_file_with_string(map_path, '2000') # looking for a 3.5 x 3.5 map
    print(map_filename_2000)
    #Map 5
    #Map 6


    annual_table_filename = find_file_with_string(annual_table_path, '4.0x5.5') #  looking for a 2.5 x 1.75 map 4_0x5_5
    print(f'located lineplot file in folder: {annual_table_filename}')

    return_period_table_fileneame = find_file_with_string(return_period_table_path, '2.5x1.8')
    print(f'located lineplot file in folder: {return_period_table_fileneame}')
    
    return_period_lineplot_fileneame = find_file_with_string(return_period_lineplot_path, '6.0x3.0')
    print(f'located lineplot file in folder: {return_period_lineplot_fileneame}')



    # Load the template image
    #template_path = 'Slide 1 Option B Template.png'

    template_image = template_image.resize((1620, 915), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(template_image)



    # Define grid parameters
    grid_spacing = 50  # Adjust the spacing as needed
    grid_color = "blue"
    grid_width = 1

    # Define the font for the grid labels
    font = ImageFont.load_default()

    # Get the dimensions of the template image
    width, height = template_image.size

    if gridlines == 'yes':
    # Draw the grid
        for x in range(0, width, grid_spacing):
            draw.line([(x, 0), (x, height)], fill=grid_color, width=grid_width)
            draw.text((x, 0), str(x), fill=grid_color, font=font)
        for y in range(0, height, grid_spacing):
            draw.line([(0, y), (width, y)], fill=grid_color, width=grid_width)
            draw.text((0, y), str(y), fill=grid_color, font=font)

    # Define the positions and sizes for placeholders
    positions = [

#These are the top 2 Conflict years
        {'position': (745, 110), 'size': (265, 275), 'label': '','filename': map_filename_0, 'folder': map_path, 'font_size': 9, 'line_width': 3},       # Year 1
        {'position': (1025, 110), 'size': (265, 275), 'label': '','filename': map_filename_1, 'folder': map_path, 'font_size':9,'line_width': 3},       # Year 1
        {'position': (1305, 110), 'size': (275, 275), 'label': '','filename': map_filename_2, 'folder': map_path, 'font_size':9,'line_width': 3},       # Year 1

#These are the selected conflict years
        {'position': (745, 505), 'size': (265, 275), 'label': '','filename': map_filename_2000, 'folder': map_path, 'font_size':9, 'line_width': 3},       # Year 1
        {'position': (1025, 505), 'size': (265, 275), 'label': '','filename': map_filename_2010, 'folder': map_path, 'font_size':9, 'line_width': 3},       # Year 1
        {'position': (1305, 505), 'size': (265, 275), 'label': '','filename': map_filename_2020, 'folder': map_path, 'font_size':9, 'line_width': 3},       # Year 1


        {'position': (50, 225), 'size': (550, 275), 'label': '','filename': return_period_table_fileneame, 'folder': return_period_table_path,'font_size':1, 'line_width': 3},     # Payout Legend 
       
        #{'position': (375, 500), 'size': (250, 375), 'label': '','filename': annual_table_filename, 'folder': annual_table_path,'font_size':1},     # Payout Legend 
        {'position': (50, 550), 'size': (550, 300), 'label': '','filename': return_period_lineplot_fileneame, 'folder': return_period_lineplot_path,'font_size':1, 'line_width': 0},     # Payout Legend 

        #{'position': (425, 575), 'size': (400, 50), 'label': 'Legend'},     # Payout Legend Title
        #{'position': (925, 100), 'size': (650, 50), 'label': 'Legend'},     # Payout Legend Title

    ]

        # Define the positions and sizes for text boxes
    text_boxes = [
        #{'position': (425, 575), 'size': (400, 50), 'label': 'Payout Legend','font_size': 24},     # Payout Legend Title
        #{'position': (925, 100), 'size': (650, 50), 'label': 'Top Conflict Years','font_size': 32},     # Payout Legend Title
        #{'position': (65, 215), 'size': (270, 325), 'label':  summary_text,'font_size': 15}
    ]

    title = [
        #{'position': (425, 575), 'size': (400, 50), 'label': 'Payout Legend','font_size': 24},     # Payout Legend Title
        #{'position': (925, 100), 'size': (650, 50), 'label': 'Top Conflict Years','font_size': 32},     # Payout Legend Title
        {'position': (50, 25), 'size': (600, 125), 'label':  country, 'font_size': 92}
    ]

    title_boxes = [
        {'position': (50, 175), 'size': (550, 35), 'label': 'Return period labels and threshold values','font_size': 18, 'background_color': 'darkgrey', 'line_width': 2, 'text_color': 'white'},     # Payout Legend Title

        {'position': (800, 385), 'size': (150, 35), 'label': year__0,'font_size': 24, 'background_color': None, 'line_width': 0, 'text_color': 'black'},     # Year Label for Top year
        {'position': (1085, 385), 'size': (150, 35), 'label': year__1,'font_size': 24, 'background_color': None, 'line_width': 0, 'text_color': 'black'},     # Year Label for Top 2 year
        {'position': (1355, 385), 'size': (150, 35), 'label': year__2,'font_size': 24, 'background_color': None, 'line_width': 0, 'text_color': 'black'},     # Year Label for Top 3 year

        {'position': (800, 785), 'size': (150, 35), 'label': '2000','font_size': 24, 'background_color': None, 'line_width': 0, 'text_color': 'black'},     # empty text box
        {'position': (1085, 785), 'size': (150, 35), 'label':  '2010','font_size': 24, 'background_color': None, 'line_width': 0, 'text_color': 'black'},
        {'position': (1355, 785), 'size': (150, 35), 'label':  '2020','font_size': 24, 'background_color': None, 'line_width': 0, 'text_color': 'black'}

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
        background_color = title_b['background_color']  # Get the font size from the dictionary
        line_width = title_b['line_width']
        text_color = title_b['text_color']
            # Create a font object with the specified size
        try:
            font = ImageFont.truetype(font_path, font_size)  # Use a valid font on your system
        except IOError:
            font = ImageFont.load_default()

    #     Draw a rectangle around the text box area with a dark grey background
        draw.rectangle([x, y, x + w, y + h], fill= background_color, outline="black", width=line_width)

    #     # Calculate the bounding box of the text
        text_bbox = draw.textbbox((0, 0), label, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

         # Calculate the position to center the text
        text_x = x + (w - text_width) / 2
        text_y = y + (h - text_height) / 3

    #     # Draw the text centered in the box with white color
        draw.text((text_x, text_y), label, fill=text_color, font=font)
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

    #Draw rectangles at specified positions
    for pos in positions:
        x, y = pos['position']
        w, h = pos['size']
        line_width = pos['line_width']  # Get the line width from the dictionary
        draw.rectangle([x, y, x + w, y + h], outline="black", width=line_width)
        draw.text((x, y - 20), pos['label'], fill="black")
        font_size = pos['font_size']  # Get the font size from the dictionary

        try:
            font = ImageFont.truetype(font_path, font_size)  # Use a valid font on your system
        except IOError:
            font = ImageFont.load_default()

    # Save and show the template with marked positions
    #marked_template_path = '/Users/gbenz/Desktop/tmp.png'
            
        # Save the final image with a specified filename
    if returnperiodmethod == 'Event year':
        return_period_definition = 'bigp'
    else:
        return_period_definition = 'littlep'


    output_filename = os.path.join(output_path, f'event_cat_rp_{country}_{aggregation_string}_{return_period_definition}_{year_datastart}_{year_dataend}.png')
    output_filename = output_filename.replace(' ', '_')

    print()
    print('file saved to:')
    print(output_filename)
    template_image.save(output_filename)
    template_image.show()


def map_event_cat_rp_2x2(country, method, returnperiodmethod, aggregation='0', gridlines='no'): 

    """ 
    This was built as a secondary option to map_event_cat_rp. If deployed, user should first consult the map_event_cat_rp code to keep references consistent.

    """

    base_directory = os.getcwd()
    font_path = base_dir + '/src/utils/functions_for_graphics/layout_formats/OpenSans-VariableFont.ttf'
    template_path = base_dir + '/src/utils/functions_for_graphics/layout_formats/PRIO Layout Method 3_1.png'
    template_image = Image.open(template_path)


    if aggregation == '1':
        aggregation_string = aggregation + 'x' + aggregation

        map_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + 'map_png/'
        print(map_path)
        annual_table_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/' + aggregation_string + '/table_png/'
        print(annual_table_path)
        return_period_table_path = base_directory + '/files/' + country + '/' + method + '/' + returnperiodmethod  + '/table_png/percentile and payout table/'
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
    map_filename_0 = find_file_with_string(map_path, 'conflict year 0') # looking for a 3.5 x 3.5 map 
    print(f'located map rank1: {map_filename_0}')
    #Map 2
    map_filename_1 = find_file_with_string(map_path, 'conflict year 1 ') # looking for a 3.5 x 3.5 map
    print(f'located map rank 2: {map_filename_1}')
    #Map 3
    map_filename_2010 = find_file_with_string(map_path, '2010') # looking for a 3.5 x 3.5 map
    print(map_filename_2010)
    #Map 4
    map_filename_2020 = find_file_with_string(map_path, '2020') # looking for a 3.5 x 3.5 map
    print(map_filename_2020)
    #Map 5
    #Map 6


    annual_table_filename = find_file_with_string(annual_table_path, '4.0x5.5') #  looking for a 2.5 x 1.75 map 4_0x5_5
    print(f'located lineplot file in folder: {annual_table_filename}')

    return_period_table_fileneame = find_file_with_string(return_period_table_path, '2.5x1.8')
    print(f'located lineplot file in folder: {return_period_table_fileneame}')
    
    return_period_lineplot_fileneame = find_file_with_string(return_period_lineplot_path, '6.0x3.0')
    print(f'located lineplot file in folder: {return_period_lineplot_fileneame}')



    # Load the template image
    #template_path = 'Slide 1 Option B Template.png'

    template_image = template_image.resize((1620, 915), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(template_image)



    # Define grid parameters
    grid_spacing = 50  # Adjust the spacing as needed
    grid_color = "blue"
    grid_width = 1

    # Define the font for the grid labels
    font = ImageFont.load_default()

    # Get the dimensions of the template image
    width, height = template_image.size

    if gridlines == 'yes':
    # Draw the grid
        for x in range(0, width, grid_spacing):
            draw.line([(x, 0), (x, height)], fill=grid_color, width=grid_width)
            draw.text((x, 0), str(x), fill=grid_color, font=font)
        for y in range(0, height, grid_spacing):
            draw.line([(0, y), (width, y)], fill=grid_color, width=grid_width)
            draw.text((0, y), str(y), fill=grid_color, font=font)

    # Define the positions and sizes for placeholders
    positions = [

#These are the top 2 Conflict years
        {'position': (765, 110), 'size': (325, 325), 'label': '','filename': map_filename_0, 'folder': map_path, 'font_size': 9, 'line_width': 3},       # Year 1
        {'position': (1215, 110), 'size': (325, 325), 'label': '','filename': map_filename_1, 'folder': map_path, 'font_size':9,'line_width': 3},       # Year 1
        
#These are the selected conflict years
        {'position': (765, 505), 'size': (325, 325), 'label': '','filename': map_filename_2010, 'folder': map_path, 'font_size':9, 'line_width': 3},       # Year 1
        {'position': (1215, 505), 'size': (325, 325), 'label': '','filename': map_filename_2020, 'folder': map_path, 'font_size':9, 'line_width': 3},       # Year 1

        {'position': (50, 225), 'size': (550, 275), 'label': '','filename': return_period_table_fileneame, 'folder': return_period_table_path,'font_size':1, 'line_width': 3},     # Payout Legend 
       
        #{'position': (375, 500), 'size': (250, 375), 'label': '','filename': annual_table_filename, 'folder': annual_table_path,'font_size':1},     # Payout Legend 
        {'position': (50, 550), 'size': (550, 300), 'label': '','filename': return_period_lineplot_fileneame, 'folder': return_period_lineplot_path,'font_size':1, 'line_width': 0},     # Payout Legend 

        #{'position': (425, 575), 'size': (400, 50), 'label': 'Legend'},     # Payout Legend Title
        #{'position': (925, 100), 'size': (650, 50), 'label': 'Legend'},     # Payout Legend Title

    ]

        # Define the positions and sizes for text boxes
    text_boxes = [
        #{'position': (425, 575), 'size': (400, 50), 'label': 'Payout Legend','font_size': 24},     # Payout Legend Title
        #{'position': (925, 100), 'size': (650, 50), 'label': 'Top Conflict Years','font_size': 32},     # Payout Legend Title
        #{'position': (65, 215), 'size': (270, 325), 'label':  summary_text,'font_size': 15}
    ]

    title = [
        #{'position': (425, 575), 'size': (400, 50), 'label': 'Payout Legend','font_size': 24},     # Payout Legend Title
        #{'position': (925, 100), 'size': (650, 50), 'label': 'Top Conflict Years','font_size': 32},     # Payout Legend Title
        {'position': (50, 25), 'size': (600, 125), 'label':  country, 'font_size': 92}
    ]

    title_boxes = [
        {'position': (50, 175), 'size': (550, 35), 'label': 'Payout Legend','font_size': 18},     # Payout Legend Title
        #{'position': (750, 25), 'size': (800, 35), 'label': 'Top Conflict Years','font_size': 24},     # Payout Legend Title
        #{'position': (750, 450), 'size': (800, 35), 'label': 'Selected Conflict Years','font_size': 24},     # Payout Legend Title
        #{'position': (50, 200), 'size': (300, 350), 'label': '','font_size': 32},     # empty text box

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
    # for box in text_boxes:
    #     x, y = box['position']
    #     w, h = box['size']
    #     label = box['label']
    #     font_size = box['font_size']  # Get the font size from the dictionary

    #     # Create a font object with the specified size
    #     try:
    #         font = ImageFont.truetype(font_path, font_size)  # Use a valid font on your system
    #     except IOError:
    #         font = ImageFont.load_default()

    #     # Draw a rectangle around the text box area with a dark grey background
    #     #draw.rectangle([x, y, x + w, y + h], fill="white", outline="white", width=2)
    #     #draw.rectangle([x, y, x + w, y + h])

    #     # Wrap the text to fit inside the box
    #     wrapped_text = []
    #     words = label.split()
    #     line = ""

    #     for word in words:
    #         # Add the word to the line and check if it fits
    #         test_line = line + word + " "
    #         text_bbox = draw.textbbox((0, 0), test_line, font=font)
    #         test_width = text_bbox[2] - text_bbox[0]

    #         if test_width <= w:
    #             line = test_line
    #         else:
    #             # If the line is too long, add the current line to wrapped_text and start a new line
    #             wrapped_text.append(line.strip())
    #             line = word + " "

    #     # Add the last line
    #     wrapped_text.append(line.strip())

    #     # Draw the text line by line, adjusting the position
    #     current_y = y
    #     for line in wrapped_text:
    #         draw.text((x, current_y), line, fill="black", font=font)
    #         current_y += font_size  # Move to the next line

    #     # Ensure that the text doesn't overflow the box height
    #     if current_y > y + h:
    #         print("Warning: Text overflow in the box. Consider reducing the font size or the amount of text.")

#-------------------------------------------------------------------------------------------------------------------------------------------------------         
#-------------------------------------------------------------------------------------------------------------------------------------------------------         

    #Draw rectangles at specified positions
    for pos in positions:
        x, y = pos['position']
        w, h = pos['size']
        line_width = pos['line_width']  # Get the line width from the dictionary
        draw.rectangle([x, y, x + w, y + h], outline="black", width=line_width)
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