import math, random


# Gets the center associated with the given metric, using the given distance function.
def getCenter(centers, metric, distanceFunction):
    minDistance = distanceFunction(metric, centers[0])
    minCenter = centers[0]

    for center in centers[1:]:
        distance = distanceFunction(metric, center)
        if distance < minDistance:
            minDistance = distance
            minCenter = center

    return minCenter


# Gets the distance to the center associated with the given metric, using the given distance function
def distanceToCenter(centers, metric, distanceFunction):
    return distanceFunction(metric, getCenter(centers, metric, distanceFunction))


def centersToSets(centers, metrics, distanceFunction):
    sets = []

    for center in centers:
        subset = set()
        
        for metric in metrics:
            if getCenter(centers, metric, distanceFunction) == center:
                subset.add(metric)

        sets.append(subset)

    return sets


def kMeansPP(metrics, centerCount, distanceFunction):
    centers = [metrics[0]]

    while len(centers) < centerCount:
        distances = [pow(distanceToCenter(centers, metric, distanceFunction), 2) for metric in metrics]
        totalDistance = sum(distances)
        
        for index in range(len(distances)):
            distances[index] /= totalDistance

        uniform = random.uniform(0.0, 1.0)

        cumulative = 0.0

        for index in range(len(distances)):
            cumulative += distances[index];
        
            if uniform <= cumulative:
                centers.append(metrics[index])
                break

    return centersToSets(centers, metrics, distanceFunction)


def gonzales(metrics, centerCount, distanceFunction):
    centers = list()
    centers.append(metrics[0])
    dict_clusters = {}
    for point in metrics:
        dict_clusters[point] = centers[0]

    for i in range(1, centerCount):
        centers.append(metrics[0])
        max_min_distance = 0
        new_center = None
        for j in range(0, len(metrics)):
            min_distance = min([distanceFunction(metrics[j], c) for c in centers])
            if min_distance > max_min_distance:
                max_min_distance = min_distance
                new_center = metrics[j]
        centers[i] = new_center

        for j in range(0, len(metrics)):
            if distanceFunction(metrics[j], dict_clusters[metrics[j]]) > distanceFunction(metrics[j], centers[i]):
                dict_clusters[metrics[j]] = centers[i]

	#return list of sets
    return centersToSets(centers, metrics, distanceFunction)


# TODO implement
def lloyds(metrics, centerCount, distanceFunction):
    return set()


def heirarchical_cluster_single_link(metrics, centerCount, pointDistanceFunction):
    return heirarchical_cluster(metrics, centerCount, pointDistanceFunction, single_link_distance)


def heirarchical_cluster_complete_link(metrics, centerCount, pointDistanceFunction):
    return heirarchical_cluster(metrics, centerCount, pointDistanceFunction, complete_link_distance)


def heirarchical_cluster(metrics, desiredClusterCount, pointDistanceFunction, setDistanceFunction):
    clusters = []

    for point in metrics:
        point_set = set()
        point_set.add(point)
        clusters.append(point_set)

    while desiredClusterCount < len(clusters):
        closest_cluster1 = 0
        closest_cluster2 = 1
        cluster_distance = setDistanceFunction(clusters[0], clusters[1], pointDistanceFunction)
        for i in range(0, len(clusters)):
            for j in range(i + 1, len(clusters)):
                new_cluster_distance = setDistanceFunction(clusters[i], clusters[j], pointDistanceFunction)
                if new_cluster_distance < cluster_distance:
                    closest_cluster1 = i
                    closest_cluster2 = j
                    cluster_distance = new_cluster_distance
        merge_clusters(clusters, closest_cluster1, closest_cluster2)

    return clusters


def single_link_distance(set1, set2, distanceFunction):
    shortest_distance = float("inf")
    for point1 in set1:
        for point2 in set2:
            if distanceFunction(point1, point2) < shortest_distance:
                shortest_distance = distanceFunction(point1, point2)
    return shortest_distance


def complete_link_distance(set1, set2, distanceFunction):
    largest_distance = 0
    for point1 in set1:
        for point2 in set2:
            if distanceFunction(point1, point2) > largest_distance:
                largest_distance = distanceFunction(point1, point2)
    return largest_distance


def merge_clusters(clusterData, index1, index2):
    clusterData[index1] = clusterData[index1].union(clusterData[index2])
    clusterData.pop(index2)

    


def getMaxDistance(instructor, cluster, distanceFunction):
    maxDistance = 0

    for otherInstructor in cluster:
        distance = distanceFunction(instructor, otherInstructor)
        
        if distance > maxDistance:
            maxDistance = distance

    return maxDistance
    
def getRepresentative(cluster, distanceFunction):
    representative = None
    representativeDistance = None
    
    for instructor in cluster:
        distance = getMaxDistance(instructor, cluster, distanceFunction)

        if representative is None or distance < representativeDistance:
            representative = instructor
            representativeDistance = distance
        
    return representative
    
def refineClusters(clusters, instructors, distanceFunction):
    newCenters = []
    
    for cluster in clusters:
        newCenters.append(getRepresentative(cluster, distanceFunction))
    
    return centersToSets(newCenters, instructors, distanceFunction)