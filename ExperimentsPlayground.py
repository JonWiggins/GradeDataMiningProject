from DataLoader import *
import numpy as np


def averagebycoursenumber(classes):
    toreturn = {}

    for instance in classes.values():
        if instance.number in toreturn:
            toreturn[instance.number][0] += instance.a
            toreturn[instance.number][1] += instance.b
            toreturn[instance.number][2] += instance.c
            toreturn[instance.number][3] += instance.d
            toreturn[instance.number][4] += instance.e
            toreturn[instance.number][5] += instance.w
            toreturn[instance.number][6] += instance.other
        else:
            toadd = [instance.a, instance.b, instance.c,
                     instance.d, instance.e, instance.w, instance.other]
            toreturn[instance.number] = toadd

    return toreturn


def averagebyinstructor(classes):
    toreturn = {}

    for instance in classes.values():
        for prof in instance.instructors:
            if prof in toreturn:
                toreturn[prof][0] += instance.a
                toreturn[prof][1] += instance.b
                toreturn[prof][2] += instance.c
                toreturn[prof][3] += instance.d
                toreturn[prof][4] += instance.e
                toreturn[prof][5] += instance.w
                toreturn[prof][6] += instance.other
            else:
                toadd = [instance.a, instance.b, instance.c,
                         instance.d, instance.e, instance.w, instance.other]
                toreturn[prof] = toadd
    return toreturn


def dicttounitvec(classes):
    toreturn = {}

    for instance in classes.items():
        magnitude = 0
        for val in instance[1]:
            magnitude += np.power(val, 2)
        magnitude = np.sqrt(magnitude)
        if magnitude == 0:
            newvec = [0 for e in instance[1]]
        else:
            newvec = [e / magnitude for e in instance[1]]
        toreturn[instance[0]] = newvec
    return toreturn


def distance(first, second):
    magnitude = 0
    for index in range(0, len(first)):
        magnitude += np.power(first[index] - second[index], 2)
    return np.sqrt(magnitude)


def printpremilresults():
    allclasses = getallclasses()
    avgs = averagebycoursenumber(allclasses)
    ideal = ("Ideal", [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    units = dicttounitvec(avgs)
    print("CourseNum\tDistanceFromIdeal\tAvgVec")
    for u in units.items():
        print(u[0] + "\t" + str(distance(u[1], ideal[1])) + "\t" + str(u[1]))

    avgperson = averagebyinstructor(allclasses)

    units = dicttounitvec(avgperson)
    print("Instructor\tDistanceFromIdeal\tAvgVec")
    for u in units.items():
        print(u[0] + "\t" + str(distance(u[1], ideal[1])) + "\t" + str(u[1]))


def wagegapfinder():
    instructors = getallinstructors()
    maletotal = 0
    malecount = 0
    femaletotal = 0
    femalecount = 0

    for instructor in instructors:
        if instructor.sex == "Male":
            malecount += 1
            maletotal += instructor.pay
        else:
            femalecount += 1
            femaletotal += instructor.pay

    print("Male Average Pay: " + str(maletotal / malecount) + " Female Average Pay: " + str(femaletotal / femalecount))


wagegapfinder()

