"""Phase 0: Bibliometric mapping over the 6 binary combinations of seeds.

For each binary combination (Ax, Ay), we issue a small set of arXiv queries
that combine primary terms from each seed, with AND, restricted to recent
years. We persist raw responses, compute density metrics, and emit a
markdown report with a heat map.

This is a pure-data phase: no semantic judgement here. The semantic filter
is applied downstream by the human + LLM curator.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from axiom_explorer.arxiv_search import ArxivQueryResult, polite_search
from axiom_explorer.seeds import SEEDS, binary_combinations

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUT = REPO_ROOT / "research" / "phase0-bibliometric" / "output"
DEFAULT_DATA = REPO_ROOT / "data" / "phase0"


def _query_terms_for_pair(a: str, b: str) -> list[list[str]]:
    """Build a small fan-out of queries for a binary combination.

    We use:
      1. primary x primary (AND): the strict joint signal.
      2. primary_a + each related_b: catches more recall on b's side.
      3. primary_b + each related_a: catches more recall on a's side.

    Each query is a list of phrases that the search client AND-joins.
    """
    sa = SEEDS[a]
    sb = SEEDS[b]
    queries: list[list[str]] = []

    # 1. primary × primary  (one query per pair of primaries, capped)
    for pa in sa.primary_terms:
        for pb in sb.primary_terms:
            queries.append([pa, pb])

    # 2. primary_a × related_b  (limit fanout to keep total queries small)
    for pa in sa.primary_terms[:1]:
        for rb in sb.related_terms[:3]:
            queries.append([pa, rb])

    # 3. primary_b × related_a
    for pb in sb.primary_terms[:1]:
        for ra in sa.related_terms[:3]:
            queries.append([pb, ra])

    return queries


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _save_query_result(result: ArxivQueryResult, out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)


def _slug(s: str) -> str:
    return (
        s.lower()
        .replace('"', "")
        .replace(" ", "-")
        .replace("(", "")
        .replace(")", "")
        .replace(",", "")
        .replace("/", "-")
    )


def _density_score(results: list[ArxivQueryResult]) -> dict[str, float | int]:
    """Compute density metrics from a list of query results for one pair."""
    total_hits = sum(r.total_results for r in results)
    fetched_papers = sum(r.fetched for r in results)
    # Unique paper count across queries (by arxiv_id).
    unique_ids: set[str] = set()
    for r in results:
        for p in r.papers:
            unique_ids.add(p.arxiv_id)
    return {
        "total_hits_sum": total_hits,
        "fetched_papers_sum": fetched_papers,
        "unique_papers_in_top_k": len(unique_ids),
        "n_queries": len(results),
    }


def _classify(unique_papers: int) -> str:
    """Heuristic classification of literature density.

    Tuned for the top-50 fetch window per query, AND-joined phrases. Calibration
    will be revisited after seeing the actual numbers in the report.
    """
    if unique_papers >= 100:
        return "saturated"
    if unique_papers >= 30:
        return "warm"
    if unique_papers >= 5:
        return "sparse"
    return "virgin"


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
    queries_log = queries_log_path.open("w", encoding="utf-8")

    try:
        for a, b in pairs:
            pair_key = f"{a}x{b}"
            terms_list = _query_terms_for_pair(a, b)
            print(f"[phase0] {pair_key}: {len(terms_list)} queries")
            results = polite_search(terms_list, max_results=50)
            for terms, result in zip(terms_list, results, strict=True):
                fname = f"{pair_key}__{_slug('+'.join(terms))}.json"
                _save_query_result(result, raw_dir / fname)
                queries_log.write(
                    json.dumps(
                        {
                            "pair": pair_key,
                            "terms": terms,
                            "query": result.query,
                            "timestamp_utc": result.timestamp_utc,
                            "total_results": result.total_results,
                            "fetched": result.fetched,
                            "raw_file": fname,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
            density = _density_score(results)
            density["classification"] = _classify(int(density["unique_papers_in_top_k"]))
            summary[pair_key] = density
            print(f"[phase0]   density: {density}")
    finally:
        queries_log.close()

    finished = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    summary_path = out / "summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(
            {"started_utc": started, "finished_utc": finished, "pairs": summary},
            f,
            ensure_ascii=False,
            indent=2,
        )

    # Emit a draft REPORT.md (the curator will refine the prose).
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
    lines.append("# Phase 0 — Bibliometric Mapping (draft, machine-generated)\n")
    lines.append(f"- Started (UTC): `{started}`")
    lines.append(f"- Finished (UTC): `{finished}`")
    lines.append(f"- Raw dumps: `{raw_dir.relative_to(REPO_ROOT)}`")
    lines.append("")
    lines.append("## Density per binary combination\n")
    lines.append("| Pair | n_queries | total_hits_sum | unique_papers_top_k | classification |")
    lines.append("|------|-----------|----------------|---------------------|----------------|")
    for a, b in pairs:
        key = f"{a}x{b}"
        d = summary[key]
        lines.append(
            f"| {key} | {d['n_queries']} | {d['total_hits_sum']} | "
            f"{d['unique_papers_in_top_k']} | {d['classification']} |"
        )
    lines.append("")
    lines.append("## Notes\n")
    lines.append(
        "- `total_hits_sum` is the sum of arXiv reported hits per query; it overcounts "
        "papers that match multiple queries. `unique_papers_top_k` deduplicates within "
        "the top-50 fetch window per query."
    )
    lines.append(
        "- Classification thresholds are heuristic and will be revisited after first "
        "calibration run."
    )
    lines.append("")
    lines.append("## Curator's pass (to fill in)\n")
    lines.append(
        "- Identify which sparse/virgin pairs are *frontier* vs. *incompatible*."
    )
    lines.append(
        "- Identify within saturated pairs whether the literature already covers "
        "the natural cross-statements or only adjacent ones."
    )
    lines.append("- Pick 2–3 pairs to advance to Phase 2.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
