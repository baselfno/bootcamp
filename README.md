## Requirements
- Python 3.11+
- uv (recommended)



## Commandline



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







