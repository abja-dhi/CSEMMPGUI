from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
from matplotlib.collections import PolyCollection
from mikecore.DfsuFile import DfsuFile
import contextily as ctx
import geopandas as gpd
from pyproj import Transformer, transform, Proj
from matplotlib.animation import Animation, FuncAnimation
from matplotlib.animation import FFMpegWriter
from tqdm import tqdm

def interpolate_to_nodes(num_nodes, elements, element_values):
    """
    Interpolate element-based values to nodes by averaging adjacent element values.
    """
    node_values = np.zeros(num_nodes)
    node_counts = np.zeros(num_nodes)

    for elem, value in zip(elements, element_values):
        for node_idx in elem:
            node_values[node_idx] += value
            node_counts[node_idx] += 1

    # Avoid division by zero
    node_counts[node_counts == 0] = 1
    return node_values / node_counts

def split_quads_to_tris(elements):
    """
    Convert quadrilateral elements to triangles.
    Assumes elements are lists of node indices (length 3 or 4).
    """
    triangles = []
    for elem in elements:
        if len(elem) == 3:
            triangles.append(elem)
        elif len(elem) == 4:
            # Split quad into two triangles
            triangles.append([elem[0], elem[1], elem[2]])
            triangles.append([elem[0], elem[2], elem[3]])
    return triangles

fname = "MT20241002.dfsu"
dfsu = DfsuFile.Open(fname)
nodes = np.stack([dfsu.X, dfsu.Y], axis=-1)
elements = np.stack(dfsu.ElementTable, axis=0) - 1
transformer = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
x_merc, y_merc = transformer.transform(nodes[:, 0], nodes[:, 1])
data = dfsu.ReadItemTimeStep(itemNumber=1, timestepIndex=0).Data * 1000


node_values = interpolate_to_nodes(nodes.shape[0], elements, data)
finite_mask = (np.isfinite(node_values)) & (node_values > 0)
masked_values = np.ma.array(node_values, mask=~finite_mask)
tri_elements = split_quads_to_tris(elements)
triang = tri.Triangulation(x_merc, y_merc, tri_elements)
tri_mask = np.any(~finite_mask[triang.triangles], axis=1)
triang.set_mask(tri_mask)
vmin = 0.01
vmax = 10.0
norm = LogNorm(vmin=vmin, vmax=vmax)

fig, ax = plt.subplots(figsize=(10, 8))

contour = ax.tricontourf(triang, masked_values, levels=np.logspace(np.log10(vmin), np.log10(vmax), 200), cmap='jet', norm=norm, extend='max', alpha=0.5)
ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery)
cbar = fig.colorbar(contour, label='Water Level')
cbar.set_ticks([0.01, 0.1, 1.0, 10.0])
cbar.set_ticklabels(['0.01', '0.1', '1.0', '10.0'])
ax.set_title('Smooth Filled Contour of Water Level')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.axis('equal')
fig.tight_layout()

def update(frame):
    data = dfsu.ReadItemTimeStep(itemNumber=1, timestepIndex=frame).Data * 1000
    node_values = interpolate_to_nodes(nodes.shape[0], elements, data)
    finite_mask = (np.isfinite(node_values)) & (node_values > 0)
    masked_values = np.ma.array(node_values, mask=~finite_mask)
    tri_mask = np.any(~finite_mask[triang.triangles], axis=1)
    triang.set_mask(tri_mask)
    for c in contour.collections:
        c.remove()
    new_contour = ax.tricontourf(triang, masked_values, levels=np.logspace(np.log10(vmin), np.log10(vmax), 200), cmap='jet', norm=norm, extend='max', alpha=0.5)
    contour.collections[:] = new_contour.collections
    ax.set_title(f'Total SSC at Timestep {frame}')
    return new_contour.collections

writer = FFMpegWriter(fps=10, metadata=dict(artist='ABJA'), bitrate=1800)
with writer.saving(fig, "output.mp4", dpi=150):
    for frame in tqdm(range(1, dfsu.NumberOfTimeSteps), desc="Creating animation"):
        update(frame)
        writer.grab_frame()
# ani = FuncAnimation(fig, update, frames=range(1, dfsu.NumberOfTimeSteps), blit=False, repeat=False)
    
# plt.show()
