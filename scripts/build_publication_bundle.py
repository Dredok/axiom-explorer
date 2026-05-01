#!/usr/bin/env python3
"""Build local publication bundles for the axiom-explorer preprint.

This script intentionally uses only the Python standard library so it can run
inside or outside the project virtual environment. Pattern adapted from
vera-paper (gitlab.loneorc.com/research/vera-paper).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]

PUBLICATION_FILES = [
    "README.md",
    "HANDOFF.md",
    "LICENSE",
    "CITATION.cff",
    ".zenodo.json",
    "pyproject.toml",
    "uv.lock",
    "paper/preprint.pdf",
    "paper/preprint.tex",
    "paper/references.bib",
    "docs/synthesis/CONJECTURE.md",
    "docs/synthesis/EMAIL_DRAFT_HAINE.md",
    "docs/00-hypothesis.md",
    "docs/01-methodology.md",
]

SOURCE_DIRS = [
    "src",
    "tests",
    "lean",
    "templates",
]

RESEARCH_DIRS = [
    "research",
    "docs",
]

ARXIV_FILES = [
    "paper/preprint.tex",
    "paper/references.bib",
    "paper/preprint.bbl",
]


def run_git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def ensure_clean_worktree(allow_dirty: bool) -> None:
    status = run_git("status", "--porcelain")
    if status and not allow_dirty:
        raise RuntimeError(
            "Refusing to build a publication bundle from a dirty worktree. "
            "Commit the release state first, or pass --allow-dirty for a local test."
        )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_file(relative: str) -> Path:
    path = ROOT / relative
    if not path.is_file():
        raise FileNotFoundError(f"Required file is missing: {relative}")
    return path


def maybe_dir(relative: str) -> Path | None:
    path = ROOT / relative
    return path if path.is_dir() else None


def copy_file(relative: str, target_root: Path) -> None:
    source = require_file(relative)
    target = target_root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def copy_dir(relative: str, target_root: Path) -> None:
    source = maybe_dir(relative)
    if source is None:
        return
    target = target_root / relative
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns(
            "__pycache__",
            "*.pyc",
            ".pytest_cache",
            ".ruff_cache",
            ".lake",
            "build",
        ),
    )


def write_manifest(target_root: Path, version: str, commit: str) -> None:
    files: list[dict[str, object]] = []
    for path in sorted(target_root.rglob("*")):
        if path.is_file():
            relative = path.relative_to(target_root).as_posix()
            if relative == "release_manifest.json":
                continue
            files.append(
                {
                    "path": relative,
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )

    manifest = {
        "name": "axiom-explorer preprint publication bundle",
        "version": version,
        "git_commit": commit,
        "created_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "files": files,
    }
    manifest_path = target_root / "release_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    text_lines = [
        "axiom-explorer preprint publication bundle",
        f"Version: {version}",
        f"Git commit: {commit}",
        "",
        "Files:",
    ]
    text_lines.extend(f"- {item['path']} ({item['bytes']} bytes)" for item in files)
    (target_root / "RELEASE_MANIFEST.txt").write_text(
        "\n".join(text_lines) + "\n",
        encoding="utf-8",
    )


def make_zip(source_root: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(source_root.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source_root))


def build_zenodo_bundle(version: str, output_dir: Path, commit: str) -> Path:
    stage = output_dir / version
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    for relative in PUBLICATION_FILES:
        copy_file(relative, stage)
    for relative in SOURCE_DIRS:
        copy_dir(relative, stage)
    for relative in RESEARCH_DIRS:
        copy_dir(relative, stage)

    write_manifest(stage, version, commit)
    zip_path = output_dir / f"{version}-zenodo.zip"
    make_zip(stage, zip_path)
    return zip_path


def build_arxiv_bundle(version: str, output_dir: Path) -> Path:
    stage = output_dir / f"{version}-arxiv-source"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    for relative in ARXIV_FILES:
        source = require_file(relative)
        shutil.copy2(source, stage / source.name)

    zip_path = output_dir / f"{version}-arxiv-source.zip"
    make_zip(stage, zip_path)
    return zip_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version",
        default="axiom-explorer-v1-preprint",
        help="Bundle directory and zip prefix.",
    )
    parser.add_argument(
        "--output-dir",
        default="dist/publication",
        help="Output directory for generated bundles.",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow building from a dirty worktree for local testing.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = (ROOT / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    ensure_clean_worktree(args.allow_dirty)
    commit = run_git("rev-parse", "HEAD")
    zenodo_zip = build_zenodo_bundle(args.version, output_dir, commit)
    arxiv_zip = build_arxiv_bundle(args.version, output_dir)

    print(json.dumps(
        {
            "version": args.version,
            "git_commit": commit,
            "zenodo_bundle": str(zenodo_zip.relative_to(ROOT)),
            "arxiv_source_bundle": str(arxiv_zip.relative_to(ROOT)),
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()
