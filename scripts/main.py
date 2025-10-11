"""
This code is the main file to capture the inputs needed, max credits, and output file location.
"""

from make_schedule import make_schedule
import os
import sys


def main():
    # input files
    pdf_src = "input/degree_works.pdf"
    schedule_excel_file = "input/4-year schedule.xlsx"
    study_plan_excel_file = "input/Graduate Study Plans -revised.xlsx"

    max_credits = 9
    # output file
    if getattr(sys, 'frozen', False):
    # We are running as a PyInstaller executable (.exe)
    # sys.executable is the path to the .exe itself.
        base_dir = os.path.dirname(sys.executable)
    else:
    # We are running as a normal Python script
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full, absolute path for the output file
    output_folder = os.path.join(base_dir, "output")
    path = os.path.join(output_folder, "to_take.xlsx")

    # Ensure the output directory exists before trying to write to it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    make_schedule(pdf_src, schedule_excel_file, study_plan_excel_file, max_credits, path)



if __name__ == "__main__":
    main()
