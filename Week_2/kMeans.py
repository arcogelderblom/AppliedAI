import numpy as np, random, math

# import training data
data = np.genfromtxt('Dataset/dataset1.csv', delimiter=';', usecols=[1,2,3,4,5,6,7])

# import validation data
dataValidation = np.genfromtxt('Dataset/validation1.csv', delimiter=';', usecols=[1,2,3,4,5,6,7])

def getMaxValues(data):
    # Calculate max values for a good range for random math
    maxValues= []
    for i in range(0, len(data[0])):
        tmp = []
        for dataEntry in data:
            tmp.append(dataEntry[i])
        # Add lowest possible number
        tmp.sort()
        maxValues.append([tmp[0]])
        # Add highest possible number
        tmp.sort(reverse=True)
        maxValues[i] += [tmp[0]]
    return maxValues

def getRandomPoints(values, k):
    points = []
    for i in range(0, k):
        point = []
        for value in values:
            point.append(random.randrange(value[0], value[1]))
        points.append(point)
    return points

def closestCluster(entry, clusters):
    # Calculate distances
    distances = []
    for cluster in clusters:
        distance = 0
        for j in range(0, len(entry)):
            distance += ((entry[j]-cluster[j])**2)
        distances.append(math.sqrt(distance))

    # Get the labels k number of lowest distances
    lowest = sorted(distances)
    return clusters[distances.index(lowest[0])]

def assignToCluster(clusters, data):
    assigned = {}
    for entry in data:
        closest = str(closestCluster(entry, clusters))
        if closest in assigned:
            tmp = assigned[closest]
            tmp.append(entry)
            assigned[closest] = tmp
        else:
            assigned[closest] = [entry]
    return assigned

def getNewCentroid(data, length):
    centroid = []
    for i in range(0, length):
        tmp = 0
        for j in range(0, len(data)):
            tmp += data[j][i]
        mean = tmp/(j+1)
        centroid.append(mean)
    return centroid

def getNewCentroids(data):
    centroids = []
    for i in data:
        centroids.append(getNewCentroid(data[i], len(data[i][0])))
    return centroids

def kMeans(data, k):
    maxValues = getMaxValues(data)
    centroids = getRandomPoints(maxValues, k)
    assigned = assignToCluster(centroids, data)
    for i in range(k):
        try:
            print(len(assigned[list(assigned.keys())[i]]))
        except:
            print(0)
    print("======")

    for i in range(100):
        assigned = assignToCluster(centroids, data)
        centroids = getNewCentroids(assigned)
    return assigned

k = 4
for i in range(10):
    means = kMeans(data, k)
    for i in range(k):
        try:
            print(len(means[list(means.keys())[i]]))
        except:
            print(0)
    print()

"""
K MEANS ALGORITHM
Given:
    • Training set X of examples {x⃗1,...,x⃗n} where
            – x ̄i is the feature vector of example i
    • A set K of centroids {c⃗1,...,⃗ck}
Do:
1. Foreachpoint⃗xi:
    (a) Find the nearest centroid ⃗cj;
    (b) Assign point ⃗xi to cluster j;
2. For each cluster j = 1,...,k:
    (a) Calculate new centroid ⃗c j as the mean of all points ⃗xi that are assigned to cluster j.
"""