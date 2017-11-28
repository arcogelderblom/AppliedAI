import numpy as np, random, math
import matplotlib.pyplot as plt

# import training data
data = np.genfromtxt('Dataset/dataset1.csv', delimiter=';', usecols=[1,2,3,4,5,6,7])
dates = np.genfromtxt('Dataset/dataset1.csv', delimiter=';', usecols=[0])
labels = []
for label in dates:
    if label < 20000301:
        labels.append('winter')
    elif 20000301 <= label < 20000601:
        labels.append('lente')
    elif 20000601 <= label < 20000901:
        labels.append('zomer')
    elif 20000901 <= label < 20001201:
        labels.append('herfst')
    else:
        labels.append('winter')

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

def calculateIntraclusterDistance(means):
    intraDistance = 0
    for centroid in means:
        distance = 0
        # create list of a string
        tmp = []
        for i in centroid.strip('[]').replace(",", "").split():
            tmp.append(float(i))

        # calculate distances
        for cluster in means[centroid]:
            distance = 0
            for j in range(len(tmp)):
                distance += ((tmp[j]-cluster[j])**2)
            distance += math.sqrt(distance)
        intraDistance += distance
    return intraDistance

## DETERMINE LABELS
means = kMeans(data, 4)
labelOptions = ['winter', 'herfst', 'zomer', 'lente']
counter = 1
for i in means:
    tmp = []
    for j in means[i]:
        for index in range(len(data)):
            if str(j) == str(data[index]):
                tmp.append(labels[index])
                break

    solution = ''
    amount = -1
    for option in labelOptions:
        print(option, tmp.count(option))
        if tmp.count(option) > amount:
            solution = option
            amount = tmp.count(option)
    print("Cluster {} is season '{}'".format(counter, solution))
    counter += 1

## PLOTTEN
y = []
x = []
for k in range(1, 11):
    distance = []
    for j in range(10):
        means = kMeans(data, k)
        distance.append(calculateIntraclusterDistance(means))
    x.append(k)
    y.append(sorted(distance)[0])
    print("x {} y {}".format(x, y))
plt.plot(x, y)
plt.show()
