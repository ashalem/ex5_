import json
import os

COURSES_KEYS = "registered_courses"
NAME_KEY = "student_name"


def names_of_registered_students(input_json_path, course_name):
    """
    This function returns a list of the names of the students who registered for
    the course with the name "course_name".

    :param input_json_path: Path of the students database json file.
    :param course_name: The name of the course.
    :return: List of the names of the students.
    """
    
    # Open the json dictionary
    with open(input_json_path, "r") as json_file: 
        studentsIdToInfos = json.load(json_file)

    # return list comprehenstion
    return [studentsIdToInfo[NAME_KEY] for 
            studentsIdToInfo in studentsIdToInfos.values()
            if course_name in studentsIdToInfo[COURSES_KEYS]]


def get_all_courses(input_json_path):
    """
    This function returns a set with all courses in the json DB

    :param input_json_path: Path of the students database json file.
    """
    # Open the json dictionary
    with open(input_json_path, "r") as json_file: 
        studentsIdToInfos = json.load(json_file)

    courses = []
    for studentsIdToInfo in studentsIdToInfos.values():
        courses.extend(studentsIdToInfo[COURSES_KEYS])
    return set(courses)

def enrollment_numbers(input_json_path, output_file_path):
    """
    This function writes all the course names and the number of enrolled
    student in ascending order to the output file in the given path.

    :param input_json_path: Path of the students database json file.
    :param output_file_path: Path of the output text file.
    """

    # Open the json dictionary
    with open(input_json_path, "r") as json_file: 
        studentsIdToInfos = json.load(json_file)

    course_to_students_num = { course : len(names_of_registered_students(input_json_path, course))
                            for course in get_all_courses(input_json_path) }

    with open(output_file_path, "w") as out_file:
        for course, num_of_enrolled in sorted(course_to_students_num.items()):
            out_file.write('"{}" {}{}'.format(course, num_of_enrolled, os.linesep))

"""
def get_lectureres_to_courses(file_path):
    with open(file_path, "r") as json_db:
        courses_to_lecturers = json.load(json_db)

    lectureres_to_courses = {}
    for course_info in courses_for_lecturers.values():
        for lecturer in course_info["lecturers"]:
            if lecturer not in lectureres_to_courses:
                lectureres_to_courses[lecturer] = []
            lectureres_to_courses[lecturer].append(course_info["course_name"])
            
    return lectureres_to_courses
"""
def courses_for_lecturers(json_directory_path, output_json_path):
    """
    This function writes the courses given by each lecturer in json format.

    :param json_directory_path: Path of the semsters_data files.
    :param output_json_path: Path of the output json file.
    """
    lecturers_to_courses = {}
    for file_basename in os.listdir(json_directory_path):
        if not file_basename.endswith(".json"):
            continue

        file_path = os.path.join(json_directory_path, file_basename)
        with open(file_path, "r") as json_db:
            courses_to_lecturers = json.load(json_db)

        for course_info in courses_to_lecturers.values():
            for lecturer in course_info["lecturers"]:
                if lecturer not in lecturers_to_courses:
                    lecturers_to_courses[lecturer] = set()
                lecturers_to_courses[lecturer].add(course_info["course_name"])
    

    for lecturer in lecturers_to_courses:
        lecturers_to_courses[lecturer] = list(lecturers_to_courses[lecturer])
    with open(output_json_path, "w") as json_out_db:
        json.dump(lecturers_to_courses, json_out_db)




