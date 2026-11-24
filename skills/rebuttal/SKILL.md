---
name: rebuttal
description: "Address external feedback on an existing LaTeX paper: referee or reviewer reports, revise-and-resubmit, major or minor revisions, writing the response (rebuttal) letter, or comments and edit requests that co-authors or advisors left in the text (e.g. \\XX{...} macros, todonotes, % comments). Use ONLY when someone else's comments or requests must be answered. Not for polishing, proofreading, drafting or improving a paper on the authors' own initiative (even if the text contains comment macros), and not for venue formatting. Every issue is handled one at a time with the reviewer's verbatim quote, the paper snippet and the exact diff, and the user approves each change. It never invents results, experiments or citations, and never commits unless asked."
---

# Rebuttal

Help the authors answer feedback they received: reviewer reports, or comments co-authors and advisors left in the text. The authors decide what to change and how to answer; you organise the issues, propose changes and replies, and apply only what is approved. Every proposal shows where the request comes from (the reviewer's exact words and location) and where it lands in the paper.

**Scope.** Only someone else's feedback. For polishing, proofreading or rewriting on the authors' own initiative, say this skill doesn't apply and work without it (with `latex-style` if present), leaving comment macros untouched unless the user mentions them; if ambiguous (e.g. "work on Section 3" in a section full of `\XX{}` comments), ask. Venue formatting: `paper-submission-prep`, if present.

The skill is self-contained: apply other skills it names only if installed. Ask questions with AskUserQuestion, or, if unavailable, in chat with numbered options, waiting for the answer.

## Two modes

In a first session (no `rebuttal/STATUS.md` yet), the first question is the mode, unless the request already makes it clear:

- **Quick internal review** (co-author or advisor comments, typically in the text): no planning files, no letter, no setup questions up front; ask each when it first matters (the reply macro at the first comment; compile only if the build command is known or the user wants it). Still apply: the issue list in chat (§1) in the user's order; one change at a time with quote, location and diff, mechanical items batched (§3); replies and `\XXdone` if wanted (§5); git rules (§6) and hard rules (§7). If the job grows (a letter is needed, deferred items pile up, more than one session), offer to switch to detailed mode, creating the planning files from the current state.
- **Detailed rebuttal to a journal or conference**: the full workflow: setup (§0), planning files (§2), response letter (§4).

## 0. Pre-flight (detailed mode)

**Resuming** (`rebuttal/STATUS.md` exists): pull first if the project syncs with Overleaf; read `STATUS.md` and `OPEN.md` (not `ARCHIVE.md`), relying on Settings instead of re-reading the preamble; run the resume check (§2); open with a one-line status counting every status ("Resuming: 13 issues: 4 applied, 1 declined, 6 to discuss, 1 deferred, 1 open"); ask about any mismatch before asking which issue is next.

**First session.** Read the project's `CLAUDE.md`, the preamble (comment macros and their colors, packages such as `xcolor`) and how the paper is built. Infer what the workspace answers and say so (no comment macros: skip 4; a letter already containing the comments settles 2; a build command in `CLAUDE.md` settles where to compile; no git: skip 6). Ask the rest in up to two batches (AskUserQuestion takes 4 questions per call), most important first, and record the answers in `STATUS.md`.

1. **Where the feedback is**: reviewer reports (files in the project, pasted text, PDF, email), comments in the text (which macros, e.g. `\XX{...}`, `\YY{...}`, `\todo{...}`), or both.
2. **Response letter** (for reviewer reports): needed or not.
   - If a letter **already containing the reviewers' comments** exists, work on it directly; it is the source of the quotes (§1).
   - Otherwise ask for a template (the journal's or the user's) and copy the comments verbatim into it, following its style (environments, numbering, how replies are set apart). With none, offer `references/revision_letter_template.tex` from this skill (if present): a cover letter to the editors, then one section per reviewer with each comment quoted in the reviewer's color and the reply below it.
3. **How changes are marked in the manuscript**, if the journal asks: latexdiff at the end, a colored macro (e.g. `\rev{...}`), or none. A color macro can't show deletions or moved text: mention them in the letter, or recommend latexdiff if they must be visible. Its color must differ from the existing comment macros (it may match the letter's color for that reviewer).
4. **Replies to in-text comments**: the user's own macro (e.g. `\ME{...}`), and whether replies go right after each comment. If yes, propose (as preamble diffs, approved first): `\usepackage{xcolor}` if missing; a reply macro, if none exists, in a clearly visible color (blue, orange, red, ...) different from every commenter's and from the change macro (§0.3); a "done" variant of each commenter macro, e.g. `\newcommand{\XXdone}[1]{\textcolor{gray}{[XX: #1]}}` (§5).
5. **Compilation**: after each applied change, "Yes (Recommended)" or "No" (then flag every change as untested and ask the user to compile). Where: the session scratch directory (default), a project folder such as `build/` (git handling as for `rebuttal/`), or a user path.
6. **Git and Overleaf**: how git handles `rebuttal/`: `.git/info/exclude` (local, never pushed; recommended with Overleaf), `.gitignore`, or tracked; whether the project syncs with Overleaf (then pull first, stop on merge conflicts). Don't ask about commits (§7).
7. **Archive**: "Keep `ARCHIVE.md` (Recommended)", one line per settled issue, or "Delete settled issues from `OPEN.md`", relying on the `STATUS.md` index and git.

The edit flow is fixed: propose in chat, apply after approval. If there are several main files (e.g. `main.tex` and a journal version), ask which ones the revision targets (often all that `\input` the edited sources, or what the journal requests): preamble changes go in each of those, and builds cover them all.

## 1. Intake: the issue list

**A checkable source for every quote**: a text file with line numbers.
- Reports already in the project (text, `.tex`, or the letter): cite them in place.
- Pasted, PDF or email reports: save them verbatim once to `rebuttal/reviews/R1.txt`, `R2.txt`, ... (editor: `E.txt`), giving fixed `file:line` references without re-reading the PDF each session. For PDFs fix only extraction artefacts (hyphenation, ligatures); never paraphrase or tidy.
- Before showing a quote, verify it: grep a short distinctive phrase to find the line (quotes often span lines), then compare the full quote with whitespace collapsed. If not found, don't present it as a quote; say so and give the location only.

**Atomic issues**: one per request; a comment asking for two things becomes `R2.3a`, `R2.3b`, sharing the quote. **IDs** are stable and never reused: `R<reviewer>.<n>` (`E.<n>` for the editor) in report order; `<MACRO>.<n>` (e.g. `XX.4`) for in-text comments, in source order.

**A new round of review** (new reports after a revision was submitted): keep the previous round's files as a read-only record, save the new reports in `reviews/round2/`, prefix the new IDs with the round (`2R1.3`), and start a new index in `STATUS.md`, linking to an earlier issue when a reviewer comes back to it.

**Each issue records**: the quote and its location; for in-text comments an **anchor** (a short distinctive phrase, to find the comment after lines shift); the paper location and snippet (`sec3.tex:120-124`, or "general"; in the index, file and section rather than lines, which shift); category; owner.

**Owner and duplicates.** A point raised by several reviewers belongs to the first (lowest reviewer number, then earliest comment), whose letter section gets the full answer. Later mentions get their own ID, marked as duplicates, and their reply refers to the owner's ("Please see our reply to Reviewer 1, Comment 3"), adding only what is specific. An in-text comment asking the same as a reviewer issue is a duplicate settled by that issue's decision, with no separate question; when applied, it becomes `\XXdone` with a reply pointing to the issue (§5).

**Categories**:
- `mechanical`: a change with no real alternative (a typo, a word swap the reviewer spelled out, a missing reference to a figure). Deleting content, or changing a claim, a number or math, is never mechanical, even if the request names the exact text;
- `edit`: a change that needs drafting (a clarification, a new paragraph, a reworded claim);
- `new-work`: needs material only the authors can provide (experiments, proofs, data, new figures);
- `answer-only`: a question or remark answered in the letter, possibly with no change to the paper. If the answer needs knowledge only the authors have (why a figure looks as it does, what a result means), ask for it; if they don't know yet, set `discuss` with a `\TODO`. You may offer your own explanation, labelled as an unchecked suggestion;
- `disagree`: the authors may want to argue against the request.

Show the issue list in chat as a compact table (ID, owner, one-line summary, category, paper location), then ask about the order: "Mechanical batch first (Recommended)", "In report order", "By reviewer", or Other with a list of IDs (skip the options that make no difference, e.g. "By reviewer" with one reviewer). Follow the user's order; at the end of each issue or batch, say what comes next.

## 2. Planning files in `rebuttal/`

They survive interrupted sessions and are split so a session loads only what it needs. Keep them concise: one line per item where possible, issues referred to by ID.

- **`STATUS.md`** (always read; under ~80 lines plus the table): **Settings** (answers from §0, build command, date, current commit) and the **Index** `| ID | Owner | Summary | Paper loc | Category | Status |`, one row per issue.
- **`OPEN.md`** (read when picking the next issue and at round end): full entries (quote and location, paper location, plan or question) in **To do** (not yet proposed), **To discuss with co-authors** (applied or proposed but needing a co-author's agreement, and `new-work` author tasks; with question, options, current state) and **Deferred**.
- **`ARCHIVE.md`** (if kept, §0.7; append only; read only if asked): settled issues, one line each (ID, what was done or why declined, date, commit). Without it, settled issues are deleted from `OPEN.md` and the index row is the only record, with a declined issue's reason in its Summary.
- **`reviews/`**: verbatim reports, only when needed (§1).

Statuses: `open`, `proposed`, `applied`, `deferred`, `discuss`, `declined`. Update the index and move the entry right after each decision. Details live only in `OPEN.md`; the index just points to them. The files as you find them are the reference, including the user's direct edits.

**Resume check** (a few greps, not a re-read): every `open`/`deferred`/`discuss` row has an `OPEN.md` entry and vice versa; each unsettled in-text issue's anchor is still inside `\XX{...}`, each applied one inside `\XXdone{...}` (or followed by a reply if there is no done macro), and a reply saying something was done matches a change actually there. List mismatches (typically hand edits or comments answered on Overleaf) and ask which side is right; never fix them silently.

## 3. One issue at a time

**Each non-mechanical issue** gets one self-contained question with:
1. **What the reviewer asks**: the verbatim quote and location (`rebuttal/reviews/R2.txt:14`, `response.tex:88`, `sec3.tex:88`);
2. **Where in the paper**: the current snippet with `file:line`;
3. **The change**: the exact diff in the option's preview, one per variant when real alternatives exist. A long diff (over ~15 lines) goes in chat just before the question, with one-line option labels;
4. **The reply**: the proposed letter text and/or inline reply (`\ME{...}`).

Options: "Apply as proposed (Recommended)", variants, "Defer", "Discuss with co-authors"; decline via Other. With two variants (4-option limit), drop "Discuss" (still reachable via Other). Defer: status `deferred`. Discuss: applied or not as the user says, status `discuss`. Declined: status `declined`, archived (§0.7) with the reason, which you ask the user for and use in the letter if needed. If the user asks something or wants changes, answer or revise, then ask again.

**Mechanical issues**: one batch. List every item in chat (ID, quote with location, one-line diff), then ask one short question: "Apply all", "Choose individually" (then Implement / Don't implement per item), "Defer all", or Other with a subset of IDs.

**`new-work`**: never draft text reporting results, experiments or proofs that don't exist. Record it under To discuss as an author task with a `\TODO{...}` in the letter; once the authors provide the material, treat it as an `edit`.

**`disagree`**: ask the user's stance first (accept, partly accept, rebut); argue only from material in the paper or given by the authors, politely and with evidence.

**Applying**: only what was picked. Keep diffs clean (only the lines needed, no rewrapping, keep `%` comments) and follow the project's conventions (macros, label prefixes, one sentence per line) and `latex-style` if present. Wrap new text in the change macro, if one was chosen (§0.3). Compile if chosen (§6) and report.

## 4. Response letter

- **One section per reviewer** (and the editor), each issue in its owner's section in report order; duplicates refer to the owner's reply (§1).
- **Per comment**: the verbatim text (only the markup LaTeX needs may change: math mode, quotes, escaped characters; never the wording), one reply covering all its parts (`a`, `b`, ...), and where the paper changed (section, equation, figure, table; via `\ref` if compiled with the manuscript, else in words). Page and line numbers only at the final build, since they shift.
- **Replies only for settled issues**: `applied` (what was done), `declined` (why, in the authors' words), `answer-only`. Others get a `\TODO{...}`. Never promise anything on the authors' behalf.
- **Tone**: thank each reviewer once, at the start of their section; no over-apologising; concise, factual, polite.

## 5. In-text comments

- **Applied**: replace `\XX{` with `\XXdone{` for that occurrence only (if the done macro was agreed, §0.4) and add the reply right after the comment, e.g. `\XXdone{I don't like this plot, replace it} \ME{Done: replaced with Figure~\ref{fig:new}.}`.
- **Nested braces** (`\XX{see \cite{x} and \textbf{this}}`): replace only the `\XX{` prefix, and find the comment's end by counting balanced braces, never with a regex up to the first `}`.
- **Deferred or discussed**: keep `\XX`; reply only to state the open question or current state, if the user agrees. **Declined**: keep `\XX`, reply with the user's reason.

## 6. Compilation, git and the end of each round

**Compilation** (if chosen, §0.5):
- Compile on a copy in the chosen build folder, never in the user's tree (excluding `.git`, `rebuttal/` and the build folder).
- Build a baseline from the sources as they were before any change (including approved preamble changes; e.g. from `git archive HEAD`); after each change compare errors, undefined references and citations, new warnings (e.g. overfull boxes), page count. Errors already in the baseline: report once, record in Settings, fix only if asked.
- A check that prints nothing is not a pass. BibTeX's "I found no \citation commands" is not an error when nothing is cited yet. If something can't be compiled or tested, say so. biber on macOS (universal TeX Live binary) may fail with "extracting arm64 binary with lipo failed": run `lipo "$(which biber)" -thin arm64 -output <build>/biber-arm64` and use that binary, without changing the user's system.
**Overleaf**: pull before starting, stop and ask on merge conflicts. If the user brings files back from Overleaf, re-check only those files for applied changes.

**End of each round**: compile (if chosen) and report plainly; update `STATUS.md` (with the commit) and move settled entries to `ARCHIVE.md` or delete them (§0.7); list every changed file and `git diff --stat`, reminding the user to commit them all and push or sync with Overleaf (uncommitted changes are easily lost); summarise applied, deferred, to discuss, declined, and what is next.

**End of the revision**, offer:
- a draft of the cover letter's summary of the main changes (if the letter has one), built only from `applied` issues, for the user to approve;
- a latexdiff PDF against the submitted version, if the journal wants one: on a copy with `.git` outside the user's tree, run `latexdiff-vc --git --flatten -r <commit> main.tex` and compile the result (say so if `latexdiff` is missing);
- a final check: no commenter macros (`\XX{`) left that should be addressed, no `\TODO` in letter or paper, every issue `applied`, `declined`, `answer-only`, or left open by the user's choice.

## 7. Hard rules

- **Quotes are verbatim and checked** against their source; never paraphrase a reviewer inside a quote.
- **Never invent** results, numbers, experiments, proofs, citations or reasons for declining.
- **The letter never claims** a change that wasn't applied.
- **One decision per issue**, except approved mechanical batches; never infer approval from silence, an earlier approval or a related answer.
- **Ask before any preamble change** (packages, macros, colors), in the manuscript and the letter alike (e.g. a `\TODO` macro the template lacks).
- **No new claims in drafted text**: new text may not promote a statement the paper doesn't support (e.g. "negligible cost" with no timings) to a contribution or a stronger claim. Untested ideas are written as such ("could", "we did not test"); examples or methods taken from the reviewer get a `\TODO{cite: ...}` rather than going in uncited.
- **Never edit or delete** a commenter's text unless asked.
- **Never commit** unless explicitly asked, and then only what was asked; a request covers that commit, not later ones.
- Say when something is your suggestion rather than what the reviewer asked for.
