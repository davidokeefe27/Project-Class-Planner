from get_prerequisites import get_prerequisites


def test_get_prerequisites():
    unique_subject_designator = ['CPSC']
    all_courses = ['CPSC 6121','CPSC 6124']

    prerequisites_list = get_prerequisites(unique_subject_designator, all_courses)
    print("Prerequisite Dict: ", prerequisites_list)
    assert get_prerequisites(unique_subject_designator, all_courses)
