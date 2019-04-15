import sys, re

from DataLoader import getInstructorsWithClasses
from distances import researchDistance
from Clustering import *

def normalizeString(string):
    string = string.lower()
    string = re.sub(r"[\.,/:\-\";\(\)]", " ", string)
    string = re.sub(r"\s+", " ", string)
    string = string.strip()

    return string

def getMaxDistance(instructor, cluster):
    maxDistance = 0

    for otherInstructor in cluster:
        distance = researchDistance(instructor, otherInstructor)
        
        if distance > maxDistance:
            maxDistance = distance

    return maxDistance

def getRepresentative(cluster):
    representative = None
    representativeDistance = None
    
    for instructor in cluster:
        distance = getMaxDistance(instructor, cluster)

        if representative is None or distance < representativeDistance:
            representative = instructor
            representativeDistance = distance
        
    return representative

def refine(clusters, instructors):
    newCenters = []

    for cluster in clusters:
        newCenters.append(getRepresentative(cluster))

    return centersToSets(newCenters, instructors, researchDistance)

def kgrams(string, k, type="character"):
    data = normalizeString(string)

    if type == "word":
        data = string.split(' ')
 
    grams = set()
    if len(data) < k:
        gram = []
        for i in range(len(data)):
            gram.append(data[i])

        grams.add(tuple(gram))
    else:
        for i in range(len(data) - (k - 1)):
            gram = []
            for j in range(k):
                gram.append(data[i + j])
                
            grams.add(tuple(gram))
                
    return grams

def printClusters(clusters):
    for cluster in clusters:
        representative = getRepresentative(cluster)
        
        for instructor in cluster:
            if instructor == representative:
                print(">>", instructor.instructorname, instructor.researchtext)
            else:
                print(instructor.instructorname, instructor.researchtext)

        print("\n")
    

instructors = getInstructorsWithClasses(silent=True)

clusteringMethods = {
    "gonzales": gonzales,
    "kMeansPP": kMeansPP,
    "hSingleLink": heirarchical_cluster_single_link,
    "hCompleteLink": heirarchical_cluster_complete_link
}

if len(sys.argv) == 1:
    print("Specify clustering method")
elif len(sys.argv) == 2:
    print("Specify cluster count")
elif len(sys.argv) == 3:
    print("Specify gram type")
elif len(sys.argv) == 4:
    print("specify k")
else:
    method = clusteringMethods[sys.argv[1]]
    clusterCount = int(sys.argv[2])
    
    type = sys.argv[3]
    k = int(sys.argv[4])

    # recalculate kgrams
    for instructor in instructors:
        instructor.researchkgram = kgrams(instructor.researchtext, k, type)

    clusters = method(instructors, clusterCount, researchDistance)
        
    print(f'method = {sys.argv[1]}, cluster count = {clusterCount}, type = {type}, k = {k}\n')
    printClusters(clusters)

    while True:
        print("Refine? ", end="")
        response = input()

        if response.lower() == "yes" or response.lower() == "y":
            clusters = refine(clusters, instructors)
            printClusters(clusters)
        else:
            break;
