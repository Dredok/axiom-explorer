"""Minimal arXiv search client using the public Atom API.

We hit https://export.arxiv.org/api/query directly. Rate limit: roughly one
request every 3 seconds is courteous (arXiv recommends 3s between calls).
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

import feedparser
import httpx

ARXIV_ENDPOINT = "https://export.arxiv.org/api/query"
DEFAULT_DELAY_S = 3.1


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
    timestamp_utc: str
    total_results: int
    fetched: int
    papers: list[ArxivPaper]

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "timestamp_utc": self.timestamp_utc,
            "total_results": self.total_results,
            "fetched": self.fetched,
            "papers": [p.to_dict() for p in self.papers],
        }


def _build_search_query(terms: list[str], operator: str = "AND") -> str:
    """Build an arXiv search_query string from a list of phrases.

    Each phrase is wrapped in quotes and joined by the operator. We restrict
    to all-fields by default (all:).
    """
    parts = [f'all:"{t}"' for t in terms]
    joiner = f" {operator} "
    return joiner.join(parts)


def search(
    terms: list[str],
    *,
    operator: str = "AND",
    max_results: int = 50,
    sort_by: str = "relevance",
    sort_order: str = "descending",
    timeout_s: float = 30.0,
) -> ArxivQueryResult:
    """Search arXiv with the given terms (joined by AND or OR).

    Returns the parsed result. Caller is responsible for rate-limiting
    between successive calls — see `polite_search` for a wrapper.
    """
    query = _build_search_query(terms, operator=operator)
    params = {
        "search_query": query,
        "start": "0",
        "max_results": str(max_results),
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    with httpx.Client(timeout=timeout_s) as client:
        resp = client.get(ARXIV_ENDPOINT, params=params)
    resp.raise_for_status()

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
        timestamp_utc=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        total_results=total,
        fetched=len(papers),
        papers=papers,
    )


def polite_search(
    terms_list: list[list[str]],
    *,
    delay_s: float = DEFAULT_DELAY_S,
    **kwargs: Any,
) -> list[ArxivQueryResult]:
    """Run multiple searches with polite spacing between calls."""
    results: list[ArxivQueryResult] = []
    for i, terms in enumerate(terms_list):
        if i > 0:
            time.sleep(delay_s)
        results.append(search(terms, **kwargs))
    return results
