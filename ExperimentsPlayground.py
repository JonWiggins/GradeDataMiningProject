from DataLoader import *
import numpy as np


def cumulativebycourse():
    classes = getallclasses()

    toreturn = {}

    for tuple, clas in classes.items():
        if tuple[0] in toreturn:
            toreturn[tuple[0]].a += clas.a
            toreturn[tuple[0]].b += clas.b
            toreturn[tuple[0]].c += clas.c
            toreturn[tuple[0]].d += clas.d
            toreturn[tuple[0]].e += clas.e
            toreturn[tuple[0]].w += clas.w
            toreturn[tuple[0]].other += clas.other
        else:
            toadd = CumulativeClass(tuple[0], clas.a, clas.b, clas.c, clas.d, clas.e, clas.w, clas.other)
            toreturn[tuple[0]] = toadd

    for number, cumclass in toreturn.items():
        total = cumclass.a + cumclass.b + cumclass.c + cumclass.d + cumclass.e + cumclass.w + cumclass.other

        if total == 0:
            cumclass.l1 = [0, 0, 0, 0, 0, 0, 0]
            cumclass.l2 = [0, 0, 0, 0, 0, 0, 0]
            continue

        cumclass.l1 = [cumclass.a / total, cumclass.b / total, cumclass.c / total,
                       cumclass.d / total, cumclass.e / total, cumclass.w / total,
                       cumclass.other / total]

        magnitude = pow(cumclass.a, 2) + pow(cumclass.b, 2) + pow(cumclass.c, 2) + pow(cumclass.d, 2)
        magnitude += pow(cumclass.e, 2) + pow(cumclass.w, 2) + pow(cumclass.other, 2)

        magnitude = np.sqrt(magnitude)

        cumclass.l2 = [cumclass.a / magnitude, cumclass.b / magnitude, cumclass.c / magnitude,
                       cumclass.d / magnitude, cumclass.e / magnitude, cumclass.w / magnitude,
                       cumclass.other / magnitude]

    return toreturn


def cumulativebyinstructor(classes):
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


def integrateinstructorbyl1(instructors):
    toreturn = {}

    for instructor in instructors:
        remansum = instructor.l1gradevector[0] * 4
        remansum += instructor.l1gradevector[1] * 3
        remansum += instructor.l1gradevector[2] * 2
        remansum += instructor.l1gradevector[3] * 1

        toreturn[instructor] = remansum
    return toreturn


def integrateclassbyl1(cumulativeclass):
    remansum = cumulativeclass.l1[0] * 4
    remansum += cumulativeclass.l1[1] * 3
    remansum += cumulativeclass.l1[2] * 2
    remansum += cumulativeclass.l1[3] * 1

    return remansum


def printpremilresults():

    classes = cumulativebycourse()

    print("CourseNum\tIntegral\tAvgVec")
    for number, vals in classes.items():
        print(number, "\t", integrateclassbyl1(vals), "\t", vals.l1)

    instrucors = getInstructorsWithClasses()
    vals = integrateinstructorbyl1(instrucors)
    print("Instructor\tIntegral\tAvgVec")
    for instructor, val in vals.items():
        print(instructor.instructorname, "\t", val, "\t", instructor.l1gradevector)


def gendergapfinder():
    instructors = getInstructorsWithClasses()
    maletotal = 0
    malecount = 0
    femaletotal = 0
    femalecount = 0
    malegrades = [0] * 7
    femalegrades = [0] * 7

    for instructor in instructors:
        if instructor.sex == "Male":
            malecount += 1
            maletotal += instructor.pay
            malegrades = [sum(x) for x in zip(malegrades, instructor.gradevector)]
        else:
            femalecount += 1
            femaletotal += instructor.pay
            femalegrades = [sum(x) for x in zip(femalegrades, instructor.gradevector)]

    print("Gender\tCount\tAverage Pay\tGPA\tL1 Grave Vector")
    avgmalegrade = [x / sum(malegrades) for x in malegrades]
    avgfemalegrade = [x / sum(femalegrades) for x in femalegrades]

    maleGPA = (avgmalegrade[0] * 4) + (avgmalegrade[1] * 3) + (avgmalegrade[2] * 2) + (avgmalegrade[3] * 1)
    femaleGPA = (avgfemalegrade[0] * 4) + (avgfemalegrade[1] * 3) + (avgfemalegrade[2] * 2) + (avgfemalegrade[3] * 1)

    print("Male\t", malecount, "\t", maletotal/malecount, "\t", maleGPA, "\t", avgmalegrade)
    print("Female\t", femalecount, "\t", femaletotal/femalecount, "\t", femaleGPA, "\t", avgfemalegrade)


def titlegapfinder():
    instructors = getInstructorsWithClasses()
    titles = {}

    for instructor in instructors:
        for title in instructor.positions:
            if title in titles:
                titles[title].wage += instructor.pay
                titles[title].gradevec = [sum(x) for x in zip(instructor.gradevector, titles[title].gradevec)]

            else:
                toadd = CumulativeTitle(instructor.pay, instructor.gradevector, 0, 0)
                titles[title] = toadd

            if instructor.sex == "Male":
                titles[title].malecount += 1
            else:
                titles[title].femalecount += 1

    print("Title\tAverage Pay\tMales\tFemales\tGPA\tL1 Grade Vector")

    for (title, values) in titles.items():
        l1vec = [0] * 7
        if not sum(values.gradevec) == 0:
            l1vec = [x / sum(values.gradevec) for x in values.gradevec]
        GPA = (l1vec[0] * 4) + (l1vec[1] * 3) + (l1vec[2] * 2) + (l1vec[3] * 1)
        print(title, "\t", values.wage / (values.malecount + values.femalecount), "\t", values.malecount, "\t",
              values.femalecount, "\t", GPA, "\t", l1vec)


class CumulativeClass:

    def __init__(self, number, a, b, c, d, e, w, other):
        self.number = number
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.w = w
        self.other = other

        self.l1 = []
        self.l2 = []


class CumulativeTitle:
    def __init__(self, wage, gradevec, malecount, femalecount):
        self.wage = wage
        self.gradevec = gradevec
        self.malecount = malecount
        self.femalecount = femalecount


gendergapfinder()
# titlegapfinder()

