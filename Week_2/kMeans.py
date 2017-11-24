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

    #recalculate centroids until there is something assigned to every one
    tmp = 0
    while tmp < k:
        tmp = 0
        for i in assigned:
            tmp+=1
        if tmp < k:
            centroids = getRandomPoints(maxValues, k)
            assigned = assignToCluster(centroids, data)

    for i in range(k):
        try:
            print(len(assigned[list(assigned.keys())[i]]))
        except:
            print(0)
    print("======")

    while True:
        tmp = assigned
        centroids = getNewCentroids(assigned)
        assigned = assignToCluster(centroids, data)
        # check whether the classes differ
        check = True
        for j in range(k):
            for l in range(len(assigned[list(assigned.keys())[j]])):
                try:
                    if assigned[list(assigned.keys())[j]][l].all() != tmp[list(tmp.keys())[j]][l].all():
                        check = False
                except IndexError:
                    check = False
        if check:
            return assigned

## WIP
def calculateIntraclusterDistance(means):
    intraDistance = 0
    for centroid in means:
        distance = 0
        # create list of a string
        tmp = []
        for i in centroid.strip('[]').replace(",", "").split():
            tmp.append(float(i))
        for cluster in means[centroid]:
            distance = 0
            for j in range(len(tmp)):
                distance += ((tmp[j]-cluster[j])**2)
            distance += math.sqrt(distance)
        intraDistance += distance
    print("distance",intraDistance)
    return intraDistance

for k in range(2, 10):
    means = kMeans(data, k)
    print(means)
    print(calculateIntraclusterDistance(means))
    for i in range(k):
        try:
            print(len(means[list(means.keys())[i]]))
        except:
            print(0)
    print()
# PLOT WITH MATPLOTLIB
