# ADR 0002 — Bibliometric noise mitigation

- **Date**: 2026-04-30
- **Status**: Accepted
- **Issue**: research/axiom-explorer#1 (Phase 0)

## Context

The first runs of Phase 0 produced two distinct kinds of noise that, if
unaddressed, would have biased the entire experiment.

### Incident 1: terminology under-coverage in strict AND queries

A strict `all:"condensed mathematics" AND all:"perfectoid"` returned 2
papers despite the existence of a large active research program. The
reason is structural: papers in the Scholze school routinely use one
terminology per paper. A paper on prismatic cohomology does not need to
say "condensed" in its abstract.

### Incident 2: author-name collision with physics catalogues

The first version of the author-pair query (Q4) reported **47 papers**
co-authored by "Bhatt" and "Lott" for the A3 × A4 (Perfectoid × Synthetic
Ricci) pair, classifying it as **warm-bridged**. Inspection revealed
those papers were LIGO/Virgo gravitational-wave catalogue papers in
`gr-qc` whose author lists contain dozens of names including a "Bhatt"
and a "Lott" who are not the mathematicians.

This is a real false positive: the bibliometric harness was about to
classify a virgin frontier as an active one because of a homonym in a
mass-author physics paper.

## Decision

1. **Add a Q2 grouped (OR/AND) query** to expand recall:
   `(primary_a OR related_a OR ...) AND (primary_b OR related_b OR ...)`.
   This raises the canonical-text signal floor without flooding with noise.

2. **Filter Q2 results to `primary_category.startswith("math")`** before
   counting unique papers for classification. Generic terms like "diamond",
   "tilting", "untilt" have unrelated meanings in `math.CO`, `cs.IT`,
   `cond-mat`, etc.

3. **Restrict author-pair queries (Q4) to `cat:math.*`** by default. The
   `build_author_pair_query` function takes a `math_only=True` flag and
   appends ` AND cat:math.*` to the query. A namesake collision in
   `gr-qc` is now invisible.

4. **Use Q4 as a community-bridge signal, not a count of real papers**:
   the classification logic uses a boolean "is there an author bridge"
   alongside the math-only Q2 count, rather than naively summing Q4
   papers into the density score.

5. **Reproduce and document**. The `tests/test_arxiv_query_build.py`
   covers both `math_only=True` (default) and `math_only=False` to
   prevent silent regression. The Phase 0 report contains an "Honest
   meta-note" describing the false positive.

## Consequences

- Phase 0 results are now meaningfully calibrated:
  - A2 × A3 correctly comes out as **frontier-bridged** with the Scholze
    school detected via genuine math.AG/NT/KT/RT co-authorship.
  - A3 × A4 correctly comes out as **sparse** (no author bridge), matching
    the prior expectation that perfectoid arithmetic geometry and
    synthetic Ricci on metric measure spaces have essentially no contact.
- Bibliometric outputs are now trustworthy enough to drive the Phase 2
  prioritization.
- A residual concern: even with `cat:math.*`, common surnames (Mann, Wang,
  Liu, etc.) could still produce homonym noise within math itself. This
  is acknowledged but unaddressed for now; if it shows up in Phase 2 it
  will be revisited.
