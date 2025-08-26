"""
This code extracts the courses still needed from a Degree Works PDF.
It also collects unique subject designators for later use.
Created on 08/15/2025 by Andrew Nash
"""

import pdfplumber
import re


def get_courses_still_needed(pdf_src):
    requirements = []
    unique_subject_designator = []

    # Regex patterns
    still_needed_pattern = re.compile(r'Still needed:\s*(.*)', re.IGNORECASE)
    course_pattern = re.compile(r'\w+\s\d{4}[A-Za-z]?')
    credits_pattern = re.compile(r'(\d+)\s*credits?', re.IGNORECASE)

    with pdfplumber.open(pdf_src) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            for line in text.split('\n'):
                match = still_needed_pattern.search(line)
                if not match:
                    continue

                end_line = match.group(1).strip()
                courses = course_pattern.findall(end_line)
                credits_match = credits_pattern.search(end_line)
                course_amount = int(credits_match.group(1)) if credits_match else 3

                if not courses:
                    continue

                course_list = []
                subcode = ""

                for course in courses:
                    # Capture the subject code
                    if len(course[:4].split()) == 1:
                        subcode = course[:4]

                    if subcode != "":
                        course_list.append(subcode + course[course.rfind(' '):])

                        if subcode not in unique_subject_designator:
                            unique_subject_designator.append(subcode)

                if course_list:
                    requirements.append({
                        "Amount": course_amount,
                        "Courses": ', '.join(course_list)
                    })

    return requirements, unique_subject_designator
