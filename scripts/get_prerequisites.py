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

    # Loop through each subject code given
    for subject_designator in unique_subject_designator:
        # Catalog URL with the requirements
        url = (
            "https://catalog.columbusstate.edu/course-descriptions/"
            + subject_designator.lower()
            + "/"
        )
        response = requests.get(url)

        # Verifies website request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Each course entry is inside a <div class="courseblock">
            course_blocks = soup.find_all("div", class_="courseblock")

            # Process each course entry
            for course_block in course_blocks:
                course_number_text = course_block.get_text()

                # Find the course number
                course_number_match = re.search(
                    rf"{subject_designator.upper()}\s*(\b\w+\b)",
                    course_number_text,
                )

                # Regex to identify full course codes
                course_pattern = r"[A-Z]{4}\s\d{4}[A-Za-z]?"
                # Regex for prerequisites with and/or
                prerequisites_pattern = (
                    rf"{course_pattern}|\b(?:and|or)\b(?=\s{course_pattern})"
                )

                # Getting the 4 digit course number
                course_number = (
                    course_number_match.group(1).strip()
                    if course_number_match
                    else "None"
                )
                course = subject_designator + " " + course_number

                # Get the raw text for prerequisites
                prerequisites_text = course_block.get_text().replace("\xa0", " ").strip()
                prerequisites_match = re.search(
                    r"Prerequisite\(s\):\s*(.*)", prerequisites_text
                )

                # If this course has prerequisites, and it's in our list
                if prerequisites_match and course in all_courses:
                    prerequisites = prerequisites_match.group(1).strip()

                    # Extract all prerequisite course codes
                    prerequisites = " ".join(
                        re.findall(prerequisites_pattern, prerequisites)
                    )

                    # Save prerequisites for this course
                    prerequisites_list[course].append(prerequisites)

    # Return dictionary: course -> list of prerequisites
    return prerequisites_list
