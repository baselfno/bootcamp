from pathlib import Path
import typer

from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown

app = typer.Typer()


@app.command()
def profile(
    csv_path: Path = typer.Argument(..., help="Path to the input CSV file"),
    output_dir: Path = typer.Option(
        "csv-profiler/outputs",
        help="Directory to write output reports"
    ),
    top_k: int = typer.Option(3, help="Top K most common values"),
):
    """
    Profile a CSV file and generate JSON and Markdown reports.
    """
    rows = read_csv_rows(csv_path)
    report = basic_profile(rows, top_k=top_k)

    write_json(report, output_dir / "report.json")
    write_markdown(report, output_dir / "report.md")

    typer.echo("Wrote outputs/report.json and outputs/report.md")


@app.command()
def goodbye(
    name: str,
    formal: bool = typer.Option(False, help="Use formal goodbye"),
):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


if __name__ == "__main__":
    app()
