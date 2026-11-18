---
name: paper-submission-prep
description: Prepare a LaTeX paper for submission to a specific journal or conference — check it against the venue's author guidelines, migrate it to the venue's template/class (e.g. elsarticle, svjour, IEEEtran, acmart), fix formatting requirements (references style, title page, keywords, appendices, funding, tables, figures), anonymise for double-blind review, prepare the camera-ready version, and package it for upload. Use whenever the user asks to adapt, check, or convert a manuscript for a venue, switch document class, or asks "what do I still need to fix for submission". It adapts form, not content; it does not rewrite the paper's substance unless the user explicitly asks.
---

# Paper submission prep

A careful, source-driven workflow for adapting a manuscript to a venue. The user stays in control: every requirement cites a source, every file you write is discussed first, and nothing is committed by you unless the user explicitly asks.

**Scope: form, not content.** Unless the user explicitly asks otherwise, adapt the manuscript to the venue's template and rules; don't edit its substance (arguments, results, wording, structure). When a requirement does touch content (an abstract over the word limit, a missing statement, self-citations to reword for anonymity), flag it in `SUBMISSION.md` with its source and let the authors write it; propose text only if asked.

## 0. Pre-flight: get the authoritative sources FIRST

Before proposing or editing anything, check that you have:

1. **The venue's author guidelines**: a pasted copy in the repo (e.g. `GUIDELINES.md`), a PDF, or a link. Publisher sites often block automated fetching (ScienceDirect returns 403), so a pasted copy is the most reliable.
2. **The official template/class bundle** (template `.tex`, class or `.dtx`/`.ins`, `.bst`), if the venue provides one.
3. **The class documentation** (e.g. `elsdoc.pdf`/`elsdoc.tex`), if it ships with the bundle.
4. **The publisher's LaTeX submission FAQ**, if any. It says which TeX version the submission system compiles with (e.g. Elsevier Editorial Manager: TeX Live 2022), whether subfolders are allowed, and which item types to use.

If the guidelines (1) are missing, **stop and ask the user to share them before touching the sources.** Explain briefly why: without the guide, requirements come from memory and may be wrong or out of date. For 2–4, ask whether they exist; stop only if they exist and haven't been shared. You may still do read-only work meanwhile, like listing the files or noting the document class.

Also ask, if it isn't already clear:
- Which document class, layout and options the user prefers. They may have used this venue before; reuse their earlier setup.
- Where they compile (Overleaf? which TeX Live year?) and whether the sources are also edited there. If so, ask them to pull first.
- Who commits. Default: **only the user commits.**
- Test compilation (§4), unless already recorded in `SUBMISSION.md`. Ask with two questions:
  - **Compile?** "Compile every change on a copy and check it automatically (Strongly recommended)" or "No compilation". With no compilation, every change is untested: say so when proposing it, skip the §4 checks, and ask the user to compile and report errors or visual problems.
  - **Where?** (only if compiling) "Session scratch directory (temporary, may be cleared)", "A folder inside the project, e.g. `build/`", or a path the user gives via "Other". A folder inside a git repo is handled like the planning files (§2).

  Record both answers in `SUBMISSION.md`.

## 1. Source hierarchy, and labelling what is yours

When sources disagree, the higher one wins. Note conflicts explicitly.

1. The venue's author guidelines: requirements ("must", "should", limits).
2. The official template, then the class documentation and source code: mechanics (which commands and options to use).
3. Generic conventions or your own knowledge: only as labelled advice, never as a requirement.

Cite every requirement with its exact location, e.g. `GUIDELINES.md:715`, `template.tex:20`, `class.cls:1349`. Separate **mandatory** items (the venue requires them) from **recommended** ones (the class docs suggest them) and **author choices**.

Advice is welcome, but say it is yours. Example:
- Required: "highlights go in a separate editable file with 'highlights' in its name (GUIDELINES.md:432)."
- Advice: "My suggestion, not in the guide: use .docx rather than .tex, so the submission system doesn't treat it as LaTeX source."

Never phrase an inference as a rule ("it must not be in the upload folder") when no source says so.

## 2. Planning files: short, and no duplication

Keep two planning files in the project root. They survive interrupted sessions.
- **Not a git repo** (e.g. sources downloaded from Overleaf as a zip): the workflow still applies; ignore the rules on `.git/info/exclude`, `.gitignore` and commits (§5, §9).
- **Git repo**: unless the user's choice is already written down (e.g. in `SUBMISSION.md` or `CLAUDE.md`), ask how to handle the planning files: `.git/info/exclude` (local, untracked, no commit needed), `.gitignore`, or tracked as normal files. Record the answer in `SUBMISSION.md`.

Keep them concise: one line per item where possible, point to the other file by number instead of repeating, and prune finished detail at the end of each round.

**`SUBMISSION.md`** (the dashboard; aim for under ~100 lines). Item numbers stay stable. Sections:
- **Venue facts**: 5–8 bullets (article type, limits, review model, section).
- **To do**: author actions that aren't LaTeX changes (forms, declarations, data deposit, cover letter, uploads). Checkbox, one line each.
- **To discuss with co-authors**: one bullet per decision: the question, the options, the current state, the change number if any. Move it to "Decided" once settled.
- **Decided / done**: one line each, with change number and date. Don't re-explain.
- **Suggestions (advice, not required by the guide)**: your own recommendations, one line each. Move one to "To discuss" or "To do" if the user picks it up; delete it if declined.

**`PROPOSED_CHANGES.md`** (the technical log):
- A status table `| # | File | Change | Status |`, one line per change. Numbers are never reused or renumbered; later fixes get new numbers. Take the next number from the file, not from memory.
- A full section (rationale with source lines, exact diff, dependencies) **only while a change is pending or deferred**. Once it is applied or declined, collapse it to its table row; git history keeps the diff.
- Group changes into rounds the user can review and commit in between (e.g. "Round 1: compile with the new class"; "Round 2: remaining mandatory items"; "Final: packaging").

## 3. Discuss, then ask for approval

**Discuss first, for every file you write**: paper sources, but also cover letters, highlights, READMEs. Propose the text or diff in chat and edit only after approval. The planning files are the only exception: update them, then report what changed.

For source changes:
- Use AskUserQuestion. Each question must stand alone and contain (1) the rationale with its source lines, and (2) the exact change, shown as a diff in the option preview.
- **Default: one change per question**, with options like "Apply as proposed (Recommended)", concrete variants (each with its own diff) when a real alternative exists, and two kinds of skip:
  - **"Defer (keep as to-do)"**: status `deferred`; the item stays open and is listed again in the end-of-round summary.
  - **"Won't do (decided)"**: status `declined`; record it under "Decided / done" with the date and don't propose it again.

  Questions allow at most 4 options; if variants leave no room for both skips, offer "Defer" and let the user decline via "Other".
- **Mechanical batches**: homogeneous fixes with no real alternatives (typos, `\cite` → `\parencite`, the same rule across N tables, a list of `.bib` name fixes) may go in one question that lists every item, with options "Apply all", "Defer", "Won't do", and "Other" to pick a subset. Anything with real alternatives or that changes meaning stays a single question.
- At the start, the user may opt in to auto-applying mechanical batches (default: ask). Report each auto-applied batch afterwards.
- Never infer approval from silence, from an earlier approval, or from a related answer. Apply only what was picked.
- If the user wants to clarify, answer first, then ask again.
- Update the status table immediately after each change.

## 4. Test every change on a scratch copy

Applies when the user chose to compile (§0); otherwise only the TeX-version and `.bbl` points below apply, as instructions for the user.

- Copy the sources to the chosen build folder (§0; if the session has no scratch directory, `mktemp -d` outside the repo) and compile there, never in the user's tree. Exclude `.git`, planning files and the build folder itself from the copy.
- Compare against a baseline: errors, page count, new warnings (grouped by type), overfull boxes, and the affected labels in `main.aux` (e.g. check that `tab:x` gives the expected number).
- Render pages with ghostscript when the visual result matters (`gs -sDEVICE=png16m -r80 -dFirstPage=N -dLastPage=N`); for text checks, `gs -sDEVICE=txtwrite`, and compare with whitespace removed (extraction drops spaces).
- **Test with the venue's TeX version** when it differs from yours. Class and package versions differ (e.g. elsarticle 3.3 in TeX Live 2022 vs 3.5 in 2026), and code paths that never run locally can fail there. Ask the user to compile on Overleaf with that TeX Live year, or read the older class/package sources for version-specific code. If you can't compile with it yourself, say so.
- With biblatex, the `.bbl` uploaded with the sources must come from a compatible biblatex version, because the `.bbl` format changes between releases. Generate it with the venue's TeX version (e.g. on Overleaf).
- If a test shows a side effect, report it, add a new numbered fix-up change, and get it approved too.
- Report outcomes plainly. If something couldn't be tested, say so.
- Sanity-check every verification command: a check that prints nothing is not a pass. Make sure it actually ran and produced a number (`grep -c` can be aliased; use `/usr/bin/grep` or `wc -l`).

## 5. End of each round: make sure the changes are kept

List every file changed in the round (from `git status` in a git repo, otherwise from the status table). In a git repo, remind the user to commit all of them; if they use Overleaf, remind them to sync all of them too. A change applied locally but never committed or synced is easily lost when a newer copy of the same file comes back from elsewhere. If the user does bring files back from Overleaf, check only those files for the applied changes; no routine re-checks otherwise.

Give a short summary: what was applied, deferred and declined, what's next, and (in a git repo) what `git diff --stat` shows.

## 6. Package audit (Round 1)

List the `\usepackage` calls and flag those the target class already handles or conflicts with, e.g. `geometry` (the class sets the layout), `natbib` vs biblatex, `amsaddr`, `\tableofcontents`, caption/subcaption options. Propose each removal as a change.

## 7. Final round: submission packaging

- **Flat folder**: many systems (e.g. Elsevier EM) reject subfolders. Remove `\graphicspath` entries pointing to missing directories, bundled class folders that are installed anyway, and unused images.
- **Figures** as separate files, named as the guide asks (e.g. `Figure_2a.pdf`); vector with fonts embedded, raster ≥ 300 dpi.
- **Bibliography**: include the `.bbl` built with the venue's TeX version.
- **Item types**: `.tex`, `.bib`, `.bbl` as "Manuscript"; images as "Figure". Extra `.tex` files with their own `\documentclass` (highlights, cover letter) go under their own item types, never "Manuscript".
- **Multiple `.tex` files**: check the guide. Some venues require a single `.tex` file; then submit the flattened file (`latexpand`). Where several are allowed, `\input` files at the top level are fine; keep a flattened single file as a fallback. Before relying on it, check that it compiles to the same PDF as the original (same page count and text).
- **Final checks**: fonts embedded in the PDF and figures (`pdffonts`; if unavailable, look for font warnings from `gs`); grep the sources for `TODO`, `\todo`, `\FIXME` and the log for "undefined" and `??`; ORCID, CRediT, funding and other declarations if the guide asks.
- Ask the user to check the PDF the submission system builds before approving the submission.

## 8. Conferences and double-blind venues

Based on general knowledge of recent calls (NeurIPS, ICLR, ICML, IEEE and ACM conferences), not on a specific guide: always check the current year's call and style files, since limits and rules change every year. Don't hard-code numbers.

- **Format and upload.** Many ML conferences (NeurIPS, ICLR, ICML) use a style file (e.g. `neurips_20XX.sty`, `iclr20XX_conference.sty`) on top of `article`, not a class, and take a PDF through OpenReview or CMT. The system doesn't compile the sources, so the TeX-version and flat-folder checks (§4, §7) mostly apply to journals and to camera-ready source uploads (e.g. ACM TAPS, IEEE PDF eXpress).
- **Anonymisation.** Only when the venue's guide asks for it: many journals and single-blind venues want the author names in the manuscript, and the rules differ between double-blind venues. Don't anonymise by default; follow the guide's exact rules, and if it is unclear, ask the user. When it is required: use the style's anonymous/submission option; remove the author block, acknowledgements and funding until camera-ready; cite your own work in the third person; anonymise code and data links; clear PDF metadata (`hyperref` `pdfauthor`, check with `pdfinfo` or gs) and identifying file names. Also watch for less visible leaks: with pdfLaTeX, `\pdfsuppressptexinfo=-1` drops the `/PTEX.FileName` entries (absolute paths of included PDFs, which can contain the user name); figure PDFs carry their own Author/Creator metadata; `hyperref`'s `pdfusetitle` copies `\author` into `pdfauthor`.
- **Page limits.** Check what counts (usually the main text; references, appendices and required checklists often don't) and measure on the compiled PDF.
- **Required extras.** Venue checklists (e.g. the NeurIPS paper checklist) and ethics, reproducibility or LLM-use statements, where the call asks for them.
- **Supplementary material and preprints.** Appendix in the main PDF or a separate file, and the arXiv/preprint policy: follow the call.
- **Camera-ready.** De-anonymise, switch to the final style option, add the copyright or venue block, restore acknowledgements and funding; the page allowance often changes.

## 9. Never commit, unless explicitly asked

Leave commits to the user. Commit only when the user explicitly asks, and only what they asked for; a request covers that commit, not later ones.

## Local toolchain gotchas

- **biber on macOS (universal TeX Live binary) can fail** with "extracting arm64 binary with lipo failed". Workaround: `lipo "$(which biber)" -thin arm64 -output <scratch>/biber-arm64`, then run that binary. Don't modify the user's system without asking.

## Class-specific notes

Per-class notes live in `references/<class>.md`; read the one for the target class before proposing changes. Available: `references/elsarticle.md` (Elsevier). Add one file per class (e.g. `references/acmart.md`) in the same format.
