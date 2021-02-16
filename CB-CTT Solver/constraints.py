from initialize import *


def sum_teachers(a_list, solver, input):
    solver.add(Sum(a_list) == input)


def sum_soft(a_list, solver, input):
    solver.add_soft(Sum(a_list) == input)


def sum_rooms(a_list, solver):
    solver.add(Sum(a_list) <= 1)


def teacher_one_at_a_time(solver):
    for i in range(1, len(teachers) + 1):
        for j in range(1, len(time_periods) + 1):
            for k in range(1, len(week_days) + 1):
                xor_list = []
                for m in range(1, len(courses) + 1):
                    data = courses.get(str(m)).split(" ")
                    s = data[0]
                    if data[2] != list(teachers.keys())[list(teachers.values()).index(str(i))]:
                        continue
                    for l in range(1, len(rooms) + 1):
                        var = str(s) + '.' + str(m) + '.' + str(i) + '.' + str(l) + '.' + str(j) + '.' + str(k)
                        pos = var_list.index(var)
                        xor_list.append(bools[pos])
                sum_rooms(xor_list, solver)


def only_one_class_per_room(solver):
    for i in range(1, len(rooms) + 1):
        for j in range(1, len(week_days) + 1):
            for k in range(1, len(time_periods) + 1):
                xor_list = []
                for m in range(1, len(courses) + 1):
                    data = courses.get(str(m)).split(" ")
                    s = data[0]
                    for l in range(1, len(teachers) + 1):
                        if data[2] != list(teachers.keys())[list(teachers.values()).index(str(l))]:
                            continue
                        var = str(s) + '.' + str(m) + '.' + str(l) + '.' + str(i) + '.' + str(k) + '.' + str(j)
                        pos = var_list.index(var)
                        xor_list.append(bools[pos])
                sum_rooms(xor_list, solver)


def same_semester_not_parallel(solver):
    for s in range(1, curriculumnum + 1):
        for j in range(1, len(week_days) + 1):
            for k in range(1, len(time_periods) + 1):
                xor_list = []
                for i in range(1, len(courses) + 1):
                    data = courses.get(str(i)).split(" ")
                    if data[0] != str(s):
                        continue
                    for m in range(1, len(rooms) + 1):
                        for l in range(1, len(teachers) + 1):
                            if data[2] != list(teachers.keys())[list(teachers.values()).index(str(l))]:
                                continue
                            var = str(s) + '.' + str(i) + '.' + str(l) + '.' + str(m) + '.' + str(k) + '.' + str(j)
                            pos = var_list.index(var)
                            xor_list.append(bools[pos])
                    sum_rooms(xor_list, solver)


def four_classes_per_week(solver):
    for i in range(1, len(courses) + 1):
        data = courses.get(str(i)).split(" ")
        s = data[0]
        xor_list = []
        for j in range(1, len(week_days) + 1):
            for k in range(1, len(time_periods) + 1):
                for m in range(1, len(rooms) + 1):
                    for l in range(1, len(teachers) + 1):
                        if data[2] != list(teachers.keys())[list(teachers.values()).index(str(l))]:
                            continue
                        var = s + '.' + str(i) + '.' + str(l) + '.' + str(m) + '.' + str(k) + '.' + str(j)
                        pos = var_list.index(var)
                        xor_list.append(bools[pos])
        sum_teachers(xor_list, solver, 4)


def soft_ensure_capacity(solver):
    for j in range(1, len(week_days) + 1):
        for k in range(1, len(time_periods) + 1):
            for i in range(1, len(courses) + 1):
                data = courses.get(str(i)).split(" ")
                s = data[0]
                for m in range(1, len(rooms) + 1):
                    room_data = rooms.get(str(m)).split(" ")
                    if int(room_data[1]) >= int(data[3]):
                        continue
                    xor_list = []
                    for l in range(1, len(teachers) + 1):
                        if data[2] != list(teachers.keys())[list(teachers.values()).index(str(l))]:
                            continue
                        var = str(s) + '.' + str(i) + '.' + str(l) + '.' + str(m) + '.' + str(k) + '.' + str(j)
                        pos = var_list.index(var)
                        xor_list.append(bools[pos])
                    sum_soft(xor_list, solver, 0)


def same_semester_no_timespaces(solver):
    for s in range(1, curriculumnum + 1):
        for j in range(1, len(week_days) + 1):
            for k in range(1, len(time_periods)):
                counter = k
                xor_list = []
                for i in range(1, len(courses) + 1):
                    data = courses.get(str(i)).split(" ")
                    if data[0] != str(s):
                        continue
                    for m in range(1, len(rooms) + 1):
                        for l in range(1, len(teachers) + 1):
                            if data[2] != list(teachers.keys())[list(teachers.values()).index(str(l))]:
                                continue
                            var = str(s) + '.' + str(i) + '.' + str(l) + '.' + str(m) + '.' + str(counter) + '.' + str(j)
                            if counter == k:
                                counter = k + 1
                            pos = var_list.index(var)
                            xor_list.append(bools[pos])
                sum_soft(xor_list, solver, 2)


def subgroups_same_period(solver):
    for j in range(1, len(week_days) + 1):
        for k in range(1, len(time_periods) + 1):
            xor_list = []
            for m in range(1, len(courses) + 1):
                data = courses.get(str(m)).split(" ")
                if data[1] not in repeated:
                    continue
                s = data[0]
                for i in range(1, len(rooms) + 1):
                    for l in range(1, len(teachers) + 1):
                        if data[2] != list(teachers.keys())[list(teachers.values()).index(str(l))]:
                            continue
                        var = str(s) + '.' + str(m) + '.' + str(l) + '.' + str(i) + '.' + str(k) + '.' + str(j)
                        pos = var_list.index(var)
                        xor_list.append(bools[pos])
            sum_soft(xor_list, solver, 2)


def same_subject_same_room(solver):
    for i in range(1, len(courses) + 1):
        data = courses.get(str(i)).split(" ")
        s = data[0]
        for m in range(1, len(rooms) + 1):
            xor_list = []
            for l in range(1, len(teachers) + 1):
                if data[2] != list(teachers.keys())[list(teachers.values()).index(str(l))]:
                    continue
                for j in range(1, len(week_days) + 1):
                    for k in range(1, len(time_periods) + 1):
                        var = str(s) + '.' + str(i) + '.' + str(l) + '.' + str(m) + '.' + str(k) + '.' + str(j)
                        pos = var_list.index(var)
                        xor_list.append(bools[pos])
            sum_soft(xor_list, solver, 4)