from constraints import *


def problem(solver):
    a_list = []
    a_list.append(Int("x"))
    a_list.append(Int("y"))
    a_list.append(Int("z"))
    #x_or_y = Not(And([a_list[0], a_list[1], a_list[2]]))
    x_or_y = Sum(a_list)
    solver.add(x_or_y == 0)
    print('done')


def display_schedule(semester):
    schedule = [["Free" for i in range(1, len(week_days) + 1)] for j in range(1, len(time_periods) + 1)]
    with open('solution.txt', 'r') as solution:
        for line in solution.readlines():
            data = line.split(': ')
            var = data[0].split('.')
            if var[0] != semester:
                continue
            course = courses.get(var[1]).split(' ')
            room = rooms.get(var[3]).split(' ')
            schedule[int(var[4]) - 1][int(var[5]) - 1] = "Semester " + course[0] + ' - ' + course[1] + ' [Room ' + room[0] + "] - " + course[2]
    with open('schedule.txt', 'w') as timetable:
        for i in range(0, 5):
            for j in range(0, 9):
                space = " "
                for a in range(0, j):
                    space = space + " "
                timetable.write(space + str(schedule[j][i]) + '\n')


if __name__ == '__main__':
    first = time()
    #s = Solver()
    s = Optimize()
    initialize_all()
    a = time()
    create_variables(s)
    b = time()
    print("Time to create vars: ", b-a, " seconds.")
    a = time()
    teacher_one_at_a_time(s)
    b = time()
    print("Time to teacher constraint: ", b - a, " seconds.")
    a = time()
    only_one_class_per_room(s)
    print('\nonly_one_class_per_room\n')
    same_semester_not_parallel(s)
    print('same_semester_not_parallel\n')
    four_classes_per_week(s)
    print('four_classes_per_week\n')
    same_semester_no_timespaces(s)
    subgroups_same_period(s)
    same_subject_same_room(s)
    soft_ensure_capacity(s)
    print('same_semester_no_timespaces\n')
    b = time()
    print("Time to classes constraint: ", b - a, " seconds.")
    a = time()
    with open('assertions.txt', 'w') as assertions:
        for c in s.assertions():
            assertions.write(str(c) + "\n")
    check = s.check()
    print(check)
    b = time()
    print("Time to check sat: ", b - a, " seconds.")
    with open('solution.txt', 'w') as solution:
        a = time()
        if check == sat:
            model = s.model()
            for le_bool in bools:
                if model.eval(le_bool, model_completion=True) == 1:
                    solution.write(str(le_bool) + ': ' + str(model.eval(le_bool, model_completion=True)) + '\n')
            b = time()
            print("Time to print model: ", b - a, " seconds.")
        last = time()
        print("Time total: ", last - first, " seconds.")
    display_schedule("1")