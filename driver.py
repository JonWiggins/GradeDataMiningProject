from DataLoader import *
from Clustering import *
from util import *
from distances import *


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

    if len(similaratities) == 0:
        return 0

    return round(sum(similaratities) / len(similaratities), 3)
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

    if N == 0:
        return 0

    return round(summation / N, 3)


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

            if firstinstructorclusterone == secondinstructorclusterone \
                    and firstinstructorclustertwo == secondinstructorclustertwo:
                TP += 1
            elif firstinstructorclusterone == secondinstructorclusterone \
                    and not firstinstructorclustertwo == secondinstructorclustertwo:
                FP += 1
            elif not firstinstructorclusterone == secondinstructorclusterone \
                    and firstinstructorclustertwo == secondinstructorclustertwo:
                FN += 1
            elif not firstinstructorclusterone == secondinstructorclusterone \
                    and not firstinstructorclustertwo == secondinstructorclustertwo:
                TN += 1

    if TP + FP == 0 or TP + FN == 0:
        return 0

    fpterm = TP / (TP + FP)
    fnterm = TP / (TP + FN)

    FM = np.sqrt(fpterm * fnterm)

    return round(FM, 3)


def testclusterings(clustername, clustermethod, minsize, maxsize):
    print(clustername)
    print("Cluster1 Metric\tCluster1 Size\tCluster2 Metric\tCluster2 Size\tJSHat\tPurity\tFowlkes-Mallows Index")
    instructors = getInstructorsWithClasses()

    for size in range(minsize, maxsize):
        gradeclusters = clustermethod(instructors, size, gradeDistance)
        genderclusters = clustermethod(instructors, 2, sexDistance)  # There are only two genders?
        titleclusters = clustermethod(instructors, size, titleDistance)
        wageclusters = clustermethod(instructors, size, wageDistance)
        researchclusters = clustermethod(instructors, size, researchDistance)
        feedbackclusters = clustermethod(instructors, size, feedbackDistance)

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

        print("Research\t", size, "\tGender\t", 2, "\t",
              jshat(researchclusters, genderclusters), "\t", purity(researchclusters, genderclusters),
              "\t", fowlkesmallowsindex(researchclusters, genderclusters, instructors))

        print("Research\t", size, "\tGrade\t", size, "\t",
              jshat(researchclusters, gradeclusters), "\t", purity(researchclusters, gradeclusters),
              "\t", fowlkesmallowsindex(researchclusters, gradeclusters, instructors))

        print("Research\t", size, "\tTitle\t", size, "\t",
              jshat(researchclusters, titleclusters), "\t", purity(researchclusters, titleclusters),
              "\t", fowlkesmallowsindex(researchclusters, titleclusters, instructors))

        print("Research\t", size, "\tWage\t", size, "\t",
              jshat(researchclusters, wageclusters), "\t", purity(researchclusters, wageclusters),
              "\t", fowlkesmallowsindex(researchclusters, wageclusters, instructors))

        print("Feedback\t", size, "\tWage\t", size, "\t",
              jshat(feedbackclusters, wageclusters), "\t", purity(feedbackclusters, wageclusters),
              "\t", fowlkesmallowsindex(feedbackclusters, wageclusters, instructors))

        print("Feedback\t", size, "\tResearch\t", size, "\t",
              jshat(feedbackclusters, researchclusters), "\t", purity(feedbackclusters, researchclusters),
              "\t", fowlkesmallowsindex(feedbackclusters, researchclusters, instructors))

        print("Feedback\t", size, "\tGender\t", 2, "\t",
              jshat(feedbackclusters, genderclusters), "\t", purity(feedbackclusters, genderclusters),
              "\t", fowlkesmallowsindex(feedbackclusters, genderclusters, instructors))

        print("Feedback\t", size, "\tGrade\t", size, "\t",
              jshat(feedbackclusters, gradeclusters), "\t", purity(feedbackclusters, gradeclusters),
              "\t", fowlkesmallowsindex(feedbackclusters, gradeclusters, instructors))

        print("Feedback\t", size, "\tTitle\t", size, "\t",
              jshat(feedbackclusters, titleclusters), "\t", purity(feedbackclusters, titleclusters),
              "\t", fowlkesmallowsindex(feedbackclusters, titleclusters, instructors))


def drive(minsize, maxsize):
    testclusterings("kmeans++", kMeansPP, minsize, maxsize)
    testclusterings("Gonzales", Gonzales, minsize, maxsize)
    testclusterings("Heirarchical Single-Link", SingleLink, minsize, maxsize)
    testclusterings("Heirarchical Complete", CompleteLink, minsize, maxsize)


def compare():
    clustermethods = [kMeansPP, Gonzales, CompleteLink, SingleLink]
    instructors = getInstructorsWithClasses()

    for i in range(0, len(clustermethods)):
        method1 = clustermethods[i]
        for j in range(i, len(clustermethods)):
            method2 = clustermethods[j]

            if method1.__name__ == method2.__name__:
                continue
            gradeclusters1 = method1(instructors, 3, gradeDistance)
            titleclusters1 = method1(instructors, 3, titleDistance)
            wageclusters1 = method1(instructors, 3, wageDistance)
            researchclusters1 = method1(instructors, 3, researchDistance)
            feedbackclusters1 = method1(instructors, 3, feedbackDistance)

            gradeclusters2 = method2(instructors, 3, gradeDistance)
            titleclusters2 = method2(instructors, 3, titleDistance)
            wageclusters2 = method2(instructors, 3, wageDistance)
            researchclusters2 = method2(instructors, 3, researchDistance)
            feedbackclusters2 = method2(instructors, 3, feedbackDistance)
            j = [jshat(gradeclusters1, gradeclusters2), jshat(titleclusters1, titleclusters2),
                 jshat(wageclusters1, wageclusters2), jshat(researchclusters1, researchclusters2),
                 jshat(feedbackclusters1, feedbackclusters2)]
            p = [purity(gradeclusters1, gradeclusters2), purity(titleclusters1, titleclusters2),
                 purity(researchclusters1, researchclusters2), purity(wageclusters1, wageclusters2),
                 purity(feedbackclusters1, feedbackclusters2)]
            f = [fowlkesmallowsindex(gradeclusters1, gradeclusters2, instructors),
                 fowlkesmallowsindex(titleclusters1, titleclusters2, instructors),
                 fowlkesmallowsindex(wageclusters1, wageclusters2, instructors),
                 fowlkesmallowsindex(researchclusters1, researchclusters2, instructors),
                 fowlkesmallowsindex(feedbackclusters1, feedbackclusters2, instructors)]
            print(method1.__name__, "\t", method2.__name__)
            print("Metric\tJSHat\tPurity\tFMI")
            print("Grades\t", jshat(gradeclusters1, gradeclusters2), "\t", purity(gradeclusters1, gradeclusters2), "\t",
                  fowlkesmallowsindex(gradeclusters1, gradeclusters2, instructors))
            print("Title\t", jshat(titleclusters1, titleclusters2), "\t", purity(titleclusters1, titleclusters2), "\t",
                  fowlkesmallowsindex(titleclusters1, titleclusters2, instructors))
            print("Wage\t", jshat(wageclusters1, wageclusters2), "\t", purity(wageclusters1, wageclusters2), "\t",
                  fowlkesmallowsindex(wageclusters1, wageclusters2, instructors))
            print("Research Instrests\t", jshat(researchclusters1, researchclusters2), "\t",
                  purity(researchclusters1, researchclusters2), "\t",
                  fowlkesmallowsindex(researchclusters1, researchclusters2, instructors))
            print("Feedback\t", jshat(feedbackclusters1, feedbackclusters2), "\t",
                  purity(feedbackclusters1, feedbackclusters2), "\t",
                  fowlkesmallowsindex(feedbackclusters1, feedbackclusters2, instructors))
            print("Averages\t", round(sum(j) / len(j), 3), "\t", round(sum(p) / len(p), 3), "\t",
                  round(sum(f) / len(f), 3))


def rvw():
    instructors = getInstructorsWithClasses()
    researchclusters1 = kMeansPP(instructors, 3, researchDistance)
    wageclusters1 = kMeansPP(instructors, 3, titleDistance)

    printClustering(researchclusters1)
    printClustering(wageclusters1)


# print(rvw())
# drive(3, 4)
compare()

