"""Minimal arXiv search client using the public Atom API.

We hit https://export.arxiv.org/api/query directly. Rate limit: roughly one
request every 3 seconds is courteous (arXiv recommends 3s between calls).

We support two query styles:
- AND of all-fields phrases (`build_and_query`): strict joint signal.
- AND of two OR-groups, where each group is a disjunction of phrases
  (`build_grouped_and_query`): wider recall when each side has many
  synonyms. Used for cross-community searches where neither side has a
  single canonical phrase.
- AND of all-fields + author co-mention (`build_author_query`): catches
  cross-community work via authorship even when the text doesn't literally
  combine the two terminologies.
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

import feedparser
import httpx

ARXIV_ENDPOINT = "https://export.arxiv.org/api/query"
DEFAULT_DELAY_S = 4.0


@dataclass
class ArxivPaper:
    arxiv_id: str
    title: str
    authors: list[str]
    summary: str
    published: str
    updated: str
    primary_category: str
    categories: list[str]
    pdf_url: str | None
    abs_url: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ArxivQueryResult:
    query: str
    label: str
    timestamp_utc: str
    total_results: int
    fetched: int
    papers: list[ArxivPaper]

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "label": self.label,
            "timestamp_utc": self.timestamp_utc,
            "total_results": self.total_results,
            "fetched": self.fetched,
            "papers": [p.to_dict() for p in self.papers],
        }


def build_and_query(terms: list[str]) -> str:
    parts = [f'all:"{t}"' for t in terms]
    return " AND ".join(parts)


def build_grouped_and_query(group_a: list[str], group_b: list[str]) -> str:
    """AND of (OR group_a) and (OR group_b).

    Each group is a disjunction of `all:"phrase"` clauses. Useful when each
    side has many near-synonyms.
    """
    if not group_a or not group_b:
        raise ValueError("Both groups must be non-empty")
    a = " OR ".join(f'all:"{t}"' for t in group_a)
    b = " OR ".join(f'all:"{t}"' for t in group_b)
    return f"({a}) AND ({b})"


def build_author_pair_query(
    author_a: str, author_b: str, *, math_only: bool = True
) -> str:
    """Papers co-authored by both authors (a proxy for cross-community work).

    If `math_only` is True, restrict to arXiv's `math` archive to filter
    out namesake collisions with physics catalog papers (e.g. LIGO author
    lists contain a "Bhatt" and a "Lott" who are not the mathematicians).
    """
    base = f'au:"{author_a}" AND au:"{author_b}"'
    if math_only:
        return f"{base} AND cat:math.*"
    return base


# Backwards-compatible internal alias used by older code/tests.
def _build_search_query(terms: list[str], operator: str = "AND") -> str:
    parts = [f'all:"{t}"' for t in terms]
    joiner = f" {operator} "
    return joiner.join(parts)


def _execute(query: str, label: str, max_results: int, timeout_s: float) -> ArxivQueryResult:
    params = {
        "search_query": query,
        "start": "0",
        "max_results": str(max_results),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    last_err: Exception | None = None
    backoff = 5.0
    for attempt in range(5):
        try:
            with httpx.Client(timeout=timeout_s) as client:
                resp = client.get(ARXIV_ENDPOINT, params=params)
            if resp.status_code == 429:
                retry_after = float(resp.headers.get("Retry-After", backoff))
                wait = max(retry_after, backoff)
                print(f"[arxiv] 429 received, sleeping {wait:.1f}s (attempt {attempt+1}/5)")
                time.sleep(wait)
                backoff = min(backoff * 2, 120.0)
                continue
            resp.raise_for_status()
            break
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (429, 503):
                wait = backoff
                print(f"[arxiv] {e.response.status_code} received, sleeping {wait:.1f}s")
                time.sleep(wait)
                backoff = min(backoff * 2, 120.0)
                last_err = e
                continue
            raise
        except (httpx.TimeoutException, httpx.NetworkError) as e:
            print(f"[arxiv] network error: {e}; sleeping {backoff:.1f}s")
            time.sleep(backoff)
            backoff = min(backoff * 2, 120.0)
            last_err = e
            continue
    else:
        raise RuntimeError(f"arxiv API exhausted retries: {last_err}")

    parsed = feedparser.parse(resp.text)
    total = int(parsed.feed.get("opensearch_totalresults", 0))
    papers: list[ArxivPaper] = []
    for entry in parsed.entries:
        arxiv_id = entry.get("id", "").split("/abs/")[-1]
        authors = [a.get("name", "") for a in entry.get("authors", [])]
        cats = [t.get("term", "") for t in entry.get("tags", [])]
        primary = entry.get("arxiv_primary_category", {}).get("term", cats[0] if cats else "")
        pdf_url = None
        for link in entry.get("links", []):
            if link.get("type") == "application/pdf":
                pdf_url = link.get("href")
        papers.append(
            ArxivPaper(
                arxiv_id=arxiv_id,
                title=(entry.get("title") or "").strip().replace("\n", " "),
                authors=authors,
                summary=(entry.get("summary") or "").strip().replace("\n", " "),
                published=entry.get("published", ""),
                updated=entry.get("updated", ""),
                primary_category=primary,
                categories=cats,
                pdf_url=pdf_url,
                abs_url=entry.get("link", ""),
            )
        )
    return ArxivQueryResult(
        query=query,
        label=label,
        timestamp_utc=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        total_results=total,
        fetched=len(papers),
        papers=papers,
    )


def search(
    terms: list[str],
    *,
    label: str = "and-pair",
    max_results: int = 50,
    timeout_s: float = 30.0,
) -> ArxivQueryResult:
    """Strict AND search over a list of phrases."""
    return _execute(build_and_query(terms), label, max_results, timeout_s)


def search_grouped(
    group_a: list[str],
    group_b: list[str],
    *,
    label: str = "grouped-or-and",
    max_results: int = 50,
    timeout_s: float = 30.0,
) -> ArxivQueryResult:
    """AND of two OR-groups."""
    return _execute(
        build_grouped_and_query(group_a, group_b), label, max_results, timeout_s
    )


def search_author_pair(
    author_a: str,
    author_b: str,
    *,
    math_only: bool = True,
    max_results: int = 50,
    timeout_s: float = 30.0,
) -> ArxivQueryResult:
    """Papers co-authored by both authors."""
    return _execute(
        build_author_pair_query(author_a, author_b, math_only=math_only),
        f"co-author:{author_a}+{author_b}{'(math)' if math_only else ''}",
        max_results,
        timeout_s,
    )


def polite_sleep(delay_s: float = DEFAULT_DELAY_S) -> None:
    """Sleep between API calls to respect arXiv's recommended rate."""
    time.sleep(delay_s)
