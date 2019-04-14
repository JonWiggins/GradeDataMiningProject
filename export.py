from Clustering import *
from distances import *
from clusterTests import *

from DataLoader import getInstructorsWithClasses
from csvWriter import CSVWriter

def exportToCSV(primaryClusters, secondaryClusters, instructors, filePath, primaryClusterDisplay=None, secondaryClusterDisplay=None):
    writer = CSVWriter()

    writer.writeCell("Primary Clustering", 0, 0)
    writer.append(getClusterDescriptionTable(primaryClusters, primaryClusterDisplay), 0, 1)

    writer.writeCell("Second Clustering", 3, 0)
    writer.append(getClusterDescriptionTable(secondaryClusters, secondaryClusterDisplay), 3, 1)

    writer.writeCell("Comparison Values", 6, 0)
    writer.append(getClusterComparisonTable(primaryClusters, secondaryClusters, instructors), 6, 1)
    
    writer.writeCell("Graph Tables", 9, 0)
    writer.append(getClusterComparisionGraph(primaryClusters, secondaryClusters), 9, 1)

    writer.writeToFile(filePath)

def getClusterDescriptionTable(clusters, clusterDisplay=None):
    writer = CSVWriter()
    row = 0
    
    for clusterIndex in range(len(clusters)):
        writer.writeCell(f'Cluster {clusterIndex}', 0, row)
        row += 1

        for instructor in clusters[clusterIndex]:
            writer.writeCell(instructor.instructorname, 0, row)

            if not clusterDisplay is None:
                writer.writeCell(clusterDisplay(instructor), 1, row)

            row += 1

        row += 1

    return writer

def getClusterComparisonTable(primaryClusters, secondaryClusters, instructors):
    writer = CSVWriter()

    writer.writeCell("Comparison Values", 0, 0)

    writer.writeCell("jshat", 0, 1)
    writer.writeCell(jshat(primaryClusters, secondaryClusters), 1, 1)

    writer.writeCell("purity", 0, 2)
    writer.writeCell(purity(primaryClusters, secondaryClusters), 1, 2)

    writer.writeCell("fowlkes mallows index", 0, 3)
    writer.writeCell(fowlkesmallowsindex(primaryClusters, secondaryClusters, instructors), 1, 3)
    
    return writer
    
def getClusterComparisionGraph(primaryClusters, secondaryClusters):
    writer = CSVWriter()
    row = 0

    for primaryClusterIndex in range(len(primaryClusters)):
        primaryCluster = primaryClusters[primaryClusterIndex]
        chartData = [0] * len(secondaryClusters)

        for instructor in primaryCluster:
            chartData[getContainingClusterIndex(instructor, secondaryClusters)] += 1

        writer.writeCell(f'Primary Cluster {primaryClusterIndex} Table', 0, row)
        row += 1
        
        writer.writeCell(f'Secondary Cluster Index', 0, row)
        writer.writeCell(f'Count', 1, row)
        row += 1

        for secondaryClusterIndex in range(len(chartData)):
            entry = chartData[secondaryClusterIndex]

            writer.writeCell(secondaryClusterIndex, 0, row)
            writer.writeCell(entry, 1, row)
            row += 1

        row += 1
    
    return writer


instructors = getInstructorsWithClasses(silent=True)

clusters = {
    "grades": kMeansPP(instructors, 6, gradeDistance),
    "sex": kMeansPP(instructors, 2, sexDistance),
    "title": kMeansPP(instructors, 5, titleDistance),
    "wage": kMeansPP(instructors, 4, wageDistance),
    "research": kMeansPP(instructors, 6, researchDistance),
    "feedback": kMeansPP(instructors, 6, feedbackDistance)
}

descriptors = {
    "grades": lambda instructor: instructor.gradevector,
    "sex": lambda instructor: instructor.sex,
    "title": lambda instructor: instructor.positions,
    "wage": lambda instructor: instructor.wagevec,
    "research": lambda instructor: instructor.researchtext,
    "feedback": lambda instructor: instructor.feedbackvector
}

for primaryAttribute in clusters.keys():
    for secondaryAttribute in clusters.keys():
        if primaryAttribute == secondaryAttribute:
            continue

        exportToCSV(clusters[primaryAttribute], clusters[secondaryAttribute], instructors, f'comparisons/{primaryAttribute}_vs_{secondaryAttribute}.csv', descriptors[primaryAttribute], descriptors[secondaryAttribute])
