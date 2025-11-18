Smart Class Planner

===================

This tool generates a semester-by-semester course plan using input files from DegreeWorks, the Graduate Study Plan, and the 4-Year Schedule. It checks prerequisites, determines course ordering, and outputs a recommended plan to Excel.

Requirements

------------

- Windows 10/11

- Python 3.12+

- Git (optional)

- For building a standalone `.exe`: PyInstaller

Setup

-----

1. Create and activate a virtual environment:

```

python -m venv .venv

.\.venv\Scripts\Activate.ps1 (PowerShell)

.\.venv\Scripts\activate.bat (cmd.exe)

```

2. Install dependencies:

```

pip install -r requirements.txt

```

Input & Output

--------------

Place these files inside the `input/` directory:

- degree_works.pdf

- 4-year schedule.xlsx

- Graduate Study Plans -revised.xlsx

Output file generated:

- output/to_take.xlsx

Running the Program

-------------------

```

python scripts/main.py

```

Running Tests

-------------

```

python -m pytest

python -m pytest scripts/test_make_schedule.py

```

Creating a Standalone Windows `.exe`

------------------------------------

1. Activate the virtual environment:

```

python -m venv .venv

.\.venv\Scripts\Activate.ps1

```


2. Install PyInstaller:

```

pip install pyinstaller

```

3. Build the executable:

```

pyinstaller --onefile --name SmartClassPlanner scripts/main.py

```

4. After build, you'll have:

```

dist/

SmartClassPlanner.exe

```

5. Copy `input/` into `dist/`:

```

dist/

SmartClassPlanner.exe

input/

degree_works.pdf

4-year schedule.xlsx

Graduate Study Plans -revised.xlsx

```

6. Run the executable:

```

cd dist

./SmartClassPlanner.exe

```


Demo 3 Checklist

----------------

- Installation instructions included

- How to run from source

- How to run tests

- Full `.exe` build process documented

- Input/output structure explained
