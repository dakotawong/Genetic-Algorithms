import matplotlib.pyplot as plt
from genetic import *
from item import *

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
# Define the hyperparameters
g = Genetic(population_size = 20, crossover_rate = 0.7, mutation_rate = 0.2, max_generations = 40)

# Monte-Carlos
results = []
for _ in range(100):
    best = g.run(verbose = False)
    results.append(best.fitness)

# Plot results
avg_fitness = sum(results) / len(results)
plt.plot(results, label='best individual')
plt.title('Monte-Carlos Simulation')
plt.axhline(y = avg_fitness, color = 'r', linestyle = '-', label='avgerage fitness')
ax = plt.gca()
ax.set_xlabel("Iteration")
ax.set_ylabel("Best Fitness")
plt.legend()
plt.show()