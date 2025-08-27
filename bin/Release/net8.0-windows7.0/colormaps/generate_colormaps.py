import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# import matplotlib.pyplot as plt
# import cmocean
# from PIL import Image
# import numpy as np

# for cmap_name in cmocean.cm.cmapnames:
#     gradient = np.linspace(0, 1, 256).reshape(1, -1)
#     fig, ax = plt.subplots(figsize=(2.56, 0.3), dpi=100)
#     ax.imshow(gradient, aspect='auto', cmap=getattr(cmocean.cm, cmap_name))
#     ax.axis('off')
#     path = f"{cmap_name}.png"
#     plt.savefig(path, bbox_inches='tight', pad_inches=0)
#     plt.close(fig)


import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

# List of colormaps you want previews for
colormaps = [
    "turbo", "jet", "viridis", "plasma", "inferno", "magma", "cividis",
    "cool", "hot", "spring", "summer", "autumn", "winter"
]

# Gradient to show
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

for cmap_name in colormaps:
    fig, ax = plt.subplots(figsize=(2.5, 0.3), dpi=100)
    ax.imshow(gradient, aspect="auto", cmap=cm.get_cmap(cmap_name))
    ax.set_axis_off()
    
    # Save PNG with transparent background
    plt.savefig(f"{cmap_name}.png", bbox_inches="tight", pad_inches=0, dpi=100, transparent=True)
    plt.close(fig)

print("✅ Colormap previews saved")
