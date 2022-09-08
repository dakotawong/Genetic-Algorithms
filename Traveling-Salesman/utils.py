from individual import *
from math import copysign, nan
import random

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


def selection_rank_with_elite(individuals, elite_size = 0):
    sorted_individuals = sorted(individuals, key = lambda ind: ind.fitness, reverse = True)
    rank_distance = 1 / len(individuals)
    ranks = [(1 - i * rank_distance) for i in range(len(individuals))]
    ranks_sum = sum(ranks)
    selected = sorted_individuals[0:elite_size]

    for i in range(len(sorted_individuals) - elite_size):
        shave = random.random() * ranks_sum
        rank_sum = 0
        for i in range(len(sorted_individuals)):
            rank_sum += ranks[i]
            if rank_sum > shave:
                selected.append(sorted_individuals[i])
                break

    return selected

def ordered_crossover_fitness_driven(parent1, parent2):
    p1_gene, p2_gene = parent1.gene_list, parent2.gene_list

    start, end = sorted([random.randrange(len(p1_gene)) for _ in range(2)])

    zero_shift = min(p1_gene)
    length = len(p1_gene)
    
    child1_gene, child2_gene = [nan] * length, [nan] * length

    t1, t2 = [x - zero_shift for x in p1_gene], [x - zero_shift for x in p2_gene]

    spaces1, spaces2 = [True] * length, [True] * length
    for i in range(length):
        if i < start or i > end:
            spaces1[t2[i]] = False
            spaces2[t1[i]] = False

    j1, j2 = end + 1, end + 1
    for i in range(length):

        if not spaces1[t1[(end + 1 + i) % length]]:
            child1_gene[j1 % length] = t1[(end + 1 + i) % length]
            j1 += 1 

        if not spaces2[t2[(i + end + 1) % length]]:
            child2_gene[j2 % length] = t2[(end + 1 + i) % length]
            j2 += 1
    
    for i in range(start, end + 1):
        child1_gene[i], child2_gene[i] = t2[i], t1[i]
    
    child1 = Individual([x + zero_shift for x in child1_gene])
    child2 = Individual([x + zero_shift for x in child2_gene])

    candidates = [child1, child2, parent1, parent2]
    best = sorted(candidates, key = lambda x: x.fitness, reverse = True)

    return best[0:2]

def crossover_fitness_driven_order(ind1, ind2):
    p1, p2 = ind1.gene_list, ind2.gene_list
    zero_shift = min(p1)
    length = len(p1)
    start, end = sorted([random.randrange(length) for _ in range(2)])
    c1, c2 = [nan] * length, [nan] * length
    t1, t2 = [x - zero_shift for x in p1], [x - zero_shift for x in p2]

    spaces1, spaces2 = [True] * length, [True] * length
    for i in range(length):
        if i < start or i > end:
            spaces1[t2[i]] = False
            spaces2[t1[i]] = False

    j1, j2 = end + 1, end + 1
    for i in range(length):
        if not spaces1[t1[(end + i + 1) % length]]:
            c1[j1 % length] = t1[(end + i + 1) % length]
            j1 += 1

        if not spaces2[t2[(i + end + 1) % length]]:
            c2[j2 % length] = t2[(i + end + 1) % length]
            j2 += 1

    for i in range(start, end + 1):
        c1[i], c2[i] = t2[i], t1[i]

    child1 = Individual([x + zero_shift for x in c1])
    child2 = Individual([x + zero_shift for x in c2])

    candidates = [child1, child2, ind1, ind2]
    best = sorted(candidates, key = lambda ind: ind.fitness, reverse = True)

    return best[0:2]

def mutation_fitness_driven_shift(ind, max_tries = 3):
    for t in range(0, max_tries):
        mut = copy.deepcopy(ind.gene_list)
        pos = random.sample(range(0, len(mut)), 2)
        g1 = mut[pos[0]]
        dir = int(copysign(1, pos[1] - pos[0]))
        for i in range(pos[0], pos[1], dir):
            mut[i] = mut[i + dir]
        mut[pos[1]] = g1
        mutated = Individual(mut)
        if mutated.fitness > ind.fitness:
            return mutated
    return ind

def stats(population, best_ind, fit_avg, fit_best):
    best_of_generation = max(population, key = lambda ind: ind.fitness)
    if best_ind.fitness < best_of_generation.fitness:
        best_ind = best_of_generation
    fit_avg.append(sum([ind.fitness for ind in population]) / len(population))
    fit_best.append(best_ind.fitness)

    return best_ind, fit_avg, fit_best

def plot_stats(fit_avg, fit_best, title):
    plt.plot(fit_avg, label = "Average Fitness of Generation")
    plt.plot(fit_best, label = "Best Fitness")
    plt.title(title)
    plt.legend(loc = "lower right")
    plt.show()