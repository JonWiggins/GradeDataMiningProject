import math
from util import *

def euclidianDistance(vectorOne, vectorTwo):
    if len(vectorOne) != len(vectorTwo):
        raise Exception("Dimension Mismatch")

    return math.sqrt(sum([pow(vectorOne[index] - vectorTwo[index], 2) for index in range(len(vectorOne))]))

def cdfDistance(vectorOne, vectorTwo):
    if len(vectorOne) != len(vectorTwo):
        raise Exception("Dimension Mismatch")

    vectorOne = normalize(vectorOne, 1)
    vectorTwo = normalize(vectorTwo, 1)
    
    sumOne = 0
    sumTwo = 0

    distance = 0

    for i in range(len(vectorOne)):
        sumOne += vectorOne[i]
        sumTwo += vectorTwo[i]

        distance += abs(sumOne - sumTwo)

    return distance


def sexDistance(instructorOne, instructorTwo):
    return 0 if instructorOne.sex == instructorTwo.sex else 1

# the primary distance function for grades
def gradeDistance(instructorOne, instructorTwo):
    return gradeDistanceCDF(instructorOne, instructorTwo)

def gradeDistanceGPA(instructorOne, instructorTwo):
    return abs(calculateGPA(instructorOne.gradevector) - calculateGPA(instructorTwo.gradevector))

def gradeDistanceL1(instructorOne, instructorTwo):
    pass

def gradeDistanceCDF(instructorOne, instructorTwo):
    return cdfDistance(instructorOne.gradevector, instructorTwo.gradevector)


def wageDistance(instructorOne, instructorTwo):
    return euclidianDistance(instructorOne.wagevec, instructorTwo.wagevec)


def feedbackDistance(instructorOne, instructorTwo):
    return euclidianDistance(instructorOne.l2feedback, instructorTwo.l2feedback)


def titleDistance(instructorOne, instructorTwo):
    return 1 - jaccardSimilarity(instructorOne.positions, instructorTwo.positions)


def researchDistance(instructorOne, instructorTwo):
    return 1 - jaccardSimilarity(instructorOne.researchkgram, instructorTwo.researchkgram)
