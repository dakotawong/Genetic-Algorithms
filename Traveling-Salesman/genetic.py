import random
from individual import * 
from utils import *
from path import *

class Genetic:

    def __init__(self, population_size, crossover_rate, mutation_rate , max_generations):
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations

    def generate_population(self):
        return [Individual.generate_individual() for _ in range(self.population_size)]

    def selection(self, population, size, elites):
        return tournament_selection_with_elite(population, size = size, elites=elites)
        #return selection_rank_with_elite(population, elite_size= elites)
    
    def crossover(self, population):
        crossed_offspring = []
        for x, y in zip(population[0::2], population[1::2]):
            if random.random() < self.crossover_rate:
                child1, child2 = ordered_crossover_fitness_driven(x, y)
            else:
                child1, child2 = x, y
            crossed_offspring.append(child1)
            crossed_offspring.append(child2)
        return crossed_offspring
    
    def mutation(self, population):
        mutants = []
        for ind in population:
            if random.random() < self.mutation_rate:
                mutant = mutation_fitness_driven_shift(ind)
            else:
                mutant = ind
            mutants.append(mutant)
        return mutants
    
    def run(self):

        population = self.generate_population()

        fit_list = [ind.fitness for ind in population]
        fit_avg = [sum(fit_list) / len(fit_list)]
        fit_best = [max(fit_list)]
        best_ind = random.choice(population)

        generation_number = 0

        while generation_number < self.max_generations:

            generation_number += 1

            offspring = self.selection(population, size = 10, elites = 1)

            crossed_offspring = self.crossover(offspring)

            mutated_offspring = self.mutation(crossed_offspring)

            population = mutated_offspring

            best_ind, fit_avg, fit_best = stats(population, best_ind, fit_avg, fit_best)

            print(f"Generation {generation_number}: {fit_avg[-1]}")
        
        plot_stats(fit_avg, fit_best, "TSP: US Capitals")
        return best_ind

if __name__ == "__main__":

    random.seed(43)

    points = us_capitals()
    Individual.set_points(points)

    g = Genetic(population_size = 300, crossover_rate = 0.8, mutation_rate = 0.4, max_generations = 400)
    best_individual = g.run()

    plot_path(points, best_individual.gene_list)