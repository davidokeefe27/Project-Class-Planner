import pandas as pd
from get_schedule import get_schedule
from courses_still_needed import get_courses_still_needed
from get_prerequisites import get_prerequisites

pdf_src = "degree_works_ai.pdf"
schedule_excel_file = "schedule.xlsx"
study_plan_excel_file = "study_plan.xlsx"

course_list, unique_subject_designator = get_courses_still_needed(pdf_src)

all_courses = []
for courses in course_list:
    course_codes = [course.strip() for course in courses['Courses'].split(',')]
    for course in course_codes:
        all_courses.append(course)

prerequisites = get_prerequisites(unique_subject_designator, all_courses)

for prerequisite_list in prerequisites:
    for prerequisite in prerequisite_list:
        all_courses.append(prerequisite)

classes_offered, all_semesters = get_schedule(
    schedule_excel_file,
    study_plan_excel_file,
    all_courses
)

taken_courses = []
to_take = []
schedule = {}
max_credits = 9

for item in course_list:
    amount = int(item["Amount"])
    courses = [c.strip() for c in item["Courses"].split(",")]
    count = 0

    while amount > 0 and count < len(courses):
        course = courses[count]
        offerings = classes_offered.get(course, [])

        if offerings and course not in to_take:
            to_take.append(course)
            amount -= 3

        count += 1


def semester_key(semester):
    term = semester[:2]
    year = int(semester[2:])
    if term == 'SP':
        term_number = 1
    elif term == 'SU':
        term_number = 2
    else:
        term_number = 3
    return year * 100 + term_number


all_semesters.sort(key=semester_key)
schedule = {semester: [] for semester in all_semesters}

for semester in all_semesters:
    semester_credits = len(schedule[semester])
    semester_courses = []

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

    if semester_courses:
        schedule[semester] = semester_courses

print("Schedule:")
for semester, courses in schedule.items():
    if courses:
        print(f"{semester}: {', '.join(courses)}")

columns = {}
for semester, courses in schedule.items():
    columns[semester] = pd.Series(courses)

data_frame = pd.DataFrame(columns)
data_frame.to_excel("to_take.xlsx", index=False)
