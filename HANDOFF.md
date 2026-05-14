# Handoff to the next session

> This file is the entry point for any agent picking up the
> `axiom-explorer` project. It is versioned in `main`, so it is
> visible from any clone (or via opencode web, GitLab UI, etc.) even
> when local `.agent/` state is absent.

## Status snapshot (as of 2026-05-01)

- **Phase 0 → Phase 7 toolchain complete**. All merged to `main` via 11 MRs.
- **51 tests green**, ruff clean, Lean module builds.
- **CI: paper-pdf job builds the preprint with latexmk + texlive** in ~50 s.
- **CI: publication-bundle job produces Zenodo + arXiv-source ZIPs** as 90-day artifacts.
- **Top output**: candidate L2-strong cardinality envelope of the
  condensed classifying anima of spectral ∞-topoi, corroborated across
  3 branches (geometric, model-theoretic, set-theoretic).
- **Currently paused awaiting the user** to:
  1. Replace the three ORCID placeholders flagged in `docs/preprint_checklist.md`.
  2. Click "Publish" on Zenodo manually (orchestrator does not publish).
  3. Send the courtesy email to Haine using the draft kept locally at `.agent/EMAIL_DRAFT_HAINE.md` (gitignored; never committed to the public mirror).

## What to read, in order, before doing anything

1. **This file** — orientation and stop rules.
2. **GitLab issue #6** ("[Phase 7] Preprint to Zenodo, then email
   Haine") — the operational plan agreed with the user for the next
   step.
3. **`docs/synthesis/CONJECTURE.md`** — the central conjecture
   formulated as a synthesis paper draft. This is the object to
   publish.
4. **`.agent/EMAIL_DRAFT_HAINE.md`** (gitignored, local only) — the
   draft email to Peter J. Haine. Kept out of the public mirror by
   design; see commit history of MR !21 for the cleanup that removed
   it from the public repo.
5. **`research/phase4-final-report/REPORT.md`** — full meta-analysis
   of the run.
6. **`research/phase5-pi-n-cond/REPORT.md`** — the forward open
   question (K3 surface at n=2).

If you only have time for two files: `CONJECTURE.md` and issue #6.

## Phase 7 plan (agreed with user)

The user prefers this order, given they are not a frontier-area
mathematician and cannot sustain deep technical email exchanges:

1. **Write a preprint** formalising the conjecture.
2. **Publish on Zenodo** (DOI assigned).
3. **Send a short email** to Haine referencing the DOI, framed as
   "no need to reply unless obvious", not as a discussion invitation.
4. **Iterate** preprint versions if useful feedback arrives.

Rationale: the DOI puts the observation in the public record honestly,
the user retains control of the dispatch, and the email becomes a
courtesy notification rather than a request for deep dialogue.

## Concrete first steps for the next session

### Step A — publication infrastructure (DONE in MR !10)

The Zenodo bundle pipeline is built and CI-validated, following the
pattern of `research/vera-paper`:

- `paper/preprint.tex` + `paper/references.bib` → `latexmk -pdf` → `paper/preprint.pdf`.
- `scripts/build_publication_bundle.py` → `dist/publication/*.zip`.
- `.zenodo.json` + `CITATION.cff` at root for native Zenodo/ORCID linkage.
- `LICENSE` set to CC-BY-4.0.
- `.gitlab-ci.yml` jobs `paper-pdf` and `publication-bundle` with
  90-day artifacts.

**Nothing else to build for Step A.** Move directly to Step B.

### Step B — write the v1 preprint

Working title: *A cardinality envelope for the condensed classifying
anima of spectral ∞-topoi: a synthesis across geometric,
model-theoretic and set-theoretic instances.*

Mandatory sections (see issue #6 for full list):

- Abstract + plain-language summary.
- Statement of the conjecture (verbatim from
  `docs/synthesis/CONJECTURE.md`).
- Three corroboration angles with explicit citations.
- Structural argument (sketch, declared as such).
- Falsifiability statement.
- **Honest declarations**:
  - Author position: software/methodology background, NOT frontier
    mathematics expert.
  - Production method: axiom-explorer workflow, LLM-assisted, repo
    public.
  - Synthesis vs. claims of novelty.
  - Confidence ladder L0/L1/L2/L3 per claim.
- References with DOIs.

Length target: 15–30 pages. **Better short and defensible than long
and speculative.**

### Step C — user publishes Zenodo

Manual. Orchestrator stops at draft state.

### Step D — short email to Haine

Update `.agent/EMAIL_DRAFT_HAINE.md` (gitignored, local only) so it
is a one-screen note referencing the Zenodo DOI. Tone: "I published this
preprint, here's the DOI, no need to reply unless something is obvious to
you."

## Open questions for the user when next session starts

The next agent must ask the user (do not assume):

- **ORCID number** to embed in preprint metadata.
- **License preference** (default: CC-BY 4.0).
- **Peter J. Haine's email** (not collected this session).
- **Notify other authors?** Cherubini-Coquand-Geerligs-Moeneclaey
  for the Lean skeleton link, Bergfalk-Lambie-Hanson for the
  set-theoretic angle, etc. User decides.
- **Title finalisation**.

## Stop rules (non-negotiable)

- The orchestrator **does NOT publish** to Zenodo automatically. The
  final "Publish" click is the user's.
- The orchestrator **does NOT send** any emails. The orchestrator can
  compose; the user dispatches.
- The orchestrator **does NOT claim novelty** beyond what the
  synthesis paper claims, which is explicitly limited to "this
  unification, formulated thus, does not appear in any single
  source we found".
- The orchestrator **does NOT impersonate** mathematical authority.
  All preprint declarations of author position must reflect that
  the human author is at the boundary of formal methods and software
  engineering, not a frontier-area mathematics expert.

## Key paths

```
/mnt/fastpool/research/axiom-explorer/         (local)
gitlab.loneorc.com/research/axiom-explorer     (remote, private)

docs/synthesis/CONJECTURE.md                   (the object to publish)
.agent/EMAIL_DRAFT_HAINE.md                    (email draft, gitignored)
research/phase4-final-report/REPORT.md         (full context)
research/phase5-pi-n-cond/REPORT.md            (forward question)
src/axiom_explorer/                            (Python harness)
lean/AxiomExplorer/SyntheticStoneDuality.lean  (verified L0 deliverable)
artifacts/papers/*.pdf                         (downloaded papers, gitignored)
```

## Reproducibility notes for the next session

- All papers cited can be re-downloaded with `curl` from arXiv. Paths
  in `artifacts/papers/` are gitignored but reproducible.
- Mathlib4 shallow clone in `artifacts/mathlib4/` is gitignored;
  reproducible via the `git clone --depth=1 --filter=blob:none ...`
  command in `docs/adr/0001-workspace-scaffolding.md`.
- Lean toolchain: `leanprover/lean4:v4.16.0` pinned in
  `lean/lean-toolchain`. Install with `elan` if needed.
- Python env: `uv venv .venv && uv sync --extra dev` reconstructs the
  test environment.

## Final note

This run validated qualitatively the user's original hypothesis:
iterating from modern productive axioms across distinct branches has
higher density of relevant findings. The strongest output is a
falsifiable conjecture with 7 attestations and 0 falsifying witnesses
across 3 branches. The unification it sits on top of is announced in
2024-2026 papers; the experiment surfaced and synthesised, did not
invent. Next sessions should preserve this honest framing in any
publication that goes out.
