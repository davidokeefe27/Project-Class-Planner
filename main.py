from get_schedule import get_schedule
from courses_still_needed import get_courses_still_needed
from get_prerequisites import get_prerequisites


if __name__ == '__main__':
    pdf_src = "degree_works_ai.pdf"
    schedule_excel_file = "schedule.xlsx"
    study_plan_excel_file = "study_plan.xlsx"

    # Get list of courses still needed and their subject designators
    course_list, unique_subject_designator = get_courses_still_needed(pdf_src)
    all_courses = []
    for courses in course_list:
        course = [c.strip() for c in courses['Courses'].split(',')]
        all_courses.extend(course)
    all_prerequisites = []
    # Get when courses are offered and their prerequisites
    prerequisites = get_prerequisites(unique_subject_designator, all_courses)
    print(prerequisites)
    # Add required prerequisites to course list.
    for course in all_courses:
        for prerequisite in prerequisites[course]:
            all_courses.append(prerequisite)
    classes_offered = get_schedule(schedule_excel_file, study_plan_excel_file, all_courses)
    print(classes_offered)