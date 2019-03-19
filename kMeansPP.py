import math, random

# Gets the center associated with the given metric, using the given distance function.
def getCenter(centers, metric, distanceFunction):
    minDistance = distanceFunction(metric, centers[0])
    minCenter = centers[0]

    for center in centers[1:]:
        distance = distanceFunction(metric, center)
        if(distance < minDistance):
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
    
    
def intDistance(intOne, intTwo):
    return abs(intOne - intTwo)
   
ints = [4, 5, 100, 101]
print(kMeansPP(ints, 2, intDistance))