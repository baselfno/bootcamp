## Requirements
- Python 3.11+
- uv (recommended)


## Project Structure
bootcamp/
├─ csv-profiler/
│  ├─ data/
│  │  └─ sample.csv
│  └─ outputs/
│     ├─ report.json
│     └─ report.md
├─ src/
│  ├─ main.py
│  └─ csv_profiler/
│     ├─ io.py
│     ├─ profile.py
│     └─ render.py
├─ pyproject.toml
└─ uv.lock


## Verify Environment
```bash
uv --version
uv run python --version


### . Navigate to the project root directory
Use `cd` to move to the project folder.

Example:
```bash
cd C:\project1\bootcamp


## . Verify uv is available
uv --version



## . Setup the environment
uv sync



## . Run the program
uv run python src/main.py



## . Output
After running the command, the following files will be generated:
csv-profiler/outputs/report.json
csv-profiler/outputs/report.md



## . Notes
-The input CSV file must exist at:
csv-profiler/data/sample.csv

-Always run commands from the project root directory
-Missing values are represented as empty strings





