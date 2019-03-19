from DataLoader import *
from kMeansPP import *
from jaccardSimilarity import *

def euclidianDistance(vectorOne, vectorTwo):
    if len(vectorOne) != len(vectorTwo):
        raise Exception("Dimension Mismatch")

    return math.sqrt(sum([pow(vectorOne[index] - vectorTwo[index], 2) for index in range(len(vectorOne))]))

    
def sexDistance(iOne, iTwo):
    return 0 if iOne.sex == iTwo.sex else 1
    
def gradeDistance(instructorOne, instructorTwo):
    return euclidianDistance(instructorOne.gradevector, instructorTwo.gradevector)

def wageDistance(instructorOne, instructorTwo):
    return euclidianDistance(instructorOne.wagevec, instructorTwo.wagevec)
    
def titleDistance(instructorOne, instructorTwo):
    return 1 - jaccardSimilarity(instructorOne.positions, instructorTwo.positions)
    
instructors = getInstructorsWithClasses()
clusters = kMeansPP(instructors, 20, wageDistance)

for cluster in clusters:
    print(len(cluster))
    for instructor in cluster:
        print(instructor.instructorname, instructor.wagevec)
        
    print("\n")