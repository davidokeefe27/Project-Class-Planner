from make_schedule import get_data, select_required_courses, create_schedule, output_schedule

def test_get_data():
    pdf_src = "input/degree_works.pdf"
    schedule_excel_file = "input/4-year schedule.xlsx"
    study_plan_excel_file = "input/Graduate Study Plans -revised.xlsx"
    course_list, prerequisites, classes_offered, all_semesters = get_data(
        pdf_src, schedule_excel_file, study_plan_excel_file
    )
    print("Course List:", course_list)
    print("Prerequisite List:", prerequisites)
    print("Classes Offered:", classes_offered)
    print("All Semesters", all_semesters)
    assert get_data(
        pdf_src, schedule_excel_file, study_plan_excel_file
    )

def test_select_required_courses():
    course_list = [{'Amount': 3, 'Courses': 'CPSC 6109'}, {'Amount': 3, 'Courses': 'CPSC 6119'},
           {'Amount': 3, 'Courses': 'CYBR 6126'}, {'Amount': 3, 'Courses': 'CPSC 6185'},
           {'Amount': 6, 'Courses': 'CPSC 6985, CPSC 6986, CPSC 6127, CPSC 6698'},
           {'Amount': 3, 'Courses': 'CPSC 6000'}, {'Amount': 3, 'Courses': 'CPSC 6127'},
           {'Amount': 3, 'Courses': 'CPSC 6157'}]
    classes_offered = {'CPSC 6109': ['SP25', 'FA25', 'SP26', 'FA26', 'SP27', 'FA27', 'SP28', 'FA28', 'SP29'],
              'CPSC 6119': ['SU25', 'FA25', 'SU26', 'FA26', 'SU27', 'FA27', 'SU28', 'FA28'],
              'CYBR 6126': ['SP25', 'SU25', 'FA25', 'SP26', 'SU26', 'FA26', 'SP27', 'SU27', 'FA27', 'SP28', 'SU28',
                            'FA28', 'SP29'], 'CPSC 6185': ['SP25', 'FA25', 'SP26', 'SP27', 'SP28', 'SP29'],
              'CPSC 6985': [], 'CPSC 6986': [], 'CPSC 6127': ['SP25', 'SP26', 'SP27', 'SP28', 'SP29'], 'CPSC 6698': [],
              'CPSC 6000': ['SP25', 'SU25', 'FA25', 'SP26', 'SU26', 'FA26', 'SP27', 'SU27', 'FA27', 'SP28', 'SU28',
                            'FA28', 'SP29'],
              'CPSC 6157': ['SP25', 'FA25', 'SP26', 'FA26', 'SP27', 'FA27', 'SP28', 'FA28', 'SP29']}
    to_take, not_scheduled = select_required_courses(course_list, classes_offered)
    print("To Take",to_take)
    print("Not Scheduled", not_scheduled)
    assert select_required_courses(course_list, classes_offered)

def test_create_schedule():
    all_semesters = ['SP25', 'SU25', 'FA25', 'SP26', 'SU26', 'FA26', 'SP27', 'SU27', 'FA27', 'SP28', 'SU28', 'FA28', 'SP29']
    classes_offered = {'CPSC 6109': ['SP25', 'FA25', 'SP26', 'FA26', 'SP27', 'FA27', 'SP28', 'FA28', 'SP29'],
                       'CPSC 6119': ['SU25', 'FA25', 'SU26', 'FA26', 'SU27', 'FA27', 'SU28', 'FA28'],
                       'CYBR 6126': ['SP25', 'SU25', 'FA25', 'SP26', 'SU26', 'FA26', 'SP27', 'SU27', 'FA27', 'SP28','SU28',
                                     'FA28', 'SP29'],
                       'CPSC 6185': ['SP25', 'FA25', 'SP26', 'SP27', 'SP28', 'SP29'],
                       'CPSC 6985': [],
                       'CPSC 6986': [],
                       'CPSC 6127': ['SP25', 'SP26', 'SP27', 'SP28', 'SP29'],
                       'CPSC 6698': [],
                       'CPSC 6000': ['SP25', 'SU25', 'FA25', 'SP26', 'SU26', 'FA26', 'SP27', 'SU27', 'FA27', 'SP28','SU28',
                                     'FA28', 'SP29'],
                       'CPSC 6157': ['SP25', 'FA25', 'SP26', 'FA26', 'SP27', 'FA27', 'SP28', 'FA28', 'SP29']}
    prerequisites = {'CPSC 6109': [], 'CPSC 6119': [], 'CYBR 6126': [], 'CPSC 6185': [], 'CPSC 6985': [],
                     'CPSC 6986': [], 'CPSC 6127': [], 'CPSC 6698': [], 'CPSC 6000': [], 'CPSC 6157': []}
    to_take = ['CPSC 6000', 'CPSC 6109', 'CPSC 6119', 'CPSC 6127', 'CPSC 6157', 'CPSC 6185', 'CYBR 6126']
    max_credits = 9
    schedule = create_schedule(all_semesters, classes_offered, prerequisites, to_take, max_credits)
    print("Schedule: ", schedule)
    assert schedule

def test_output_schedule():
    schedule = {'SP26': ['CPSC 6109', 'CYBR 6126', 'CPSC 6185'], 'SU26': ['CPSC 6119', 'CPSC 6000'], 'FA26': ['CPSC 6157'], 'SP27': ['CPSC 6127'], 'SU27': [], 'FA27': [], 'SP28': [], 'SU28': [], 'FA28': [], 'SP29': []}
    path = "output/to_take.xlsx"
    not_scheduled = ['Test Not Scheduled Goes Here']
    output_schedule(schedule, path, not_scheduled)
    assert True
