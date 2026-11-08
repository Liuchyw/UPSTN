"""Selected A3 and raw error clouds with full-range node-intervention ECDFs."""
from pathlib import Path
import json
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from scatter_layout import compact_rectangles
from data import load_main_data, empirical_cdf, SEEDS
HERE = Path(__file__).resolve().parent
OUT, DATA = (HERE / 'output', HERE / 'source_data')
None
LOSSES = [('spatial', 'Spatial', '#208DB0'), ('temporal', 'Temporal', '#E1A12B'), ('contrastive', 'Contrast', '#8B5BB3'), ('deviation', 'Alignment', '#D3614B'), ('combined', 'Combined', '#334E68')]
SEED_COLORS = ['#3675A8', '#CC7C39', '#51896E']
VIEW_COLORS = {'spatial': '#0072BD', 'historical': '#D95319'}
plt.style.use('default')
plt.rcParams.update({'font.family': 'Times New Roman', 'font.serif': ['Times New Roman'], 'font.size': 8, 'axes.labelsize': 8, 'axes.titlesize': 8.5, 'xtick.labelsize': 7.3, 'ytick.labelsize': 7.3, 'legend.fontsize': 7, 'legend.frameon': False, 'axes.edgecolor': 'black', 'axes.linewidth': 0.65, 'axes.grid': False, 'xtick.direction': 'in', 'ytick.direction': 'in', 'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none', 'savefig.facecolor': 'white', 'path.simplify': False})

def title(ax, text, pad=8):
    ax.set_title(text, loc='left', pad=pad, fontsize=8.5, fontweight='bold')

def gradient(ax, data):
    assert np.isfinite(data.norm_ratio).all() and (data.norm_ratio > 0).all()
    assert np.isfinite(data.area_within_pt2).all() and (data.area_within_pt2 > 0).all()
    for loss, label, color in LOSSES:
        part = data[data.loss == loss].sort_values('area_within_pt2', ascending=False)
        ax.scatter(part.cosine, part.norm_ratio, s=part.area_within_pt2, color=color, marker='o', edgecolors='none', linewidths=0, alpha=0.88)
    ax.set_yscale('log')
    ax.set_xlim(-0.34, 0.34)
    ax.set_ylim(0.012, 17)
    ax.set_xticks([-0.3, 0, 0.3])
    ax.set_yticks([0.02, 0.1, 1, 10], ['0.02', '0.1', '1', '10'])
    ax.set_xlabel('Cosine with prediction')
    ax.set_ylabel('Auxiliary / prediction norm')
    title(ax, '(a) Encoder gradients')
    handles = [Line2D([], [], marker='o', ls='None', color=c, ms=3, label=n) for _, n, c in LOSSES]
    sizes = [Line2D([], [], marker='o', ls='None', color='#777777', markeredgewidth=0, ms=np.sqrt(24 * value), label='%s×' % value) for value in [0.5, 1, 4]]
    ax.figure.legend(handles=sizes, title='Area: norm / objective median', title_fontsize=6.8, loc='upper center', bbox_to_anchor=(0.23, 0.94), ncol=3, handlelength=0.9, handletextpad=0.3, columnspacing=0.8, fontsize=7)
    return handles

def node_ecdf(ax, nodes, dataset, letter):
    colors = {'prototype': '#0072BD', 'full': '#D95319'}
    part = nodes[nodes.dataset == dataset]
    low, high = np.quantile(part.delta_mae, [0.05, 0.95])
    inset = ax.inset_axes([0.59, 0.1, 0.38, 0.43])
    for role in ['prototype', 'full']:
        x, y = empirical_cdf(part[part.role == role].delta_mae.to_numpy())
        ax.step(np.r_[x[0], x], np.r_[0, y], where='post', color=colors[role], lw=1.0)
        interior = (x > low) & (x < high)
        xx = np.r_[low, x[interior], high]
        yy = np.r_[np.searchsorted(x, low, side='right') / len(x), y[interior], np.searchsorted(x, high, side='right') / len(x)]
        inset.step(xx, yy, where='post', color=colors[role], lw=0.75)
    span = part.delta_mae.max() - part.delta_mae.min()
    ax.set_xlim(part.delta_mae.min() - span * 0.04, part.delta_mae.max() + span * 0.04)
    ax.set_ylim(0, 1.02)
    ax.set_yticks([0, 0.5, 1])
    ax.set_xticks([-0.05, 0, 0.05] if dataset == 'JiNan' else [-0.2, 0, 0.2, 0.4, 0.6])
    ax.axvline(0, color='black', ls='--', lw=0.55)
    ax.set_ylabel('Cumulative fraction of nodes', fontsize=7.5)
    ax.set_xlabel('ΔMAE (normalized)' if dataset == 'JiNan' else 'ΔMAE (mph)')
    title(ax, '(%s) %s · %d nodes' % (letter, dataset, 406 if dataset == 'JiNan' else 207))
    inset.set_xlim(low, high)
    inset.set_ylim(0, 1)
    inset.axvline(0, color='black', ls='--', lw=0.5)
    tick = 0.005 if dataset == 'JiNan' else 0.2
    assert low < 0 < tick < high
    inset.set_xticks([0, tick], ['0', '0.005' if dataset == 'JiNan' else '0.2'])
    inset.set_yticks([0, 1], ['0', '1'])
    inset.tick_params(labelsize=6.2, length=1.5, width=0.5, pad=2)
    inset.set_title('Central 90%', fontsize=6.3, pad=3)
    for spine in inset.spines.values():
        spine.set_linewidth(0.5)
    return (inset, dict(dataset=dataset, low=float(low), high=float(high), full_ecdf_denominator=True))

def main():
    OUT.mkdir(exist_ok=True)
    DATA.mkdir(exist_ok=True)
    d = load_main_data()
    fig, axes = plt.subplots(3, 3, figsize=(183 / 25.4, 172 / 25.4), gridspec_kw={'height_ratios': [1.6, 1, 1]})
    fig.subplots_adjust(left=0.085, right=0.985, bottom=0.07, top=0.84, wspace=0.43, hspace=0.75)
    before_rectangles = np.array([ax.get_position().bounds for ax in axes.ravel()])
    width_pt, height_pt = fig.get_size_inches() * 72
    scatter_rectangles = compact_rectangles(before_rectangles[3:], width_pt, height_pt)
    for ax, rectangle in zip(axes.ravel()[3:], scatter_rectangles):
        ax.set_position(rectangle)
    after_rectangles = np.array([ax.get_position().bounds for ax in axes.ravel()])
    np.testing.assert_array_equal(before_rectangles[:3], after_rectangles[:3])
    objectives = gradient(axes[0, 0], d['gradient'])
    insets, inset_records = ([], [])
    for ax, dataset, letter in zip(axes[0, 1:], ['JiNan', 'METR-LA'], ['b', 'c']):
        inset, record = node_ecdf(ax, d['nodes'], dataset, letter)
        insets.append(inset)
        inset_records.append(record)
    roles = [Line2D([], [], color=c, lw=1.2, label=n) for n, c in [('Prototype', '#0072BD'), ('Joint', '#D95319')]]
    fig.legend(handles=roles, loc='upper center', bbox_to_anchor=(0.69, 0.98), ncol=2, fontsize=7.5, handlelength=1.8, columnspacing=1.5)
    fig.text(0.69, 0.925, 'ΔMAE = alignment on − alignment off · seed 42', ha='center', fontsize=7)
    fig.legend(handles=objectives, loc='upper center', bbox_to_anchor=(0.23, 0.995), ncol=3, handlelength=0.6, handletextpad=0.3, columnspacing=1, fontsize=7)
    corr = d['correlations']
    max_x = max((x.max() for x, y in d['clouds'].values()))
    for row, view in enumerate(['spatial', 'historical'], 1):
        for col, seed in enumerate(SEEDS):
            ax = axes[row, col]
            x, y = d['clouds'][seed, view]
            visible = y <= 0.5
            ax.scatter(x[visible], y[visible], s=0.5, color=VIEW_COLORS[view], alpha=0.35, marker='o', edgecolors='none', linewidths=0, rasterized=True)
            ax.set_xlim(-0.015, max_x * 1.025)
            ax.set_ylim(0, 0.5)
            ax.set_xticks([0, 0.5, 1, 1.5])
            ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
            title(ax, '(%s) %s · seed %d' % ('defghi'[(row - 1) * 3 + col], view.capitalize(), seed), pad=17)
            r = corr[(corr.seed == seed) & (corr.view == view)].pearson
            display_mean = 0 if abs(r.mean()) < 0.005 else r.mean()
            ax.text(0.02, 1.02, 'r = %.2f ± %.2f; %d above 0.5' % (display_mean, r.std(ddof=1), (~visible).sum()), transform=ax.transAxes, fontsize=6.8, va='bottom')
            if col == 0:
                ax.set_ylabel('Normalized MAE')
            else:
                ax.tick_params(labelleft=False)
            if row == 2:
                ax.set_xlabel('Relative view distance')
    fig.canvas.draw()
    fig.savefig(OUT / 'Figure4_node_effects_main.pdf', dpi=600)
    fig.savefig(OUT / 'Figure4_node_effects_main.svg', dpi=600)
    fig.savefig(OUT / 'Figure4_node_effects_main.png', dpi=600)
    plt.close(fig)
    for name in ['gradient', 'rank', 'correlations', 'counts', 'intervention', 'nodes']:
        d[name].to_csv(DATA / (name + '.csv'), index=False)
    report = dict(input_hashes=d['input_hashes'], observations_per_cloud=32480, seeds=SEEDS, batches_per_seed=5, gradient_points=75, rank_points=45, table6_intervention_points_retained=12, node_effect_points=1226, node_effect_seed=42, rank_plot_removed_but_values_retained=True, cloud_detail_ylim=[0, 0.5], full_data_statistics=True, full_range_companion='../figure4_raw_20261108/output/C_view_error_clouds_full.pdf', independent_replicates='training seeds; node-windows and batches are nested', training_performed=False, selected_A3_coordinates_and_area_preserved=True)
    report['scatter_raster_dpi'] = 600
    report['other_marks_text_axes_remain_vector'] = True
    report['ecdf_insets'] = inset_records
    report['scatter_layout'] = dict(before_rectangles=before_rectangles.tolist(), after_rectangles=after_rectangles.tolist(), figure_width_pt=float(width_pt), figure_height_pt=float(height_pt), horizontal_gap_pt=24, vertical_gap_pt=40, upper_three_panels_unchanged=True, outer_scatter_bounds_unchanged=True)
    (HERE / 'numeric_qa.json').write_text(json.dumps(report, indent=2), encoding='utf8')
    print('Rendered node-effect main Figure 4.', flush=True)
if __name__ == '__main__':
    main()
