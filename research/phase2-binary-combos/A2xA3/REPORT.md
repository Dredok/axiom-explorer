# Phase 2 — A2 × A3: Condensed × Perfectoid

## Bridge identified — multiple, all live

A2 × A3 is the most active intersection of any pair we examined. Phase 0
detected it as **frontier-bridged**; Phase 2 confirms an entire research
program at this junction.

### Live sub-programs

| Sub-program | Lead authors | Recent landmark |
|------------|--------------|-----------------|
| Prismatic cohomology | Bhatt-Scholze | foundational papers 2019-2022 |
| Pro-étale topology and v-stacks | Bhatt-Scholze | refined by Haine et al. |
| Geometrization of local Langlands | Fargues-Scholze | 2021 |
| Solid analytic stacks | Mann, Rodríguez Camargo | 2024-2026 |
| **Condensed homotopy type of schemes** | **Haine-Holzschuh-Lara-Mair-Martini-Wolf** | **arXiv:2510.07443 (Oct 2025), 103 pp** |
| Liquid Tannaka duality | Qaisar-Taroyan | arXiv 2025-11 |

The Haine et al. paper is **particularly striking**: they construct a
"condensed homotopy type" of a scheme that:

- Refines both the étale homotopy type of Friedlander-Artin-Mazur **and**
  the proétale fundamental group of Bhatt-Scholze.
- Surprises the authors themselves: the fundamental group of the condensed
  homotopy type of $\mathbf{A}^1_{\mathbf{C}}$ is **non-trivial** (the
  classical étale fundamental group is trivial in characteristic 0).
- Recovers Bhatt-Scholze's proétale $\pi_1$ via Noohi completion.
- Is often topological after passing to the quasi-separated quotient — also
  unexpected.

**Surprise factor**: the abstract uses "unexpectedly" and "surprisingly"
explicitly. This is the live front.

## Mathlib4 state at the A2 × A3 intersection

From Phase 1:

- `Mathlib/Condensed/*` (34 files) on the A2 side: definitions of condensed
  sets, light condensed, Solid module structure (with TODOs for the key
  structure theorems).
- `Mathlib/RingTheory/Perfectoid/*` (4 files) on the A3 side: perfection,
  untilt, Fontaine theta, B_dR. **Definitions present, deep theorems pending.**

**There is no Mathlib4 file that lives at the A2 × A3 intersection**:
- No `Mathlib/Condensed/Perfectoid.lean`.
- No prismatic cohomology in Mathlib4 at all.
- No solid module over a perfectoid ring.
- No condensed analytic stack.

This is a **wide gap** in the formal landscape. The mathematics is
extremely active; the formalization is far behind.

## TODO referenced in Mathlib4 that points right at this intersection

From `Mathlib/RingTheory/Perfectoid/FontaineTheta.lean` (Jiang, 2025):

> "Establish that our definition (explicit construction of θ mod p^n) agrees
>  with the deformation-theoretic approach via the cotangent complex, as in
>  [Bhatt's lecture notes on perfectoid spaces, Remark 6.1.7]."

The deformation-theoretic / cotangent complex approach is exactly where
prismatic cohomology lives. This TODO is a **named bridge** between the
explicit perfectoid construction in Mathlib4 and the prismatic / condensed
machinery that has not been imported yet.

## Phase 3 candidate shortlist (A2 × A3)

| ID | Candidate | Confidence | Type |
|----|-----------|------------|------|
| C-A2A3-1 | Lift the Mathlib4 Fontaine-θ TODO to a partial formalization of the cotangent-complex approach | L1 | Formalization gap with explicit pointer |
| C-A2A3-2 | Investigate the Haine et al. "condensed étale fundamental group" surprise: characterize precisely *which* schemes have non-trivial condensed π_1 vs trivial classical π_1 | L2 | Open characterization in a fresh paper |
| C-A2A3-3 | Lean 4 sketch of "solid R-module" for perfectoid R, building on Mathlib's `Solid.lean` and `Untilt.lean` | L2 | Genuine new formalization at the intersection |
| C-A2A3-4 | Examine Wärn's anomaly (introduced in A1 × A2 dossier) restricted to perfectoid base — does the failure of internal projectivity propagate or correct itself when R is perfectoid? | L3 | Speculative cross-pair link |

**C-A2A3-1 is the cleanest deliverable**: an explicit, well-cited TODO in
Mathlib4 already names the gap. A first-draft formalization would be a
real contribution.

**C-A2A3-2 is the most exciting**: Haine et al. just opened a structural
question (their paper is 103pp, just submitted Oct 2025, "comments
welcome"). The literature has barely had time to digest it. A
characterization theorem of "condensed-vs-classical π_1 gap" at this
moment of community attention is a high-yield candidate.

## Honesty notes

- The bibliometric Q4 picked up these author bridges precisely because of
  Bhatt+Scholze and Fargues+Scholze co-authorship; the Haine et al. paper
  was *not* in our Q2 results because no individual term in our axiom-list
  matched the title closely enough. **Lesson for the harness**: a future
  iteration should add "condensed homotopy type", "proétale fundamental
  group", "v-stack" to A2/A3 related_terms.
- The "surprise" framing in Haine et al. is the *authors'*, not ours; we
  do not claim independent discovery, only that the experiment correctly
  routed us to the live frontier where this surprise is happening.
- C-A2A3-2 is genuinely fresh: the paper is from Oct 2025 and 103pp; we
  cannot yet verify whether the literature already has a follow-up
  characterization theorem.

## Status for orchestrator

A2 × A3 has confirmed its frontier-bridged classification with
characteristic strength: multiple live programs, an unexpectedly-fresh
landmark paper (Haine et al.), and a clearly named formalization gap with
an explicit Mathlib4 TODO pointer. **Recommend advancing**.
