from random import random, gauss, choice, uniform
from typing import List
import numpy as np
import matplotlib.pyplot as plt

# Ensures the gene is between min and max
def constraints(g, min = -10, max = 10):
    if max < g:
        g = max
    elif min > g:
        g = min
    return g

# Blends two parent genomes to produce two child genomes
# Alpha is constant that can be used to control blend
def crossover_blend(g1, g2, alpha):
    shift = (1 + 2 * alpha) * random() - alpha
    new_g1 = (1 - shift) * g1 + shift * g2
    new_g2 = shift * g1 + (1 - shift) * g2
    return constraints(new_g1), constraints(new_g2)

# Used to mutate a genome
# Parameters mu and sigma are used to define gauss
def mutate_gaussian(g, mu, sigma):
    mutated_gene = g + gauss(mu, sigma)
    return constraints(mutated_gene)

# Tournament selection process
# Picks individuals for tournament of 'size' and returns winners until we have a complete population 
def tournament_selection(population, size):
    winners = []
    for i in range(len(population)):
        candidates = []
        for j in range(size):
            candidates.append(choice(population))
        winners.append(max(candidates, key = lambda candidate: candidate.fitness))
    return winners

# Returns the fittest individual
def get_best(population):
    best = population[0]
    for individual in population:
        if individual.fitness > best.fitness:
            best = individual
    return best

# Plots the population
def plot_population(population, generation_number):
    x = np.linspace(-10, 10)
    plt.plot(x, func(x), '--', color = 'orange')
    genes = []
    fitnesses = []
    for x in population:
        genes.append(x.gene)
        fitnesses.append(x.fitness)
    plt.plot(genes, fitnesses, 'o', color = 'blue')
    best = get_best(population)
    plt.plot(best.gene, best.fitness, 's', color = 'red')
    plt.title(f"Generation Number {generation_number}")
    plt.show()
    plt.close()

# Function that we are trying to find the maximum of
def func(x):
    return np.sin(x) - 0.2 * abs(x)

