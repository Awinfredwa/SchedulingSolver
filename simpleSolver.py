from ortools.linear_solver import pywraplp

def simple_course_schedule(students, courses, preferences, capacities):
    # Create the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    # x[i, k] is an array of binary variables, which will be 1 if student i is assigned to their k-th set of preferred courses.
    x = {}
    for i in range(len(students)):
        for k in range(len(preferences[i])):
            x[i, k] = solver.BoolVar(f'x[{i},{k}]')

    # Constraints
    # Each student is assigned to at most one set of preferred courses
    for i in range(len(students)):
        solver.Add(solver.Sum([x[i, k] for k in range(len(preferences[i]))]) <= 1)

    # The number of students in each course does not exceed its capacity
    for j in range(len(courses)):
        solver.Add(solver.Sum([x[i, k] for i in range(len(students)) for k in range(len(preferences[i])) if j in preferences[i][k]]) <= capacities[j])

    # Objective
    # Maximize the total number of students attending their first preferred set of courses
    solver.Maximize(solver.Sum([x[i, 0] for i in range(len(students))]))

    # Solve
    status = solver.Solve()

    # Check if a solution exists
    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        assigned_students = 0
        for i in range(len(students)):
            is_assigned = False
            for k in range(len(preferences[i])):
                if x[i, k].solution_value() > 0:
                    assigned_students += 1
                    is_assigned = True
                    print(f"Student {students[i]} assigned to preference set {k}: {preferences[i][k]}")
            if not is_assigned:
                print(f"Student {students[i]} not assigned.")
        print(f"Total students assigned: {assigned_students}")
    else:
        print('No solution found.')

# # Example Data
# students = ["Student 1", "Student 2", "Student 3", "Student 4"]
# courses = [1, 2, 3, 4, 5, 6, 7]
# preferences = [
#     [[2, 3, 6, 7],[1, 2, 4, 5]],  # Preferences for Student 1
#     [[1, 2, 4, 5], [3, 4, 6, 7]],  # Preferences for Student 2
#     [[3, 4, 6, 7], [1, 3, 5, 7]],  # Preferences for Student 3
#     [[1, 3, 5, 7], [2, 3, 6, 7]]   # Preferences for Student 4
# ]
# capacities_hungry = [2, 2, 2, 2, 2, 2, 2]  # Maximum seats per course
# capacities_no_hungry = [3, 3, 3, 3, 3, 3, 3]  # Maximum seats per course