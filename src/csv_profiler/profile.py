from collections import Counter

def basic_profile(rows: list[dict[str, str]], top_k: int = 3) -> dict:
    if not rows:
        return {"rows": 0, "columns": {}, "notes": ["Empty dataset"]}

    columns = list(rows[0].keys())
    report_columns = {}

    for c in columns:
        values = [(row.get(c) or "").strip() for row in rows]
        non_empty = [v for v in values if v != ""]
        missing = len(values) - len(non_empty)

        #numeric vs text
        is_numeric = all(v.replace(".", "", 1).isdigit() for v in non_empty)

        # count/unique
        count = len(non_empty)
        unique = len(set(non_empty))

        # top_k 
        top_counts = Counter(non_empty).most_common(top_k)
        top = [{"value": val, "count": cnt} for val, cnt in top_counts]

        report_columns[c] = {
            "type": "number" if is_numeric else "text",
            "count": count,
            "missing": missing,
            "unique": unique,
            "top": top
        }

    return {"rows": len(rows), "columns": report_columns}






def is_missing(v: str) -> bool:
    return v is None or v.strip() == ""


def text_stats(values: list[str], top_k: int = 5) -> dict:
    
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)

    
    counts: dict[str, int] = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1

    
    top_items = sorted(
        counts.items(),
        key=lambda kv: kv[1],
        reverse=True
    )[:top_k]

    top = [{"value": v, "count": c} for v, c in top_items]

    return {
        "count": len(usable),
        "missing": missing,
        "unique": len(counts),
        "top": top
    }
