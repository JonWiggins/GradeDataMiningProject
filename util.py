import math

def vectorLength(vector, L=2):
    sum = 0
    for i in range(len(vector)):
        sum += pow(abs(vector[i]), L)

    return pow(sum, 1 / L)

# normalizes the given vector
def normalize(vector, L=2):
    length = vectorLength(vector, L)

    if length == 0:
        return vector
    else:
        return [vector[i] / length for i in range(len(vector))]

def distance(vectorOne, vectorTwo, L=2):
    if len(vectorOne) != len(vectorTwo):
        raise Exception("Dimension Mismatch")

    return pow(sum([pow(abs(vectorOne[i] - vectorTwo[i]), L) for i in range(len(vectorOne))]), 1.0 / L)
    
def getContainingClusterIndex(instructor, clusters):
    for clusterIndex in range(len(clusters)):
        cluster = clusters[clusterIndex]

        if instructor in cluster:
            return clusterIndex

    raise Exception(f"Instructor {instructor.instructorname} was not in the given clusters")

def jaccardSimilarity(setOne, setTwo):
    if len(setOne | setTwo) == 0:
        return 0
    
    return len(setOne & setTwo) / len(setOne | setTwo)

def roundVector(vector, precision):
    return [round(element, precision) for element in vector]

def calculateGPA(gradeVector):
    gradeVector = normalize(gradeVector, 1)

    return 4.0 * gradeVector[0] + 3.0 * gradeVector[1] + 2.0 * gradeVector[2] + gradeVector[3]
