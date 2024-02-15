from ortools.sat.python import cp_model
import json
# from Solver import create_course_schedule
from simpleSolver import simple_course_schedule

# classes to represent Student-preferences 
class Student:
    def __init__(self, studentId, terms):
        self.studentId = studentId
        self.terms = [Term(**term) for term in terms]

class Term:
    def __init__(self, termId, coursesPreferences):
        self.termId = termId
        self.coursesPreferences = coursesPreferences

# classes to represent Courses
class Course:
    def __init__(self, id, name, code, maxSeats, maxSections):
        self.id = id
        self.name = name
        self.code = code
        self.maxSeats = maxSeats
        self.maxSections = maxSections

# each section of a course should be treated separately, 
# just add a check so that no two sections of the same course are scheduled at the same time
class Section:
    def __init__(self, id, courseId, maxSeats):
        self.id = id
        self.courseId = courseId
        self.maxSeats = maxSeats
        self.currSeats = 0

# Function to load students
def load_students(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return [Student(**student) for student in data]

# Function to load courses
def load_courses(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return [Course(**course) for course in data]


# Load the students' preferences from 'students.json'
studentStructs = load_students('student-preferences.json')
# Load the courses from 'courses.json'
courseStructs = load_courses('courses.json')

# Print data for testing
# for course in courses:
#     print(f"ID: {course.id}, Name: {course.name}, Code: {course.code}, Max Seats: {course.maxSeats}, Max Sections: {course.maxSections}")

# for student in students:
#     print(f"ID: {student.studentId}")
#     for term in student.terms:
#         print(f"Term ID: {term.termId}")
#         for i in range (len(term.coursesPreferences)):
#             print(term.coursesPreferences[i])

model = cp_model.CpModel()

num_courses = 40
num_students = 200
num_courses_per_day = 4  # Excluding lunch block
num_days = 5
num_preferences_each = 4



students = []
for i in range(num_students):
    students.append(studentStructs[i].studentId)
courses = []
for i in range(num_courses):
    courses.append(courseStructs[i].id)
# we are only considering the students' first term preferences for now
preferences = []
for i in range(num_students):
    preferences.append(studentStructs[i].terms[0].coursesPreferences)
num_sections = []
for i in range(num_courses):
    num_sections.append(courseStructs[i].maxSections)
section_capacity = []
for i in range(num_courses):
    section_capacity.append(courseStructs[i].maxSeats)

# create_course_schedule(students, courses, preferences, num_sections, section_capacity)
simple_course_schedule(students, courses, preferences, section_capacity)
# print("Students: ", students)
# print("Courses: ", courses)
# print("Preferences: ", preferences)
# print("Num Sections: ", num_sections)
# print("Section Capacity: ", section_capacity)
