# Automation Scripts 

Small Python utilities that save time on everyday tasks: file cleanup, quick CSV reporting, and simple automations.

**Stack:** Python • argparse • Pandas (for data utilities)

---

## Scripts

### 1) Batch rename files
Renames files in a folder using a consistent pattern (useful for messy downloads or project assets).

**Example**
```bash
python3 src/rename_files.py --path "./downloads" --prefix "basel_" --dry-run
python3 src/rename_files.py --path "./downloads" --prefix "basel_"
```

### 2) CSV quick summary
Generates a quick report from a CSV (row count, missing values, basic stats, top categories).

**Example**
```bash
python3 src/csv_summary.py --file "data/sample.csv" --out "outputs/report.txt"
```

---

## Setup
```bash
pip install -r requirements.txt
```

## Notes
These scripts are intentionally small, readable, and reusable.
