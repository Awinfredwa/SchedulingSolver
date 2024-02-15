from ortools.sat.python import cp_model
from ortools.constraint_solver import pywrapcp


def create_course_schedule(students, courses, preferences, num_sections, section_capacity):
    # Initialize the solver
    solver = pywrapcp.Solver('SCIP')

    # Variables
    # Student Preference Assignment
    x = {}
    for i in range(len(students)):
        for k in range(len(preferences[i])):
            x[i, k] = solver.BoolVar(f'x[{i},{k}]')

    # Course-Time Block Assignment
    y = {}
    for j in range(len(courses)):
        for t in range(20):  # 20 time blocks
            y[j, t] = solver.BoolVar(f'y[{j},{t}]')

    # Constraints
    # 1. Each student is assigned to exactly one set of preferred courses
    for i in range(len(students)):
        solver.Add(solver.Sum(x[i, k] for k in range(len(preferences[i]))) <= 1)

    # 2. Each course is assigned to exactly one time block
    for j in range(len(courses)):
        solver.Add(solver.Sum(y[j, t] for t in range(20)) == 1)

    # 3. Students can only take one course during each time block
    for i in range(len(students)):
        for t in range(20):
            solver.Add(solver.Sum(x[i, k] * y[j, t] for k in range(len(preferences[i])) for j in preferences[i][k]) <= 1)

    # 4. Course capacities
    for j in range(len(courses)):
        total_capacity = num_sections[j] * section_capacity[j]
        solver.Add(solver.Sum(x[i, k] for i in range(len(students)) for k in range(len(preferences[i])) if j in preferences[i][k]) <= total_capacity)

    # Objective
    solver.Maximize(solver.Sum(x[i, k] for i in range(len(students)) for k in range(len(preferences[i]))))

    # Solve
    status = solver.Solve()

    if status == pywrapcp.Solver.OPTIMAL:
        print('Solution:')
        for j in range(len(courses)):
            for t in range(4):
                if y[j, t].solution_value() > 0:
                    print(f"Course {courses[j]} assigned to time block {t+1}")
        for i in range(len(students)):
            for k in range(len(preferences[i])):
                if x[i, k].solution_value() > 0:
                    print(f"Student {students[i]} assigned to preference set {k+1}: {preferences[i][k]}")
    else:
        print('No solution found.')
