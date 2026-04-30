"""Definition of the four axiomatic seeds and their canonical search terms."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Seed:
    code: str
    name: str
    branch: str
    # Canonical query phrases used for arXiv / web search. Phrases must be
    # quoted in the actual query so multi-word terms are matched as units.
    primary_terms: tuple[str, ...]
    # Synonyms / related terms used to expand recall.
    related_terms: tuple[str, ...] = field(default_factory=tuple)


SEEDS: dict[str, Seed] = {
    "A1": Seed(
        code="A1",
        name="Univalence Axiom",
        branch="Foundations / HoTT",
        primary_terms=("univalence", "homotopy type theory"),
        related_terms=("HoTT", "cubical type theory", "univalent foundations"),
    ),
    "A2": Seed(
        code="A2",
        name="Condensed Mathematics",
        branch="Topology / Functional Analysis",
        primary_terms=("condensed mathematics", "condensed sets"),
        related_terms=(
            "liquid tensor experiment",
            "solid module",
            "condensed abelian",
            "pyknotic",
        ),
    ),
    "A3": Seed(
        code="A3",
        name="Perfectoid Spaces",
        branch="Arithmetic Geometry",
        primary_terms=("perfectoid",),
        related_terms=(
            "tilting equivalence",
            "diamond",
            "prismatic cohomology",
            "almost mathematics",
        ),
    ),
    "A4": Seed(
        code="A4",
        name="Synthetic Ricci",
        branch="Analysis / Metric Geometry",
        primary_terms=("synthetic Ricci", "CD(K,N)"),
        related_terms=(
            "Lott-Sturm-Villani",
            "RCD space",
            "metric measure space curvature",
            "optimal transport curvature",
        ),
    ),
}


def all_codes() -> list[str]:
    return list(SEEDS.keys())


def binary_combinations() -> list[tuple[str, str]]:
    codes = all_codes()
    return [(a, b) for i, a in enumerate(codes) for b in codes[i + 1 :]]
