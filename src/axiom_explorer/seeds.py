"""Definition of the four axiomatic seeds and their canonical search terms.

Notes on terminology coverage:
- We expand related_terms aggressively because authors in specialised
  subcommunities rarely repeat the umbrella name. E.g. a perfectoid paper
  may not say "perfectoid mathematics", only "tilting" or "diamond".
- Synthetic Ricci is especially fragmented: CD(K,N), RCD, MCP, BE(K,N),
  Bakry-Emery, Lott-Sturm-Villani are all part of the same program.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Seed:
    code: str
    name: str
    branch: str
    primary_terms: tuple[str, ...]
    related_terms: tuple[str, ...] = field(default_factory=tuple)
    # Authors strongly associated with the seed. Used to detect community
    # overlap between two seeds even when terminology does not co-occur.
    key_authors: tuple[str, ...] = field(default_factory=tuple)


SEEDS: dict[str, Seed] = {
    "A1": Seed(
        code="A1",
        name="Univalence Axiom",
        branch="Foundations / HoTT",
        primary_terms=("univalence", "homotopy type theory"),
        related_terms=(
            "HoTT",
            "cubical type theory",
            "univalent foundations",
            "synthetic homotopy theory",
            "higher inductive type",
        ),
        key_authors=(
            "Voevodsky",
            "Awodey",
            "Coquand",
            "Shulman",
            "Cherubini",
            "Buchholtz",
            "Rijke",
        ),
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
            "condensed module",
            "condensed group",
            "condensed cohomology",
            "Mann thesis",
            "p-adic functional analysis condensed",
            # Added in Phase 3 after manual discovery of these threads:
            "condensed homotopy type",
            "kappa-pyknotic",
            "condensed infinity-category",
            "Solovay model condensed",
            "Whitehead condensed",
        ),
        key_authors=(
            "Scholze",
            "Clausen",
            "Mann",
            "Bhatt",
            "Asgeirsson",
            # Added in Phase 3:
            "Haine",
            "Holzschuh",
            "Lara",
            "Bergfalk",
            "Lambie-Hanson",
            "Bannister",
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
            "p-adic Hodge",
            "Fargues-Fontaine",
            "v-sheaves",
            "Berkovich space p-adic",
            "perfectoid space",
            "untilt",
        ),
        key_authors=(
            "Scholze",
            "Bhatt",
            "Fargues",
            "Kedlaya",
            "Caraiani",
            "Hansen",
            "Weinstein",
            "Morrow",
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
            "RCD(K,N)",
            "Bakry-Emery",
            "BE(K,N)",
            "MCP(K,N)",
            "Wasserstein curvature",
            "lower Ricci bound metric measure",
            "Ricci limit space",
            "displacement convexity",
        ),
        key_authors=(
            "Sturm",
            "Lott",
            "Villani",
            "Ambrosio",
            "Gigli",
            "Cavalletti",
            "Mondino",
            "Erbar",
            "Maas",
            "Cheeger",
            "Colding",
        ),
    ),
}


def all_codes() -> list[str]:
    return list(SEEDS.keys())


def binary_combinations() -> list[tuple[str, str]]:
    codes = all_codes()
    return [(a, b) for i, a in enumerate(codes) for b in codes[i + 1 :]]
