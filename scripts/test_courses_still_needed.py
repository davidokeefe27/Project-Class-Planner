from courses_still_needed import get_courses_still_needed


def test_get_courses_still_needed():
    pdf_src = "input/degree_works.pdf"
    requirements, unique_subject_designator = get_courses_still_needed(pdf_src)
    print("Requirements: ", requirements)
    print("Unique Subjects: ", unique_subject_designator)
    assert get_courses_still_needed(pdf_src)
