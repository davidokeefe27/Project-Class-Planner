Smart Class Planner - README

Purpose
Smart Class Planner is a command-line tool that generates a semester-by-semester course plan from a student’s DegreeWorks report and CSU planning spreadsheets. It:

- Reads required and completed courses from a DegreeWorks PDF.
- Uses the official 4-year schedule and Graduate Study Plan spreadsheets to find when courses are offered.
- Checks prerequisites and orders courses so they are taken in a valid sequence.
- Produces an Excel file showing which courses to take each term, focusing on required (core) courses only.

The goal is to help students and advisors ensure that prerequisites are not missed and that the student can graduate on time with a clear, editable plan in Excel.

Prerequisites
- Operating System: Windows 10 or Windows 11
- Python: Python 3.12+ (64-bit recommended)
- Tools (optional but recommended):
  - Git (to clone the repository)
  - A virtual environment tool (venv built into Python)
- Python packages: All Python dependencies are listed in requirements.txt. You do not need to install them one-by-one; use the single command shown below in the Build / Installation section.

Note: If you only want to use the Windows executable (SmartClassPlanner.exe), you can skip Python and requirements.txt entirely.

Download
You can obtain the project in either of these ways:

1. Clone the repository (recommended)
   From a terminal (PowerShell or Command Prompt):

   git clone <repository-url>
   cd Project-Class-Planner

   Replace <repository-url> with your GitHub or GitHub Classroom URL.

2. Download ZIP and extract
   - Download the project ZIP file from your course site or GitHub.
   - Right-click the ZIP and choose Extract All…
   - Navigate into the extracted Project-Class-Planner folder.

The project root directory should contain folders like scripts, input, output, and dist.

Build / Configuration / Installation / Deployment

Option 1: Run from source (developer / grader setup)
1. Open a terminal in the project root, for example:

   cd path\to\Project-Class-Planner

2. (Optional) Create and activate a virtual environment:

   python -m venv .venv
   .venv\Scripts\activate

3. Install all Python dependencies using requirements.txt:

   pip install -r requirements.txt

   This will install everything the project needs (for example, pandas, pdfplumber, etc.) in one step.

4. Prepare input files:
   Place the required input files in the input folder with the following exact names:

   - input/degree_works.pdf
   - input/4-year schedule.xlsx
   - input/Graduate Study Plans -revised.xlsx

   The program expects these specific filenames and relative paths.

5. (Optional) Run tests.
   From the project root or scripts folder:

   pytest

Option 1b: Build the Windows executable yourself (PyInstaller)
If SmartClassPlanner.exe is not provided, you can build it from the source code using PyInstaller.

1. Make sure you have installed dependencies as described above (pip install -r requirements.txt) and that you are in the project root (Project-Class-Planner).

2. Install PyInstaller:

   pip install pyinstaller

3. Build the executable:

   pyinstaller --onefile --name SmartClassPlanner scripts/main.py

4. After the build completes, you will have a dist folder containing:

   dist/
     SmartClassPlanner.exe

5. Copy the input folder into dist so the executable can find the required files:

   dist/
     SmartClassPlanner.exe
     input/
       degree_works.pdf
       4-year schedule.xlsx
       Graduate Study Plans -revised.xlsx

6. Run the executable from inside dist:

   cd dist
   .\SmartClassPlanner.exe

Option 2: Use an existing packaged Windows executable (SmartClassPlanner.exe)
If SmartClassPlanner.exe is already provided (for example, in the dist folder), you can use it directly without rebuilding.

1. Ensure the following structure (simplest approach is to keep everything together):

   Project-Class-Planner/
     dist/
       SmartClassPlanner.exe
     input/
       degree_works.pdf
       4-year schedule.xlsx
       Graduate Study Plans -revised.xlsx
     output/
       (generated files will appear here)

2. Open PowerShell or Command Prompt and navigate to the dist folder:

   cd path\to\Project-Class-Planner\dist

3. Run the executable:

   .\SmartClassPlanner.exe

   The executable will look for the input folder and write its output to the output folder at the project level.

Usage
-----

Running from source
From the project root (after installing prerequisites and placing input files):

   cd scripts
   python main.py

What happens when you run the program:
1. The tool reads:
   - input/degree_works.pdf (DegreeWorks audit)
   - input/4-year schedule.xlsx (CSU 4-year schedule)
   - input/Graduate Study Plans -revised.xlsx (Graduate Study Plan)
2. It determines:
   - Which courses are still needed.
   - When those courses are offered.
   - A valid order that respects prerequisites, with a default maximum of 9 credits per term.
3. It writes the recommended plan to:

   - output/to_take.xlsx

Running the Windows executable
From the dist folder:

   .\SmartClassPlanner.exe

The behavior is the same as running from source:
- Input: files from the input folder.
- Output: output/to_take.xlsx containing the semester-by-semester course plan.

Note: If you want to adjust the maximum credits per term or other behavior, edit scripts/main.py (for example, change max_credits = 9) and re-run from source or rebuild the executable with PyInstaller.