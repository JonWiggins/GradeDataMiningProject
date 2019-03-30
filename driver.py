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
def rankSamer(clusterOne, clusterTwo):
    return (rankSame(clusterOne, clusterTwo) + rankSame(clusterTwo, clusterOne)) / 2


def rankSame(clusterOne, clusterTwo):
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


def jshat(clustering1, clustering2):
    similaratities = []

    if len(clustering1) > len(clustering2):
        for cluster1 in clustering1:
            max = 0
            for cluster2 in clustering2:
                js = jaccardSimilarity(cluster1, cluster2)
                if js > max:
                    max = js
            similaratities.append(max)
    else:
        for cluster1 in clustering2:
            max = 0
            for cluster2 in clustering1:
                js = jaccardSimilarity(cluster1, cluster2)
                if js > max:
                    max = js
            similaratities.append(max)

    return sum(similaratities) / len(similaratities)
    # return similaratities


def purity(clustering1, clustering2):
    summation = 0

    # TODO investigate looping c1 vs c2
    for cluster in clustering1:
        highest = 0
        for comparer in clustering2:
            next = len(cluster.intersection(comparer))
            if next > highest:
                highest = next

        summation += highest

    # find total number of data points
    N = sum(len(cluster) for cluster in clustering1)

    return summation / N


def fowlkesmallowsindex(clustering1, clustering2, instructors):
    # TP = the number of points that are present in the same cluster in both clusterings
    # FP = the number of points that are present in the same cluster in clustering1 but not clustering2
    # FN = the number of points that are present in the same cluster in clustering2 but not clustering1
    # TN = the number of points that are in different clusters in both clusterings
    TP = 0
    FP = 0
    FN = 0
    TN = 0

    for firstinstructor in instructors:
        firstinstructorclusterone = None
        for cluster in clustering1:
            if firstinstructor in cluster:
                firstinstructorclusterone = cluster

        firstinstructorclustertwo = None
        for cluster in clustering2:
            if firstinstructor in cluster:
                firstinstructorclustertwo = cluster

        for secondinstructor in instructors:
            secondinstructorclusterone = None
            for cluster in clustering1:
                if secondinstructor in cluster:
                    secondinstructorclusterone = cluster
            secondinstructorclustertwo = None
            for cluster in clustering2:
                if secondinstructor in cluster:
                    secondinstructorclustertwo = cluster

            if firstinstructorclusterone == secondinstructorclusterone and firstinstructorclustertwo == secondinstructorclustertwo:
                TP += 1
            elif firstinstructorclusterone == secondinstructorclusterone and not firstinstructorclustertwo == secondinstructorclustertwo:
                FP += 1
            elif not firstinstructorclusterone == secondinstructorclusterone and firstinstructorclustertwo == secondinstructorclustertwo:
                FN += 1
            elif not firstinstructorclusterone == secondinstructorclusterone and not firstinstructorclustertwo == secondinstructorclustertwo:
                TN += 1

    if TP + FP == 0 or TP + FN == 0:
        return 0
    
    fpterm = TP / (TP + FP)
    fnterm = TP / (TP + FN)

    FM = np.sqrt(fpterm * fnterm)

    return FM


def testclusterings(minsize, maxsize):
    print("Cluster1 Metric\tCluster1 Size\tCluster2 Metric\tCluster2 Size\tJSHat\tPurity\tFowlkes-Mallows Index")
    instructors = getInstructorsWithClasses()

    for size in range(minsize, maxsize):
        gradeclusters = kMeansPP(instructors, size, gradeDistance)
        genderclusters = kMeansPP(instructors, 2, sexDistance)  # There are only two genders?
        titleclusters = kMeansPP(instructors, size, titleDistance)
        wageclusters = kMeansPP(instructors, size, wageDistance)

        print("Gender\t", 2, "\tGrade\t", size, "\t",
              jshat(genderclusters, gradeclusters), "\t", purity(genderclusters, gradeclusters),
              "\t", fowlkesmallowsindex(genderclusters, gradeclusters, instructors))

        print("Gender\t", 2, "\tTitle\t", size, "\t",
              jshat(genderclusters, titleclusters), "\t", purity(genderclusters, titleclusters),
              "\t", fowlkesmallowsindex(genderclusters, titleclusters, instructors))

        print("Gender\t", 2, "\tWage\t", size, "\t",
              jshat(genderclusters, wageclusters), "\t", purity(genderclusters, wageclusters),
              "\t", fowlkesmallowsindex(genderclusters, wageclusters, instructors))

        print("Grade\t", size, "\tTitle\t", size, "\t",
              jshat(gradeclusters, titleclusters), "\t", purity(gradeclusters, titleclusters),
              "\t", fowlkesmallowsindex(gradeclusters, titleclusters, instructors))

        print("Grade\t", size, "\tWage\t", size, "\t",
              jshat(gradeclusters, wageclusters), "\t", purity(gradeclusters, wageclusters),
              "\t", fowlkesmallowsindex(gradeclusters, wageclusters, instructors))

        print("Wage\t", size, "\tTitle\t", size, "\t",
              jshat(wageclusters, titleclusters), "\t", purity(wageclusters, titleclusters),
              "\t", fowlkesmallowsindex(wageclusters, titleclusters, instructors))


testclusterings(2, 8)


