"""
Genotype is a list/array of 24 items, with the first 6 being A, the next 6 being B and so on. Each item can be a 1 or
a 0.

The fitness will be calculated by calculating the lift. The higher the fitness the better the individual.

Mutation will happen on 4 spots. Every input for the lift function gets mutated. A random gene gets selected and changed
from 1 to 0 or the other way around.

The formula that we will use for lift is as follows:
lift = (A - B)^2 + (C + D)^2 - (A - 30)^3 - (C - 40)^3
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

def get_abcd(individual):
    """
    Individual consists of 4 variables encoded as a binary. This function extracts the variables and returns them as a
    base 10 integer
    :param individual: list of 0 and 1 representing the individual
    :return: returns a list of the variables easy for slicing: [a, b, c, d]
    """
    a, b, c, d = [individual[x:x+6] for x in range(0, len(individual), 6)]
    a = int("".join(str(number) for number in a), 2)
    b = int("".join(str(number) for number in b), 2)
    c = int("".join(str(number) for number in c), 2)
    d = int("".join(str(number) for number in d), 2)
    return [a, b, c, d]

def fitness(individual):
    """
    Calculate fitness of an individual based on the formula for lift
    lift = (A - B)^2 + (C + D)^2 - (A - 30)^3 - (C - 40)^3
    :param individual: list representing an individual
    :return: fitness as a number, higher is better
    """
    a, b, c, d = get_abcd(individual)
    return ((a - b) ** 2) + ((c + d) ** 2) - ((a - 30) ** 3) - ((c - 40) ** 3)

def sort_generation(population):
    """
    Get the population and return a sorted one based on how they perform on the fitness function
    :param population: population to sort
    :return: returns a sorted population
    """
    fitnessList = []
    for individual in population:
        fitnessList.append(fitness(individual))
    return [individual for fit, individual in reversed(sorted(zip(fitnessList, population)))]

def create_new_generation(population, keepBestAmount):
    """
    Create a new generation by inverting one random gene in the genotype per variable that is represented
    :param population: expects an list of the current generation ordered by fitness, the best are first, worst are last
    :param keepBestAmount: amount of 'best' that you want to keep, the rest gets mutated
    :return: returns the new generation
    """
    for i in range(len(population[keepBestAmount:])):
        sliced = [population[i+keepBestAmount][x:x+6] for x in range(0, len(population[i+keepBestAmount]), 6)]
        tmp = []
        for variable in sliced:
            index = random.randint(0, len(sliced)-1)
            if variable[index] == 0:
                variable[index] = 1
            else:
                variable[index] = 0
            tmp += variable
        population[i+keepBestAmount] = tmp
    return population # individuals are now mutated so just return the new generation

population = create_population(1000, 24, 0, 1)
amountOfGenerations = 100

for generation in range(amountOfGenerations):
    population = sort_generation(population)
    population = create_new_generation(population, 10)

population = sort_generation(population) # sort generation so we can take the best 10
print("The best individual is: {} with a fitness of: {}".format(population[0], fitness(population[0]))) # index 0 because of the sorted population

"""
After running the algorithm a 100 times the average of the max lift is: 97022.32
There is a difference between the results of about 2000. This is not a lot since the values go almost to 100000. So
this is about 2% Furthermore, it stands out that a and c almost always are 0 while b and d are changing.

The results of 100 times running are as follows:
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0] with a fitness of: 98333
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] with a fitness of: 96650
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1] with a fitness of: 96981
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1] with a fitness of: 95969
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1] with a fitness of: 97221
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0] with a fitness of: 96809
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1] with a fitness of: 96965
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0] with a fitness of: 96636
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1] with a fitness of: 97290
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0] with a fitness of: 98200
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0] with a fitness of: 97548
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0] with a fitness of: 97280
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1] with a fitness of: 95874
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0] with a fitness of: 95900
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0] with a fitness of: 96904
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] with a fitness of: 97273
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1] with a fitness of: 96537
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0] with a fitness of: 97173
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] with a fitness of: 98450
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0] with a fitness of: 97469
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1] with a fitness of: 97058
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0] with a fitness of: 97736
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0] with a fitness of: 96128
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1] with a fitness of: 97625
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] with a fitness of: 96490
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0] with a fitness of: 97085
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0] with a fitness of: 97760
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0] with a fitness of: 96625
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1] with a fitness of: 97506
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] with a fitness of: 97178
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0] with a fitness of: 96945
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0] with a fitness of: 96904
The best individual is: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1] with a fitness of: 95082
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1] with a fitness of: 95441
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1] with a fitness of: 96650
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1] with a fitness of: 97322
The best individual is: [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] with a fitness of: 96079
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0] with a fitness of: 97389
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1] with a fitness of: 98690
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0] with a fitness of: 96513
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1] with a fitness of: 95561
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1] with a fitness of: 97653
The best individual is: [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0] with a fitness of: 95148
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1] with a fitness of: 97849
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0] with a fitness of: 96945
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0] with a fitness of: 98200
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0] with a fitness of: 95624
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1] with a fitness of: 96626
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1] with a fitness of: 98565
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] with a fitness of: 96733
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1] with a fitness of: 96274
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0] with a fitness of: 96517
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0] with a fitness of: 96017
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1] with a fitness of: 96850
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0] with a fitness of: 96620
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0] with a fitness of: 97344
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1] with a fitness of: 97849
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1] with a fitness of: 95338
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1] with a fitness of: 98085
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0] with a fitness of: 97425
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0] with a fitness of: 95165
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0] with a fitness of: 97857
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1] with a fitness of: 97506
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0] with a fitness of: 97161
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0] with a fitness of: 96840
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0] with a fitness of: 97389
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1] with a fitness of: 98325
The best individual is: [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1] with a fitness of: 95591
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1] with a fitness of: 97409
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0] with a fitness of: 97736
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1] with a fitness of: 96941
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] with a fitness of: 98105
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0] with a fitness of: 98569
The best individual is: [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0] with a fitness of: 95685
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1] with a fitness of: 96506
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1] with a fitness of: 96941
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1] with a fitness of: 96850
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0] with a fitness of: 96413
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] with a fitness of: 97370
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1] with a fitness of: 97857
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0] with a fitness of: 97344
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0] with a fitness of: 98208
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1] with a fitness of: 97025
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0] with a fitness of: 98333
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1] with a fitness of: 98450
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] with a fitness of: 98218
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1] with a fitness of: 96234
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0] with a fitness of: 96204
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1] with a fitness of: 97857
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] with a fitness of: 95993
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1] with a fitness of: 97778
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] with a fitness of: 97370
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0] with a fitness of: 95961
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0] with a fitness of: 97068
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1] with a fitness of: 97613
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1] with a fitness of: 97058
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1] with a fitness of: 96834
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0] with a fitness of: 97053
The best individual is: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1] with a fitness of: 96650
The best individual is: [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1] with a fitness of: 95874
"""
