# _Skills_ is the new _libraries_
Some skills I have developed for my workflow with Claude.

These skills are still under development: feedback, issues and suggestions are very welcome.

## List of skills
- [`paper-submission-prep`](skills/paper-submission-prep/SKILL.md): used to adapt a LaTeX paper to a journal's or conference's template and guidelines when submitting, while keeping maximum control over what Claude edits (every change is cited, discussed and approved first; nothing is committed unless you ask). Includes notes for Elsevier's `elsarticle` in [`references/elsarticle.md`](skills/paper-submission-prep/references/elsarticle.md).
- [`plotting`](skills/plotting/SKILL.md): rules and a small self-contained matplotlib helper for paper figures (no titles, LaTeX labels, colorblind-safe colors, PDF output, scientific notation, legends, field plots). If the project has no convention for where figures go, it asks once and offers to record the answer. The first two colors are the blue and orange of our research group, mathLab; change `MATHLAB_BLUE` and `MATHLAB_ORANGE` to use your own. Project-specific conventions (notation, data format, output folders) go in a separate project skill; [`references/example-project.md`](skills/plotting/references/example-project.md) is an example, including a helper for fields on triangular meshes.
- [`manuscript-writing`](skills/manuscript-writing/SKILL.md): still under development! Turns the scattered or rough material of a paper (formulas, ideas, TODO notes, drafts) into connected, publication-ready LaTeX prose, and helps with co-authors' comments, references and consistency checks. In my (few) tests, its strength over a plain request was reliability rather than better prose: verified references, problems kept visible as `\TODO`s, unproven results never stated as theorems. It helped most in projects without a `CLAUDE.md`, which it sets up in the first session. A quick mode handles small polishes, a full workflow larger drafting. You decide how much each section may change; it never invents results or citations. Style defaults partly follow E. Medvet's [How to write scientific documents](https://medvet.inginf.units.it/teaching/how-to-write/).

## Installation
Two options:
- **Personal install:** clone this repo and link the skills you want into `~/.claude/skills/`. They are then available in every project and stay in sync with the repo:
  ```sh
  mkdir -p ~/.claude/skills
  ln -s /path/to/some_claude_skills/skills/manuscript-writing ~/.claude/skills/manuscript-writing
  ```
- **Copy into a project:** copy a skill folder (e.g. `skills/paper-submission-prep`) into the project's `.claude/skills/` folder, or the whole `skills` folder into `.claude/` if the project has no `skills` folder yet. If the project folder is synchronised with git (e.g. an Overleaf git remote), the `.claude/` folder gets pushed with it: add it to `.gitignore` (or `.git/info/exclude`) unless you want to share the skills with your co-authors through the repository.

## Suggested use
- **Keep project conventions in the project's `CLAUDE.md`** (language, macros, comment commands, label style, build command, co-authors) and the generic workflow in the skills: the skills read the `CLAUDE.md` first. A line in the project's `CLAUDE.md` naming the skills to use for which tasks helps Claude pick them.
- **Planning files** created by the skills: when asked how git should handle them, `.git/info/exclude` keeps them local, so they are never pushed (e.g. to Overleaf).
