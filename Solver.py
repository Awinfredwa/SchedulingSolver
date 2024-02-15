from ortools.linear_solver import pywraplp

def create_course_schedule(students, courses, preferences, sections, section_capacity):
    total_blocks = 20  # 5 days * total_blocks blocks/day
    # Initialize the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    # Student Preference Assignment
    x = {}
    for i in range(len(students)):
        for k in range(len(preferences[i])):
            x[i, k] = solver.BoolVar(f'x[{i},{k}]')

    # Course-Time Block Assignment
    y = {}
    for i in range(len(students)):  # Iterate over each student
        for c in range(len(courses)):  # Iterate over each course
            for s in range(len(sections)):  # Iterate over each section of the course
                for t in range(total_blocks):  # Iterate over each time block
                    # Create a Boolean variable for each student-course-section-time combination
                    y[i, c, s, t] = solver.BoolVar(f'y[{i},{c},{s},{t}]')


    # Constraints
    # 1. Each student is assigned to at most one set of preferred courses
    for i in range(len(students)):
        solver.Add(solver.Sum(x[i, k] for k in range(len(preferences[i]))) <= 1)

    # 2. Each course is assigned to exactly one time block
    for j in range(len(courses)):
        solver.Add(solver.Sum(y[j, t] for t in range(total_blocks)) == 1)

    # 3. Students can only take one course during each time block
    for i in range(len(students)):
        for t in range(total_blocks):
            # Initialize a list to hold the sum expression for each student and time block
            student_course_sum = []
            
            # Iterate over each preference set for student i
            for pref_set in preferences[i]:
                # Iterate over each course in the preference set
                for course in pref_set:
                    # Check if the course is assigned to the current time block
                    # and add the product of x[i, k] and y[course, t] to the sum expression list
                    student_course_sum.append(x[i, preferences[i].index(pref_set)] * y[course, t])
            
            # Add the constraint that the sum of all courses a student is interested in
            # that are scheduled at time block t does not exceed 1
            solver.Add(solver.Sum(student_course_sum) <= 1)

    # 4. Course capacities
    for j in range(len(courses)):
        total_capacity = num_sections[j] * section_capacity[j]
        solver.Add(solver.Sum(x[i, k] for i in range(len(students)) for k in range(len(preferences[i])) if j in preferences[i][k]) <= total_capacity)

    # Objective
    # Maximize the total number of students attending their first preferred set of courses
    solver.Maximize(solver.Sum([x[i, 0] for i in range(len(students))]))
    
    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        for j in range(len(courses)):
            for t in range(total_blocks):
                if y[j, t].solution_value() > 0:
                    print(f"Course {courses[j]} assigned to time block {t+1}")
        for i in range(len(students)):
            for k in range(len(preferences[i])):
                if x[i, k].solution_value() > 0:
                    print(f"Student {students[i]} assigned to preference set {k+1}: {preferences[i][k]}")
    else:
        print('No solution found.')

# Example data setup
students = ["Student 1", "Student 2", "Student 3", "Student 4"]
courses = [1, 2, 3, 4, 5, 6, 7]
preferences = [
    [[2, 3, 6, 7], [1, 4, 5, 6], [2, 4, 6, 7], [1, 3, 5, 7]],  # Preferences for Student 1
    [[1, 2, 3, 4], [2, 3, 5, 6], [1, 4, 6, 7], [3, 5, 6, 7]],  # Preferences for Student 2
    [[1, 2, 3, 4], [2, 3, 5, 6], [1, 4, 6, 7], [3, 5, 6, 7]], 
    [[1, 2, 3, 4], [2, 3, 5, 6], [1, 4, 6, 7], [3, 5, 6, 7]], 
    [[1, 2, 3, 4], [2, 3, 5, 6], [1, 4, 6, 7], [3, 5, 6, 7]], 
    [[1, 2, 3, 4], [2, 3, 5, 6], [1, 4, 6, 7], [3, 5, 6, 7]], 
    [[1, 2, 3, 4], [2, 3, 5, 6], [1, 4, 6, 7], [3, 5, 6, 7]]
]
num_sections = [2, 3, 2, 2, 3, 2, 2]  # Number of sections for each course
section_capacity = [30, 30, 30, 30, 30, 30, 30]  # Capacity for each section of each course

create_course_schedule(students, courses, preferences, num_sections, section_capacity)
