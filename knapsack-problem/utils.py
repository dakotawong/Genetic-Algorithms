import random
import matplotlib.pyplot as plt

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
    plt.plot(fit_best_ever, label = "Best Fitness", linestyle="--")
    plt.title(title)
    ax = plt.gca()
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    plt.legend(loc = "lower right")
    plt.show()