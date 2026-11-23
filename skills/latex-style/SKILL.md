---
name: latex-style
description: "Style and LaTeX-correctness rules for the prose of a LaTeX paper: the project's conventions (macros, environments, acronym packages, labels), flow, tense and voice, wording, notation, captions, LaTeX typography, cross-references and citation style, math in prose, numbers in scientific notation, tables, hygiene of the existing citations and .bib, and a build check. Use when the user asks to check, polish, proofread or clean up the style or LaTeX of a paper or part of it (e.g. \"make sure this follows LaTeX conventions\", \"proofread Section 3\", \"fix the typography\"), or when another skill or the project's CLAUDE.md says to apply it. Not for a specific one-off change (rewording a sentence, fixing a typo, changing a number), where the request itself is the whole task. It fixes form, not content: it never adds claims, numbers or references. Not for venue templates and formatting (use paper-submission-prep)."
---

# LaTeX style

Rules for how the text of a paper is written and typeset. They change form, not content: claims, numbers, math and references stay as the authors wrote them. If a style fix would need new content (a missing number, a reference, a proof step), point it out instead of writing it.

The project's conventions (its `CLAUDE.md`, macros and existing text) come first; the rules below are defaults where the project says nothing. When revising, change only what is unclear, inconsistent or wrong, and keep the authors' voice: use the most finished sections as a style sample (sentence length, "we" vs passive, how results and references are introduced). Many points follow E. Medvet's [How to write scientific documents](https://medvet.inginf.units.it/teaching/how-to-write/).

## Conventions

1. **Use what the project already has**: existing macros and environments rather than new ones, the commands of the acronym package in use (e.g. `\gls`, `\ac`) rather than hand-written acronyms, existing label prefixes, one sentence per line if that is the convention. If a convention you need is missing (language, spelling variant, one sentence per line), follow the existing text, or ask if there is none. If the paper has many acronyms written by hand and loads no acronym package, you may suggest the `glossaries` or `acronym` LaTeX package.
2. **Never change the preamble without asking**: no new `\usepackage`, `\newcommand` or `\DeclareMathOperator` unless the user agrees.
3. **Keep diffs clean**: keep existing `%` comments (a style edit is not a reason to remove them) and don't rewrap or reformat lines you didn't change.

## Style

4. **Flow**: sentences, paragraphs and sections connect, so the reader knows why each comes next; one main idea per paragraph; dense stretches of definitions or formulas get a sentence of motivation.
5. **No repetition** beyond the usual overview in abstract, introduction and conclusion; but keep technical terms identical throughout rather than varying them for style.
6. **Abstract**: context, the gap, the proposal tied to that gap, the evaluation and its main results.
7. **Tense and voice**: present for abstract, introduction and method; past for related work and what was done in experiments; active "we" for the authors' choices; consistent throughout.
8. **Wording**: no contractions; one spelling variant (US or UK); commas around "e.g." and "i.e."; acronyms introduced at first use; no unsupported hype ("novel", "significantly" without a test, "clearly").
9. **Notation**: every symbol defined before or where it is first used; one meaning per symbol; one letter per entity, related quantities via subscripts (`n_\text{pop}`, not `pop`); words in math inside `\text{}` or `\mathrm{}`; `\max`, `\min`, existing `\DeclareMathOperator` macros, or `\operatorname{...}` for operators the preamble doesn't define; the field's conventions. Flag clashes and undefined symbols rather than renaming silently.
10. **Captions**: self-contained (a reader skimming the figures understands what is shown without the text), with symbols and line styles explained; one capitalisation and punctuation style across all captions, following the existing ones. Table captions go above the table, figure captions below the figure, unless the venue's template says otherwise.

## LaTeX typography

11. `~` between a word and the reference that follows it (`Figure~\ref{...}`, `in~\cite{...}`, `see~\cref{...}`, `Equation~\eqref{...}`); a reference opening a sentence (`\Cref{fig:x} shows`) needs none. Use the project's reference commands (`\eqref`, `\cref`) consistently.
12. `\dots` for ellipses; `\emph{}` for emphasis, not `\textit{}` or bold.
13. Blank lines for paragraphs, not `\\`.
14. `` ``…'' `` for quotes, not `"…"`; `\enquote{…}` if `csquotes` is loaded.
15. `\ ` after a period that does not end a sentence (`vs.\ `, `et al.\ `), unless `\frenchspacing` is on.
16. En-dash `--` for ranges, em-dash `---` for asides.
17. **Cross-references named one way** throughout: "Figure~3" or "Fig.~3", "Equation~(2)" or "(2)", "Section~4" or "Sec.~4", following the existing text (or `\cref`, which names them for you); capitalised before a number.
18. **Citations are not nouns**: "Smith et al.~\cite{x} showed" or "as shown in~\cite{x}", not "\cite{x} showed", unless the existing text or the venue's house style does otherwise. For textual and parenthetical citations, `\citet`/`\citep` with natbib, `\textcite`/`\parencite` with biblatex.

## Math, numbers and tables

19. **Displayed equations are part of the sentence**: they take the punctuation the sentence needs (a comma or period after the equation, inside the math environment).
20. **No sentence starts with a symbol or a number**: "Here, $x$ is…", not "$x$ is…".
21. **Scalable delimiters**: unless the project sets sizes by hand (`\big`, `\Big`, …), use `\left( … \right)` (and likewise for brackets, braces and norms) around tall content such as fractions, sums and integrals in displayed equations, so the delimiters scale to it. Use `\big`/`\Big` instead when `\left`/`\right` over-scales (e.g. around sums with limits), in inline math (it prevents line breaks), and for delimiters that span lines of an `align` (where unmatched `\left`/`\right` don't compile).
22. **Scientific notation** when reporting results that span orders of magnitude or are very small or large (errors, losses, tolerances): `$1.2 \times 10^{-3}$`, or `\num{1.2e-3}` if `siunitx` is loaded. Keep the value and the number of significant digits as given, and use the same format across a table or comparison.
23. **Units in the column header** of tables (e.g. "Time (s)"), not repeated in every cell.

## Existing citations

24. **Citation hygiene**: after an edit, check locally that the keys cited in the edited text exist; look entries up online only if one looks wrong or incomplete, and audit the whole `.bib` only on request. Every `\cite` key exists in the `.bib`; no duplicates (the same paper under two keys, typically a preprint and its published version); no stale entries (preprints now published, wrong year or venue, missing DOI). Verify proposed fixes online (doi.org, Crossref, arXiv, publisher page) and never fill in metadata from memory. Keep existing citation keys; for duplicates, propose keeping the published version under one key and updating the `\cite` commands that use the other. Finding new references is out of scope.
25. **How the `.bib` is maintained**: ask once whether it is auto-exported from a reference manager (e.g. Zotero with Better BibTeX), exported manually, or edited by hand. Never modify the user's reference library.
    - Auto-exported: never edit the `.bib`, since changes are overwritten at the next export; list the fixes for the user to make in the reference manager. Changing year or authors there can change the citation key: point this out and suggest pinning the old key, or offer to update the `\cite` commands.
    - Exported manually: fixes in the `.bib` are lost at the next export, so also list them for the reference manager.
    - By hand: edit in the existing key and field style.

## Build

26. **Build** with the project's command after editing files on disk (not for text proposed only in chat). Check the log for errors, undefined references and citations, and new warnings (e.g. overfull boxes introduced by the edit). If you couldn't build, say so; a check that prints nothing is not a pass. BibTeX's "I found no \citation commands" is not a broken build when the paper has no `\cite` yet.
