"""
This code takes in a list of unique subject designators and a list of all courses.
Then searches each webpage according to the subjects given.
Outputs all courses and their prerequisites for each course listed in all courses.
"""

import re
import requests
from bs4 import BeautifulSoup


def get_prerequisites(unique_subject_designator, all_courses):
    # Dictionary to hold prerequisites for each course
    # Start with every course mapped to an empty list
    prerequisites_list = {course: [] for course in all_courses}

    course_pattern = r"[A-Z]{4}\s\d{4}[A-Za-z]?"

    for subject_designator in unique_subject_designator:
        subject = subject_designator.upper()
        # Catalog URL format
        url = (
                "https://catalog.columbusstate.edu/course-descriptions/"
                + subject.lower()
                + "/"
        )

        try:
            response = requests.get(url, timeout=10)  # Set a timeout for safety
        except requests.exceptions.RequestException as e:
            print(f"      -> ERROR: Could not access catalog for {subject} at {url}. Error: {e}")
            continue

        # Verifies website request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Each course entry is typically inside a <div class="courseblock">
            course_blocks = soup.find_all("div", class_="courseblock")

            # Process each course entry
            for course_block in course_blocks:
                course_block_text = course_block.get_text().replace("\xa0", " ").strip()

                # 1. Find the current course code (e.g., CPSC 6125)
                # This regex looks for the subject followed by 4 digits (or more letters/numbers)
                course_full_match = re.search(
                    rf"({subject}\s*\d{{4}}[A-Za-z]?)\b",
                    course_block_text,
                )

                if not course_full_match:
                    continue  # Skip blocks that don't match the expected course format

                course = course_full_match.group(1).replace(" ", "")  # Clean up spaces

                # Format to standard "CPSC 6125" for matching with all_courses
                course_code = course[:4] + " " + course[4:]

                # 2. Check if this is a course we need prerequisites for
                if course_code not in all_courses:
                    continue

                    # 3. Get the raw text for prerequisites
                prerequisites_match = re.search(
                    r"Prerequisite\(s\):\s*(.*?)(\.\s*Credit Hours|$)",
                    course_block_text,
                    re.IGNORECASE | re.DOTALL  # Ignore case and allow . to match newline
                )

                if prerequisites_match:
                    prerequisites_raw = prerequisites_match.group(1).strip()

                    # 4. Extract only the course codes from the raw prerequisite text
                    # We look for all instances of the standard course pattern
                    prereq_courses = re.findall(course_pattern, prerequisites_raw)

                    # 5. Save the clean list of prerequisite course codes
                    prerequisites_list[course_code] = prereq_courses

        else:
            print(
                f"      -> WARNING: Failed to retrieve catalog page for {subject}. Status code: {response.status_code}")

    # Return dictionary: course -> list of prerequisite courses
    return prerequisites_list