---
name: plotting
description: Group rules and a small self-contained matplotlib helper for paper figures (errors or losses vs time or parameters, field plots, latent trajectories). Use whenever you create or change a plot or a plotting function, in scripts, notebooks or library code. Also applies to figures, visualisations of results and matplotlib styling, even when the word "plot" isn't used.
---

# Plotting rules

Standalone: no project imports, copy this skill's folder to any repository. Project-specific additions (notation, field plots on meshes, output folders) belong in a separate project skill: use the project's one if it exists, otherwise define one (`<project>/.claude/skills/plot-<name>/SKILL.md`). If this skill's `references/` folder is present, `references/example-project.md` is an example to take inspiration from; if the project's data have the same format (fields on triangular meshes), reuse its `plot_fields` directly.

**Workflow**: if the project already has the helper module (e.g. `plot_style.py`), import from it; if missing, copy `scripts/plot_style.py` from this skill's folder, next to the project's plotting code (e.g. its `utils` package or `scripts/`), never in the repo root. Never paste the helpers into individual scripts or notebooks. Call `apply_rcparams()` once at the start.

**Output folder**: use the project's convention (project skill, `CLAUDE.md`, or an existing figures folder). If there is none and you are running interactively, ask the user once which folder figures should go to by default, and offer to record the answer in the project skill or `CLAUDE.md` so it isn't asked again. If running autonomously, use `figures/`. Never save figures in the repo root.

## Rules
1. **Font sizes**: axis labels 18-20, legend and ticks ~17 (smaller end for panels in a grid).
2. **No figure titles** (no `suptitle`, no `set_title` on single-panel figures): that goes in the caption. Short panel titles (`set_title`) are fine in multi-panel figures when the axis, colorbar label or legend doesn't say what a panel shows, e.g. field plots (`Ground truth`, `Prediction`, `Error`) or subplots sharing the same y axis. Rules 3 and 5 apply to them too.
3. **No camel case or title case** in labels, legend entries and file names: `Relative error`, not `RelativeError` or `Relative Error`; file names in snake_case. Acronyms keep their spelling (`GCA-ROM`).
4. **Save as PDF** with `savefig`. Always pass `rasterized=True` to heavy artists (`pcolormesh`, `tripcolor`, `tricontourf`, `scatter` with thousands of points): axes and text stay vector, the file stays small. If the PDF is still over ~2 MB, `savefig` falls back to PNG at 300 dpi.
5. **LaTeX in raw strings** should be used whenever possible, axis labels included: `r'$t$'`, `r'$\mu$'`, `r'$x$'`, `r'$\hat{u}$'`, `r'$T_\text{train}$'`. If `\text` fails on an old matplotlib, use `\mathrm`.
   For quantities that need a definition (errors, losses, QoIs), propose a default symbol, e.g. $\varepsilon_\text{rel} = \|u - \hat{u}\|_2 / \|u\|_2$. If running interactively and the symbol is not already established in the codebase or paper, ask the user once and reuse the answer. If running autonomously or the codebase already has a convention, use it (or the default) without pausing.
6. **Colors**: mathLab blue `#065895` and mathLab orange `#F79A25` for the first two series (e.g. our method vs a baseline), then the colorblind-safe `COLORS` of the helper.
7. **Colorblind-safe**: no red-vs-green encoding; with many series also vary the line style; colormaps `viridis`/`plasma`/`cividis`/`magma`, `RdBu_r` centred at 0 for signed data. Never `jet` or `rainbow`.
8. **Scientific notation** on linear axes whose values share one scale: one $\times 10^{k}$ factor, ticks with at most 2 decimals (`sci_axis`), more only when needed to keep tick labels distinct. Use log axes for values spanning orders of magnitude.
9. **Field subplots** (ground truth, prediction, error): truth and prediction share one colormap (default `viridis`) and the same color range, so their colorbars show the same limits; the error field gets a different colormap (default `plasma`) and its own colorbar. For fields on triangular meshes, see `plot_fields` in `references/example-project.md` (if present).
10. **Extrapolation in time**: dashed black vertical line at the end of the training time, labelled $T_\text{train}$ next to the line (`add_train_end`).
11. **Flexible code**: plotting functions take `labels=None` and `style=None` dictionaries merged with defaults; no font size, label or color hard-coded in the function body.
12. **Large legends go outside**: on the right (one or more columns) or above (several columns). `place_legend` does it automatically. **Shared legend**: when panels show the same series (same models, methods or labels), draw one legend for the whole figure instead of repeating it in each panel: `fig.legend(*axs.flat[0].get_legend_handles_labels(), loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=...)` above the panels, or on the right. This also avoids a per-panel legend above a panel covering its title.
13. **Grids**: on by default, light dashed lines, alpha ~0.2, on both major and minor ticks: `ax.grid(True, which='both', linestyle='--', alpha=0.2)`. Turn them off (`grid=False` in `plot_curves`) if the user asks or they clutter the figure.
14. **No overlapping text**: tick labels, axis labels, offset text ($\times 10^k$), $T_\text{train}$, panel titles, legends and colorbar labels must not overlap each other or another panel. `savefig` runs `find_overlaps` and prints a warning; also look at the saved figure (open the PDF/PNG), since the check doesn't see text over curves or data. If anything clashes, fix it and regenerate the figure (at most 3 attempts): fewer ticks (`ax.xaxis.set_major_locator(ticker.MaxNLocator(4))`), `sci_axis` for long numbers, `layout='constrained'` in `plt.subplots`, a larger `figsize`, the legend outside (`place_legend`), shared axes/labels in grids. Shrink fonts only within the ranges of rule 1. If clashes remain after 3 attempts, report them instead of saving silently. If the check flags text that looks fine (e.g. rotated tick labels), pass `style={'overlap_gap': 0}` to flag only actual overlaps; `None` skips it (e.g. very heavy figures where the extra draw is slow).

## Helper: `scripts/plot_style.py`

Tested with matplotlib 3.9. To create the project's module, copy the file with `cp` from this skill's folder (don't retype it). Read it only to change or extend it.

- `COLORS` (mathLab blue and orange first, then colorblind-safe), `LINESTYLES`, `STYLE` (defaults: font sizes, `figsize`, colormaps `field_cmap`/`error_cmap`/`signed_error_cmap`, `legend_max_inside`, `sci_decimals`, `sci_powerlimits`, `max_pdf_mb`, `png_dpi`, `overlap_gap`). Every function takes `style=None`, a dict overriding `STYLE`; unknown keys raise `KeyError`.
- `apply_rcparams(style=None)`: rcParams (font sizes, line width, color cycle, mathtext, default colormap).
- `plot_curves(x, curves, labels=None, style=None, ax=None, logy=False, t_train=None, legend='auto', sci=None, grid=True)` → `(fig, ax)`. `curves`: `{legend label: y}` or `{legend label: {'y': y, **plot_kwargs}}`; `labels`: `{'x': ..., 'y': ...}` (default x label `$t$`); `legend`: `'auto'`, `'inside'`, `'right'`, `'above'` or `None`; `sci`: `'x'`, `'y'` or `'both'`. Draws into `ax` if given (subplots).
- `savefig(fig, path, style=None, close=True)` → written path. PDF, PNG fallback over `max_pdf_mb`, removes a stale file of the other format, warns on overlapping text (rule 14).
- `place_legend(ax, where='auto', ncol=None, style=None, **kwargs)`: `'inside'` up to `legend_max_inside` entries, otherwise outside.
- `sci_axis(ax, axis='y', style=None)`: rule 8 on linear axes; for colorbars, `cb.formatter = SciFormatter()`.
- `add_train_end(ax, t_train, label=r'$T_\text{train}$', style=None)`: rule 10.
- `find_overlaps(fig, gap=2)` → list of clashing text pairs (empty if none).

## Usage

```python
apply_rcparams()
fig, ax = plot_curves(t, {'Ours': err_ours, 'Baseline': err_base}, logy=True, t_train=t_end_train,
                      labels={'y': r'$\varepsilon_\text{rel}$'})
savefig(fig, 'figures/rel_errors_test')

fig, ax = plot_curves(mu, curves, labels={'x': r'$\mu$'}, sci='y', legend='above', style={'label_size': 18})
```

New plotting functions follow the same pattern: `labels=None, style=None` merged with defaults, colors from `COLORS`, output through `savefig`.