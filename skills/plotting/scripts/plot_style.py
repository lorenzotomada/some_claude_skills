"""Plotting helper of the `plotting` skill: copy this file into the project (do not retype it).

Tested with matplotlib 3.9. `SciFormatter` overrides private matplotlib methods: check the tick labels
after upgrading matplotlib.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.text import Text
from cycler import cycler

MATHLAB_BLUE = '#065895'
MATHLAB_ORANGE = '#F79A25'
# checked with simulated deuteranopia, protanopia and tritanopia: every pair stays distinguishable
COLORS = [MATHLAB_BLUE, MATHLAB_ORANGE, '#009E73', '#CC79A7', '#56B4E9', '#555555']
LINESTYLES = ['-', '--', '-.', ':']

STYLE = {
    'label_size': 20, 'legend_size': 17, 'tick_size': 17, 'line_width': 2.0, 'figsize': (8, 5),
    'field_cmap': 'viridis', 'error_cmap': 'plasma', 'signed_error_cmap': 'RdBu_r',
    'legend_max_inside': 4,          # more entries -> legend outside
    'sci_decimals': 2,
    'sci_powerlimits': (-2, 3),      # plain numbers in [0.01, 1000) if they fit; (0, 0) = always 10^k
    'max_pdf_mb': 2.0, 'png_dpi': 300,
    'overlap_gap': 2,                # px for find_overlaps in savefig; 0 = only actual overlaps, None = no check
}


def get_style(style=None):
    unknown = set(style or {}) - set(STYLE)
    if unknown:
        raise KeyError(f'unknown style keys: {sorted(unknown)}')
    return {**STYLE, **(style or {})}


def apply_rcparams(style=None):
    s = get_style(style)
    plt.rcParams.update({
        'axes.labelsize': s['label_size'], 'legend.fontsize': s['legend_size'],
        'xtick.labelsize': s['tick_size'], 'ytick.labelsize': s['tick_size'],
        'lines.linewidth': s['line_width'], 'axes.prop_cycle': cycler(color=COLORS),
        'axes.formatter.use_mathtext': True, 'image.cmap': s['field_cmap'],
    })


class SciFormatter(ticker.ScalarFormatter):
    """Ticks with at most `decimals` decimals and, when needed, one common 10^k factor."""

    def __init__(self, decimals=2, powerlimits=(-2, 3)):
        super().__init__(useOffset=False, useMathText=True)
        self.decimals = decimals
        self.set_powerlimits(powerlimits)

    def _digits(self, oom):  # fewest decimals that represent all ticks, None if > self.decimals
        v = np.asarray(self.locs, dtype=float) / 10.0 ** oom
        if not v.size:
            return 0
        tol = 1e-6 * max(1.0, np.abs(v).max())
        return next((d for d in range(self.decimals + 1) if np.allclose(v, np.round(v, d), atol=tol)), None)

    def _set_order_of_magnitude(self):
        super()._set_order_of_magnitude()
        nz = np.abs(np.asarray(self.locs, dtype=float))
        nz = nz[nz > 0]
        if self.orderOfMagnitude == 0 and nz.size and self._digits(0) is None:
            self.orderOfMagnitude = int(np.floor(np.log10(nz.max())))

    def _set_format(self):
        d = self._digits(self.orderOfMagnitude)
        if d is None:  # more than `decimals` needed: use the fewest that keep the labels distinct
            v = np.asarray(self.locs, dtype=float) / 10.0 ** self.orderOfMagnitude
            d = next((k for k in range(self.decimals, 10) if np.unique(np.round(v, k)).size == v.size), self.decimals)
        self.format = f'%1.{d}f'


def sci_axis(ax, axis='y', style=None):
    """axis: 'x', 'y' or 'both'; log axes are left unchanged. For colorbars: cb.formatter = SciFormatter()."""
    s = get_style(style)
    for name in (['x', 'y'] if axis == 'both' else [axis]):
        a = getattr(ax, f'{name}axis')
        if a.get_scale() == 'linear':
            a.set_major_formatter(SciFormatter(s['sci_decimals'], s['sci_powerlimits']))
            a.get_offset_text().set_fontsize(s['tick_size'])


def add_train_end(ax, t_train, label=r'$T_\text{train}$', style=None):
    s = get_style(style)
    ax.axvline(t_train, color='black', linestyle='--', linewidth=1.5)
    if label:
        ax.text(t_train, 0.97, label, transform=ax.get_xaxis_transform(), rotation=90,
                va='top', ha='right', fontsize=s['legend_size'])


def place_legend(ax, where='auto', ncol=None, style=None, **kwargs):
    """where: 'auto', 'inside', 'right' (outside, vertical) or 'above' (outside, columns)."""
    s = get_style(style)
    n = len(ax.get_legend_handles_labels()[1])
    if n == 0:
        return None
    if where == 'auto':
        where = 'inside' if n <= s['legend_max_inside'] else 'right'
    if where == 'inside':
        return ax.legend(ncol=ncol or 1, **kwargs)
    if where == 'right':
        return ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), ncol=ncol or -(-n // 10), **kwargs)
    if where == 'above':
        return ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=ncol or min(n, 4),
                         frameon=False, **kwargs)
    raise ValueError(f'unknown legend position {where!r}')


def find_overlaps(fig, gap=2):
    """Pairs of texts (tick labels, axis labels, panel titles, annotations, legends) that overlap or are closer than
    `gap` pixels, and texts covering another panel. Empty list = no clash found."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    items = []  # (artist, owning axes or None)
    for ax in fig.axes:
        for a in (ax.xaxis, ax.yaxis):
            lo, hi = sorted(a.get_view_interval())
            ticks = a.get_major_ticks() + a.get_minor_ticks()  # log axes label minor ticks on short ranges
            items += [(t, ax) for k in ticks if lo <= k.get_loc() <= hi for t in (k.label1, k.label2)]
            items += [(a.label, ax), (a.get_offset_text(), ax)]
        titles = [ax.title, getattr(ax, '_left_title', None), getattr(ax, '_right_title', None)]  # private: guard
        items += [(t, ax) for t in [*titles, *ax.texts] if t is not None] + ([(ax.get_legend(), ax)] if ax.get_legend() else [])
    items += [(t, None) for t in fig.texts + fig.legends]
    items = [(t, o) for t, o in items if t.get_visible() and (not isinstance(t, Text) or t.get_text().strip())]
    boxes = [t.get_window_extent(r).padded(gap / 2) for t, _ in items]
    name = lambda t: repr(t.get_text().replace(r'\mathdefault', '')) if isinstance(t, Text) else 'legend'
    out = [(name(a), name(b)) for i, ((a, _), ba) in enumerate(zip(items, boxes))
           for (b, _), bb in zip(items[i + 1:], boxes[i + 1:]) if ba.overlaps(bb)]
    panel = lambda j, ax: 'colorbar' if ax.get_label() == '<colorbar>' else f'panel {j}'
    out += [(name(t), panel(j, ax)) for (t, o), bt in zip(items, boxes)
            for j, ax in enumerate(fig.axes) if ax is not o and bt.overlaps(ax.get_window_extent(r))]
    return out


def savefig(fig, path, style=None, close=True):
    """Save as PDF; if heavier than max_pdf_mb, PNG instead. Returns the written path.
    Removes a stale file of the other format with the same name, so LaTeX can't pick up an old one.
    close=False keeps the figure (to show it in a notebook or save it again).
    Prints a warning if find_overlaps reports clashing text (rule 14)."""
    s = get_style(style)
    clashes = find_overlaps(fig, s['overlap_gap']) if s['overlap_gap'] is not None else []
    if clashes:
        print(f'WARNING: {path}: overlapping text, fix and regenerate: {clashes}')
    root = os.path.splitext(path)[0]
    os.makedirs(os.path.dirname(root) or '.', exist_ok=True)
    out = root + '.pdf'
    fig.savefig(out, bbox_inches='tight')
    if os.path.getsize(out) > s['max_pdf_mb'] * 2**20:
        os.remove(out)
        out = root + '.png'
        fig.savefig(out, bbox_inches='tight', dpi=s['png_dpi'])
        print(f'PDF over {s["max_pdf_mb"]} MB, saved {out}; try rasterized=True on heavy artists')
    stale = root + ('.png' if out.endswith('.pdf') else '.pdf')
    if os.path.exists(stale):
        os.remove(stale)
    if close:
        plt.close(fig)
    return out


def plot_curves(x, curves, labels=None, style=None, ax=None, logy=False, t_train=None, legend='auto', sci=None,
                grid=True):
    """curves: {legend label: y} or {legend label: {'y': y, **plot_kwargs}}; labels: {'x': ..., 'y': ...}."""
    s = get_style(style)
    labels = {'x': r'$t$', 'y': None, **(labels or {})}
    fig, ax = plt.subplots(figsize=s['figsize']) if ax is None else (ax.figure, ax)
    for i, (name, c) in enumerate(curves.items()):
        kw = dict(c) if isinstance(c, dict) else {'y': c}
        kw.setdefault('color', COLORS[i % len(COLORS)])
        kw.setdefault('linewidth', s['line_width'])
        if len(curves) > 3:  # shifted index: every (color, line style) pair is distinct
            kw.setdefault('linestyle', LINESTYLES[(i + i // len(COLORS)) % len(LINESTYLES)])
        ax.plot(x, kw.pop('y'), label=name, **kw)
    if logy:
        ax.set_yscale('log')
    ax.set_xlabel(labels['x'] or '', fontsize=s['label_size'])
    ax.set_ylabel(labels['y'] or '', fontsize=s['label_size'])
    ax.tick_params(labelsize=s['tick_size'])
    if grid:
        ax.grid(True, which='both', linestyle='--', alpha=0.2)
    if t_train is not None:
        add_train_end(ax, t_train, style=style)
    if sci:
        sci_axis(ax, sci, style)
    if legend:
        place_legend(ax, legend, style=style)
    return fig, ax
