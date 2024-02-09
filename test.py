from ortools.sat.python import cp_model

model = cp_model.CpModel()

num_courses = 40
num_students = 200
num_courses_per_day = 4  # Excluding lunch block
num_days = 5
num_preferences_each = 4

# create class/structs for the data
# need student struct, preference struct, result struct