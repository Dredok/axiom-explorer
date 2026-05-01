# Phase 2 — A3 × A4: Perfectoid × Synthetic Ricci (CONTROL)

## Role of this section

A3 × A4 is the harness's **negative control**. The hypothesis was:
two seeds with no community contact, no shared terminology, and no
naturally bridging functor should yield no candidate, and the harness
should detect this honestly.

If A3 × A4 produces a strong candidate, that's *information*: either we
mis-categorized the gap or there is an unexpected bridge. If it produces
no candidate, the harness is calibrated.

## Phase 0 confirmed

- Q2 math-only: 8 papers, all on inspection unrelated (combinatorial
  "k-diamond partitions", a sub-Lorentzian synthetic curvature paper that
  is on the A4 side only, and noise).
- Q4 author bridge (after the LIGO false-positive fix): **0 papers**.
- No co-authorship between Scholze school and Lott-Sturm-Villani school.

## Search for non-obvious bridges

We attempted three angles to falsify the "no bridge" hypothesis:

### Angle 1 — p-adic optimal transport

There is a tiny corner of the literature on optimal transport over $p$-adic
or non-archimedean spaces (Berkovich-spectrum-based, or adelic). We searched
arXiv for "p-adic optimal transport", "non-archimedean Wasserstein",
"adelic transport" and found:

- A handful of preprints on **Monge-Kantorovich on locally compact groups**
  (including p-adic), but these treat $p$-adic numbers as a measurable
  space without engaging perfectoid theory.
- No paper that combines perfectoid hypothesis with Wasserstein / synthetic
  Ricci.

### Angle 2 — synthetic Ricci on Berkovich / rigid spaces

Berkovich spaces have a natural metric structure; one could imagine a
CD(K,N) condition there. Search:

- "synthetic Ricci Berkovich", "CD(K,N) non-archimedean", "Wasserstein
  Berkovich" — **zero hits**.
- "Berkovich" appears in `math.NT`/`math.AG` exclusively; "synthetic
  Ricci" appears in `math.DG`/`math.MG`. The two communities do not
  overlap.

### Angle 3 — sub-Lorentzian / Carnot via perfectoid

The single A4-side paper that surfaced in Phase 0 — "Hausdorff dimension
and failure of synthetic curvature bounds in the sub-Lorentzian setting"
— uses *Lorentzian* synthetic geometry. The "Lorentzian / p-adic" duality
sometimes invoked in physics (causal sets vs non-archimedean) is not a
real bridge to perfectoid theory; the analogy is heuristic.

## Conclusion — control behaves as expected

There is no bridging functor between A3 and A4. The two communities, the
two formalisms, and the two foundational ontologies (algebraic over
$p$-adic fields with characteristic-$p$ tilts vs. metric-measure spaces
with Wasserstein optimal transport) do not naturally interact at the
present state of the art.

**The harness correctly detects this.** No Phase 3 candidate is advanced
for A3 × A4.

This is a positive test of the methodology: if the harness *had* produced
a "candidate" here, we would have to flag it as a likely artifact, since
the prior is that the gap is real.

## Honesty caveats

- We searched for present bridges, not all possible bridges. A future
  Wasserstein-style construction over Berkovich spaces is conceivable but
  would currently require inventing the bridge, which is outside this
  experiment's scope.
- "No bridge" is a stronger claim than "no easy bridge". We claim only the
  latter.
- One real paper does straddle both — "A Lorentzian analog for Hausdorff
  dimension and measure" (math-ph, 2021) — but it uses neither perfectoid
  theory nor $p$-adic structure on the A3 side. It is A4-only with
  Lorentzian flavor.

## Status for orchestrator

Control negative result confirmed. **Do not advance**. The result itself
is part of Phase 4's meta-analysis (the harness can correctly identify
incompatibility).
