import numpy as np
import matplotlib.pyplot as plt
from black_box import *

# values for each parameter
a_range = np.arange(0, 1, 0.1)
b_range = np.arange(0, 1, 0.1)
x_range = np.arange(-100, 100, 0.2)
n_range = np.arange(0, 20, 1)
func_range = ['sin', 'cos']

# Track results
maximum = black_box(a_range[0], b_range[0], x_range[0],
            n_range[0], func_range[0])
counter = 0
results = []

# Begin Brute force search
for a in a_range:
    for b in b_range:
        for x in x_range:
            for n in n_range:
                for func in func_range:
                    counter += 1
                    val = black_box(a, b, x, n, func)
                    if val > maximum:
                        maximum = val
                    results.append(maximum)

# Plot results
plt.plot(results, label = "Best Fitness")
plt.title("Brute Force")
ax = plt.gca()
ax.set_xlabel("Individuals")
ax.set_ylabel("Fitness")
plt.legend(loc = "lower right")
plt.show()

# Print Final Solution (Considers 4,000,000 individuals )
print(f"The best fintess was {maximum}")
print(f"The total individuals considered was: {counter}")


