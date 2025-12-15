from __future__ import annotations

import json
from pathlib import Path


def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )


def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    columns = report.get("columns", {})
    rows_count = report.get("rows", 0)

    lines: list[str] = []

    
    lines.append("# CSV Profiling Report\n")

    
    lines.append("## Summary\n")
    lines.append(f"- **Rows:** {rows_count}")
    lines.append(f"- **Columns:** {len(columns)}\n")

    
    lines.append("## Columns Profile\n")
    lines.append("| Column | Type | Count | Missing | Unique |")
    lines.append("|--------|------|-------|---------|--------|")

    for col_name, col_info in columns.items():
        lines.append(
            f"| {col_name} | {col_info.get('type', 'unknown')} | "
            f"{col_info.get('count', 0)} | "
            f"{col_info.get('missing', 0)} | "
            f"{col_info.get('unique', 0)} |"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
