from ortools.linear_solver import pywraplp

def create_course_schedule(students, courses, preferences, sections, section_capacity):
    total_blocks = 20  # 5 days * total_blocks blocks/day
    M=50 # Big M parameter value, larger than maximum course possible but keep away from INT MAX
    # Initialize the solver
    solver = pywraplp.Solver.CreateSolver('SAT')

    # Variables
    # Student Preference Assignment
    x = {}
    for i in range(len(students)):
        for k in range(len(preferences[i])):
            x[i, k] = solver.BoolVar(f'x[{i},{k}]')

    # Student-Section Assignment
    y = {}
    for i in range(len(students)):  # Iterate over each student
        for c in range(len(courses)):  # Iterate over each course
            for s in range(sections[c]):  # Iterate over each section of the course
                for t in range(total_blocks):
                # Create a Boolean variable for each student-course-section combination
                    y[i, c, s,t] = solver.BoolVar(f'y[{i},{c},{s}]')

    # course section time block assignment
    z = {}
    for c in range(len(courses)):
        for s in range(sections[c]):
            for t in range(total_blocks):
                z[c, s, t] = solver.BoolVar(f'z[{c},{s},{t}]')

                
    # Align the course section time block assignment variables with the student-section-time assignment variables
    for i in range(len(students)):  # Iterate over each student
        for c in range(len(courses)):  # Iterate over each course
            for s in range(sections[c]):  # Iterate over each section of the course
                for t in range(total_blocks):  # Iterate over each time block
                    # Add a constraint that if a student is assigned to a course section at a time block,
                    # then that course section must be scheduled at that time block
                    solver.Add(y[i, c, s, t] <= z[c, s, t])

    # Each section of courses is assigned to at most one time block
    for c in range(len(courses)):
        for s in range(sections[c]):
            # Ensure each section is assigned to at most one time block
            solver.Add(sum(z[c, s, t] for t in range(total_blocks)) <= 1)
    
    # No multiple section of a same course can be assigned to the same time block
    for i in range(len(courses)):
        for t in range(total_blocks):
            section_sum = []
            for j in range(sections[i]):
                section_sum.append(z[i, j, t])
            solver.Add(solver.Sum(section_sum) <= 1)

    # Course capacities
    for i in range(len(courses)):
        for t in range(sections[i]):
            student_sum = [y[j, i, t, c] for c in range(total_blocks) for j in range(len(students))]
            solver.Add(solver.Sum(student_sum) <= section_capacity[i])
         
   
    
    # Each student is assigned to at most one set of preferred courses
    for i in range(len(students)):
        solver.Add(solver.Sum(x[i, k] for k in range(len(preferences[i]))) <= 1)

    # Students can only take one course during each time block
    for i in range(len(students)):  # Iterate over each student
        for t in range(total_blocks):  # Iterate over each time block
            # Add a constraint that sums all y[i, c, s, t] for student i at time t across all courses and sections
            # The sum should be less than or equal to 1, ensuring only one course per time block
            solver.Add(solver.Sum(y[i, c-1, s, t] for c in courses for s in range(sections[c-1])) <= 1)

    # Align the student-section-time assignment variables with the student-preference assignment variables
    for i in range(len(students)):  # Iterate over each student
        for k in range(len(preferences[i])):  # Iterate over each preference set for student i
            total_courses = [y[i, c, s, t] for c in range(len(courses)) for s in range(sections[c]) for t in range(total_blocks)]

            # Use big M method to introduce a constraint
            # If x[i,k]=1, we force the sum of total courses of this student to the length of the preference set
            # Otherwise we introduce a loose bound that's equivalent to no constraint.
            solver.Add(solver.Sum(total_courses) <=len(preferences[i][k])+M*(1-x[i,k]))
            solver.Add(solver.Sum(total_courses) >=len(preferences[i][k])-M*(1-x[i,k]))
            for c in preferences[i][k]:  # Iterate over each course in the k-th preference set
                # Create a list to hold the section-time assignment variables for course c
                section_time_assignments = [y[i, c-1, s, t] for s in range(sections[c-1]) for t in range(total_blocks)]

                # Add a constraint that ensures the sum of section-time assignments for course c is equal to x[i, k]
                # This means if x[i, k] = 1 (preference set k is selected), exactly one section-time assignment must be selected for course c
                # If x[i, k] = 0, no section-time assignment should be selected for course c


                # Ensures a universal upper bound
                solver.Add(solver.Sum(section_time_assignments) <= 1)

                # Constraint ensuring that if x[i, k] = 1, then one section_time_assignment must be selected, otherwise no constraint
                solver.Add(solver.Sum(section_time_assignments) >= x[i, k])

    for i in range(len(students)):
        solver.Add(solver.Sum(y[i, c, s, t] for c in range(len(courses)) for s in range(sections[c]) for t in range(total_blocks)) == len(preferences[i]))

    # Objective
    # Maximize the total number of students attending their first or second preferred set of courses
    solver.Maximize(solver.Sum([x[i, k] for i in range(len(students)) for k in range(1)]))
    
    # Solve
    status = solver.Solve()

    schedule = {}

    if status == pywraplp.Solver.OPTIMAL:
        print("Solver status:", status)
        print('Solution:')
        for i in range(len(students)):  # Iterate over each student
            student_schedule = []
            for c in range(len(courses)):  # Iterate over each course
                for s in range(sections[c]):  # Iterate over each section of the course
                    for t in range(total_blocks):  # Iterate over each time block
                        if y[i, c, s, t].solution_value() > 0:
                            print(f"Student {i} attends course {c+1} assigned to section {s+1} at time block {t+1}")
                            student_schedule.append({
                                'course': c+1,
                                'section': s+1,
                                'time_block': t+1
                            })
            schedule[students[i]] = student_schedule
        for i in range(len(students)):
            for k in range(len(preferences[i])):
                if x[i, k].solution_value() > 0:
                    print(f"Student {students[i]} assigned to preference set {k+1}: {preferences[i][k]}")
        for c in range(len(courses)):
            for s in range(sections[c]):
                for t in range(total_blocks):
                    if z[c, s, t].solution_value() > 0:
                        print(f"Course {c+1} section {s+1} assigned at time block {t+1}")
    else:
        print("Solver status:", status)
        print('No solution found.')
    
    return {
        'status': 'OPTIMAL' if status == pywraplp.Solver.OPTIMAL else 'NOT OPTIMAL',
        'schedule': schedule
    }

# Example data setup
students = ["Student 1", "Student 2", "Student 3", "Student 4"]
courses = [1, 2, 3, 4, 5, 6, 7]
preferences = [
    [[2, 3, 6, 7], [1, 4, 5, 6], [2, 4, 6, 7], [1, 3, 5, 7]],  # Preferences for Student 1
    [[1, 2, 3, 4], [2, 3, 5, 6], [1, 4, 6, 7], [3, 5, 6, 7]],  # Preferences for Student 2
    [[1, 2, 3, 4], [2, 3, 5, 6], [1, 4, 6, 7], [3, 5, 6, 7]], 
    [[1, 2, 3, 4], [2, 3, 5, 6], [1, 4, 6, 7], [3, 5, 6, 7]]
]

sections = [2, 3, 2, 2, 3, 2, 2]  # Number of sections for each course
section_capacity = [3, 3, 3, 3, 3, 3, 3]  # Capacity for each section of each course

create_course_schedule(students, courses, preferences, sections, section_capacity)