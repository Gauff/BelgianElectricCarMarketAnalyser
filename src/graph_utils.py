import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


def generate_color_scale(size, cmap_name="viridis"):
    """
    Generate a color scale with the specified number of colors.

    Parameters:
    - size (int): The number of colors in the scale.
    - cmap_name (str): The name of the colormap to use. Defaults to 'viridis'.

    Returns:
    - List of color codes in hex format.
    """
    cmap = plt.get_cmap(cmap_name)
    color_scale = [mcolors.to_hex(cmap(i / (size - 1))) for i in range(size)]
    color_scale[0] = "#808080"
    return color_scale


def generate_log_marks(min_val, max_val):
    min_exp = int(np.floor(np.log10(min_val)))
    max_exp = int(np.ceil(np.log10(max_val)))
    marks = {10**i: {"label": str(10**i)} for i in range(min_exp, max_exp + 1)}
    return marks


if __name__ == "__main__":

    Viridis = generate_color_scale(10)
    print("Viridis =", Viridis)
