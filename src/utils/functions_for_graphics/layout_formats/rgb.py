import matplotlib.colors as mcolors

def rgb_to_hex(rgb):
    return mcolors.to_hex([x/255.0 for x in rgb])