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
            for s in range(num_sections[c]):  # Iterate over each section of the course
                # Create a Boolean variable for each student-course-section combination
                y[i, c, s] = solver.BoolVar(f'y[{i},{c},{s}]')

    # course section time block assignment
    z = {}
    for c in range(len(courses)):
        for s in range(num_sections[c]):
            for t in range(total_blocks):
                z[c, s, t] = solver.BoolVar(f'z[{c},{s},{t}]')


    # 2. Each section of courses is assigned to at most one time block
    for c in range(len(courses)):
        for s in range(sections[c]):
            # Ensure each section is assigned to at most one time block
            solver.Add(sum(z[c, s, t] for t in range(total_blocks)) <= 1)

    #2.5 no multiple section of a same course can be assigned to the same time block
    for i in range(len(courses)):
        for t in range(total_blocks):
            section_sum = []
            for j in range(sections[i]):
                section_sum.append(z[i, j, t])
            solver.Add(solver.Sum(section_sum) <= 1)

 
    # 4. Course capacities 
    for i in range(len(courses)):
        for t in range(num_sections[i]):
            student_sum = []
            for j in range(len(students)):
                student_sum.append(y[j, i, t])
            solver.Add(solver.Sum(student_sum) <= section_capacity[i])


    # Objective
    # Maximize the total number of students attending their first preferred set of courses
    solver.Maximize(solver.Sum([x[i, k] for i in range(len(students)) for k in range(2)]))
    
    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        for j in range(len(courses)):
            for t in range(total_blocks):
                if y[j, t, c].solution_value() > 0:
                    print(f"Course {courses[j]} assigned to time block {t+1} section {c+1}")
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
section_capacity = [3, 3, 3, 3, 3, 3, 3]  # Capacity for each section of each course

create_course_schedule(students, courses, preferences, num_sections, section_capacity)
