"""
This code is the brains of the project.
Takes in the Degree Works PDF, Schedule Excel, and Study Plan Excel files.
Imports courses_still_needed, get_prerequisites, and get_schedule to create the final schedule to output.
"""


import pandas as pd
from datetime import date
from courses_still_needed import get_courses_still_needed  # Extracts courses still needed from DegreeWorks PDF
from get_prerequisites import get_prerequisites  # Gets prerequisites for courses from catalog
from get_schedule import get_schedule  # Reads schedule Excel files to find when courses are offered


def get_data(pdf_src, schedule_excel_file, study_plan_excel_file):
    # Gets list of courses and subject codes from PDF
    course_list, unique_subject_designator = get_courses_still_needed(pdf_src)

    # Build a list of all courses
    all_courses = []
    for courses in course_list:
        course_codes = [course.strip() for course in courses['Courses'].split(',')]
        for course in course_codes:
            all_courses.append(course)

    # Fetch prerequisites for all courses
    prerequisites = get_prerequisites(unique_subject_designator, all_courses)

    # Add prerequisites into the full list of courses
    for prerequisite_list in prerequisites.values():
        all_courses.extend(prerequisite_list)

    # Get course offerings and available semesters from schedule Excel files
    classes_offered, all_semesters = get_schedule(
        schedule_excel_file,
        study_plan_excel_file,
        all_courses
    )

    return course_list, prerequisites, classes_offered, all_semesters

def get_current_semester():
    year = date.today().year
    month = date.today().month
    semester = ""
    if month <= 5 :
        semester = "SP" # Current is Spring
    elif month <= 8:
        semester = "SU" # Current is Summer
    else:
        semester = "FA" # Current is Fall
    semester = semester + str(year)[-2:]
    return semester


def select_required_courses(course_list, classes_offered):
    # Selects which courses must be taken to satisfy requirements
    to_take = []
    not_scheduled = []
    course_list = sorted(course_list, key=lambda d: (d["Amount"], d["Courses"]))
    for item in course_list:
        class_credits = int(item["Amount"])   # number of credits needed
        courses = [c.strip() for c in item["Courses"].split(",")]
        count = 0
        # Keep adding courses until the required credits are satisfied
        while class_credits > 0 and count < len(courses):
            course = courses[count]
            offerings = classes_offered.get(course, [])
            if offerings and course not in to_take:
                to_take.append(course)
                class_credits -= 3  # assume each course is 3 credits
            count += 1
        if class_credits > 0:
            not_scheduled.append(str(class_credits) + " Credit(s) in "+item["Courses"])
    return to_take, not_scheduled


def semester_key(semester):
    # Converts a semester code into a numeric key for sorting
    term = semester[:2]
    year = int(semester[2:])
    if term == 'SP':
        term_number = 1
    elif term == 'SU':
        term_number = 2
    else:
        term_number = 3
    return year * 100 + term_number


def create_schedule(
        all_semesters,
        classes_offered,
        prerequisites,
        to_take,
        max_credits
):
    # Sort semester list and only schedule if after current semester
    all_semesters.sort(key=semester_key)
    semester_index = all_semesters.index(get_current_semester())+1 # Next semester
    all_semesters[:] = all_semesters[semester_index:]

    # Initialize schedule dict and fill with all semesters
    schedule = {semester: [] for semester in all_semesters}
    taken_courses = []

    # Fill each semester with eligible courses
    for semester in all_semesters:
        semester_credits = len(schedule[semester])  # current credits in semester
        semester_courses = []

        # First loop to prioritize adding courses that are prerequisites
        for course, semesters in classes_offered.items():
            if (
                course not in taken_courses
                and semester in semesters
                and semester_credits + 3 <= max_credits
                and all(pre in taken_courses for pre in prerequisites.get(course, []))
                and course in to_take
                #and course in prerequisite list
            ):
                semester_courses.append(course)
                taken_courses.append(course)
                semester_credits += 3

        # Second loop repeats logic to fill with classes that are not prerequisites
        for course, semesters in classes_offered.items():
            if (
                course not in taken_courses
                and semester in semesters
                and semester_credits + 3 <= max_credits
                and all(pre in taken_courses for pre in prerequisites.get(course, []))
                and course in to_take
            ):
                semester_courses.append(course)
                taken_courses.append(course)
                semester_credits += 3

        # Save courses scheduled for this semester
        if semester_courses:
            schedule[semester] = semester_courses

    return schedule


def output_schedule(schedule, path, not_scheduled):
    # Write the schedule dictionary into an Excel file
    columns = {}
    for semester, courses in schedule.items():
        if courses:
            columns[semester] = pd.Series(courses)  # one column per semester
    if not_scheduled:
        columns["Not Able to Schedule: "] = pd.Series(not_scheduled)
    data_frame = pd.DataFrame(columns)
    data_frame.to_excel(path, index=False)


def make_schedule(pdf_src, schedule_excel_file, study_plan_excel_file, max_credits, path):
    # Extract data
    course_list, prerequisites, classes_offered, all_semesters = get_data(
        pdf_src, schedule_excel_file, study_plan_excel_file
    )
    # Choose courses
    to_take, not_scheduled = select_required_courses(course_list, classes_offered)
    # Build plan
    schedule = create_schedule(all_semesters, classes_offered, prerequisites, to_take, max_credits)
    # Save output
    output_schedule(schedule, path, not_scheduled)
