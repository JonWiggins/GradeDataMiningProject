from DataLoader import *
from util import *


def sortByGrades():
    instructors = getInstructorsWithClasses()

    instructors.sort(key=lambda instructor: cdfDistance(instructor.gradevector, [1, 0, 0, 0, 0, 0, 0]))

    for rank in range(len(instructors)):
        print((rank + 1), instructors[rank].instructorname, instructors[rank].gradevector)


sortByGrades()
