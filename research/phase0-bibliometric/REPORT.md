# Phase 0 — Bibliometric Mapping (machine-generated draft)

- Started (UTC): `2026-05-01T00:44:35Z`
- Finished (UTC): `2026-05-01T00:54:28Z`
- Raw dumps: `data/phase0/raw`

## Method recap

For each binary combination of the four seeds we issued four query types against the arXiv API:

- **Q1**: strict AND of primary phrases (canonical signal).
- **Q2**: grouped (OR within each side) AND between sides — the main recall query and the basis for the density classification.
- **Q3**: primary × related, capped fanout, both directions.
- **Q4**: author co-publication queries between seeds' key authors. Catches community bridges when terminology does not co-occur.

## Density per binary combination

| Pair | Q1 hits | Q2 total | Q2 math-only | Q3 hits | Q4 bridge | Q5 topic | shared authors | classification |
|------|---------|----------|--------------|---------|----------|----------|----------------|----------------|
| A1xA2 | 1 | 1 | 1 | 0 | 0 | 1 | - | **frontier-bridged** |
| A1xA3 | 0 | 3 | 1 | 1 | 0 | 0 | - | **virgin** |
| A1xA4 | 0 | 1 | 1 | 0 | 0 | 0 | - | **virgin** |
| A2xA3 | 2 | 5 | 4 | 0 | 10 | 20 | Scholze | **frontier-bridged** |
| A2xA4 | 0 | 1 | 1 | 0 | 0 | 0 | - | **virgin** |
| A3xA4 | 0 | 13 | 8 | 0 | 0 | 0 | - | **sparse** |

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