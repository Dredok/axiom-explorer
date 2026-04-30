"""Phase 0: Bibliometric mapping over the 6 binary combinations of seeds.

Strategy (revised after a first calibration run revealed that strict
AND-of-canonical-phrases massively under-reports cross-community work):

For each binary combination (Ax, Ay) we issue four query types:

  Q1 — strict primary AND: pa AND pb  (per pair of primary phrases)
  Q2 — grouped OR/AND: (primary_a OR related_a) AND (primary_b OR related_b)
       This is the main recall query and the basis for density classification.
  Q3 — primary × related, both directions, capped at 3 each side.
  Q4 — author co-publication: papers co-authored by an author from each seed.
       This catches community overlap when terminology doesn't co-occur.

We persist raw responses and a per-pair density block. Classification uses
Q2 unique-paper counts as the dominant signal, with Q4 as a secondary
"community-bridge" indicator.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from axiom_explorer.arxiv_search import (
    ArxivQueryResult,
    polite_sleep,
    search,
    search_author_pair,
    search_grouped,
)
from axiom_explorer.seeds import SEEDS, binary_combinations

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUT = REPO_ROOT / "research" / "phase0-bibliometric" / "output"
DEFAULT_DATA = REPO_ROOT / "data" / "phase0"

# Cap on author-pair queries per binary combination to keep total API cost
# bounded. We pick the most prolific authors of each side.
MAX_AUTHOR_PAIR_QUERIES = 6


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _slug(s: str) -> str:
    return (
        s.lower()
        .replace('"', "")
        .replace(" ", "-")
        .replace("(", "")
        .replace(")", "")
        .replace(",", "")
        .replace("/", "-")
        .replace("+", "_")
    )


def _save(result: ArxivQueryResult, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)


def _classify(unique_papers: int, has_community_bridge: bool) -> str:
    """Heuristic classification of literature density at the intersection.

    We combine the Q2 unique-paper count with the author-bridge signal:
    a sparse Q2 count combined with a real author bridge is reclassified
    upwards as 'warm-bridged'.
    """
    if unique_papers >= 100:
        return "saturated"
    if unique_papers >= 30:
        return "warm"
    if unique_papers >= 5:
        return "warm-bridged" if has_community_bridge else "sparse"
    return "frontier-bridged" if has_community_bridge else "virgin"


def _run_pair(
    a: str,
    b: str,
    raw_dir: Path,
    queries_log,
) -> dict:
    sa = SEEDS[a]
    sb = SEEDS[b]
    pair = f"{a}x{b}"
    print(f"[phase0] === {pair}: {sa.name} × {sb.name}")

    all_results: list[ArxivQueryResult] = []
    unique_q2_ids: set[str] = set()
    community_bridge_ids: set[str] = set()
    bridge_evidence: list[dict] = []  # noqa: F841 (kept for future expansion)

    # --- Q1: strict primary × primary (canonical signal)
    for pa in sa.primary_terms:
        for pb in sb.primary_terms:
            r = search([pa, pb], label="q1-strict-primary", max_results=50)
            polite_sleep()
            _save(r, raw_dir / f"{pair}__q1__{_slug(pa)}__{_slug(pb)}.json")
            queries_log.write(
                json.dumps(
                    {
                        "pair": pair,
                        "kind": "q1",
                        "terms": [pa, pb],
                        "query": r.query,
                        "total_results": r.total_results,
                        "fetched": r.fetched,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            all_results.append(r)

    # --- Q2: grouped OR/AND (recall query)
    group_a = list(sa.primary_terms) + list(sa.related_terms)
    group_b = list(sb.primary_terms) + list(sb.related_terms)
    r2 = search_grouped(group_a, group_b, label="q2-grouped", max_results=100)
    polite_sleep()
    _save(r2, raw_dir / f"{pair}__q2__grouped.json")
    queries_log.write(
        json.dumps(
            {
                "pair": pair,
                "kind": "q2",
                "groups": {"a": group_a, "b": group_b},
                "query": r2.query,
                "total_results": r2.total_results,
                "fetched": r2.fetched,
            },
            ensure_ascii=False,
        )
        + "\n"
    )
    all_results.append(r2)
    unique_q2_ids.update(p.arxiv_id for p in r2.papers)
    # Mathematics-only filter: papers whose primary_category starts with 'math'.
    # This removes physics/CS/cond-mat noise from generic terms ("diamond",
    # "condensed", "tilting" all match unrelated work in other archives).
    q2_math_papers = [p for p in r2.papers if p.primary_category.startswith("math")]
    q2_math_ids = {p.arxiv_id for p in q2_math_papers}

    # --- Q3: primary × related, capped fanout
    for pa in sa.primary_terms[:1]:
        for rb in sb.related_terms[:3]:
            r = search([pa, rb], label="q3-primary-related", max_results=50)
            polite_sleep()
            _save(r, raw_dir / f"{pair}__q3a__{_slug(pa)}__{_slug(rb)}.json")
            queries_log.write(
                json.dumps(
                    {"pair": pair, "kind": "q3a", "terms": [pa, rb], "total_results": r.total_results},
                    ensure_ascii=False,
                )
                + "\n"
            )
            all_results.append(r)
    for pb in sb.primary_terms[:1]:
        for ra in sa.related_terms[:3]:
            r = search([pb, ra], label="q3-primary-related", max_results=50)
            polite_sleep()
            _save(r, raw_dir / f"{pair}__q3b__{_slug(pb)}__{_slug(ra)}.json")
            queries_log.write(
                json.dumps(
                    {"pair": pair, "kind": "q3b", "terms": [pb, ra], "total_results": r.total_results},
                    ensure_ascii=False,
                )
                + "\n"
            )
            all_results.append(r)

    # --- Q4: author pairs (community bridge)
    pair_count = 0
    for au_a in sa.key_authors[:3]:
        for au_b in sb.key_authors[:3]:
            if au_a == au_b:
                # Authors can appear on both sides (e.g. Scholze in A2 and A3).
                # That is itself a bridge signal — record but skip self-pair.
                community_bridge_ids.add(f"self::{au_a}")
                continue
            if pair_count >= MAX_AUTHOR_PAIR_QUERIES:
                break
            r = search_author_pair(au_a, au_b, max_results=50)
            polite_sleep()
            _save(r, raw_dir / f"{pair}__q4__{_slug(au_a)}__{_slug(au_b)}.json")
            queries_log.write(
                json.dumps(
                    {
                        "pair": pair,
                        "kind": "q4",
                        "author_a": au_a,
                        "author_b": au_b,
                        "total_results": r.total_results,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            for p in r.papers:
                community_bridge_ids.add(p.arxiv_id)
            all_results.append(r)
            pair_count += 1
        if pair_count >= MAX_AUTHOR_PAIR_QUERIES:
            break

    # Aggregate
    q2_unique = len(unique_q2_ids)
    q2_unique_math = len(q2_math_ids)
    bridge_papers = len([x for x in community_bridge_ids if not x.startswith("self::")])
    self_authors = sorted(
        x.removeprefix("self::") for x in community_bridge_ids if x.startswith("self::")
    )
    bridged = bridge_papers > 0 or len(self_authors) > 0

    # Use the math-filtered Q2 count for classification — this is the cleaner
    # signal for "is there real cross-area math literature here?".
    classification = _classify(q2_unique_math, bridged)
    print(
        f"[phase0]   q2_total={r2.total_results}  q2_math={q2_unique_math}  "
        f"bridge={bridge_papers}  self={self_authors}  -> {classification}"
    )

    return {
        "pair": pair,
        "q1_total_hits_sum": sum(
            r.total_results for r in all_results if r.label == "q1-strict-primary"
        ),
        "q2_total_results": r2.total_results,
        "q2_unique_top_k": q2_unique,
        "q2_unique_math": q2_unique_math,
        "q3_total_hits_sum": sum(
            r.total_results for r in all_results if r.label == "q3-primary-related"
        ),
        "q4_bridge_papers": bridge_papers,
        "q4_self_authors": self_authors,
        "n_queries": len(all_results),
        "classification": classification,
    }


def run(out_dir: str | None = None) -> int:
    out = Path(out_dir) if out_dir else DEFAULT_OUT
    data = DEFAULT_DATA
    _ensure_dir(out)
    _ensure_dir(data)
    raw_dir = data / "raw"
    _ensure_dir(raw_dir)

    started = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    pairs = binary_combinations()
    summary: dict[str, dict] = {}

    queries_log_path = data / "queries.jsonl"
    with queries_log_path.open("w", encoding="utf-8") as queries_log:
        for a, b in pairs:
            try:
                summary[f"{a}x{b}"] = _run_pair(a, b, raw_dir, queries_log)
            except Exception as e:  # noqa: BLE001
                print(f"[phase0] ERROR on {a}x{b}: {e}")
                summary[f"{a}x{b}"] = {"pair": f"{a}x{b}", "error": str(e)}

    finished = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    summary_path = out / "summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(
            {"started_utc": started, "finished_utc": finished, "pairs": summary},
            f,
            ensure_ascii=False,
            indent=2,
        )

    report_path = REPO_ROOT / "research" / "phase0-bibliometric" / "REPORT.md"
    _emit_report(report_path, summary, started, finished, pairs, raw_dir)

    print(f"[phase0] summary written to {summary_path}")
    print(f"[phase0] draft report written to {report_path}")
    return 0


def _emit_report(
    path: Path,
    summary: dict,
    started: str,
    finished: str,
    pairs: list[tuple[str, str]],
    raw_dir: Path,
) -> None:
    lines: list[str] = []
    lines.append("# Phase 0 — Bibliometric Mapping (machine-generated draft)\n")
    lines.append(f"- Started (UTC): `{started}`")
    lines.append(f"- Finished (UTC): `{finished}`")
    lines.append(f"- Raw dumps: `{raw_dir.relative_to(REPO_ROOT)}`")
    lines.append("")
    lines.append("## Method recap\n")
    lines.append(
        "For each binary combination of the four seeds we issued four query "
        "types against the arXiv API:\n"
    )
    lines.append("- **Q1**: strict AND of primary phrases (canonical signal).")
    lines.append(
        "- **Q2**: grouped (OR within each side) AND between sides — the main "
        "recall query and the basis for the density classification."
    )
    lines.append("- **Q3**: primary × related, capped fanout, both directions.")
    lines.append(
        "- **Q4**: author co-publication queries between seeds' key authors. "
        "Catches community bridges when terminology does not co-occur."
    )
    lines.append("")
    lines.append("## Density per binary combination\n")
    lines.append(
        "| Pair | Q1 hits | Q2 total | Q2 math-only | Q3 hits | "
        "Q4 bridge | shared authors | classification |"
    )
    lines.append(
        "|------|---------|----------|--------------|---------|----------|----------------|----------------|"
    )
    for a, b in pairs:
        key = f"{a}x{b}"
        d = summary.get(key, {})
        if "error" in d:
            lines.append(f"| {key} | error | error | error | error | error | error | {d['error']} |")
            continue
        lines.append(
            f"| {key} | {d['q1_total_hits_sum']} | {d['q2_total_results']} | "
            f"{d['q2_unique_math']} | {d['q3_total_hits_sum']} | "
            f"{d['q4_bridge_papers']} | {', '.join(d['q4_self_authors']) or '-'} | "
            f"**{d['classification']}** |"
        )
    lines.append("")
    lines.append("## Classification legend\n")
    lines.append("Classification uses Q2 *math-only* unique paper count "
                 "(papers whose primary arXiv category is `math.*`). This "
                 "removes physics/CS/cond-mat noise from generic terms "
                 "(\"diamond\", \"condensed\", \"tilting\" match unrelated work "
                 "in other archives).")
    lines.append("")
    lines.append("- **saturated** (≥ 100): cross-area heavily explored.")
    lines.append("- **warm** (30–99): well-trodden, novelty needs care.")
    lines.append("- **warm-bridged** (5–29 + bridge): living frontier.")
    lines.append("- **sparse** (5–29, no bridge): possibly artificial gap.")
    lines.append("- **frontier-bridged** (< 5 + bridge): high-yield candidate.")
    lines.append("- **virgin** (< 5, no bridge): true gap, possibly incompatible.")
    lines.append("")
    lines.append("## Curator's pass (machine-suggested, to be reviewed)\n")
    lines.append(
        "- **Frontier-bridged** and **warm-bridged** pairs are the most likely to "
        "yield novel and connectable candidates, and should be prioritized for Phase 2."
    )
    lines.append(
        "- **Virgin** pairs deserve a short dossier to decide whether the gap "
        "is a research opportunity or an inherent incompatibility."
    )
    lines.append(
        "- **Saturated** pairs go to Phase 2 only if a sub-niche is identified "
        "where the harness can still add a new vantage point."
    )
    lines.append("")
    lines.append("## Honesty notes\n")
    lines.append(
        "- arXiv's `all:` field searches abstract + metadata, not full text. "
        "Cross-community papers that use one side's terminology in the abstract "
        "but the other's only in the body will be missed by Q1/Q2/Q3."
    )
    lines.append(
        "- Q4 partially compensates this by indexing community membership via "
        "co-authorship, but the author lists in `seeds.py` are deliberately "
        "non-exhaustive."
    )
    lines.append(
        "- Classification thresholds are heuristic and should be revisited if "
        "the resulting prioritization disagrees strongly with the curator's read."
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
