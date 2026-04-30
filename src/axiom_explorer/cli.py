"""Top-level CLI entry point."""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="axiom-explorer")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run-phase", help="Run a research phase end-to-end.")
    run_p.add_argument("phase")
    run_p.add_argument("--out-dir", default=None)

    sub.add_parser("seeds", help="Print seed definitions.")

    args = parser.parse_args(argv)

    if args.cmd == "run-phase":
        from axiom_explorer.run_phase import main as run_phase_main

        return run_phase_main([args.phase] + (["--out-dir", args.out_dir] if args.out_dir else []))
    if args.cmd == "seeds":
        from axiom_explorer.seeds import SEEDS

        for code, s in SEEDS.items():
            print(f"{code}: {s.name}  [{s.branch}]")
            print(f"   primary: {', '.join(s.primary_terms)}")
            print(f"   related: {', '.join(s.related_terms)}")
        return 0
    return 1
