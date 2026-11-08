"""Compact panel a using the unchanged empirical series and geographic regions."""
from pathlib import Path
import hashlib
import json
import sys
import importlib.util
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch
HERE = Path(__file__).resolve().parent
ROOT = HERE
OUT = HERE / 'output'
None

def main():
    import geo_helpers as original
    weekly_path = HERE / 'source_data/weekly.csv'
    nodes_path = HERE / 'source_data/nodes.csv'
    edges_path = HERE / 'source_data/edges.csv'
    weekly = pd.read_csv(weekly_path)
    nodes = pd.read_csv(nodes_path)
    edges = pd.read_csv(edges_path)
    assert len(weekly) == 2016 and len(nodes) == 406
    coords = nodes[['longitude', 'latitude']].to_numpy()
    crop = (118.0, 118.4, 37.8, 38.0)
    mask = original.in_bounds(coords, crop)
    dense, sparse = original.choose_regions(coords[mask])
    counts = [int(original.in_bounds(coords[mask], bounds).sum()) for bounds in [dense, sparse]]
    assert counts == [56, 5], counts
    mean_lat = float(nodes.loc[mask, 'latitude'].mean())
    plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 6.2, 'axes.titlesize': 7.2, 'axes.labelsize': 6.2, 'xtick.labelsize': 5.8, 'ytick.labelsize': 5.8, 'pdf.fonttype': 42, 'svg.fonttype': 'none', 'path.simplify': False})
    fig = plt.figure(figsize=(80 / 25.4, 105 / 25.4))
    fig.text(0.015, 0.985, '(a) Complementary traffic information', va='top', weight='bold', fontsize=8.8)
    ax = fig.add_axes([0.16, 0.645, 0.78, 0.23])
    x = weekly.weekday_slot.to_numpy()
    ax.axvspan(5 * 288, 7 * 288, color='#F2F3F4', zorder=0)
    ax.fill_between(x, weekly.q25, weekly.q75, color='#D9E3EF', linewidth=0, label='Interquartile range')
    ax.plot(x, weekly['median'], color='#3D6FA6', lw=0.85, label='Median network flow')
    for day in range(1, 7):
        ax.axvline(day * 288, color='#D4D8DC', lw=0.4, zorder=0)
    ax.set(xticks=np.arange(7) * 288 + 144, xticklabels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], xlim=(0, 2015), ylim=(0, 95), yticks=[0, 20, 40, 60, 80], ylabel='Traffic flow', xlabel='Time of week')
    ax.set_title('JiNan typical weekly traffic pattern', loc='left', pad=4, weight='bold')
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(length=2, pad=2)
    fig.legend(*ax.get_legend_handles_labels(), loc='upper center', bbox_to_anchor=(0.55, 0.947), ncol=2, frameon=False, fontsize=5.5, handlelength=1.3, handletextpad=0.3, columnspacing=0.8, borderaxespad=0)
    geo = fig.add_axes([0.16, 0.14, 0.78, 0.38])
    original.draw_network(geo, nodes, edges, bounds=crop, node_size=3.8)
    original.style_map(geo, mean_lat, show_coordinates=True)
    geo.set_xticks([118.0, 118.1, 118.2, 118.3, 118.4])
    geo.set_yticks([37.8, 37.85, 37.9, 37.95, 38.0])
    geo.tick_params(labelsize=5.8, length=2, pad=2)
    geo.set_title('JiNan sensor network', loc='left', pad=16, fontsize=7.2, weight='bold')
    insets = []
    for bounds, color, label, count, rect in [(dense, original.ORANGE, 'R1', 56, [0.035, 0.57, 0.245, 0.34]), (sparse, original.GREEN, 'R2', 5, [0.715, 0.61, 0.245, 0.3])]:
        ins = geo.inset_axes(rect, zorder=10)
        ins.set_facecolor('white')
        original.draw_network(ins, nodes, edges, bounds=bounds, highlight=color, node_size=5.3)
        original.style_map(ins, mean_lat)
        geo.text(rect[0], 1.015, '(%s) %s (n=%d)' % (label, 'Dense' if label == 'R1' else 'Sparse', count), transform=geo.transAxes, weight='bold', fontsize=5.5, va='bottom')
        geo.add_patch(Rectangle((bounds[0], bounds[2]), bounds[1] - bounds[0], bounds[3] - bounds[2], fill=False, edgecolor=color, linestyle=(0, (3, 2)), linewidth=0.7, zorder=5))
        if label == 'R1':
            geo.text(118.22, 37.832, label, color=color, weight='bold', fontsize=6, va='bottom')
        else:
            geo.text(bounds[0], bounds[3], label, color=color, weight='bold', fontsize=6, va='bottom')
        fig.add_artist(ConnectionPatch(xyA=(bounds[1], (bounds[2] + bounds[3]) / 2), coordsA=geo.transData, xyB=(0, 0.12), coordsB=ins.transAxes, color=color, lw=0.5, ls=(0, (3, 2)), clip_on=False))
        insets.append(ins)
    geo.annotate('N', xy=(0.49, 0.91), xytext=(0.49, 0.78), xycoords='axes fraction', textcoords='axes fraction', ha='center', va='center', fontsize=6.2, arrowprops=dict(arrowstyle='-|>', color='#333333', lw=0.6))
    span = 5 / (111.32 * np.cos(np.deg2rad(mean_lat)))
    sx = 118.0 + 0.07 * 0.4
    sy = 37.8 + 0.07 * 0.2
    geo.plot([sx, sx + span], [sy, sy], color='#333333', lw=0.8)
    for end in [sx, sx + span]:
        geo.plot([end, end], [sy - 0.0016, sy + 0.0016], color='#333333', lw=0.6)
    geo.text(sx + span / 2, sy + 0.0044, '5 km', ha='center', va='bottom', fontsize=5.5)
    fig.text(0.56, 0.04, 'Nodes: sensor coordinates | Edges: recorded connections', ha='center', fontsize=5.5)
    fig.canvas.draw()
    for suffix in ['pdf', 'svg']:
        fig.savefig(OUT / ('a_traffic_structure.' + suffix))
    fig.savefig(OUT / 'a_traffic_structure.png', dpi=300)
    plt.close(fig)
    audit = dict(weekly_slots=2016, nodes=406, visible_nodes=int(mask.sum()), region_counts=counts, dense_bounds=list(dense), sparse_bounds=list(sparse), crop=list(crop), data_changes=False, panel_width_mm=80, panel_height_mm=105, title_font_pt=8.8, source_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [weekly_path, nodes_path, edges_path]})
    (OUT / 'a_data_audit.json').write_text(json.dumps(audit, indent=2))
    print(audit)
if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    main()
