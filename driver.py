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


def printClustering(clusters):
    for cluster in clusters:
        print(len(cluster))
        for instructor in cluster:
            print(instructor.instructorname)
            
        print("\n")


def rankSameness(instructors, clusterOne, clusterTwo):
    pairCount = 0
    matchCount = 0
    
    for firstInstructor in instructors:
        firstInstructorClusterOne = None
        for cluster in clusterOne:
            if firstInstructor in cluster:
                firstInstructorClusterOne = cluster
                
        firstInstructorClusterTwo = None
        for cluster in clusterTwo:
            if firstInstructor in cluster:
                firstInstructorClusterTwo = cluster
    
        for secondInstructor in instructors:
            if secondInstructor in firstInstructorClusterOne and secondInstructor in firstInstructorClusterTwo:
                matchCount += 1
            else:
                pairCount += 1
            #elif secondInstructor in firstInstructorClusterOne or secondInstructor in firstInstructorClusterTwo:
            #    pairCount += 1

    totalCount = len(instructors) * len(instructors)
    return pairCount / totalCount, matchCount / totalCount, matchCount / pairCount


# double sided rank same
def rankSamer(instructors, clusterOne, clusterTwo):
    return (rankSame(instructors, clusterOne, clusterTwo) + rankSame(instructors, clusterTwo, clusterOne)) / 2


def rankSame(instructors, clusterOne, clusterTwo):
    total = 0
    
    for cluster in clusterOne:
        matches = {}
        
        for instructor in cluster:
            for index in range(len(clusterTwo)):
                if instructor in clusterTwo[index]:
                    if index in matches:
                        matches[index] += 1
                    else:
                        matches[index] = 1
                        
                    break
                    
        if len(matches) > 0:
            total += max([value for value in matches.values()]) / len(cluster)
        
    return total / len(clusterOne)
                    
        

ints = [-2, -3, -4, 10, 12]
clusterOne = kMeansPP(ints, 2, lambda l, r: abs(l - r))
clusterTwo = kMeansPP(ints, 2, lambda l, r: abs(l / abs(l) - r / abs(r)))

print(clusterOne)
print(clusterTwo)

print(rankSamer(ints, clusterTwo, clusterOne))

 
instructors = getInstructorsWithClasses()
#
print("wage x title", rankSame(instructors, kMeansPP(instructors, 5, wageDistance), kMeansPP(instructors, 5, titleDistance)))
print("wage x grade", rankSame(instructors, kMeansPP(instructors, 5, wageDistance), kMeansPP(instructors, 5, gradeDistance)))
print("wage x sex", rankSame(instructors, kMeansPP(instructors, 3, wageDistance), kMeansPP(instructors, 2, sexDistance)))