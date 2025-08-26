"""
This code takes a list of unique_subject_designator to find all courses
and their prerequisites for each subject.
Created on 08/15/2025 by Andrew Nash
"""

import re
import requests
from bs4 import BeautifulSoup


def get_prerequisites(unique_subject_designator, all_courses):
    prerequisites_list = {course: [] for course in all_courses}

    for subject_designator in unique_subject_designator:
        url = (
            "https://catalog.columbusstate.edu/course-descriptions/"
            + subject_designator.lower()
            + "/"
        )
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            course_blocks = soup.find_all("div", class_="courseblock")

            for course_block in course_blocks:
                course_number_text = course_block.get_text()

                # Find parent course number
                course_number_match = re.search(
                    rf"{subject_designator.upper()}\s*(\b\w+\b)",
                    course_number_text,
                )

                course_pattern = r"[A-Z]{4}\s\d{4}[A-Za-z]?"
                prerequisites_pattern = (
                    rf"{course_pattern}|\b(?:and|or)\b(?=\s{course_pattern})"
                )

                course_number = (
                    course_number_match.group(1).strip()
                    if course_number_match
                    else "None"
                )
                course = subject_designator + " " + course_number

                prerequisites_text = course_block.get_text().replace("\xa0", " ").strip()
                prerequisites_match = re.search(
                    r"Prerequisite\(s\):\s*(.*)", prerequisites_text
                )

                if prerequisites_match and course in all_courses:
                    prerequisites = prerequisites_match.group(1).strip()
                    prerequisites = " ".join(
                        re.findall(prerequisites_pattern, prerequisites)
                    )
                    prerequisites_list[course].append(prerequisites)

    return prerequisites_list
