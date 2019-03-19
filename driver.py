from DataLoader import *
from kMeansPP import *

def euclidianDistance(vectorOne, vectorTwo):
    if len(vectorOne) != len(vectorTwo):
        raise Exception("Dimension Mismatch")

    return math.sqrt(sum([pow(vectorOne[index] - vectorTwo[index], 2) for index in range(len(vectorOne))]))

    
def sexDistance(iOne, iTwo):
    return 0 if iOne.sex == iTwo.sex else 1
    
def gradeDistance(instructorOne, instructorTwo):
    return euclidianDistance(instructorOne.gradevector, instructorTwo.gradevector)

instructors = getInstructorsWithClasses()
clusters = kMeansPP(instructors, 5, gradeDistance)

for cluster in clusters:
    print(len(cluster))
    for instructor in cluster:
        print(instructor.instructorname, instructor.gradevector)
        
    print("\n")