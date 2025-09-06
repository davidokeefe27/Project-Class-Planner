# Smart Class Planner

This tool creates a semester-by-semester class plan from a DegreeWorks PDF, a Graduate Plan Excel, and a 4-Year Schedule Excel.

## Setup
```bash
pip install -r requirements.txt
```

## Usage
1. Place these files in the project input folder:
   - degree_works.pdf
   - 4-year schedule.xlsx
   - Graduate Study Plans -revised.xlsx

2. Run:
```bash
python scripts/main.py
```

The output plan will be written to an Excel file inside the output folder.
