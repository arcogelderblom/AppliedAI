"""
Genotype is a list/array of 10 items, each representing a number that is possible on the card, index 0 being a number
1 and index 9 being number 10. So index+1 is the actual number. Each position is marked with an 1 or an 0. 1 for being
on pile_1 and 0 for being on pile_0.

The fitness will be calculated using the expected outcome. Everything that is 'tagged' with 0 must sum as close to 36 as
possible, with the deviation being a measure for fitness (lower is better). Everything that is 'tagged' with 1 must
multiply as close to 360 as possible. The deviation is a measure for the fitness. These 2 measures are then summed to
become one integer representing the fitness. The lower the number the better.
"""

import random

def create_population(amount, listLength, minValue, maxValue):
    return [create_individual(listLength, minValue, maxValue) for x in range(amount)]


def create_individual(listLength, minValue, maxValue):
    return [random.randint(minValue, maxValue) for x in range(listLength)]

def fitness(individual, expectedSum, expectedMultiply):
    sum = 0
    multiply = 0
    for index in range(len(individual)):
        print(individual[index])
        if individual[index] == 0:
            sum += index + 1
        else:
            if multiply == 0:
                multiply = index + 1
            else:
                multiply *= index + 1
    resultSum = abs(sum - expectedSum)
    resultMultiply = abs(multiply - expectedMultiply)
    return resultSum+resultMultiply

population = create_population(1, 10, 0, 1)
expectedSum = 36
expectedMultiply = 360

print(population)
print("Calculating fitness:")
for individual in population:
    print(individual, fitness(individual, expectedSum, expectedMultiply))