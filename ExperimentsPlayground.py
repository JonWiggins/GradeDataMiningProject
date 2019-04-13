from DataLoader import *
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm




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


def integrateinstructorbypdf(instructors):
    toreturn = {}

    for instructor in instructors:
        remansum = instructor.gradepdf[0] * 4
        remansum += instructor.gradepdf[1] * 3
        remansum += instructor.gradepdf[2] * 2
        remansum += instructor.gradepdf[3] * 1

        toreturn[instructor] = remansum
    return toreturn


def integrateclassbypdf(cumulativeclass):
    remansum = cumulativeclass.l1[0] * 4
    remansum += cumulativeclass.l1[1] * 3
    remansum += cumulativeclass.l1[2] * 2
    remansum += cumulativeclass.l1[3] * 1

    return remansum


def printpremilresults():

    classes = cumulativebycourse()

    print("CourseNum\tGPA\tGrade PDF")
    for number, vals in classes.items():
        print(number, "\t", round(integrateclassbypdf(vals), 2), "\t", [round(x, 3) for x in vals.l1])

    instrucors = getInstructorsWithClasses()
    vals = integrateinstructorbypdf(instrucors)
    print("Instructor\tGPA\tMean Feedback\tGrade PDF\tFeedback PDF")
    for instructor, val in vals.items():
        pdf = [0] * 6
        if not sum(instructor.feedbackvector) == 0:
            pdf = [x / sum(instructor.feedbackvector) for x in instructor.feedbackvector]
        mean = sum([x[0] * x[1] for x in zip(pdf, [5, 4, 3, 2, 1, 0])])
        print(instructor.instructorname, "\t", round(val, 2), "\t", round(mean, 3), "\t",
              [round(x, 3) for x in instructor.gradepdf], "\t", [round(x, 3) for x in pdf])


def gendergapfinder():
    instructors = getInstructorsWithClasses()
    maletotal = 0
    malecount = 0
    femaletotal = 0
    femalecount = 0
    malegrades = [0] * 7
    femalegrades = [0] * 7

    malefeedback = [0] * 6
    femalefeedback = [0] * 6

    for instructor in instructors:
        if instructor.sex == "Male":
            malecount += 1
            maletotal += instructor.pay
            malegrades = [sum(x) for x in zip(malegrades, instructor.gradevector)]
            malefeedback = [sum(x) for x in zip(malefeedback, instructor.feedbackvector)]
        else:
            femalecount += 1
            femaletotal += instructor.pay
            femalegrades = [sum(x) for x in zip(femalegrades, instructor.gradevector)]
            femalefeedback = [sum(x) for x in zip(femalefeedback, instructor.feedbackvector)]

    print("Gender\tCount\tAverage Pay\tGPA\tFeedback PDF\tGrade PDF")
    avgmalegrade = [round(x / sum(malegrades), 2) for x in malegrades]
    avgfemalegrade = [round(x / sum(femalegrades), 2) for x in femalegrades]

    maleGPA = (avgmalegrade[0] * 4) + (avgmalegrade[1] * 3) + (avgmalegrade[2] * 2) + (avgmalegrade[3] * 1)
    femaleGPA = (avgfemalegrade[0] * 4) + (avgfemalegrade[1] * 3) + (avgfemalegrade[2] * 2) + (avgfemalegrade[3] * 1)
    maleGPA = round(maleGPA, 2)
    femaleGPA = round(femaleGPA, 2)

    print("Male\t", malecount, "\t", maletotal/malecount, "\t", maleGPA, "\t",
          [round(x / sum(malefeedback), 3) for x in malefeedback], "\t", avgmalegrade)
    print("Female\t", femalecount, "\t", femaletotal/femalecount, "\t", femaleGPA, "\t",
          [round(x / sum(femalefeedback), 3) for x in femalefeedback], "\t", avgfemalegrade)


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

            for index in range(0, 6):
                titles[title].feedback[index] += instructor.feedbackvector[index]

            titles[title].feedback = [sum(x) for x in zip(titles[title].feedback, instructor.feedbackvector)]

    print("Title\tAverage Pay\tMales\tFemales\tGPA\tFeedback PDF\tGrade PDF")

    for (title, values) in titles.items():
        l1vec = [0] * 7
        if not sum(values.gradevec) == 0:
            l1vec = [round(x / sum(values.gradevec), 3) for x in values.gradevec]
        GPA = (l1vec[0] * 4) + (l1vec[1] * 3) + (l1vec[2] * 2) + (l1vec[3] * 1)
        GPA = round(GPA, 2)
        feedbackdist = [0] * 6
        if not sum(values.feedback) == 0:
            feedbackdist = [round(x / sum(values.feedback), 3) for x in values.feedback]

        print(title, "\t", round(values.wage / (values.malecount + values.femalecount)), "\t", values.malecount, "\t",
              values.femalecount, "\t", round(GPA, 2), "\t", feedbackdist, "\t", l1vec)


def phillipsfinder():
    instructors = getInstructorsWithClasses()

    for instructor in instructors:
        if instructor.instructorname == "PHILLIPS, J.":
            print("Cumu", instructor.gradevector)
            print("L1", instructor.gradepdf)
            print("L2,", instructor.l2gradevector)
            print("Courses Taught", instructor.teachinghistory)
            print("Feedback", instructor.feedbackvector)
            print("L2 Feedback,", instructor.l2feedback)
            return


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
        self.feedback = [0] * 6


def regressiongatherer():
    instructors = integrateinstructorbypdf(getInstructorsWithClasses())
    print("GPA\tMean Review")
    gpas = []
    means = []
    for instructor, gpa in instructors.items():
        pdf = [0] * 6
        if not sum(instructor.feedbackvector) == 0:
            pdf = [x / sum(instructor.feedbackvector) for x in instructor.feedbackvector]
        mean = sum([x[0] * x[1] for x in zip(pdf, [5, 4, 3, 2, 1, 0])])

        if not gpa == 0.0 and not mean == 0.0:
            print(gpa, "\t", mean)
            plt.scatter(gpa, mean, alpha=0.5)
            gpas.append(gpa)
            means.append(mean)
    plt.xlabel("GPA")
    plt.ylabel("Feedback")
    plt.title("GPA vs Feedback Regression")
    x = np.arange(2.3, 4.1, .1)
    y = 2.15 + (x * .4976)
    plt.plot(x, y)
    plt.show()


printpremilresults()

# gendergapfinder()
# titlegapfinder()

# phillipsfinder()
#regressiongatherer()

