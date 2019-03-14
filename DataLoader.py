import re


def getallclasses():
    toreturn = {}
    csvfiles = ["csvfiles/Fall2014.csv", "csvfiles/Fall2015.csv", "csvfiles/Fall2016.csv", "csvfiles/Fall2017.csv",
                "csvfiles/Fall2018.csv", "csvfiles/Spring2015.csv", "csvfiles/Spring2016.csv",
                "csvfiles/Spring2017.csv", "csvfiles/Spring2018.csv"]
    for file in csvfiles:
        toreturn.update(readinfile(file))
    return toreturn


def readinfile(filename):
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

