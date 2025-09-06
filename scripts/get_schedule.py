"""
This code takes in an Excel file containing courses and their semesters they are offered and a list of all courses.
Then searches the Excel file for each course given for their semesters offered.
Outputs all course given with their semester offerings.
"""

import pandas as pd


def get_data_4year(data_frame_4year, all_courses):
    course_offer_4year = {course: [] for course in all_courses}
    all_semesters = []
    # Iterate through each row in the dataframe
    for index, row in data_frame_4year.iterrows():
        # First column where course number is listed
        course_number = str(row.iloc[0]).strip()

        # Columns where SP25 starts and SP29 ends
        semester_data = row.iloc[14:27]
        # List to store all semesters offered for a course
        offered_semesters = []

        # Loop through each column in the given row
        for semester, cell in semester_data.items():
            cell_text = str(cell).strip()
            if semester not in all_semesters:
                all_semesters.append(semester)
            # If the cell is not blank or a dot, add to offered semesters list
            if cell_text not in ["", ".", "nan"]:
                offered_semesters.append(semester)

        # Add the course to dictionary if valid and in course_list
        if course_number in all_courses:
            course_offer_4year[course_number] = offered_semesters
    return course_offer_4year, all_semesters


def get_schedule(excel_file, excel_file2, all_courses):
    # Reads Excel file and starts on row 3 where the data starts
    data_frame_4year = pd.read_excel(excel_file, header=2)

    # Find courses offered for each course and create list of all semesters
    course_offer, all_semesters = get_data_4year(data_frame_4year, all_courses)
    # Return dictionary: course -> list of semesters offered
    # and list of all semesters
    return course_offer, all_semesters
