---
name: plot-example-project
description: "Project-specific plotting conventions for this repo (a method for solving PDEs, compared against several baselines on a few test cases). Covers notation, field plots on the unstructured meshes, where figures go, and the legacy package/utils/plotting.py. Use together with the general `plotting` skill whenever you make or change a figure in this repo."
---

# Plotting in this repo

*Example project skill for the general `plotting` skill: copy it to `<project>/.claude/skills/plot-<name>/SKILL.md` and replace the content with your project's conventions.*

Apply the general `plotting` skill first; this file only adds what is specific to this repo.

## Where the code lives
- Helpers: `package/utils/plot_style.py`. If it does not exist yet, copy `scripts/plot_style.py` of the `plotting` skill and add `plot_fields` below.
- `package/utils/plotting.py` is legacy: it predates the rules (uses `jet`, font size 14 in places, some titles, `plt.show()`). When you touch one of its functions, bring that function in line with the rules; do not restyle the whole file in passing.
- Its functions call `plt.show()`: run scripts with `MPLBACKEND=Agg`.

## Where figures go
Default output folders, as chosen by the user (the general skill asks for them when a project has none):
- Into the run folder (`HyperParams.net_dir`, or `runs/<problem>/...` for `package.run`), or `figures/` for paper figures. Never into the repo root.
- Do not write into the protected checkpoint folders (the released test cases; see AGENTS.md).

## Notation
Use the same symbols in every figure; check the paper draft or existing figures before introducing a new one.
- Time $t$, end of training $T_\text{train}$ (`final_training_time` in the unsteady scripts), parameters $\mu$ / $\mu_i$, coordinates $x$, $y$.
- True (high-fidelity) solution $\boldsymbol{u}_h$, prediction $\boldsymbol{u}_\text{sim}$; bold for vector fields, plain $u_h$ for scalars; pressure $p$.
- Latent state $\mathbf{s}$, components $s_i$.
- Relative error $\varepsilon_\text{rel}$ (relative L2 over the mesh), pointwise error field $e_\text{rel}$; variants of a method get a subscript naming the variant, as in `plotting.py`.
- Method names: our method and the baselines are spelled exactly as in the paper (see `README.md`).

## Field plots on the meshes
The datasets store triangles 1-based (MATLAB): use `dataset.T - 1`. Coordinates are per snapshot (`xx[:, k]`, `yy[:, k]`), so test cases with a moving domain have a different mesh at every time. Errors are in physical units: inverse-scale prediction and truth first (see the scaler in `plotting.py`).

```python
import matplotlib.tri as mtri
from matplotlib.colors import Normalize, TwoSlopeNorm
from matplotlib import ticker


def plot_fields(x, y, fields, error=None, triangles=None, labels=None, style=None, layout='row'):
    """fields: {colorbar label: values} (shared colormap and range); error: (colorbar label, values)."""
    s = get_style(style)
    labels = {'x': r'$x$', 'y': r'$y$', **(labels or {})}
    tri = mtri.Triangulation(x, y, triangles)
    panels = list(fields.items()) + ([tuple(error)] if error is not None else [])
    n = len(panels)
    shape, size = ((1, n), (5.5 * n, 4.5)) if layout == 'row' else ((n, 1), (5.5, 4.5 * n))
    fig, axes = plt.subplots(*shape, figsize=size, squeeze=False)
    axes = axes.ravel()
    allv = np.concatenate([np.ravel(v) for v in fields.values()])
    levels = lambda lo, hi: np.linspace(lo, hi if hi > lo else lo + 1e-12, 101)  # explicit -> same colorbar limits
    field_norm, field_levels = Normalize(allv.min(), allv.max()), levels(allv.min(), allv.max())
    for i, (ax, (name, v)) in enumerate(zip(axes, panels)):
        v = np.ravel(v)
        if error is not None and i == n - 1:
            m = np.abs(v).max()
            cmap, norm, lev = ((s['signed_error_cmap'], TwoSlopeNorm(0.0, -m, m), levels(-m, m)) if v.min() < 0
                               else (s['error_cmap'], Normalize(v.min(), v.max()), levels(v.min(), v.max())))
        else:
            cmap, norm, lev = s['field_cmap'], field_norm, field_levels
        cs = ax.tricontourf(tri, v, lev, cmap=cmap, norm=norm)
        cs.set_rasterized(True)  # keeps the PDF small
        cb = fig.colorbar(cs, ax=ax)
        cb.set_label(name, fontsize=s['label_size'] - 2)
        cb.ax.tick_params(labelsize=s['tick_size'])
        cb.locator = ticker.MaxNLocator(5)
        cb.formatter = SciFormatter(s['sci_decimals'], s['sci_powerlimits'])
        cb.update_ticks()
        cb.ax.yaxis.get_offset_text().set_fontsize(s['tick_size'])
        ax.set_aspect('equal')
        ax.tick_params(labelsize=s['tick_size'])
        ax.set_xlabel(labels['x'] or '', fontsize=s['label_size'])
        ax.set_ylabel(labels['y'] or '', fontsize=s['label_size'])
    fig.tight_layout()
    return fig, axes
```

Example:
```python
fig, axes = plot_fields(xx[:, k], yy[:, k], {r'$u_h$': u_true, r'$u_\text{sim}$': u_pred},
                        error=(r'$|u_h - u_\text{sim}|$', np.abs(u_true - u_pred)), triangles=np.asarray(dataset.T - 1))
savefig(fig, HyperParams.net_dir + f'field_solution_snap{k}')
```
