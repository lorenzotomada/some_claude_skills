---
name: rebuttal
description: "Address external feedback on an existing LaTeX paper: referee or reviewer reports, revise-and-resubmit, major or minor revisions, the response (rebuttal) letter, or comments and edit requests co-authors or advisors left in the text (e.g. \\XX{...} macros, todonotes, % comments). Use ONLY when someone else's comments must be answered; not for polishing, proofreading or drafting on the authors' own initiative (even if the text has comment macros), nor for venue formatting. Each issue is handled one at a time with the reviewer's verbatim quote, the paper snippet and the exact diff, approved by the user. Never invents results, experiments or citations; never commits unless asked."
---

# Rebuttal

Help the authors answer feedback: reviewer reports, or comments co-authors and advisors left in the text. The authors decide what to change and how to answer; you organise the issues, propose changes and replies, and apply only what is approved, always showing where a request comes from (the reviewer's exact words and location) and where it lands in the paper.

**Scope.** Only someone else's feedback. For polishing or rewriting on the authors' own initiative, say this skill doesn't apply and work without it (with `latex-style` if present), leaving comment macros untouched unless mentioned; if ambiguous ("work on Section 3" in a section full of `\XX{}` comments), ask. Mixed requests ("clean up Section 2 and resolve the comments there"): comments first with this skill, then ordinary editing. Venue formatting: `paper-submission-prep`, if present.

The skill is self-contained: apply other skills it names only if installed. Ask with AskUserQuestion, or, if unavailable, in chat with numbered options, and wait.

## Two modes

In a first session (no `rebuttal/STATUS.md`), first ask the mode, unless the request makes it clear:

- **Quick internal review** (co-author or advisor comments, typically in the text): no planning files, no letter, no setup questions up front; ask each when it first matters (the reply macro at the first comment; compile only if the build command is known or the user wants it). Still apply §1 (issue list in chat, user's order), §3 (one change at a time with quote, location and diff; mechanical items batched), §5 if replies are wanted, §6 and §7. If the job grows (a letter is needed, deferred items pile up, several sessions), offer to switch to detailed mode, creating the planning files from the current state.
- **Detailed rebuttal to a journal or conference**: the full workflow (§0–§7).

## 0. Pre-flight (detailed mode)

**Resuming** (`rebuttal/STATUS.md` exists): pull first if synced with Overleaf; read `STATUS.md` and `OPEN.md` (not `ARCHIVE.md`), relying on Settings instead of re-reading the preamble; run the resume check (§2); open with a one-line status counting every status ("Resuming: 13 issues: 4 applied, 1 declined, 6 to discuss, 1 deferred, 1 open"); ask about mismatches before asking which issue is next.

**First session.** Read the project's `CLAUDE.md`, the preamble (comment macros and their colors, packages such as `xcolor`) and how the paper is built. Infer what the workspace answers and say so (no comment macros: skip 4; a letter already containing the comments settles 2; a build command in `CLAUDE.md` settles where to compile; no git: skip 6). Ask the rest in up to two batches (4 questions per call), most important first; record the answers in `STATUS.md`.

1. **Where the feedback is**: reviewer reports (project files, pasted text, PDF, email), comments in the text (which macros, e.g. `\XX{...}`, `\todo{...}`), or both.
2. **Response letter**: needed or not. If a letter **already containing the comments** exists, work on it directly (it is the source of the quotes, §1). Otherwise ask for a template (the journal's or the user's) and copy the comments verbatim into it, following its style; with none, offer `references/revision_letter_template.tex` (if present): a cover letter, then one section per reviewer, comments quoted in the reviewer's color, replies below.
3. **How changes are marked in the manuscript**, if the journal asks: latexdiff at the end, a colored macro (e.g. `\rev{...}`), or none. A color macro can't show deletions or moved text: mention them in the letter, or recommend latexdiff. One color for all changes, whichever reviewer they address, different from the comment macros and the reviewers' colors in the letter, which states it; per-reviewer colors only if the journal asks.
4. **Replies to in-text comments**: the user's own macro (e.g. `\ME{...}`), and whether replies go right after each comment. If yes, propose as preamble diffs: `\usepackage{xcolor}` if missing; a reply macro, if none exists, in a clearly visible color (blue, orange, red, ...) different from every commenter's and the change macro's; a "done" variant per commenter macro, e.g. `\newcommand{\XXdone}[1]{\textcolor{gray}{[XX: #1]}}` (§5).
5. **Compilation** after each applied change: "Yes (Recommended)" or "No" (then flag each change as untested and ask the user to compile). Where: the session scratch directory (default), a project folder such as `build/` (git handling as for `rebuttal/`), or a user path.
6. **Git and Overleaf**: `rebuttal/` in `.git/info/exclude` (local, never pushed; recommended with Overleaf), `.gitignore`, or tracked; whether the project syncs with Overleaf (then pull first, stop on merge conflicts). Don't ask about commits (§7).
7. **Archive**: "Keep `ARCHIVE.md` (Recommended)", one line per settled issue, or "Delete settled issues from `OPEN.md`", relying on the index and git.

The edit flow is fixed: propose in chat, apply after approval. With several main files (e.g. `main.tex` and a journal version), ask which the revision targets (often all that `\input` the edited sources, or what the journal requests); preamble changes go in each, and builds cover all.

## 1. Intake: the issue list

**A checkable source for every quote**: a text file with line numbers.
- Reports already in the project (text, `.tex`, or the letter): cite them in place.
- Pasted, PDF or email reports: save them verbatim once to `rebuttal/reviews/R1.txt`, `R2.txt`, ... (editor: `E.txt`), for fixed `file:line` references without re-reading the PDF. For PDFs fix only extraction artefacts (hyphenation, ligatures); never paraphrase or tidy.
- Verify a quote before showing it: grep a short distinctive phrase to find the line (quotes often span lines), then compare the full quote with whitespace collapsed. If not found, say so and give the location only.

**Atomic issues**: one per request (a two-part comment becomes `R2.3a`, `R2.3b`, sharing the quote). **IDs** are stable, never reused: `R<reviewer>.<n>` (`E.<n>` for the editor) in report order; `<MACRO>.<n>` (e.g. `XX.4`) for in-text comments, in source order.

**A new round of review**: keep the previous round's files as a read-only record, save the new reports in `reviews/round2/`, prefix new IDs with the round (`2R1.3`), and start a new index in `STATUS.md`, linking to earlier issues a reviewer returns to.

**Each issue records**: the quote and location; for in-text comments an **anchor** (a short distinctive phrase, to find the comment after lines shift); the paper location and snippet (`sec3.tex:120-124`, or "general"; in the index, file and section, since lines shift); category; owner.

**Owner and duplicates.** A point raised by several reviewers belongs to the first (lowest number, then earliest comment), whose letter section gets the full answer. Later mentions get their own ID, marked as duplicates, with a reply referring to the owner's ("Please see our reply to Reviewer 1, Comment 3") plus anything specific. An in-text comment asking the same as a reviewer issue is settled by that issue's decision, with no separate question; when applied, it becomes `\XXdone` with a reply pointing to the issue (§5).

**Categories**:
- `mechanical`: no real alternative (a typo, a word swap spelled out by the reviewer, a missing figure reference). Deleting content, or changing a claim, number or math, is never mechanical, even if the request names the exact text;
- `edit`: needs drafting (a clarification, a new paragraph, a reworded claim);
- `new-work`: needs material only the authors have (experiments, proofs, data, figures);
- `answer-only`: answered in the letter, possibly with no change to the paper. If the answer needs the authors' knowledge (why a figure looks as it does, what a result means), ask; if they don't know yet, set `discuss` with a `\TODO`. You may offer your own explanation, labelled as an unchecked suggestion;
- `disagree`: the authors may want to argue against the request.

Show the issues in chat as a compact table (ID, owner, summary, category, paper location), then ask the order: "Mechanical batch first (Recommended)", "In report order", "By reviewer", or Other with IDs (skip options that make no difference, e.g. "By reviewer" with one reviewer). Follow it; after each issue or batch, say what comes next.

## 2. Planning files in `rebuttal/`

They survive interrupted sessions and are split so a session loads only what it needs. Keep them concise: one line per item where possible, issues referred to by ID.

- **`STATUS.md`** (always read; under ~80 lines plus the table): **Settings** (answers from §0, build command, date, commit) and the **Index** `| ID | Owner | Summary | Paper loc | Category | Status |`.
- **`OPEN.md`** (read when picking the next issue and at round end): full entries (quote and location, paper location, plan or question) under **To do**, **To discuss with co-authors** (applied or proposed but needing a co-author's agreement, and `new-work` author tasks; with question, options, current state) and **Deferred**.
- **`ARCHIVE.md`** (if kept, §0.7; append only; read only if asked): one line per settled issue (ID, what was done or why declined, date, commit). Without it, settled issues are deleted from `OPEN.md`, and a declined issue's reason goes in its index Summary.
- **`reviews/`**: verbatim reports, only when needed (§1).

Statuses: `open`, `proposed`, `applied`, `deferred`, `discuss`, `declined`. Update the index and move the entry right after each decision. Details live only in `OPEN.md`; the index points to them. The files as you find them are the reference, including the user's direct edits.

**Resume check** (a few greps, not a re-read): every `open`/`deferred`/`discuss` row has an `OPEN.md` entry and vice versa; each unsettled in-text issue's anchor is still inside `\XX{...}` and each applied one inside `\XXdone{...}` (or followed by a reply); a reply saying something was done matches a change actually there. List mismatches (typically hand edits or comments answered on Overleaf) and ask which side is right; never fix them silently.

## 3. One issue at a time

**Each non-mechanical issue** gets one self-contained question with:
1. **What the reviewer asks**: the verbatim quote and location (`rebuttal/reviews/R2.txt:14`, `response.tex:88`, `sec3.tex:88`);
2. **Where in the paper**: the current snippet with `file:line`;
3. **The change**: the exact diff in the option's preview, one per variant when real alternatives exist. A long diff (over ~15 lines) goes in chat just before the question, with one-line option labels;
4. **The reply**: the proposed letter text and/or inline reply (`\ME{...}`).

Options: "Apply as proposed (Recommended)", variants, "Defer", "Discuss with co-authors"; decline via Other. With two variants (4-option limit), drop "Discuss" (still reachable via Other). Defer: `deferred`. Discuss: applied or not as the user says, `discuss`. Declined: `declined`, archived (§0.7) with the reason, asked from the user and used in the letter if needed. If the user asks something or wants changes, answer or revise, then ask again.

**Mechanical issues**: one batch. List every item in chat (ID, quote with location, one-line diff), then ask: "Apply all", "Choose individually" (then Implement / Don't implement per item), "Defer all", or Other with a subset of IDs.

**`new-work`**: never draft text reporting results, experiments or proofs that don't exist. Record it under To discuss as an author task, with a `\TODO{...}` in the letter; once the authors provide the material, treat it as an `edit`.

**`disagree`**: ask the user's stance first (accept, partly accept, rebut); argue only from the paper or the authors' material, politely and with evidence.

**Applying**: only what was picked. Keep diffs clean (only the lines needed, no rewrapping, keep `%` comments), follow the project's conventions (macros, label prefixes, one sentence per line) and `latex-style` if present, wrap new text in the change macro if chosen (§0.3), then compile if chosen (§6) and report.

## 4. Response letter

- **One section per reviewer** (and the editor), each issue in its owner's section in report order; duplicates refer to the owner's reply (§1).
- **Per comment**: the verbatim text (only LaTeX markup may change: math mode, quotes, escapes such as `\%`, `\&`; never the wording; verify it against the source ignoring that markup), one reply covering all its parts (`a`, `b`, ...), and where the paper changed (section, equation, figure, table: in words, or via `\ref` only if the letter loads `xr`/`xr-hyper`, otherwise it prints `??`). At the final build, add page and line numbers if wanted, and recheck hand-written numbers of figures, tables, equations and sections.
- **Replies only for settled issues**: `applied` (what was done), `declined` (why, in the authors' words), `answer-only`; others get a `\TODO{...}`. Never promise anything on the authors' behalf.
- **Tone**: thank each reviewer once, at the start of their section; no over-apologising; concise, factual, polite.

## 5. In-text comments

- **Applied**: replace `\XX{` with `\XXdone{` for that occurrence only (if agreed, §0.4) and add the reply right after the comment, e.g. `\XXdone{I don't like this plot, replace it} \ME{Done: replaced with Figure~\ref{fig:new}.}`.
- **Nested braces** (`\XX{see \cite{x} and \textbf{this}}`): replace only the `\XX{` prefix; find the comment's end by counting balanced braces, never with a regex up to the first `}`.
- **Deferred or discussed**: keep `\XX`; reply only to state the open question or current state, if the user agrees. **Declined**: keep `\XX`, reply with the user's reason.

## 6. Compilation, git and the end of each round

**Compilation** (if chosen, §0.5):
- Compile on a copy in the chosen build folder, never in the user's tree (excluding `.git`, `rebuttal/` and the build folder).
- Baseline: the sources before any change, preamble changes included (e.g. from `git archive HEAD`). After each change compare errors, undefined references and citations, new warnings (e.g. overfull boxes), page count. Errors already in the baseline: report once, record in Settings, fix only if asked.
- A check that prints nothing is not a pass. BibTeX's "I found no \citation commands" is not an error when nothing is cited yet. If something can't be compiled or tested, say so. biber on macOS (universal TeX Live binary) may fail with "extracting arm64 binary with lipo failed": run `lipo "$(which biber)" -thin arm64 -output <build>/biber-arm64` and use that binary, without changing the user's system.

**Overleaf**: pull before starting, stop and ask on merge conflicts. If the user brings files back from Overleaf, re-check only those for applied changes.

**End of each round**: compile (if chosen) and report plainly; update `STATUS.md` (with the commit) and move settled entries to `ARCHIVE.md` or delete them (§0.7); list every changed file and `git diff --stat`, reminding the user to commit them all and push or sync with Overleaf; summarise applied, deferred, to discuss, declined, and what is next.

**End of the revision**, offer:
- a draft of the cover letter's summary of changes (if it has one), only from `applied` issues, for approval;
- a latexdiff PDF against the submitted version, if the journal wants one: on a copy with `.git` outside the user's tree, run `latexdiff-vc --git --flatten -r <commit> main.tex` and compile it (say so if `latexdiff` is missing). If it doesn't compile, retry once with `--math-markup=0`; if it still fails, report the error and fall back to the change macro, without debugging latexdiff further;
- a final check: no commenter macros (`\XX{`) left to address, no `\TODO` in letter or paper, every issue `applied`, `declined`, `answer-only`, or left open by the user's choice.

## 7. Hard rules

- **Quotes are verbatim and checked** against their source; never paraphrase a reviewer inside a quote.
- **Never invent** results, numbers, experiments, proofs, citations or reasons for declining.
- **The letter never claims** a change that wasn't applied.
- **One decision per issue**, except approved mechanical batches; never infer approval from silence, an earlier approval or a related answer.
- **Ask before any preamble change** (packages, macros, colors), in the manuscript and the letter alike (e.g. a `\TODO` macro the template lacks).
- **No new claims in drafted text**: never promote a statement the paper doesn't support (e.g. "negligible cost" with no timings) to a contribution or a stronger claim. Write untested ideas as such ("could", "we did not test"); examples or methods taken from the reviewer get a `\TODO{cite: ...}`, never go in uncited.
- **Never edit or delete** a commenter's text unless asked.
- **Never commit** unless explicitly asked, and then only what was asked; a request covers that commit, not later ones.
- Say when something is your suggestion rather than what the reviewer asked for.
