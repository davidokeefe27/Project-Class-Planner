"""
This code take in a Degree Works PDF file.
Then it extracts the courses still needed from the PDF.
It also collects unique subject designators for later use.
    > To know what pages to search in the catalog for prerequisites.
"""

import pdfplumber
import re


def get_courses_still_needed(pdf_src):
    requirements = []                 # List of requirements
    unique_subject_designator = []    # List of unique subject codes

    # Regex patterns to match lines in the PDF
    still_needed_pattern = re.compile(r'Still needed:\s*(.*)', re.IGNORECASE)
    course_pattern = re.compile(r'\w+\s\d{4}[A-Za-z]?')
    credits_pattern = re.compile(r'(\d+)\s*credits?', re.IGNORECASE)

    # Open the Degree Works PDF
    with pdfplumber.open(pdf_src) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            # Process each line of text
            for line in text.split('\n'):
                match = still_needed_pattern.search(line)
                if not match:
                    continue  # Skip lines that do not contain "Still needed:"

                # Extract text after "Still needed:"
                end_line = match.group(1).strip()

                # Find courses and credit requirements
                courses = course_pattern.findall(end_line)
                credits_match = credits_pattern.search(end_line)
                course_amount = int(credits_match.group(1)) if credits_match else 3

                if not courses:
                    continue  # Skip if no valid course codes found

                course_list = []
                subcode = ""  # Holds the subject code in case the next course does not have on listed just uses the
                # last subject code. (ex CPSC 6125, 6126)

                # Searches for multiple courses listed in each line.
                for course in courses:
                    # Capture the subject code (first 4 characters)
                    if len(course[:4].split()) == 1:
                        subcode = course[:4]

                    # Add full course code with subject and number
                    if subcode != "":
                        course_list.append(subcode + course[course.rfind(' '):])

                        # Keep track of unique subject codes
                        if subcode not in unique_subject_designator:
                            unique_subject_designator.append(subcode)

                # Save the found credits and courses corresponding to a given requirement
                if course_list:
                    requirements.append({
                        "Amount": course_amount,
                        "Courses": ', '.join(course_list)
                    })

    # Return both requirements: Amount: course -> Courses: list of courses
    # and the list of unique subject codes
    return requirements, unique_subject_designator
