import random
import copy
from utils import *
from individual import *

# Class for the genetic algorithm
class Genetic:

    # Constructor which accepts hyperparameters
    def __init__(self, population_size, crossover_rate, mutation_rate, max_generations):
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
    
    # Crossover of two individuals (specific to this problem)
    def crossover(self, parent1, parent2):
        prob = self.crossover_rate
        a1, b1, x1, n1, func1 = copy.deepcopy(parent1.gene_list)
        a2, b2, x2, n2, func2 = copy.deepcopy(parent2.gene_list)

        if random.random() < prob:
            a1, a2 = crossover_blend(a1, a2, 0.3)
        if random.random() < prob:
            b1, b2 = crossover_blend(b1, b2, 0.5)
        if random.random() < prob:
            x1, x2 = crossover_blend(x1, x2, 1)
        if random.random() < prob:
            n1, n2 = crossover_blend(n1, n2, 0.5)
        if random.random() < prob:
            func1, func2 = crossover_swap(func1, func2)

        return Individual([a1, b1, x1, n1, func1]), Individual([a2, b2, x2, n2, func2])
    
    # Mutation of two Individuals (specific to this problem)
    def mutation(self, individual):
        prob = self.mutation_rate
        a, b, x, n, func = copy.deepcopy(individual.gene_list)

        if random.random() < prob:
            a = mutation_deviation(a, 0, .2)
        if random.random() < prob:
            b = mutation_deviation(b, 0, .2)
        if random.random() < prob:
            x = mutation_deviation(x, 0, 1)
        if random.random() < prob:
            n = mutation_deviation(n, 0, 1)
        if random.random() < prob:
            func = mutation_enum(individual.func_set)
        
        return Individual([a, b, x, n, func])
    
    # Selects offspring using tournament selection
    # Tournaments are of size 5 and the number of elites is 3
    def selection(self, population):
        return tournament_selection_with_elite(population, size = 5, elites = 3)
    
    # Generates and returns a random population
    def get_population(self):
        return [Individual() for _ in range(self.population_size)]

    # Runs the genetic algorithm
    def run(self):

        # Generates the initial population
        population = self.get_population()
        
        # Compute intial metrics
        fit_list = [x.fitness for x in population]
        fit_avg = [sum(fit_list) / len(fit_list)]
        fit_best = [max(fit_list)]
        fit_best_ever = [max(fit_list + fit_best)]
        best_ind = random.choice(population)
        
        # Declare generation counter
        generation_number = 0

        # Begin evolutionary process
        while generation_number < self.max_generations:

            # Increment generation counter
            generation_number += 1
            
            # SELECTION
            offspring = self.selection(population)

            # CROSSOVER
            crossed_offspring = crossover_procedure(offspring, self.crossover, self.crossover_rate)

            # MUTATION
            mutated_offspring = mutation_procedure(crossed_offspring, self.mutation, self.crossover_rate)

            # The future generation
            population = mutated_offspring.copy()

            # Compute the metrics for the new generation
            best_ind, fit_avg, fit_best, fit_best_ever = get_stats(population, best_ind, fit_avg, fit_best, fit_best_ever)
        
        # Output the results of the algorithm
        plot_stats(fit_avg, fit_best, fit_best_ever, "Genetic Algorithm Stats")
        print(f'Maximum: {best_ind.fitness}')
        print(f'Best Individual : {best_ind.gene_list}')
        print(f'Number of Individuals: {Individual.counter}')

# Runs the algorithms
if __name__ == '__main__':
    random.seed(57)
    g = Genetic(population_size = 200, crossover_rate = 0.8, mutation_rate = 0.2, max_generations = 1000)
    g.run()

        


