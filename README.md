# Smart Class Planner

This tool creates a semester-by-semester class plan from a DegreeWorks PDF, a Graduate Plan Excel, and a 4-Year Schedule Excel.

## 🛠️ Setup
```bash
pip install -r requirements.txt
```

## 🧑‍💻 Usage
1. Place these files in the project input folder:
   - degree_works.pdf
   - 4-year schedule.xlsx
   - Graduate Study Plans -revised.xlsx

2. Run:
```bash
python scripts/main.py
```

## 🚀 Execution Guide: Running the Course Planner (Windows)
The output plan will be written to an Excel file inside the output folder.This tool is provided as a standalone Windows executable (.exe) and does not require Python or external installations. Please dowload the files in the [here](https://github.com/davidokeefe27/Project-Class-Planner/releases/tag/v1.0.0).

### Requirements
Ensure your input files are placed in the required structure (Replace input files with your own):

```
Course_Planner/
├── Course_Planner.exe
└── input/
    ├── degree_works.pdf          # DegreeWorks List
    ├── 4-year schedule.xlsx      # 4-Year Schedule
    └── Graduate Study Plans -revised.xlsx # Graduate Study Plan
```

### Intructions 
1. Extract the Files: Right-click the main `.zip` file and select "Extract All..." You cannot run the program reliably while it is still compressed.
2. Organize Inputs: Place all three required input files inside the `input/` folder of the extracted directory.
3. Run: Double-click the `Course_Planner.exe`.
4. Find Output: The program will automatically create a new folder named `output/` in the same location.
    - The results are saved in: `output/to_take.xlsx`

*Note: If the output file does not appear, move the entire extracted folder to an accessible location like your Desktop and run the `.exe` again to resolve potential Windows permissions issues.*

## 🧪 Running the Unit Tests

This guide outlines the steps to execute the unit tests for the Course Planner project. The tests are written using the pytest framework and require the project's dependencies to be installed within a virtual environment.

- You must have the following installed to run the tests:
- Python 3.x
- Virtual Environment (.venv or venv folder created)

All required dependencies (pytest, pdfplumber, pandas, etc.) installed via pip install -r requirements.txt (or equivalent commands).

To execute all tests found in the test_*.py files within your project structure (including scripts/):

```
python -m pytest
```

To Run a Specific Test File
To execute tests only in a specific file (e.g., test_make_schedule.py):

```
python -m pytest .\scripts\test_make_schedule.py
```
