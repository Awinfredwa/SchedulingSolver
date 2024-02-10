from ortools.linear_solver import pywraplp

def create_course_schedule(students, courses, preferences, capacities):
    # Create the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    # x[i, j] is an array of binary variables, which will be 1 if student i is assigned to course j.
    x = {}
    for i in range(len(students)):
        for j in range(len(courses)):
            x[i, j] = solver.BoolVar(f'x[{i},{j}]')

    # Constraints
    # Each student is assigned to at most one course
    for i in range(len(students)):
        solver.Add(solver.Sum([x[i, j] for j in range(len(courses))]) <= 1)

    # The number of students in each course does not exceed its capacity
    for j in range(len(courses)):
        solver.Add(solver.Sum([x[i, j] for i in range(len(students))]) <= capacities[j])

    # Objective
    # Maximize the total number of students attending their preferred courses
    solver.Maximize(solver.Sum([x[i, j] * preferences[i][j] for i in range(len(students)) for j in range(len(courses))]))

    # Solve
    status = solver.Solve()

    # Check if a solution exists
    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        for i in range(len(students)):
            for j in range(len(courses)):
                if x[i, j].solution_value() > 0:
                    print(f"Student {i} assigned to course {j}")
    else:
        print('No solution found.')

# Example Data
students = ["Student 1", "Student 2", "Student 3"]
courses = ["Course A", "Course B", "Course C"]
preferences = [[1, 0, 0], [0, 1, 0], [1, 1, 0]]  # Simplified preference matrix (1 for preferred, 0 for not preferred)
capacities = [2, 2, 2]  # Maximum seats per course

# Create the course schedule
create_course_schedule(students, courses, preferences, capacities)
