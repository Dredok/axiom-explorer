"""Phase 1: Formal-state inventory across Mathlib4 and adjacent Lean/Agda projects.

Produces a markdown inventory of:
- Per-seed Mathlib4 files and exposed definitions/theorems.
- Adjacent projects (Liquid Tensor Experiment, perfectoid-spaces, synthetic-zariski,
  synthetic-geometry).
- Identified TODOs in source headers (formalization gaps).

Reads the cloned mathlib4 / synthetic-zariski / synthetic-geometry under
artifacts/ ; does not require running Lean or Agda.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = REPO_ROOT / "artifacts"
DEFAULT_OUT = REPO_ROOT / "research" / "phase1-formal-state" / "output"

MATHLIB_PATHS = {
    "A2": ["Mathlib/Condensed"],
    "A3": [
        "Mathlib/RingTheory/Perfectoid",
        "Mathlib/RingTheory/Perfection.lean",
    ],
    # A1 (HoTT/Univalence) and A4 (Synthetic Ricci) have negligible mathlib4 footprint;
    # we record them as gaps explicitly, no glob necessary.
}


def _scan_lean_file(path: Path) -> dict:
    """Extract definitions, theorems, TODOs, and authors from a Lean file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    defs = re.findall(r"^\s*(?:noncomputable\s+)?def\s+(\w+)", text, re.MULTILINE)
    theorems = re.findall(r"^\s*theorem\s+(\w+)", text, re.MULTILINE)
    lemmas = re.findall(r"^\s*lemma\s+(\w+)", text, re.MULTILINE)
    todos = re.findall(r"TODO[^\n]*", text)
    authors = re.findall(r"Authors?:\s*([^\n-]+)", text)
    return {
        "path": str(path.relative_to(ARTIFACTS / "mathlib4")),
        "n_defs": len(defs),
        "n_theorems": len(theorems),
        "n_lemmas": len(lemmas),
        "todos": todos[:10],
        "authors": [a.strip() for a in authors[:3]],
        "lines": text.count("\n") + 1,
    }


def _scan_seed_paths(paths: list[str]) -> list[dict]:
    base = ARTIFACTS / "mathlib4"
    files: list[Path] = []
    for p in paths:
        full = base / p
        if full.is_dir():
            files.extend(sorted(full.rglob("*.lean")))
        elif full.is_file() and full.suffix == ".lean":
            files.append(full)
    return [_scan_lean_file(f) for f in files]


def _scan_synthetic_zariski_open_questions() -> list[dict]:
    """Extract open questions / conjectures from synthetic-zariski README."""
    path = ARTIFACTS / "synthetic-zariski" / "README.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    # Look for the "# Questions" section.
    m = re.search(r"#\s*Questions\s*\n(.*?)(?=\n#\s*[A-Z]|$)", text, re.DOTALL)
    if not m:
        return []
    block = m.group(1)
    questions = re.findall(r"^-\s*(.+)$", block, re.MULTILINE)
    return [{"question": q.strip()} for q in questions]


def _scan_axioms() -> list[dict]:
    """Extract the four axioms of Synthetic Stone Duality from condensed-summary/axiom.tex."""
    path = ARTIFACTS / "synthetic-zariski" / "condensed-summary" / "axiom.tex"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    # Capture each axiomNum block by name + body.
    pattern = re.compile(
        r"\\begin\{axiomNum\}\[([^\]]+)\]\s*(.*?)\\end\{axiomNum\}",
        re.DOTALL,
    )
    return [
        {"name": m.group(1).strip(), "body": re.sub(r"\s+", " ", m.group(2)).strip()}
        for m in pattern.finditer(text)
    ]


def _scan_agda_files() -> list[dict]:
    """List the Agda formalization modules in synthetic-geometry."""
    base = ARTIFACTS / "synthetic-geometry" / "SyntheticGeometry"
    if not base.exists():
        return []
    files = sorted(list(base.rglob("*.agda")) + list(base.rglob("*.lagda.md")))
    out: list[dict] = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        out.append(
            {
                "path": str(f.relative_to(ARTIFACTS / "synthetic-geometry")),
                "lines": text.count("\n") + 1,
                "n_postulate": len(re.findall(r"\bpostulate\b", text)),
            }
        )
    return out


def run(out_dir: str | None = None) -> int:
    out = Path(out_dir) if out_dir else DEFAULT_OUT
    out.mkdir(parents=True, exist_ok=True)
    summary: dict = {
        "generated_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "mathlib4": {},
        "synthetic_zariski": {
            "open_questions": _scan_synthetic_zariski_open_questions(),
            "stone_duality_axioms": _scan_axioms(),
        },
        "synthetic_geometry_agda": _scan_agda_files(),
    }
    for code, paths in MATHLIB_PATHS.items():
        summary["mathlib4"][code] = _scan_seed_paths(paths)

    summary_path = out / "summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    report_path = REPO_ROOT / "research" / "phase1-formal-state" / "REPORT.md"
    _emit_report(report_path, summary)
    print(f"[phase1] summary -> {summary_path}")
    print(f"[phase1] report  -> {report_path}")
    return 0


def _emit_report(path: Path, summary: dict) -> None:
    lines: list[str] = []
    lines.append("# Phase 1 — Formal-State Inventory (machine-generated draft)\n")
    lines.append(f"- Generated (UTC): `{summary['generated_utc']}`\n")
    lines.append("## Mathlib4 footprint per seed\n")

    a2 = summary["mathlib4"].get("A2", [])
    a3 = summary["mathlib4"].get("A3", [])

    lines.append("### A1 — Univalence / HoTT")
    lines.append("Mathlib4 footprint: **NONE**. Mathlib uses classical foundations.")
    lines.append("Univalence lives in: Coq UniMath, Agda Cubical, Lean 4 HoTT fork (separate).")
    lines.append("")
    lines.append(f"### A2 — Condensed Mathematics ({len(a2)} files in Mathlib/Condensed)\n")
    lines.append("| File | lines | defs | thms | lemmas | TODOs |")
    lines.append("|------|-------|------|------|--------|-------|")
    for f in a2:
        lines.append(
            f"| `{f['path']}` | {f['lines']} | {f['n_defs']} | "
            f"{f['n_theorems']} | {f['n_lemmas']} | {len(f['todos'])} |"
        )
    interesting_todos: list[tuple[str, str]] = []
    for f in a2:
        for t in f["todos"]:
            interesting_todos.append((f["path"], t))
    if interesting_todos:
        lines.append("\n**Notable A2 TODOs (formalization gaps)**")
        for p, t in interesting_todos[:15]:
            lines.append(f"- `{p}`: {t.strip()[:200]}")
    lines.append("")
    lines.append(f"### A3 — Perfectoid Spaces ({len(a3)} files)\n")
    lines.append("| File | lines | defs | thms | lemmas | TODOs |")
    lines.append("|------|-------|------|------|--------|-------|")
    for f in a3:
        lines.append(
            f"| `{f['path']}` | {f['lines']} | {f['n_defs']} | "
            f"{f['n_theorems']} | {f['n_lemmas']} | {len(f['todos'])} |"
        )
    a3_todos: list[tuple[str, str]] = []
    for f in a3:
        for t in f["todos"]:
            a3_todos.append((f["path"], t))
    if a3_todos:
        lines.append("\n**Notable A3 TODOs (formalization gaps)**")
        for p, t in a3_todos[:15]:
            lines.append(f"- `{p}`: {t.strip()[:200]}")
    lines.append("")
    lines.append("### A4 — Synthetic Ricci")
    lines.append("Mathlib4 footprint: **NONE**.")
    lines.append("- No CD(K,N), no RCD, no Wasserstein, no Lott-Sturm-Villani.")
    lines.append("- `Mathlib/Geometry/Euclidean/MongePoint.lean` is unrelated (classical Euclidean).")
    lines.append("- `Mathlib/MeasureTheory/Measure/Tilted.lean` is statistics, unrelated.")
    lines.append("- This is one of the largest unformalized active mathematical programs in Mathlib4.")
    lines.append("")

    # Synthetic Stone Duality axioms (the actual A1 × A2 frontier object).
    lines.append("## A1 × A2 frontier — Synthetic Stone Duality\n")
    lines.append(
        "Cherubini-Coquand-Geerligs-Moeneclaey (Dec 2024, arXiv:2412.03203) extend HoTT "
        "with **4 axioms** to talk internally about light condensed sets. These are the "
        "concrete bridging axioms between A1 (Univalence/HoTT) and A2 (Condensed).\n"
    )
    for ax in summary["synthetic_zariski"]["stone_duality_axioms"]:
        lines.append(f"### Axiom — {ax['name']}")
        lines.append(f"> {ax['body']}\n")
    lines.append("")

    # Open questions
    qs = summary["synthetic_zariski"]["open_questions"]
    if qs:
        lines.append("## Synthetic Zariski / Stone Duality open questions (verbatim from README)\n")
        for q in qs:
            lines.append(f"- {q['question']}")
        lines.append("")

    # Agda formalization
    agda = summary["synthetic_geometry_agda"]
    if agda:
        lines.append(f"## Agda formalization (synthetic-geometry, {len(agda)} files)\n")
        lines.append(
            "Formalizes Synthetic Algebraic Geometry over the Zariski topos. "
            "**Does not formalize Synthetic Stone Duality** (the condensed side).\n"
        )
        lines.append("| File | lines | postulates |")
        lines.append("|------|-------|------------|")
        for f in agda:
            lines.append(f"| `{f['path']}` | {f['lines']} | {f['n_postulate']} |")
        lines.append("")

    lines.append("## Formalization-gap shortlist for Phase 2\n")
    lines.append("1. **A2-Solid**: Mathlib's `Mathlib.Condensed.Solid` defines `IsSolid` but "
                 "carries explicit TODOs for the structure theorems. Concrete formalization gap.")
    lines.append("2. **A1×A2 axiom system in Lean**: the four Synthetic Stone Duality axioms are "
                 "documented in TeX (Cherubini et al. 2024) and partially formalized in Cubical "
                 "Agda elsewhere, but **not in Lean 4 / Mathlib4**. A minimal axiomatic Lean "
                 "module could be a clean entry point.")
    lines.append("3. **Wärn's anomaly**: Cherubini et al. note that an important property of "
                 "condensed abelian groups is *not* internally valid (Wärn 2024). Identifying "
                 "the precise statement and where Mathlib4's external definitions diverge from "
                 "the internal HoTT view is a candidate for Phase 2.")
    lines.append("4. **A3-perfectoid B_dR**: Mathlib4's `BDeRham.lean` has a TODO connecting the "
                 "explicit theta-mod-p^n construction to the deformation-theoretic / cotangent "
                 "complex view (Bhatt). This is a known gap pointed at the prismatic line.")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
