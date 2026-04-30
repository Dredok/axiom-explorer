# Phase 0 — Bibliometric Mapping (machine-generated draft)

- Started (UTC): `2026-04-30T23:44:00Z`
- Finished (UTC): `2026-04-30T23:50:29Z`
- Raw dumps: `data/phase0/raw`

## Method recap

For each binary combination of the four seeds we issued four query types against the arXiv API:

- **Q1**: strict AND of primary phrases (canonical signal).
- **Q2**: grouped (OR within each side) AND between sides — the main recall query and the basis for the density classification.
- **Q3**: primary × related, capped fanout, both directions.
- **Q4**: author co-publication queries between seeds' key authors. Catches community bridges when terminology does not co-occur.

## Density per binary combination

| Pair | Q1 hits | Q2 total | Q2 math-only | Q3 hits | Q4 bridge | shared authors | classification |
|------|---------|----------|--------------|---------|----------|----------------|----------------|
| A1xA2 | 1 | 1 | 1 | 0 | 0 | - | **virgin** |
| A1xA3 | 0 | 3 | 1 | 1 | 0 | - | **virgin** |
| A1xA4 | 0 | 1 | 1 | 0 | 0 | - | **virgin** |
| A2xA3 | 2 | 5 | 4 | 0 | 10 | Scholze | **frontier-bridged** |
| A2xA4 | 0 | 1 | 1 | 0 | 0 | - | **virgin** |
| A3xA4 | 0 | 13 | 8 | 0 | 0 | - | **sparse** |

## Classification legend

Classification uses Q2 *math-only* unique paper count (papers whose primary arXiv category is `math.*`). This removes physics/CS/cond-mat noise from generic terms ("diamond", "condensed", "tilting" match unrelated work in other archives).

- **saturated** (≥ 100): cross-area heavily explored.
- **warm** (30–99): well-trodden, novelty needs care.
- **warm-bridged** (5–29 + bridge): living frontier.
- **sparse** (5–29, no bridge): possibly artificial gap.
- **frontier-bridged** (< 5 + bridge): high-yield candidate.
- **virgin** (< 5, no bridge): true gap, possibly incompatible.

## Curator's pass (machine-suggested, to be reviewed)

- **Frontier-bridged** and **warm-bridged** pairs are the most likely to yield novel and connectable candidates, and should be prioritized for Phase 2.
- **Virgin** pairs deserve a short dossier to decide whether the gap is a research opportunity or an inherent incompatibility.
- **Saturated** pairs go to Phase 2 only if a sub-niche is identified where the harness can still add a new vantage point.

## Honesty notes

- arXiv's `all:` field searches abstract + metadata, not full text. Cross-community papers that use one side's terminology in the abstract but the other's only in the body will be missed by Q1/Q2/Q3.
- Q4 partially compensates this by indexing community membership via co-authorship, but the author lists in `seeds.py` are deliberately non-exhaustive.
- Classification thresholds are heuristic and should be revisited if the resulting prioritization disagrees strongly with the curator's read.

---

## Curator's analysis (manual pass on the raw dumps)

### A2 × A3 — Condensed × Perfectoid → **prioritize for Phase 2**

**Bibliometric reading.** Q2 reports only 4 math papers, but Q4 author bridges
return 10 high-impact papers including:

- Scholze + Bhatt: *Prisms and Prismatic Cohomology* (2019), *Prismatic F-crystals* (2021), *The pro-étale topology for schemes* (2013) — all `math.AG`/`math.NT`.
- Scholze + Fargues: *Geometrization of the local Langlands correspondence* (2021) — `math.RT`.
- Clausen + Bhatt: *Remarks on K(1)-local K-theory* (2020) — `math.KT`.

The school exists and is prolific. The reason Q2 looks small is structural:
authors writing in this intersection use one terminology per paper (a
prismatic-cohomology paper does not need to repeat "condensed" in the
abstract). The author bridge captures the truth.

**Phase 2 question.** What in this rich cross-area is *not yet a theorem*
but is a natural conjecture once both formalisms are accepted? Plausible
families:

1. Solid/liquid analogues of perfectoid-style tilting equivalences for
   non-archimedean Banach algebras.
2. Condensed reformulation of pro-étale and v-sheaves over diamonds; what
   is the universal property?
3. Prismatic cohomology in a fully condensed homological setting — where
   does Mann's solid analytic stack framework extend to integral Hodge?

### A3 × A4 — Perfectoid × Synthetic Ricci → **probe before committing**

**Bibliometric reading.** Q2 returns 8 math papers; on inspection most are
unrelated ("broken k-diamond partitions" in `math.CO`; "Diophantine
finiteness"; etc.). Two are real candidates:

- *Hausdorff dimension and failure of synthetic curvature bounds in the
  sub-Lorentzian setting* — `math.DG`, 2025-09. Genuinely synthetic curvature
  in a sub-Riemannian/sub-Lorentzian setting; tangentially adjacent to
  arithmetic geometry only via the Lorentzian/p-adic analogy.
- *A Lorentzian analog for Hausdorff dimension and measure* — `math-ph`, 2021.
  Synthetic dimension, Lorentzian, no perfectoid contact.

No author bridge. The two communities (Scholze school vs. Sturm-Lott-Villani
school) appear to have **zero co-publication on arXiv**.

**Curator's call.** **Sparse, possibly with a real gap.** The honest answer
is that no natural functor connects the perfectoid world (algebra over
p-adic fields, characteristic-p tilts) to the synthetic Ricci world (metric
measure spaces, Wasserstein optimal transport). Demote unless Phase 2
uncovers an unforeseen bridge (e.g., adelic/p-adic optimal transport × the
diamond formalism — a real but tiny corner of arithmetic geometry).

### A1 × A2, A1 × A3, A1 × A4, A2 × A4 — virgin

These four pairs share a common reading: **the HoTT/univalence community
and the synthetic-Ricci community have negligible overlap with arithmetic
geometry, condensed mathematics, and each other** at the arXiv-indexed
level.

Within these:

- **A1 × A2 (Univalence × Condensed)** has emerging activity (Cherubini's
  "synthetic algebraic geometry over HoTT", Coquand's group on cubical
  models for condensed) — this is **plausibly the most fertile of the four
  virgin pairs** despite the bibliometric silence, because the foundational
  question "what does condensed look like in a univalent foundation?" is
  natural and partially attacked.
- **A1 × A4 (Univalence × Synthetic Ricci)** is the most virgin: synthetic
  Ricci is fundamentally an *analysis* program; univalence is fundamentally
  *foundational/categorical*. The harness has no a-priori bridge.
- **A2 × A4 (Condensed × Synthetic Ricci)** — see A3 × A4: no community
  contact. There is one indirect angle via condensed-style reformulations
  of measure theory (Asgeirsson, Ben Moshe) but nothing on Wasserstein.
- **A1 × A3 (Univalence × Perfectoid)** — minimal direct work. Synthetic
  algebraic geometry over HoTT is the natural meeting point but does not
  reach perfectoid generality.

### Selected for Phase 2

Based on the above, **two pairs advance**:

1. **A2 × A3 (Condensed × Perfectoid)** — frontier-bridged, deeply active.
   Phase 2 task: identify open conjectures or unformalized landmark
   theorems and check what the harness can usefully say.
2. **A1 × A2 (Univalence × Condensed)** — virgin in arXiv but
   conceptually the most natural foundational question. Phase 2 task:
   read the recent (2023–2025) Cherubini/Coquand/Wärn line and locate a
   formal gap or a candidate inter-branch lemma.

**Held in reserve, not advanced now**:

- **A3 × A4** as a sanity check on whether the harness can detect
  inherent incompatibility (i.e., it should *not* yield a candidate).
- The remaining three virgin pairs are noted as background but not
  pursued in this run; they may be revisited if a bridging concept
  emerges in Phase 2.

### Honest meta-note on the Q4 false positive

An earlier run of the harness reported A3 × A4 as **warm-bridged** with 47
author-bridge papers because the unfiltered author search matched a "Bhatt"
and a "Lott" who are namesakes of the mathematicians in the LIGO/Virgo
gravitational-wave catalogue. The harness now restricts author-pair
queries to the `cat:math.*` archive and tests cover both cases. ADR-0002
documents this incident. The first lesson of Phase 0: **author-name
disambiguation is non-trivial, and bibliometric proxies need archive
filtering to be trustworthy.**
