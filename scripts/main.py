"""
This code is the main file to capture the inputs needed, max credits, and output file location.
"""

from make_schedule import make_schedule


def main():
    # input files
    pdf_src = "input/degree_works.pdf"
    schedule_excel_file = "input/4-year schedule.xlsx"
    study_plan_excel_file = "input/Graduate Study Plans -revised.xlsx"

    max_credits = 9
    # output file
    path = "output/to_take.xlsx"
    make_schedule(pdf_src, schedule_excel_file, study_plan_excel_file, max_credits, path)


if __name__ == "__main__":
    main()
