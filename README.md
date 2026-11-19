# _Skills_ is the new _libraries_
Some skills I have developed for my workflow with Claude.

## List of skills
- [`paper-submission-prep`](skills/paper-submission-prep/SKILL.md): used to adapt a LaTeX paper to a journal's or conference's template and guidelines when submitting, while keeping maximum control over what Claude edits (every change is cited, discussed and approved first; nothing is committed unless you ask). Includes notes for Elsevier's `elsarticle` in [`references/elsarticle.md`](skills/paper-submission-prep/references/elsarticle.md).
- [`plotting`](skills/plotting/SKILL.md): rules and a small self-contained matplotlib helper for paper figures (no titles, LaTeX labels, colorblind-safe colors, PDF output, scientific notation, legends, field plots). If the project has no convention for where figures go, it asks once and offers to record the answer. The first two colors are the blue and orange of our research group, mathLab; change `MATHLAB_BLUE` and `MATHLAB_ORANGE` to use your own. Project-specific conventions (notation, data format, output folders) go in a separate project skill; [`references/example-project.md`](skills/plotting/references/example-project.md) is an example, including a helper for fields on triangular meshes.

## Installation
Copy a skill folder (e.g. `skills/paper-submission-prep`) into your project's `.claude/skills/` folder, or copy the whole `skills` folder into `.claude/` if the project has no `skills` folder yet.
