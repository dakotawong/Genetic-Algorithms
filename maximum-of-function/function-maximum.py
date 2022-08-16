from random import random, gauss, choice, uniform
from typing import List
import numpy as np
import matplotlib.pyplot as plt

# Import some functions required for GA
from utils import *

# Function we are trying to find the maximum of
def func(x):
    return np.sin(x) - 0.2 * abs(x)

# Class for Individuals
class Individual:

    def __init__(self, gene):
        self.gene = gene
        self.fitness = func(gene)

# Genetic Class
class Genetic:

    # Constructor that accepts algorithm parameters
    def __init__(self, population_size = 10, crossover_rate = 0.8, mutation_rate =0.1, max_generations = 10):
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
    
    # Crossover function used to create child genomes
    def crossover(self, parent1, parent2):
        child1, child2 = crossover_blend(parent1.gene, parent2.gene, 1)
        return Individual(child1), Individual(child2)
    
    # Mutate function used to mutate genomes
    def mutate(self, individual):
        mutated_gene = mutate_gaussian(individual.gene, 0, 1)
        return Individual(mutated_gene)
    
    # Performs tournament selection on population
    # Returns the selected individuals
    def select(self, population):
        return tournament_selection(population, size = 3)
    
    # Creates a random individual with a random gene between -10 and 10
    def create_random(self):
        return Individual(uniform(-10, 10))
    
    # Runs the genetic algorithm
    def run(self):

        # Generates the initial population
        population = []
        generation_num = 0
        for i in range(self.population_size):
            population.append(self.create_random())
        plot_population(population, 0)

        # Iterates through generations
        while generation_num < self.max_generations:
            generation_num += 1

            # Selection (selects individuals using tournament selection)
            offspring = self.select(population)

            # Crossover (used to generates new offspring)
            crossed_offspring = []
            for x, y in zip(offspring[0::2], offspring[1::2]): # slides window of length 2 across population
                if random() < self.crossover_rate:
                    child1, child2 = self.crossover(x, y)
                    crossed_offspring.append(child1)
                    crossed_offspring.append(child2)
                else:
                    crossed_offspring.append(x)
                    crossed_offspring.append(y)
            
            # Mutation (used to mutate some of the offspring)
            mutated_offspring = []
            for individual in crossed_offspring:
                if random() < self.mutation_rate:
                    mutated_offspring.append(self.mutate(individual))
                else:
                    mutated_offspring.append(individual)
            population = mutated_offspring

            # Print the population
            plot_population(population, generation_num)

if __name__ == "__main__":
    genetic = Genetic()
    genetic.run()


