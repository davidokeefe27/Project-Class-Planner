from get_schedule import get_schedule


def test_get_schedule():
    excel_file = "input/4-year schedule.xlsx"
    excel_file2 = "input/Graduate Study Plans -revised.xlsx"
    all_courses = ['CPSC 6147','CPSC 6157']
    course_offer, all_semesters = get_schedule(excel_file, excel_file2, all_courses)
    print("get_schedule() outputs:")
    print("Course Offerings: ", course_offer)
    print("All Semesters: ", all_semesters)
    assert get_schedule(excel_file, excel_file2, all_courses)
