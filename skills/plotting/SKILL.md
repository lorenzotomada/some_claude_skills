---
name: plotting
description: Group rules and a small self-contained matplotlib helper for paper figures (errors or losses vs time or parameters, field plots, latent trajectories). Use whenever you create or change a plot or a plotting function, in scripts, notebooks or library code. Also applies to figures, visualisations of results and matplotlib styling, even when the word "plot" isn't used.
---

# Plotting rules

Standalone: no project imports, copy this file to any repository. Project-specific additions (notation, field plots on meshes, output folders) belong in a separate project skill: use the project's one if it exists, otherwise define one (`<project>/.claude/skills/plot-<name>/SKILL.md`). If this skill's `references/` folder is present, `references/example-project.md` is an example to take inspiration from; if the project's data have the same format (fields on triangular meshes), reuse its `plot_fields` directly.

**Workflow**: if the project already has the helper module (e.g. `plot_style.py`), import from it; create it from the block below only if missing. Never paste the helpers into individual scripts or notebooks. Call `apply_rcparams()` once at the start.

**Output folder**: use the project's convention (project skill, `CLAUDE.md`, or an existing figures folder). If there is none and you are running interactively, ask the user once which folder figures should go to by default, and offer to record the answer in the project skill or `CLAUDE.md` so it isn't asked again. If running autonomously, use `figures/`. Never save figures in the repo root.

## Rules
1. **Font sizes**: axis labels 18-20, legend and ticks ~17 (smaller end for panels in a grid).
2. **No titles**, also none on subplot panels (no `set_title`). What a panel shows goes in the axis label, colorbar label or legend; the rest goes in the caption.
3. **No camel case or title case** in labels, legend entries and file names: `Relative error`, not `RelativeError` or `Relative Error`; file names in snake_case. Acronyms keep their spelling (`GCA-ROM`).
4. **Save as PDF** with `savefig` below. Always pass `rasterized=True` to heavy artists (`pcolormesh`, `tripcolor`, `tricontourf`, `scatter` with thousands of points): axes and text stay vector, the file stays small. If the PDF is still over ~2 MB, `savefig` falls back to PNG at 300 dpi.
5. **LaTeX in raw strings** should be used whenever possible, axis labels included: `r'$t$'`, `r'$\mu$'`, `r'$x$'`, `r'$\hat{u}$'`, `r'$T_\text{train}$'`. If `\text` fails on an old matplotlib, use `\mathrm`.
   For quantities that need a definition (errors, losses, QoIs), propose a default symbol, e.g. $\varepsilon_\text{rel} = \|u - \hat{u}\|_2 / \|u\|_2$. If running interactively and the symbol is not already established in the codebase or paper, ask the user once and reuse the answer. If running autonomously or the codebase already has a convention, use it (or the default) without pausing.
6. **Colors**: mathLab blue `#065895` and mathLab orange `#F79A25` for the first two series (e.g. our method vs a baseline), then the colorblind-safe `COLORS` below.
7. **Colorblind-safe**: no red-vs-green encoding; with many series also vary the line style; colormaps `viridis`/`plasma`/`cividis`/`magma`, `RdBu_r` centred at 0 for signed data. Never `jet` or `rainbow`.
8. **Scientific notation** on linear axes whose values share one scale: one $\times 10^{k}$ factor, ticks with at most 2 decimals (`sci_axis`), more only when needed to keep tick labels distinct. Use log axes for values spanning orders of magnitude.
9. **Field subplots** (ground truth, prediction, error): truth and prediction share one colormap (default `viridis`) and the same color range, so their colorbars show the same limits; the error field gets a different colormap (default `plasma`) and its own colorbar. For fields on triangular meshes, see `plot_fields` in `references/example-project.md` (if present).
10. **Extrapolation in time**: dashed black vertical line at the end of the training time, labelled $T_\text{train}$ next to the line (`add_train_end`).
11. **Flexible code**: plotting functions take `labels=None` and `style=None` dictionaries merged with defaults; no font size, label or color hard-coded in the function body.
12. **Large legends go outside**: on the right (one or more columns) or above (several columns). `place_legend` does it automatically.
13. **Grids**: on by default, light dashed lines, alpha ~0.2, on both major and minor ticks: `ax.grid(True, which='both', linestyle='--', alpha=0.2)`. Turn them off (`grid=False` in `plot_curves`) if the user asks or they clutter the figure.

## Helper (copy into a module, e.g. `plot_style.py`)

Tested with matplotlib 3.9. `SciFormatter` overrides private matplotlib methods: check the tick labels after upgrading matplotlib.

```python
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
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


def savefig(fig, path, style=None, close=True):
    """Save as PDF; if heavier than max_pdf_mb, PNG instead. Returns the written path.
    Removes a stale file of the other format with the same name, so LaTeX can't pick up an old one.
    close=False keeps the figure (to show it in a notebook or save it again)."""
    s = get_style(style)
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
```

## Usage

```python
apply_rcparams()
fig, ax = plot_curves(t, {'Ours': err_ours, 'Baseline': err_base}, logy=True, t_train=t_end_train,
                      labels={'y': r'$\varepsilon_\text{rel}$'})
savefig(fig, 'figures/rel_errors_test')

fig, ax = plot_curves(mu, curves, labels={'x': r'$\mu$'}, sci='y', legend='above', style={'label_size': 18})
```

New plotting functions follow the same pattern: `labels=None, style=None` merged with defaults, colors from `COLORS`, output through `savefig`.