# elsarticle (Elsevier) notes

*Per-class notes for the `paper-submission-prep` skill; also an example of the format for other classes (e.g. `references/acmart.md`).*

Verified on elsarticle 3.5 (TeX Live 2026) and checked against 3.3 (TeX Live 2022, used by Elsevier EM). The venue's guide overrides everything here.

**Class options.** Use `elsarticle-template-harv.tex` for author–year styles, the `-num` templates for numbered ones. `preprint,12pt` gives a narrow 384pt block and much longer papers (35 → 58 pages in one case); `final,3p` (single column, 468pt) usually looks best for submission; `final,5p` / `3p,twocolumn` approximate print but overflow equations. `times` switches to Times; omit it to keep Computer Modern.

**TeX Live 2022 + `nonatbib` (elsarticle ≤ 3.3).** The class runs `\global\bibsep=0pt` for 1p/3p/5p, but `\bibsep` only exists when natbib is loaded. Result: "Undefined control sequence", and "=0pt" printed at the top of page 1. Overleaf keeps going; EM stops. Fix, harmless on newer versions:
```latex
\newlength{\bibsep}% elsarticle <= 3.3 (TeX Live 2022) sets \bibsep even with nonatbib
\documentclass[final,3p,authoryear,nonatbib]{elsarticle}
```

**biblatex.** Needs `nonatbib`. APA: `\usepackage[style=apa]{biblatex}` with `\parencite`/`\textcite`. Remove `doi=false`/`eprint=false` if DOIs or preprint IDs are required. To drop months, clear `month`, `labelmonth`, `labelday` and `day`. Switching to APA exposes Zotero leftovers (`note = {Publisher: …}`, DOIs stored as URLs, `edition = {0}`, `version: 1` in notes). Fields containing "and" need double braces (`publisher = {{Chapman and Hall/CRC}}`), or they print "Chapman; Hall/CRC". Check name casing (`DOE, JANE`, lowercase names, particles like `{van der Berg}, Anna M.`).

**Front matter.** Everything inside `frontmatter` (replaces `\maketitle`): `\author[a]`, `\affiliation[a]{organization=…, addressline=…, city=…, postcode=…, country=…}`, `\corref{cor1}` + `\cortext[cor1]{…}`, `\ead{…}`. Keywords in `\begin{keyword} … \sep … \end{keyword}`, not in the abstract. amsart's `\title[short]`, `\address`, `\email`, `amsaddr` don't work. Non-text in `\author` (ORCID icons, `\corref`, `\,`) must be inside `\texorpdfstring{…}{}`.

**Highlights.** The `highlights` environment prints a separate Highlights page before page 1 (and resets the page counter). Guides usually want a separate file. Standalone version (one page, compiles alone):
```latex
\newlength{\bibsep}
\documentclass[final,3p,authoryear,nonatbib]{elsarticle}
\usepackage[T1]{fontenc}
\begin{document}
\title{…}\author{…}\author{…}
\begin{highlights}
\item …
\end{highlights}
\makeatletter\elsarticleprelims\makeatother
\end{document}
```

**Appendices.** `\appendix` sets `\thesection` to "Appendix A" (class ~1349), so `Appendix~\ref{}` prints "Appendix Appendix A" and theorems print "Definition Appendix A.1". Fix at the top of the appendix:
```latex
\renewcommand{\thesection}{\Alph{section}}
\makeatletter
\def\appsecprefix@section{\appendixname~}
\renewcommand{\@seccntformat}[1]{\ifcsname appsecprefix@#1\endcsname\csname appsecprefix@#1\endcsname\fi\csname the#1\endcsname\@seccntDot\hskip 0.5em}
\makeatother
```
Don't use `\@tempa`/`\@tempb` there (class internals). Remove `\numberwithin{table}{section}`; add `\counterwithin*{table}{section}` so tables restart at A.1. Placement (before or after the references) is the authors' choice when the guide wants Acknowledgements directly before the reference list.

**Misc.** `\paragraph{Title.}` prints "Title.." because the class adds a period. With glossaries, irregular plurals need `\newacronym[longplural={Degrees of Freedom}]{dof}{DoF}{Degree of Freedom}`. `amsthm` is fine (it overrides the class's theorem definitions). Overfull boxes jump when switching layout; the class manual asks authors to check equation breaking in the final format.
