import random
import matplotlib.pyplot as plt

# Crossover operation for real-encodings
def crossover_blend(g1, g2, alpha):
    shift = (1 + 2 * alpha) * random.random() - alpha
    new_g1 = (1 - shift) * g1 + shift * g2
    new_g2 = shift * g1 + (1 - shift) * g2
    return new_g1, new_g2

# Crossover operation for binary genes
def crossover_swap(g1, g2):
    return g2, g1

# Mutation operation for real-encodings
def mutation_deviation(g, mu, sigma):
    mutated_gene = g + random.gauss(mu, sigma)
    return mutated_gene

# Mutation operation for enums encoding geners
def mutation_enum(enums):
    return random.choice(enums)

# Tournament Selection with elite
# Picks individuals for tournament of 'size' and returns winners until we have a complete population 
def tournament_selection_with_elite(population, size, elites):
    winners = []
    sorted_population = sorted(population, key = lambda x: x.fitness, reverse = True)
    winners = sorted_population[:elites]
    for i in range(len(population) - elites):
        candidates = []
        for j in range(size):
            candidates.append(random.choice(population))
        winners.append(max(candidates, key = lambda candidate: candidate.fitness))
    assert len(winners) == len(population)
    return winners

# Crossover procedure across a population
def crossover_procedure(population, method, prob):
    crossed_offspring = []
    for x, y in zip(population[0::2], population[1::2]):
        if random.random() < prob:
            child1, child2 = method(x, y)
            crossed_offspring.append(child1)
            crossed_offspring.append(child2)
        else:
            crossed_offspring.append(x)
            crossed_offspring.append(y)
    return crossed_offspring

# Mutation procedure across a population
def mutation_procedure(population, method, prob):
    mutated_offspring = []
    for x in population:
        if random.random() < prob:
            mutant = method(x)
            mutated_offspring.append(mutant)
        else:
            mutated_offspring.append(x)
    return mutated_offspring

# Computes statistics across a population
def get_stats(population, best_ind, fit_avg, fit_best, fit_best_ever):
        best_of_generation = max(population, key = lambda ind: ind.fitness)
        if best_ind.fitness < best_of_generation.fitness:
            best_ind = best_of_generation
        fit_avg.append(sum([ind.fitness for ind in population]) / len(population))
        fit_best.append(best_of_generation.fitness)
        fit_best_ever.append(max(fit_best + fit_best_ever))

        return best_ind, fit_avg, fit_best, fit_best_ever

# Plots statistics
def plot_stats(fit_avg, fit_best, fit_best_ever, title):
    plt.plot(fit_avg, label = "Average Fitness of Gen")
    plt.plot(fit_best, label = "Best Fitness of Gen")
    plt.plot(fit_best_ever, label = "Best Fitness")
    plt.title(title)
    ax = plt.gca()
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    plt.legend(loc = "lower right")
    plt.show()