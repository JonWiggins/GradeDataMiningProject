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


def jaccardSimilarity(setOne, setTwo):
    if len(setOne | setTwo) == 0:
        return 0
    return len(setOne & setTwo) / len(setOne | setTwo)


# Distance functions
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
