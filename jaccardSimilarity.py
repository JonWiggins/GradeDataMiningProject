def jaccardSimilarity(setOne, setTwo):
    if len(setOne | setTwo) == 0:
        return 0
    return len(setOne & setTwo) / len(setOne | setTwo)

