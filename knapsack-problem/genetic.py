from audioop import cross
from inspect import indentsize
import random
from individual import *
from utils import *

class Genetic:

    # Constructor which accepts hyperparameters
    def __init__(self, population_size, crossover_rate, mutation_rate, max_generations):
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations

    # Crossover operator between to parent individuals
    # In this case we used single-point mutation driven crossover
    def crossover_operation(self, parent1, parent2):
        gene1, gene2 = parent1.gene_list, parent2.gene_list
        index = random.randint(1, len(gene1)-1)
        new_gene1 , new_gene2 = gene1, gene2
        new_gene1[index:] = gene2[index:]
        new_gene2[:index] = gene1[:index]
        child1, child2 = Individual(gene1), Individual(gene2)
        candidates = [child1, child2, parent1, parent2]

        best = sorted(candidates, key = lambda ind: ind.fitness, reverse = True)

        return best[0:2]
    
    # Mutation Operator for an individual
    # In this case we used a bit-flip fitness driven mutator
    # Parameter 'attempts' specifies how many times we try to mutated a fitter individual.
    # If we exceed the 'attempts' limit just return the unmutated individual
    def mutation_operation(self, individual, attempts = 3):
        for _ in range(attempts):
            gene_list = individual.gene_list
            index = random.randint(0, len(gene_list) - 1)
            gene_list[index] = (gene_list[index] + 1) % 2
            mutant = Individual(gene_list)
            if individual.fitness < mutant.fitness:
                return mutant
        return individual

    # Generates a random population of self.population_size
    def generate_population(self,):
        return [Individual.generate_individual(zeros = 10, ones = 1) for _ in range(self.population_size)]

    # Selection process which uses tournament selection with elite
    # Tournaments are of size 6 and there are 3 elites
    # Returns the selected individuals
    def selection(self, population):
        return tournament_selection_with_elite(population, size=6, elites=3)

    # Crossover procedure over a population
    # Returns the crossed offspring of the input population
    def crossover(self, population):
        crossed_offspring = []
        for p1, p2 in zip(population[0::2], population[1::2]):
            if random.random() < self.crossover_rate:
                c1, c2 = self.crossover_operation(p1, p2)
                crossed_offspring.append(c1)
                crossed_offspring.append(c2)
            else:
                crossed_offspring.append(p1)
                crossed_offspring.append(p2)
        return crossed_offspring
    
    # Mutation procedure over a population
    # Returns the mutated individuals of the input population
    def mutation(self, population):
        mutated_offspring = []
        for ind in population:
            if random.random() < self.mutation_rate:
                mutant = self.mutation_operation(ind, attempts = 3)
                mutated_offspring.append(mutant)
            else:
                mutated_offspring.append(ind)
        return mutated_offspring
    
    # Runs the genetic algorithm
    def run(self, verbose = True):

        # Generate initial population
        population = self.generate_population()

        # Checks the average weight of the initial population
        if verbose:
            avg_weight = sum([ind.weight() for ind in population]) / len(population)
            print(f"Average Weight: {avg_weight} kg")

        # Compute metrics for initial population
        fit_list = [ind.fitness for ind in population]
        fit_avg = [sum(fit_list) / len(fit_list)]
        fit_best = [max(fit_list)]
        fit_best_ever = [max(fit_best + fit_list)]
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
            crossed_offspring = self.crossover(offspring)

            # MUTATION
            mutated_offspring = self.mutation(crossed_offspring)

            # Next generation
            population = mutated_offspring
            
            # Compute metrics for the next generation
            best_ind, fit_avg, fit_best, fit_best_ever = get_stats(population, best_ind, fit_avg, fit_best, fit_best_ever)

        if verbose:
            # Plot the metrics from the algorithms
            plot_stats(fit_avg, fit_best, fit_best_ever, "Knapsack Problem")

            # Print the solution
            print("############################################################################")
            items_packed = [item.name for item in compress(best_ind.items, best_ind.gene_list)]
            print(f"Items Packed: {items_packed}")
            print(f"Value: ${best_ind.fitness}")
            print(f"Weight: {best_ind.weight()} kg")
            print(f'Number of Individuals: {Individual.counter}')
            print("############################################################################")

        # Returns the best individual
        return best_ind

if __name__ == "__main__":
    
    random.seed(28)

    # Items to consider in the knapsack problem
    items = [
        Item('laptop', 3, 300),
        Item('book', 2, 15),
        Item('radio', 1, 30),
        Item('tv', 6, 230),
        Item('potato', 5, 7),
        Item('brick', 3, 1),
        Item('bottle', 1, 2),
        Item('camera', 0.5, 280),
        Item('smartphone', 0.1, 500),
        Item('picture', 1, 170),
        Item('flower', 2, 5),
        Item('chair', 3, 4),
        Item('watch', 0.05, 500),
        Item('boots', 1.5, 30),
        Item('radiator', 5, 25),
        Item('tablet', 0.5, 450),
        Item('printer', 4.5, 170)
    ]

    # Set the items
    Individual.set_items(items)

    # Set the weight limit
    Individual.set_weight(10)

    # Run the algorithms
    g = Genetic(population_size = 20, crossover_rate = 0.7, mutation_rate = 0.2, max_generations = 40)
    g.run()
