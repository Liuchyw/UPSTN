"""Plain Matplotlib small multiples and an unfiltered fixed-day forecast case."""
from pathlib import Path
import csv
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
CONFIGS = ['Prototype', '+Spatial', '+Temporal', 'Joint']
SEEDS = [42,123,456]
HERE = Path(__file__).resolve().parent
OUT = HERE / 'output'
None

def setup():
    plt.style.use('default')
    plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 7, 'axes.labelsize': 6.7, 'axes.titlesize': 7.3, 'xtick.labelsize': 6.2, 'ytick.labelsize': 6.2, 'legend.fontsize': 6.5, 'legend.frameon': False, 'axes.linewidth': 0.6, 'pdf.fonttype': 42, 'svg.fonttype': 'none', 'path.simplify': False, 'xtick.direction': 'in', 'ytick.direction': 'in'})

def style(ax):
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(length=2.2, pad=2)
    ax.grid(color='#DDDDDD', linewidth=0.35)
    ax.set_axisbelow(True)

def save(fig, stem, axes, **kwargs):
    fig.canvas.draw()
    fig.savefig(OUT / (stem + '.pdf'))
    fig.savefig(OUT / (stem + '.svg'))
    fig.savefig(OUT / (stem + '.png'), dpi=300)
    plt.close(fig)

def panel_b():
    rows = list(csv.DictReader((HERE / 'source_data/horizon_differences.csv').open()))
    fig, axes = plt.subplots(2, 2, figsize=(99 / 25.4, 50 / 25.4), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.17, right=0.98, bottom=0.15, top=0.77, wspace=0.45, hspace=0.55)
    fig.text(0.015, 0.98, '(b) Do auxiliary objectives help?', va='top', weight='bold', fontsize=8.8)
    colors = ['#0072BD', '#D95319', '#228833']
    for ax, name in zip(axes.flat, CONFIGS):
        style(ax)
        for seed, color in zip(SEEDS, colors):
            part = [r for r in rows if r['configuration'] == name and int(r['seed']) == seed]
            assert [int(r['horizon']) for r in part] == list(range(1, 13))
            ax.plot(range(1, 13), [float(r['display_difference']) for r in part], color=color, linewidth=0.85, alpha=1)
        ax.axhline(0, color='#555555', linewidth=0.55, linestyle='--')
        ax.set(xlim=(1, 12), ylim=(-1.5, 5), xticks=[1, 6, 12], yticks=[0, 2, 4])
        ax.set_title(name, pad=3)
    fig.legend(handles=[Line2D([], [], color=c, lw=1, label=str(s)) for s, c in zip(SEEDS, colors)], title='Training seed', title_fontsize=6.5, loc='upper center', bbox_to_anchor=(0.58, 0.915), ncol=3, handlelength=1.5, columnspacing=1, borderaxespad=0)
    fig.text(0.02, 0.47, 'MAE − prediction-only (×10⁻³)', rotation=90, va='center', fontsize=6.7)
    fig.text(0.57, 0.015, 'Forecast horizon', ha='center', fontsize=6.7)
    save(fig, 'b_paired_horizon_differences', list(axes.flat))

def panel_c():
    rows = list(csv.DictReader((HERE / 'source_data/fixed_day.csv').open()))
    d = {k: np.array([float(r[k]) for r in rows]) for k in rows[0]}
    h = d['hour']
    fig = plt.figure(figsize=(99 / 25.4, 53 / 25.4))
    fig.text(0.015, 0.985, '(c) What is the loss-specific effect?', va='top', weight='bold', fontsize=8.8)
    fig.text(0.57, 0.88, 'Node 210 · seed 42 · one-step forecasts', ha='center', fontsize=6.5)
    main = fig.add_axes([0.17, 0.53, 0.44, 0.18])
    detail = fig.add_axes([0.79, 0.53, 0.19, 0.18])
    err = fig.add_axes([0.17, 0.15, 0.81, 0.2])
    for ax in [main, detail, err]:
        style(ax)
    series = [('truth', '#222222', 'Truth'), ('full_on', '#0072BD', 'Alignment on'), ('full_off', '#D95319', 'Alignment off')]
    for key, color, label in series:
        main.plot(h, d[key], color=color, linewidth=0.65, alpha=1, label=label)
        select = (h >= 7) & (h <= 9)
        detail.plot(h[select], d[key][select], color=color, linewidth=0.65, alpha=1)
    main.set(xlim=(0, 24), ylim=(0, 150), xticks=[0, 12, 24], yticks=[0, 75, 150], ylabel='Traffic flow')
    selected = np.concatenate([d[k][select] for k, _, _ in series])
    low = max(0, float(selected.min()) - 4)
    high = min(150, float(selected.max()) + 4)
    main.add_patch(Rectangle((7, low), 2, high - low, fill=False, edgecolor='#666666', linewidth=0.6))
    main.set_title('Joint forecasts', pad=3)
    detail.set(xlim=(7, 9), xticks=[7, 8, 9])
    detail.set_title('07:00–09:00', pad=3)
    detail.yaxis.set_major_locator(plt.MaxNLocator(3))
    detail.tick_params(labelsize=5.6)
    fig.legend(*main.get_legend_handles_labels(), loc='upper center', bbox_to_anchor=(0.57, 0.84), ncol=3, handlelength=1.4, handletextpad=0.3, columnspacing=0.65, borderaxespad=0)
    for key, color, label in [('prototype_error_difference', '#7E2F8E', 'Prototype'), ('joint_error_difference', '#228833', 'Joint')]:
        err.plot(h, d[key], color=color, linewidth=0.6, alpha=1, label=label)
    err.axhline(0, color='#555555', linestyle='--', linewidth=0.55)
    err.set(xlim=(0, 24), ylim=(-21, 21), xticks=[0, 6, 12, 18, 24], yticks=[-20, 0, 20], xlabel='Hour of day', ylabel='Error: On − Off')
    err.set_title('Local absolute-error change', loc='left', pad=8)
    err.legend(loc='lower right', bbox_to_anchor=(1, 1.04), ncol=2, handlelength=1.3, columnspacing=0.8, borderaxespad=0)
    save(fig, 'c_fixed_day_loss_effects', [main, detail, err], panel_ids=['forecast', 'zoom', 'error'], row_groups=[dict(id='forecast-row', panels=['forecast', 'zoom'])], column_groups=[], exemptions=[dict(panels=['forecast', 'zoom', 'error'], checks=['column', 'panel-width'], reason='Case plot, fixed-time zoom and full-width error plot have deliberately unequal spans.')])
if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    setup()
    panel_b()
    panel_c()
