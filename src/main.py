from pathlib import Path

from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown


def main() -> None:
    
    base_dir = Path(__file__).resolve().parent.parent

    
    csv_path = base_dir / "csv-profiler" / "data" / "sample.csv"
    output_dir = base_dir / "csv-profiler" / "outputs"

    rows = read_csv_rows(csv_path)
    report = basic_profile(rows)

    write_json(report, output_dir / "report.json")
    write_markdown(report, output_dir / "report.md")

    print("Wrote outputs/report.json and outputs/report.md")


if __name__ == "__main__":
    main()
