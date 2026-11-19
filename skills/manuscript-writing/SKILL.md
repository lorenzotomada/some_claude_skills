---
name: manuscript-writing
description: "Turn the raw material of a paper (formulas, chunks of ideas, TODO notes, notes in another language, or text that exists but is not publication-ready) into publication-ready LaTeX prose. Use whenever the user asks to draft, write, restructure, rewrite, polish or proofread a paper or part of it (from a single paragraph to the whole manuscript), to turn notes into text, to organise the paper's story and outline, or to check its consistency (notation, claims vs results, cross-references, citations). It works on content, not venue formatting (use paper-submission-prep for that), and never invents results, numbers or citations."
---

# Manuscript writing

Help the authors turn their material into a publication-ready paper. The authors own the ideas, claims, math and voice; you organise, draft, polish and check. Nothing is invented, the user decides how much you change, and nothing is committed unless the user explicitly asks.

**Scope: content, not form.** Venue templates, anonymisation and packaging belong to `paper-submission-prep`; replies to reviewers to a rebuttal workflow. Writing a paper without material is out of scope: when material is missing, say what is missing.

## Two modes

- **Quick mode**, for minor, local requests: polish or proofread a paragraph, a section or a few sentences, fix the wording of a definition, shorten an abstract. Skip the inventory, the planning file and the story/outline step (§1–§3). Still read the project's conventions (§0.1) and the surrounding text, apply the hard rules (§5) and the writing style (§6), build if the project can be built (§9), and summarise what changed. If the edit flow isn't recorded, don't stop to ask: propose the change in chat one paragraph at a time and apply it once approved; mechanical fixes (typos, spacing, one spelling variant) across the section can go in one grouped proposal, as in §4. If the request turns out to need more (missing material, structural problems), say so and offer the full workflow.
- **Full workflow** (§0–§11), for drafting from notes, restructuring, or work across several sections.

When unclear, choose quick mode for requests about a single paragraph or section, and ask otherwise.

## 0. Pre-flight

1. **Project conventions first.** Read the project's `CLAUDE.md` (or equivalent) and any known-issues file before touching the text. If key conventions are missing, ask about the ones the task needs and offer to record the answers in the project's `CLAUDE.md`:
   - language of the paper, and whether notes in other languages are intentional;
   - one sentence per line in `.tex` files, or not;
   - existing macros, theorem environments, glossary/acronym commands, label prefixes;
   - comment/review macros (e.g. per-author note commands, `\TODO`) and which material is parked (e.g. a file not included in `main.tex`). This skill writes gaps as `\TODO{...}`: use the project's own TODO macro if it has one under another name; if it has none, propose adding `\newcommand{\TODO}[1]{\textcolor{red}{[TODO: #1]}}` (needs `xcolor`) to the preamble, and until it is approved use `% TODO: ...` comments, so the build never breaks on an undefined macro;
   - how to build the paper (command, TeX version) and where the sources are also edited (Overleaf?). If co-authors edit elsewhere, pull first; stop and ask on merge conflicts. After pulling, check what changed against `PAPER_PLAN.md` (§2).
2. **Ask few questions up front.** Unless already recorded in `PAPER_PLAN.md`, ask only the **edit flow**: "Write into the files, I review with `git diff`", "Propose in chat, one paragraph at a time", or "Propose in chat, one section at a time" (without git, recommend a "propose" option, or a backup copy). Ask the other settings when they first matter, then record them so each is asked once:
   - target venue and audience: when drafting the outline or the abstract (they set length, depth and tone);
   - git handling of `PAPER_PLAN.md`: when first creating it (§2);
   - whether addressed TODOs may be removed: at the first addressed TODO (§4);
   - how replies to co-author comments are written: at the first one (§4);
   - how the `.bib` is maintained: at the first citation task (§7);
   - who commits: default only the user, so ask only if the user mentions committing.
3. **Questions vs findings.** Ask only about *decisions* that are the user's and block the current step (edit flow, outline, which of two conflicting numbers is right, whether to drop a claim). Everything else is a *finding*: missing material, symbols to define, math to check, assumptions to state. Findings go in the text as `\TODO` (§4), under "Open questions" in `PAPER_PLAN.md`, and in the round summary; they don't block the work.
   - Batch the decisions of a round into one set of questions (a few at a time), most important first.
   - Where a sensible default exists (e.g. renaming one of two clashing symbols, US vs UK spelling following the existing text), apply it, mark it visibly (a `\TODO` or the summary) and say how to change it, instead of asking.
   - Defaults never cover content: anything that changes meaning, claims, numbers or math still needs the user's decision.

## 1. Inventory

Read in full the preamble and macros, the sections you will work on, the sections they refer to, and everything that holds results (tables, figure captions), so that no claim is checked against material you haven't read. In a short paper, simply read everything. In a long one, skim the rest (headings, comment and TODO macros, labels), search the `.bib` and parked or commented material (read-only unless asked) for what the task needs, and read them in full when the task requires it; a full consistency pass (§8) reads everything. For each section note what exists, its state (notes / rough draft / near-final), open TODOs and co-author comments, and gaps. Report the inventory briefly before writing.

## 2. Planning file `PAPER_PLAN.md`

Short (aim for under ~100 lines), in the project root; it survives interrupted sessions. Git handling as in `paper-submission-prep`: in a git repo, unless already recorded, ask whether it goes in `.git/info/exclude`, `.gitignore`, or is tracked; without git, ignore these rules. Sections:
- **Settings**: the answers from §0.2 (edit flow, venue/audience, git handling, TODO removal, reply format, `.bib` maintenance, who commits) and the build command.
- **Story**: the paper in one paragraph, and the numbered contribution list.
- **Outline**: one line per section: its purpose and which material goes there.
- **Notation**: symbol, meaning, macro, only for symbols that are non-obvious, project-specific or at risk of clashing; one meaning per symbol. If the paper has a notation section or a macros file, point to it instead of copying it.
- **Status**: per section: state, chosen intensity (§4), open TODOs; in a git repo, the commit the status reflects.
- **Open questions**: for the authors or co-authors, one line each; move to the status line once answered.

When you create `PAPER_PLAN.md`, or change its story or outline, summarise in chat the story (one or two sentences), the contribution list, the outline (one line per section) and only the blocking open questions: this is the proposal to agree on in §3. Say the full plan is in the file, which the user can discuss or edit directly; don't paste it.

When a session resumes from an existing `PAPER_PLAN.md`, read it first and open with a one-line status (e.g. "Resuming: Section 3 drafted, Section 4 next, 2 open questions"). The file as you find it is the reference, including any edits the user made directly.

Keep the plan in sync with the text. On resume and after each pull, look at what changed since the recorded commit (`git diff <commit>`; without git, re-read the sections the plan marks as in progress) and update the status of the affected sections. Point out changes that disagree with the plan (a renamed symbol, a section that changed purpose, an open question answered in the text) instead of silently adopting or reverting them.

## 3. Story and outline before prose

Agree on the contribution list and the outline before drafting. Propose them from the material; the authors decide. Flag material that fits nowhere, and contributions the material doesn't yet support.

If the request covers a single section, agreeing on that section's outline is enough (its purpose, the order of its points, which material goes where); check that it fits the paper's story if one is recorded, and don't require an outline of the whole paper.

## 4. Drafting and revising, one section at a time

- **Ask the intensity for each section** and record it (in quick mode the request usually implies it, e.g. "proofread" is a copyedit and "polish" a polish; ask only if unclear): *copyedit* (grammar, typos, wording), *polish* (clarity and flow, same structure), *restructure* (reorder and merge paragraphs, same content), *rewrite from notes* (new prose from the material).
- **Keep the authors' math, claims and voice.** Use the most finished sections as a style sample: sentence length, "we" vs passive, how results and references are introduced. Translate notes in other languages into the paper's language.
- **Gaps become `\TODO{...}`** saying what is missing (a number, a proof step, a reference, a figure), never filler or plausible-sounding content.
- **TODOs as material.** Sort TODOs into those that can be written from the existing material and those that need the authors (new results, experiments, decisions, missing data). Write the first kind like any other text, at the section's chosen intensity; list the second kind under "Open questions". Ask once whether addressed TODOs may be removed after drafting, or left for the user to remove (default: leave them). Raw notes in `%` comments that have been turned into prose follow the same setting.
- **Replies to co-author comments.** When an edit fixes an issue raised in a co-author's comment, or answers it, add a brief reply next to the comment saying what was done or answering the question (e.g. "Done: rewritten as suggested, now uses Definition 2"). Never remove or edit the co-author's comment unless asked. Ask once how replies are written, matching what the project already uses: its author-note macro (e.g. `\AB{...}`), `todonotes` or `changes`, colored text, or a `% reply: ...` comment invisible in the PDF. If the choice needs a new package or macro, propose adding it to the preamble first.
- One section or task per round. With "propose", show the text or diff in chat at the chosen size: one paragraph or one change (a rewritten paragraph, a moved block, a reworded claim), or the whole section; apply only what was approved before moving to the next; options per proposal: apply, a variant, "Defer (keep as to-do)", "Won't do (decided)". Mechanical fixes with no real alternative (typos, `~` before `\cite`, one spelling variant) may be grouped into one proposal that lists every item, so the user can approve all or pick a subset. With "write + git diff", edit, then summarise what changed and why, and point to anything that needs the authors' judgement.

## 5. Hard rules

- **Never invent** results, numbers, experimental details, proofs, quotes or citations.
- **Unproven results stay unproven.** A statement without a proof (or without a source) is never written as a theorem, proposition or lemma, nor listed as a contribution. Write it as expected or conjectured ("we expect a bound of the form…"), with a `\TODO`, until the authors provide the proof.
- **Never silently change math or numbers.** If a formula, claim or number looks wrong or disagrees with another section, a table or a figure, flag it with both locations and let the authors decide.
- **Never remove** comment or TODO macros, or edit parked material, unless asked (or, for addressed TODOs, allowed in Settings). When an edit addresses a note, say which one in your summary; for co-author comments, also add a reply (§4).
- **Follow the project's conventions**: existing macros and environments rather than new ones (ask before defining one), the glossary rather than hand-written acronyms, existing label prefixes, `~` before `\cite`, `\ref` and `\eqref`, one sentence per line if that is the convention.
- No text copied from cited papers; related work is summarised in your own words.
- Say when something is your suggestion rather than a fix (e.g. "my suggestion: move Remark 3 to the appendix").

## 6. Writing style

Defaults for new text and hints when revising; the project's conventions and the authors' voice come first. When copyediting or polishing, change only what is unclear, inconsistent or wrong. Many points follow E. Medvet's [How to write scientific documents](https://medvet.inginf.units.it/teaching/how-to-write/); point users to it for details.
- **Flow**: sentences, paragraphs and sections connect (the reader knows why each comes next); one main idea per paragraph; dense stretches of definitions or formulas get a sentence of motivation.
- **No repetition** beyond the usual overview in abstract, introduction and conclusion; but keep technical terms identical throughout rather than varying them for style.
- **Abstract**: context, the gap, the proposal tied to that gap, the evaluation and its main results.
- **Tense and voice**: present for abstract, introduction and method; past for related work and what was done in experiments; be consistent. Active "we" for the authors' choices.
- **Wording**: no contractions; one spelling variant (US or UK); commas around "e.g." and "i.e."; acronyms introduced at first use; no unsupported hype ("novel", "significantly" without a test, "clearly").
- **Notation**: define every symbol before or right where it is first used; prefer one letter per entity, related quantities via subscripts (`n_\text{pop}`, not `pop`); words in math inside `\text{}` or `\mathrm{}`; `\max`, `\min` and `\DeclareMathOperator` for operators; follow the field's conventions.
- **LaTeX typography**: `\dots` for ellipses; `\emph{}` for emphasis; blank lines for paragraphs, not `\\`; `` ``…'' `` for quotes; `\ ` after a period that does not end a sentence (`vs.\ `); `~` before references and citations; en-dash `--` for ranges, em-dash `---` for asides.

## 7. Citations

- Mark claims that need support. Cite according to the generality of the claim: seminal papers, monographs or established reviews for general statements; the papers that actually establish a result for specific statements.
- Propose specific references only after verifying them online (DOI, authors, title, year, venue: doi.org, Crossref, arXiv, publisher page). If you can't verify, including when web access is unavailable or blocked, leave `\TODO{cite: ...}` with what kind of reference is needed, say that verification couldn't be run, and never fill in metadata from memory.
- Keep citation TODOs short, so the PDF stays readable (e.g. `\TODO{cite: DeepONet, FNO}`); put the full candidates (authors, title, venue, year, DOI) in your summary and under "Open questions" in `PAPER_PLAN.md`.
- **How the `.bib` is maintained.** Unless recorded, ask at the first citation task whether the `.bib` is auto-exported from a reference manager (e.g. Zotero with Better BibTeX), exported manually from one, or edited by hand, and record it in Settings. Never modify the user's reference library yourself.
  - Auto-exported: never edit the `.bib`, since changes would be overwritten at the next export. List the fixes and new entries for the user to make in the reference manager. Changing the year or authors there can change the generated citation key and break `\cite` commands: point this out, and suggest pinning the old key (Better BibTeX supports pinned keys) or offer to update the `\cite` commands.
  - Exported manually: fixes made in the `.bib` are lost at the next export, so also list them for the user to make in the reference manager.
- Add entries to the `.bib` only after approval (unless it is auto-exported), in the existing key and field style. Never fabricate an entry.
- **Bibliography refresh** (on request, or offered in §8): look for stale entries (preprints that now have a published version, wrong year or venue, missing DOI) and duplicates (the same paper under two keys, typically a preprint and its published version). Compare against the user's library when it is reachable (a Zotero MCP server, Zotero's local API at `http://localhost:23119/api/` with Zotero open and the local API enabled, or a Better BibTeX export) and against arXiv and Crossref. The library shows what the user has, not what is correct: verify metadata online as above before proposing it.
  - Read the library only. Use the Zotero web API only if the user asks, since it needs an API key and sends requests to zotero.org.
  - If the library isn't reachable, or there is none, say so and check online sources only.
  - Report each stale entry with the proposed replacement and its source, and keep its citation key. For duplicates, propose keeping the journal or conference version under one key and updating the `\cite` commands that use the other.
  - Apply only what is approved, following how the `.bib` is maintained (above).

## 8. Consistency passes

On request, or at the end of a round of drafting:
- notation and terminology against `PAPER_PLAN.md`; acronyms through the glossary;
- labels and cross-references; every figure and table referenced in the text;
- abstract, introduction and conclusion against the contribution list;
- claims against the numbers in tables and figures;
- tense and person (§6);
- repetitions across sections, and how the sections flow into each other;
- the bibliography refresh (§7): offer it, and run it only if the user agrees.

Report findings as a list with locations; fix only what the user approves (or what the chosen edit flow allows).

## 9. Build and check

After each round, build with the project's command (ask if unknown). Check the log for errors and for undefined references and citations, and compare page count and warnings with the previous build. Report plainly; if you couldn't build, say so. A check that prints nothing is not a pass: make sure it ran. BibTeX exits with an error when the paper has no `\cite` yet ("I found no \citation commands"); that is not a broken build, so run the remaining LaTeX passes and say so.

## 10. On request

- **Referee pass**: a fresh agent, without the conversation's context, reads a section or the whole paper as a reviewer of the target venue would, and lists weaknesses (unclear contributions, missing comparisons, unsupported claims, hard-to-follow parts). Give the findings to the user; don't apply them automatically.
- **latexdiff for co-authors**: a PDF marking the changes since a given commit. Work on a copy of the project (with `.git`) outside the user's tree: `latexdiff-vc --git --flatten -r <commit> main.tex`, then build the resulting `main-diff<commit>.tex`. If `latexdiff` isn't installed, say so.

## 11. End of each round

Update Status and Open questions in `PAPER_PLAN.md` (with the current commit, in a git repo). List the changed files and summarise what was drafted or revised, what was flagged, and what is next. In a git repo, remind the user to commit; if they use Overleaf, to sync too. Never commit unless explicitly asked, and only what was asked.

Once per paper, remind the authors to check the venue's policy on AI-assisted writing and whether it must be disclosed.
