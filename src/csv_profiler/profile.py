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
