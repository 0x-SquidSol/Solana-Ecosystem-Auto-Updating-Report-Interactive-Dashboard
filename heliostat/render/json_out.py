"""Machine-readable JSON output."""

from __future__ import annotations

import json
from pathlib import Path


def render(report: dict, output_dir: str | Path) -> Path:
    """Write the canonical report as pretty-printed JSON; returns the path."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "report.json"
    path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path
