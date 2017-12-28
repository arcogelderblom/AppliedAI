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
    """
    Create a population
    :param amount: amount of individuals in the population
    :param listLength: needed for create_individual
    :param minValue: needed for create_individual
    :param maxValue: needed for create_individual
    :return: returns a list of individual, a population
    """
    return [create_individual(listLength, minValue, maxValue) for x in range(amount)]


def create_individual(listLength, minValue, maxValue):
    """
    Create a individual based on a few constraints
    :param listLength: length of the created genotype
    :param minValue: minimal value a gene can have
    :param maxValue: maximal value a gene can have
    :return: returns a list with values representing an individual
    """
    return [random.randint(minValue, maxValue) for x in range(listLength)]

def fitness(individual, expectedSum, expectedMultiply):
    """
    Calculate fitness of an individual based on the expected sum and the expected multiplication
    :param individual: list representing an individual
    :param expectedSum: integer representing the expected sum
    :param expectedMultiply: integer representing the expected multiplication
    :return: fitness as a number, lower is better
    """
    sum = 0
    multiply = 0
    for index in range(len(individual)):
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

def sort_generation(population, expectedSum, expectedMultiply):
    """
    Get the population and return a sorted one based on how they perform on the fitness function
    :param population: population to sort
    :param expectedSum: needed for fitness function
    :param expectedMultiply: needed for fitness function
    :return: returns a sorted population
    """
    fitnessList = []
    for individual in population:
        fitnessList.append(fitness(individual, expectedSum, expectedMultiply))
    return [individual for fit,individual in sorted(zip(fitnessList,population))]

def create_new_generation(population, keepBestAmount):
    """
    Create a new generation by inverting one random gene in the genotype
    :param population: expects an list of the current generation ordered by fitness, the best are first, worst are last
    :param keepBestAmount: amount of 'best' that you want to keep, the rest gets mutated
    :return: returns the new generation
    """
    for individual in population[keepBestAmount:]:
        index = random.randint(0, len(individual)-1)
        if individual[index] == 0:
            individual[index] = 1
        else:
            individual[index] = 0
    return population # individuals are now mutated so just return the new generation

population = create_population(100, 10, 0, 1)
expectedSum = 36
expectedMultiply = 360
amountOfGenerations = 10

for generation in range(amountOfGenerations):
    population = sort_generation(population, expectedSum, expectedMultiply)
    population = create_new_generation(population, 10)

population = sort_generation(population, expectedSum, expectedMultiply) # sort generation so we can take the best 10
print("The best individual is: {} with a fitness of: {}".format(population[0], fitness(population[0], expectedSum, expectedMultiply))) # index 0 because of the sorted population

"""
The algorithm performs very good. It often finds the perfect individual with a fitness of 0, meaning it is exactly as
we want it. After running it 100 times the majority is a fitness of 0 while the highest fitness (so worst individual
of them all) has a fitness of 4, which still is not bad.

The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [0, 1, 0, 1, 1, 0, 0, 0, 1, 0] with a fitness of: 1
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [0, 1, 1, 0, 0, 1, 0, 0, 0, 1] with a fitness of: 2
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 1, 0, 1, 1, 0, 0, 0, 1, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 1, 0, 1, 1, 0, 0, 0, 1, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 1, 0, 1, 1, 0, 0, 0, 1, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 0, 0, 1, 0, 0, 0, 0, 1, 1] with a fitness of: 4
The best individual is: [0, 1, 0, 1, 1, 0, 0, 0, 1, 0] with a fitness of: 1
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 1, 0, 1, 1, 0, 0, 0, 1, 0] with a fitness of: 1
The best individual is: [1, 1, 0, 1, 1, 0, 0, 0, 1, 0] with a fitness of: 2
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 0, 0, 1, 0, 0, 1, 1, 0] with a fitness of: 4
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [0, 1, 1, 0, 0, 1, 0, 0, 0, 1] with a fitness of: 2
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 1, 0, 1, 1, 0, 0, 0, 1, 0] with a fitness of: 2
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [1, 1, 0, 1, 1, 0, 0, 0, 1, 0] with a fitness of: 2
The best individual is: [0, 1, 1, 0, 0, 1, 0, 0, 0, 1] with a fitness of: 2
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [0, 1, 1, 0, 0, 1, 0, 0, 0, 1] with a fitness of: 2
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 1, 1, 0, 0, 1, 0, 0, 0, 1] with a fitness of: 2
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 1, 0, 1, 1, 0, 0, 0, 1, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 1, 1, 0, 0, 1, 0, 0, 0, 1] with a fitness of: 2
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 1, 0, 1, 1, 0, 0, 0, 1, 0] with a fitness of: 1
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 0
The best individual is: [0, 0, 1, 1, 1, 1, 0, 0, 0, 0] with a fitness of: 1
"""
