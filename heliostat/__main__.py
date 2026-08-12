"""Command-line entry point: ``python -m heliostat``."""

import sys

from heliostat import __version__


def main() -> int:
    if sys.version_info < (3, 10):
        print("heliostat requires Python 3.10 or newer", file=sys.stderr)
        return 1
    print(f"heliostat {__version__} - collectors not wired up yet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
