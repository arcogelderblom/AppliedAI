import numpy as np, math

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

#import validation data
dataValidation = np.genfromtxt('Dataset/validation1.csv', delimiter=';', usecols=[1,2,3,4,5,6,7])
datesValidation = np.genfromtxt('Dataset/validation1.csv', delimiter=';', usecols=[0])
labelsValidation = []
for label in datesValidation:
    if label < 20010301:
        labelsValidation.append('winter')
    elif 20010301 <= label < 20010601:
        labelsValidation.append('lente')
    elif 20010601 <= label < 20010901:
        labelsValidation.append('zomer')
    elif 20010901 <= label < 20011201:
        labelsValidation.append('herfst')
    else:
        labelsValidation.append('winter')

labelOptions = ['winter', 'herfst', 'zomer', 'lente']

def getSeasonLabel(array, data, k):
    # Calculate distances
    distances = []
    for entry in data:
        distance = 0
        for j in range(0, len(array)):
            distance += ((array[j]-entry[j])**2)
        distances.append(math.sqrt(distance))

    # Get the labels k number of lowest distances
    lowest = sorted(distances)
    lowestIndexLabels = []
    for i in range(0, k):
        lowestIndexLabels.append(labels[distances.index(lowest[i])])

    # Determine which label belongs to the array
    solution = ''
    amount = -1
    for option in labelOptions:
        if lowestIndexLabels.count(option) >= amount:
            tmp = option
            if lowestIndexLabels.count(option) == amount:
                for season in lowestIndexLabels:
                    if season == option:
                        tmp = option
                        amount = lowestIndexLabels.count(option)
                        break
                    elif season == solution:
                        tmp = solution
                        break
            amount = lowestIndexLabels.count(option)
            solution = tmp

    # Return the string representing the season
    return solution

bestK = 0
tmpPercentage = 0
for k in range(1,len(data)):
    hits = 0
    for i in range(0, len(dataValidation)):
        if getSeasonLabel(dataValidation[i], data, k) == labelsValidation[i]:
            hits += 1
    percentage = hits/len(dataValidation)*100
    if percentage > tmpPercentage:
        bestK = k
        tmpPercentage = percentage
    print("Amount of hits for k={} is {} which is a hit percentage of {}%".format(k, hits, percentage))
    print("K: {:3} ERROR: {}%".format(k, 100-percentage))
print("\nThe best k to use is {} and it had a hit percentage of {}%".format(bestK, tmpPercentage))

days = np.genfromtxt('Dataset/days.csv', delimiter=';', usecols=[1,2,3,4,5,6,7])
counter = 1
for day in days:
    # Use the best K to determine which season it is
    print("Day number {}, is in season: {}".format(counter, getSeasonLabel(day, data, bestK)))
    counter += 1
