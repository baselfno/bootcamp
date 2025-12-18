import csv
import json
import zipfile
from io import StringIO, BytesIO
import sys
from pathlib import Path as _Path

import streamlit as st

# --- project paths ---
ROOT = _Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown


# ---------- constants ----------
OUT_DIR = ROOT / "csv-profiler" / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# (case-insensitive) tokens treated as missing
MISSING_TOKENS = {"", "na", "n/a", "null", "none", "nan"}
MISSING_NOTE = "Missing values are: `''`, `na`, `n/a`, `null`, `none`, `nan` (case-insensitive)"


# ---------- helpers ----------
def is_missing_token(v: str | None) -> bool:
    if v is None:
        return True
    s = v.strip()
    return s == "" or s.lower() in MISSING_TOKENS


def clean_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """
    Remove fully-missing rows using MISSING_TOKENS.
    Also strip whitespace from values.
    """
    cleaned: list[dict[str, str]] = []
    for r in rows:
        normalized = {k: (v or "").strip() for k, v in r.items()}
        if any(not is_missing_token(v) for v in normalized.values()):
            cleaned.append(normalized)
    return cleaned


def make_zip(json_text: str, md_text: str) -> bytes:
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("report.json", json_text)
        z.writestr("report.md", md_text)
    return buf.getvalue()


def without_notes(report: dict) -> dict:
    return {k: v for k, v in report.items() if k != "notes"}


def ensure_notes_in_markdown(md_text: str) -> str:
    if "## Notes" in md_text or "Missing values are:" in md_text:
        return md_text
    return md_text + "\n\n## Notes\n\n- " + MISSING_NOTE + "\n"


# ---------- UI ----------
st.set_page_config(page_title="CSV Profiler", layout="wide")

page = st.sidebar.radio("Navigation", ["Home", "Profiler"], index=1)

# ---------- Home ----------
if page == "Home":
    st.title("CSV Profiler")
    st.markdown(
        """
### Overview
This tool profiles CSV files and generates:

- **report.json**
- **report.md**

### Workflow
1. Upload CSV  
2. Click **Generate report**  
3. Download outputs or preview results
"""
    )
    st.stop()

# ---------- Profiler ----------
st.title("CSV Profiler")

uploaded = st.file_uploader("Upload a CSV", type=["csv"])
show_json = st.checkbox("Show JSON", value=True)

if "report" not in st.session_state:
    st.session_state["report"] = None

if uploaded is None:
    st.info("Upload a CSV to begin.")
    st.stop()

# --- load CSV (fast) ---
try:
    text = uploaded.getvalue().decode("utf-8-sig")
    rows = clean_rows(list(csv.DictReader(StringIO(text))))

    if len(rows) == 0:
        st.error("CSV loaded but has no data rows.")
        st.stop()

    st.write("Filename:", uploaded.name)
    st.write("Rows loaded:", len(rows))

except UnicodeDecodeError:
    st.error("CSV must be UTF-8 encoded.")
    st.stop()
except Exception as e:
    st.error("Failed to read CSV: " + str(e))
    st.stop()

# --- generate report (slow) ---
if st.button("Generate report"):
    try:
        report = basic_profile(rows)

        # force the Summary row count to match the real loaded rows
        report["rows"] = len(rows)

        # JSON should NOT include notes (notes only in markdown)
        report_json = without_notes(report)

        st.session_state["report"] = report_json

        write_json(report_json, OUT_DIR / "report.json")
        write_markdown(report, OUT_DIR / "report.md")  # keep notes in markdown via report

        st.success("Report generated successfully.")
    except Exception as e:
        st.error("Failed to generate report: " + str(e))
        st.stop()

report_json = st.session_state["report"]
if report_json is None:
    st.warning("No report yet. Click **Generate report**.")
    st.stop()

# ---------- download ----------
try:
    json_text = json.dumps(report_json, indent=2, ensure_ascii=False)

    md_text = (OUT_DIR / "report.md").read_text(encoding="utf-8")
    md_text = ensure_notes_in_markdown(md_text)  # make sure missing-values note appears


    zip_bytes = make_zip(json_text, md_text)

    st.download_button(
        "Download (JSON + Markdown)",
        data=zip_bytes,
        file_name="csv_profiler_outputs.zip",
        mime="application/zip",
    )
except Exception as e:
    st.error("Failed to prepare downloads: " + str(e))
    st.stop()

# ---------- markdown preview (OLD STYLE) ----------
st.subheader("Report (Markdown)")
st.markdown(md_text)

# ---------- JSON preview (RAW / row-based, NO NOTES) ----------
if show_json:
    st.subheader("Report (JSON)")
    st.json(report_json)
