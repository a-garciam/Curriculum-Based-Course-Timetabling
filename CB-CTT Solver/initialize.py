from z3 import *
from time import time

from collections import Counter
from dictionaries.week_days import *
from dictionaries.courses import *
from dictionaries.rooms import *
from dictionaries.time_periods import *
from dictionaries.teachers import *


curriculumnum = 2
course_list = []
subjects = []
repeated = []
room_list = []
periods_list = []
days_list = []
teacher_list = []
bools = []
var_list = []


def initialize_list(dict1, list1):
    length = len(dict1)
    for x in range(1, length + 1):
        x = str(x)
        list1.append(x)


def initialize_all():
    initialize_list(courses, course_list)
    initialize_list(rooms, room_list)
    initialize_list(time_periods, periods_list)
    initialize_list(week_days, days_list)


def initialize_courses():
    global curriculumnum
    index = 0
    for course in courses:
        data = courses.get(course).split(" ")
        subjects.append(data[1])
        if int(data[0]) > curriculumnum:
            curriculumnum = int(data[0])
        if data[2] in teachers:
            course_list[index] = course_list[index] + '.' + teachers.get(data[2])
            course_list[index] = data[0] + '.' + course_list[index]
        index += 1
    rep_dict = Counter(subjects)
    for element in rep_dict:
        if rep_dict.get(element) == 2:
            repeated.append(element)
        elif rep_dict.get(element) > 2:
            print("In our program, there can't be more than 2 subgroups")


def create_variables(solver):
    initialize_courses()
    for course in course_list:
        for room in room_list:
            for period in periods_list:
                for day in days_list:
                    name = course + '.' + room + '.' + period + '.' + day
                    var_list.append(name)
                    int_obj = Int(name)
                    bools.append(int_obj)
                    solver.add(int_obj >= 0)
