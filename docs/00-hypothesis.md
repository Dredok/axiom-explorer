# Hypothesis

## Origin

This experiment originated from a conversation about whether the bridge between
geometry and calculus generalizes — and if so, whether iterating deductively
over a small set of *modern* axiomatic seeds (rather than classical ones) gives
a better-than-random shot at uncovering new mathematics.

## Core claim

> Given a set of axioms that is (a) **productive** (already known to generate
> non-trivial theorems in its branch), (b) **recent** (so the deductive closure
> is by definition less explored), and (c) **drawn from distinct branches**
> (so cross-branch combinations are largely unexplored), an iterative deductive
> harness with expert relevance filtering will have **higher yield density** —
> measured as plausibly-relevant candidates per unit of search effort — than
> the same harness seeded with classical axioms.

## Why this might work

1. **Frontier proximity.** Theorems "at distance N" from a 2010+ axiom are
   probabilistically less likely to already be in the literature than those at
   distance N from Peano.
2. **Pre-selected fertility.** Communities adopt new axioms because they're
   already suspected to open territory. The seed comes pre-curated.
3. **Re-derivation as discovery.** Even when the harness rediscovers a known
   theorem from a modern seed, the *new route* itself may be a contribution —
   shorter proofs from richer axioms have historical precedent (schemes
   trivializing classical AG, HoTT trivializing certain ZFC-heavy equivalences).
4. **Cross-branch combinations.** Most actual research lives within one branch;
   pairs like Synthetic-Ricci × Condensed are sparsely populated even when
   each side is well-explored.

## Why this might fail

1. **Trivial recombination.** Most syntactic combinations of axioms produce
   trivial or vacuously-true statements; the relevance filter has to do all
   the work.
2. **Concept gap.** New mathematics historically advances by *inventing
   concepts*, not by recombining existing ones. A purely deductive harness
   cannot invent vocabulary.
3. **Knowledge cutoff.** The relevance filter (LLM-based) has bounded
   awareness of recent literature; "novel" candidates may be already known.
4. **Selection bias.** Combinations the harness can compute or formalize will
   be over-represented; the most promising abstract combinations may be
   exactly the ones we cannot mechanize.

## Falsifiability

The experiment falsifies its own hypothesis if, after exhausting the planned
phases (Phase 0 through Phase 4), **zero candidates** survive the four
relevance tests of Phase 4 (novelty, inter-branch connectivity, tangency to
open problem, non-triviality). This is a real possible outcome and would be
reported honestly as a negative result.

## Acknowledged limitations

- This run uses a single seed quartet (Univalence, Condensed, Perfectoid,
  Synthetic Ricci) chosen as the user's domain expert preference. A
  different quartet might yield different results; this is not a claim about
  *all* modern seeds.
- The relevance filter is the human operator + LLM agent; both have biases.
- Compute budget caps the depth of search per combination.

## Relation to prior work

- **AM / EURISKO** (Lenat, late 70s/early 80s): conjecturing from primitives.
- **Graffiti** (Fajtlowicz, 80s+): conjectures in graph theory.
- **Ramanujan Machine** (2021): identity conjectures for constants.
- **AlphaProof / AlphaGeometry** (DeepMind, 2024): theorem proving on IMO.
- **Liquid Tensor Experiment** (Scholze + Lean community, 2020-2022):
  formalization of a recent deep theorem from condensed mathematics.

This experiment is closer in spirit to Graffiti and Ramanujan Machine than to
AlphaProof: we are not trying to *prove* given conjectures but to *surface*
candidate ones from a curated frontier seed.
