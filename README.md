# _Skills_ is the new _libraries_
Some skills I have developed for my workflow with Claude.

These skills are still under development: feedback, issues and suggestions are very welcome.

## List of skills
- [`paper-submission-prep`](skills/paper-submission-prep/SKILL.md): used to adapt a LaTeX paper to a journal's or conference's template and guidelines when submitting, while keeping maximum control over what Claude edits (every change is cited, discussed and approved first; nothing is committed unless you ask). Includes notes for Elsevier's `elsarticle` in [`references/elsarticle.md`](skills/paper-submission-prep/references/elsarticle.md).
- [`plotting`](skills/plotting/SKILL.md): rules and a small self-contained matplotlib helper, [`scripts/plot_style.py`](skills/plotting/scripts/plot_style.py), for paper figures (no figure titles, LaTeX labels, colorblind-safe colors, PDF output, scientific notation, shared and outside legends, field plots). Claude copies the helper into the project when it's missing, and its `savefig` warns about overlapping labels, which Claude then fixes. The helper is kept in a separate file so its code isn't loaded every time the skill is used: `SKILL.md` only has a short summary of its functions. If you change the helper (functions, arguments, `STYLE` keys), update that summary in `SKILL.md` as well. If the project has no convention for where figures go, it asks once and offers to record the answer. The first two colors are the blue and orange of our research group, mathLab; change `MATHLAB_BLUE` and `MATHLAB_ORANGE` in `scripts/plot_style.py` (and in rule 6 of `SKILL.md`) to use your own. Project-specific conventions (notation, data format, output folders) go in a separate project skill; [`references/example-project.md`](skills/plotting/references/example-project.md) is an example, including a helper for fields on triangular meshes.
- [`latex-style`](skills/latex-style/SKILL.md): a compact, cheap-to-load set of style and LaTeX-correctness rules for the prose of a LaTeX paper, used when you ask Claude to check, polish or proofread the style or LaTeX of a paper or part of it (not for specific one-off changes). The project's conventions come first (existing macros, acronym packages, labels; it may suggest an acronym package but never adds one unasked), then flow, tense, wording, notation, captions, typography, cross-references and citations, math in prose, scientific notation for results and units in table headers (partly following E. Medvet's [How to write scientific documents](https://medvet.inginf.units.it/teaching/how-to-write/)). It keeps diffs clean (no rewrapped lines, `%` comments kept), checks the citations already in the paper and the `.bib` (without editing auto-exported Zotero files), and builds the paper after editing files. It fixes form, not content: it never adds claims, numbers or references. Other skills (or the project's `CLAUDE.md`) can name it to have it applied in their workflows.

## Installation
Two options:
- **Personal install:** clone this repo and link the skills you want into `~/.claude/skills/`. They are then available in every project and stay in sync with the repo:
  ```sh
  mkdir -p ~/.claude/skills
  ln -s /path/to/some_claude_skills/skills/latex-style ~/.claude/skills/latex-style
  ```
- **Copy into a project:** copy a skill folder (e.g. `skills/paper-submission-prep`) into the project's `.claude/skills/` folder, or the whole `skills` folder into `.claude/` if the project has no `skills` folder yet. If the project folder is synchronised with git (e.g. an Overleaf git remote), the `.claude/` folder gets pushed with it: add it to `.gitignore` (or `.git/info/exclude`) unless you want to share the skills with your co-authors through the repository.

## Suggested use
- **Keep project conventions in the project's `CLAUDE.md`** (language, macros, comment commands, label style, build command, co-authors) and the generic workflow in the skills: the skills read the `CLAUDE.md` first. A line in the project's `CLAUDE.md` naming the skills to use for which tasks helps Claude pick them.
- **Planning files** created by `paper-submission-prep`: when asked how git should handle them, `.git/info/exclude` keeps them local, so they are never pushed (e.g. to Overleaf).
