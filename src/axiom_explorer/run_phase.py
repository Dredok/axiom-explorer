"""Phase runner: dispatches to the correct phase implementation."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run an axiom-explorer research phase.")
    parser.add_argument(
        "phase",
        help="Phase identifier, e.g. 'phase0', 'phase1', 'phase2', 'phase3', 'phase4'.",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Override output directory (defaults under research/<phase>/output/).",
    )
    args = parser.parse_args(argv)

    phase = args.phase.lower()
    if phase in ("phase0", "phase0-bibliometric"):
        from axiom_explorer.phases import phase0_bibliometric

        return phase0_bibliometric.run(out_dir=args.out_dir)
    raise SystemExit(f"Unknown phase: {phase}")


if __name__ == "__main__":
    sys.exit(main())
