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
    # Constraint 1: Each student is assigned to at most one set of preferred courses
    for i in range(len(students)):
        solver.Add(solver.Sum([x[i, j] for j in range(len(courses))]) == 1)

    # Constraint 2: Each course is assigned to at most one time block
    for j in range(len(courses)):
        solver.Add(solver.Sum([x[i, j] for i in range(len(students))]) <= 1)

    # Constraint 3: Students can only take one course during each time block
    for i in range(len(students)):
        for p in range(len(preferences[i])):
            for q in range(len(preferences[i])):
                if p != q:
                    solver.AddImplication(x[i, preferences[i][p]], x[i, preferences[i][q]].Not())

    # Capacity Constraints
    for j in range(len(courses)):
        solver.Add(solver.Sum([x[i, j] for i in range(len(students))]) <= capacities[j])

    # Solve
    status = solver.Solve()

    # Check if a solution exists
    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        for i in range(len(students)):
            for j in range(len(courses)):
                if x[i, j].solution_value() > 0:
                    print(f"Student {students[i]} assigned to course {courses[j]}")
    else:
        print('No solution found.')


# Example usage:
students = ["Student 1", "Student 2", "Student 3", "Student 4", "Student 5"]
courses = ["Course A", "Course B", "Course C"]
preferences = [[1, 0], [1, 2]], [[0, 2], [0, 1]], [[0, 1], [1, 2]], [[0, 2], [1, 2]], [[0, 1], [0, 2]]
capacities = [2, 2, 2]  # Maximum seats per course

create_course_schedule(students, courses, preferences, capacities)