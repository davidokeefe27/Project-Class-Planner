import pandas as pd


def get_schedule(excel_file, excel_file2, course_list):
    course_offer = {course: [] for course in course_list}
    # Reads Excel file and starts on row 3 where the data starts.
    data_frame = pd.read_excel(excel_file, header=2)
    data_frame2 = pd.read_excel(excel_file2)
    all_semesters = []
    # Iterate through each row in the dataframe.
    for index, row in data_frame.iterrows():
        # First column where course number is listed.
        course_number = str(row.iloc[0]).strip()

        # Columns where SP25 starts and SP29 ends.
        semester_data = row.iloc[14:27]
        # List to store all semesters offered for a course.
        offered_semesters = []

        # Loop through each column in the given row.
        for semester, cell in semester_data.items():
            cell_text = str(cell).strip()
            if semester not in all_semesters:
                all_semesters.append(semester)
            # If the cell is not blank or a dot, add to offered semesters list.
            if cell_text not in ["", ".", "nan"]:
                offered_semesters.append(semester)

        # Add the course to dictionary if valid and in course_list
        if course_number in course_list:
            course_offer[course_number] = offered_semesters
    # Get second excel data. If no data from first Excel sheet then use the second one to fill out semester list for
    # each course.
    excel_data = dict(zip(data_frame2.iloc[:, 1].str.strip(), data_frame2.iloc[:, 5].str.strip()))
    for item in excel_data:
        offer = str(excel_data[item]).lower()
        semesters = []
        if "fall" in offer and not course_offer.get(item, []):
            for semester in all_semesters:
                if "FA" in semester:
                    semesters.append(semester)
        if "spring" in offer and not course_offer.get(item, []):
            for semester in all_semesters:
                if "SP" in semester:
                    semesters.append(semester)
        if "summer" in offer and not course_offer.get(item, []):
            for semester in all_semesters:
                if "SU" in semester:
                    semesters.append(semester)
        if semesters:
            course_offer[item] = semesters
    return course_offer, all_semesters
