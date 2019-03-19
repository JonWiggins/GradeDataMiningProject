import re
import math


def getallclasses():
    toreturn = {}
    csvfiles = ["csvfiles/Fall2014.csv", "csvfiles/Fall2015.csv", "csvfiles/Fall2016.csv", "csvfiles/Fall2017.csv",
                "csvfiles/Fall2018.csv", "csvfiles/Spring2015.csv", "csvfiles/Spring2016.csv",
                "csvfiles/Spring2017.csv", "csvfiles/Spring2018.csv"]
    for file in csvfiles:
        toreturn.update(readinclassfile(file))
    return toreturn


def getallinstructors():
    toreturn = []

    file = open("csvfiles/FacultyInformation.csv")

    for line in file:
        regex = \
            r"^\"(.{2,50}),(.{2,50})\",\"(.{2,50})\",(.{5,50}),(Male|Female),(\"\d+,\d+\"|\d+),(\"\d+,\d+\"|\d+),(\"\d+,\d+\"|\d+),(.*)$"
        match = re.match(regex, line)
        if match:
            # 1. Last 2. First 3. Intname 4. Title 5. Gender 6. Salary 7. Benifits 8. Leave 9. Intrests
            toreturn.append(Instructor(match.group(2), match.group(1), match.group(3), match.group(4), match.group(5),
                                       match.group(6), match.group(7), match.group(8), match.group(9)))
    return toreturn


def getInstructorsWithClasses():
    toreturn = getallinstructors()


    #fill vectors

    for toadd in getallclasses():
        for instructor in toreturn:
            if instructor.instructorname in toadd.instructors:
                instructor.gradevector[0] += toadd.a
                instructor.gradevector[1] += toadd.b
                instructor.gradevector[2] += toadd.c
                instructor.gradevector[3] += toadd.d
                instructor.gradevector[4] += toadd.e
                instructor.gradevector[5] += toadd.w
                instructor.gradevector[6] += toadd.other

    # make them into unit vectors
    for instructor in toreturn:
        magnitude = 0
        for g in instructor.gradevector:
            magnitude += pow(g, 2)
        magnitude = math.sqrt(magnitude)

        for index in range(0, len(instructor.gradevector)):
            instructor.gradevector[index] = instructor.gradevector[index] / magnitude

    return toreturn


def readinclassfile(filename):
    toreturn = {}

    file = open(filename)

    for line in file:
        regex = r"^(\d+),\d+-\d+,(\w+),(\d+),.+,(\d+),(\w\d{4}),\"(.+)\"$"
        match = re.match(regex, line)
        if match:
            # 1: Class number 2: Grade 3: Section 4: Count 5: Semester 6: Instructors
            nexttuple = (match.group(1), match.group(3), match.group(5))
            if nexttuple in toreturn:

                if match.group(2) == "A":
                    toreturn[nexttuple].a += int(match.group(4))
                elif match.group(2) == "B":
                    toreturn[nexttuple].b += int(match.group(4))
                elif match.group(2) == "C":
                    toreturn[nexttuple].c += int(match.group(4))
                elif match.group(2) == "D":
                    toreturn[nexttuple].d += int(match.group(4))
                elif match.group(2) == "E":
                    toreturn[nexttuple].e += int(match.group(4))
                elif match.group(2) == "W":
                    toreturn[nexttuple].w += int(match.group(4))
                else:
                    toreturn[nexttuple].other += int(match.group(4))

            else:
                toadd = Class(match.group(1), match.group(3), match.group(5), match.group(6))
                toreturn[nexttuple] = toadd

    return toreturn


class Class:
    # ^ XD

    def __init__(self, number, section, semester, instructors):
        self.number = number
        self.semester = semester
        self.section = section
        self.instructors = self.getinstructors(instructors)
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.w = 0
        self.other = 0

    def getinstructors(self, instructors):
        return instructors.split(" AND ")


class Instructor:

    def __init__(self, first, last, intname, title, sex, salary, benifits, leave, researchinterests):
        self.first = first
        self.last = last
        self.instructorname = intname
        self.positions = set(self.getpositions(title))
        self.sex = sex

        self.salary = int(salary.replace("\"", "").replace("\'", "").replace(",", ""))
        self.benifits = int(benifits.replace("\"", "").replace("\'", "").replace(",", ""))
        self.leave = int(leave.replace("\"", "").replace("\'", "").replace(",", ""))

        self.wagevec = [self.salary, self.benifits, self.leave]

        self.pay = self.salary + self.benifits + self.leave
        self.researchtext = researchinterests
        self.classes = []

        self.gradevector = []

    def getpositions(self, title):
        return title.split(" AND ")
