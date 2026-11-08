from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch, Rectangle
import numpy as np
import pandas as pd
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'], 'svg.fonttype': 'none', 'pdf.fonttype': 42, 'font.size': 7.5, 'axes.titlesize': 9, 'axes.labelsize': 7.5, 'axes.linewidth': 0.75, 'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5})
BLUE = '#3F78B5'
BLUE_DARK = '#24558A'
ORANGE = '#D98245'
GREEN = '#4F8A66'
EDGE = '#AEB7C0'
FRAME = '#667686'

def region_bounds(coords, center_idx, half_lon, half_lat):
    lon, lat = coords[center_idx]
    return (lon - half_lon, lon + half_lon, lat - half_lat, lat + half_lat)

def in_bounds(coords, bounds):
    x0, x1, y0, y1 = bounds
    return (coords[:, 0] >= x0) & (coords[:, 0] <= x1) & (coords[:, 1] >= y0) & (coords[:, 1] <= y1)

def choose_regions(coords):
    """Choose dense and sparse examples inside the requested coordinate crop."""
    lat0 = np.deg2rad(coords[:, 1].mean())
    scaled = np.column_stack([coords[:, 0] * np.cos(lat0), coords[:, 1]])
    dist = np.sqrt(((scaled[:, None, :] - scaled[None, :, :]) ** 2).sum(axis=2))
    radius = 0.012
    local_count = (dist <= radius).sum(axis=1)
    dense_idx = int(np.argmax(local_count))
    sparse_candidates = np.where((local_count >= 3) & (local_count <= np.quantile(local_count, 0.3)))[0]
    sparse_idx = int(sparse_candidates[np.argmax(dist[dense_idx, sparse_candidates])])
    dense = region_bounds(coords, dense_idx, 0.021, 0.021)
    sparse = region_bounds(coords, sparse_idx, 0.021, 0.021)
    return (dense, sparse)

def draw_network(ax, nodes, edges, bounds=None, highlight=None, node_size=7):
    lookup = nodes.set_index('node')[['longitude', 'latitude']]
    if bounds is None:
        visible = np.ones(len(nodes), dtype=bool)
    else:
        visible = in_bounds(nodes[['longitude', 'latitude']].to_numpy(), bounds)
    visible_ids = set(nodes.loc[visible, 'node'].astype(int))
    for row in edges.itertuples(index=False):
        source, target = (int(row[0]), int(row[1]))
        if source not in lookup.index or target not in lookup.index:
            continue
        if bounds is not None and source not in visible_ids and (target not in visible_ids):
            continue
        p0, p1 = (lookup.loc[source], lookup.loc[target])
        ax.plot([p0.longitude, p1.longitude], [p0.latitude, p1.latitude], color=EDGE, lw=0.42, alpha=0.6, zorder=1)
    pts = nodes.loc[visible]
    colors = highlight if highlight is not None else BLUE
    ax.scatter(pts.longitude, pts.latitude, s=node_size, c=colors, edgecolors='white', linewidths=0.25, alpha=0.92, zorder=3)
    if bounds is not None:
        ax.set_xlim(bounds[0], bounds[1])
        ax.set_ylim(bounds[2], bounds[3])

def style_map(ax, mean_lat, show_coordinates=False):
    ax.set_aspect(1 / np.cos(np.deg2rad(mean_lat)))
    for spine in ax.spines.values():
        spine.set_color(FRAME)
        spine.set_linewidth(0.65)
    if show_coordinates:
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.tick_params(direction='out', length=2.5, width=0.55, colors='#525A62')
    else:
        ax.set_xticks([])
        ax.set_yticks([])
