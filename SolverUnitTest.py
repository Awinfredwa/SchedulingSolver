import unittest
from Solver import create_course_schedule
import random

class TestCourseScheduler(unittest.TestCase):
    def test_basic_functionality(self):
        students = ["Alice", "Bob"]
        courses = [1, 2]
        preferences = [[[1], [2]], [[2], [1]]]
        sections = [1, 1]
        section_capacity = [2, 2]

        result = create_course_schedule(students, courses, preferences, sections, section_capacity)

        self.assertEqual(result['status'], 'OPTIMAL')
        self.assertIn('Alice', result['schedule'])
        self.assertIn('Bob', result['schedule'])

    def test_no_solution_possible(self):
        students = ["Alice", "Bob"]
        courses = [1, 2]
        preferences = [[[1], [2]], [[1], [2]]]
        sections = [1, 1] 
        section_capacity = [1, 1]
        result = create_course_schedule(students, courses, preferences, sections, section_capacity)

        self.assertNotEqual(result['status'], 'OPTIMAL')

    def test_large_number_of_students_fail(self):

        students = ["Student " + str(i) for i in range(100)]
        courses = [1, 2, 3]
        preferences = [[[1, 2], [2, 3], [3, 1]] for _ in students]
        sections = [5, 5, 5]
        section_capacity = [10, 10, 10]

        result = create_course_schedule(students, courses, preferences, sections, section_capacity)

        self.assertEqual(result['status'], 'NOT OPTIMAL')

    def test_large_number_of_students_success(self):
        students = ["Student " + str(i) for i in range(100)]
        courses = [1, 2, 3]
        preferences = [[[1, 2], [2, 3], [3, 1]] for _ in students]
        sections = [5, 5, 5]
        section_capacity = [20, 20, 20]

        result = create_course_schedule(students, courses, preferences, sections, section_capacity)

        self.assertEqual(result['status'], 'OPTIMAL')

    def test_varied_preferences_scheduling(self):
        students = [f"Student_{i}" for i in range(500)]
        courses = list(range(1, 16)) 
        preferences = [[random.sample(courses, 4) for _ in range(3)] for _ in range(500)]

        sections = [5 for _ in range(15)] 
        section_capacity = [40 for _ in range(15)] 

        result = create_course_schedule(students, courses, preferences, sections, section_capacity)

        self.assertEqual(result['status'], 'OPTIMAL')
        self.assertEqual(len(result['schedule']), len(students))


if __name__ == '__main__':
    unittest.main()
