import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib.pyplot as plt
import cmocean
from PIL import Image
import numpy as np

for cmap_name in cmocean.cm.cmapnames:
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    fig, ax = plt.subplots(figsize=(2.56, 0.3), dpi=100)
    ax.imshow(gradient, aspect='auto', cmap=getattr(cmocean.cm, cmap_name))
    ax.axis('off')
    path = f"{cmap_name}.png"
    plt.savefig(path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

# Virdis, jet, turbo, and the reversed versions of the colormaps