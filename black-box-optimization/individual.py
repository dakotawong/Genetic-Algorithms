import random
from black_box import *

# Class to represent the individuals
class Individual:

    # Params for all individuals
    func_set = ['sin', 'cos']
    n_set = range(0,21)
    counter = 0

    # Constructor for individuals
    # If no genes are specified a randomized indiviudal is created
    # Otherwise uses the genes to generate an individual
    def __init__(self, genes = None):
        
        # Increment the counter of TOTAL individuals
        self.__class__.counter += 1

        if genes == None: 
            # Creates random individual
            self.gene_list = [
                random.uniform(0, 1),
                random.uniform(0, 1),
                random.uniform(-10, 10),
                random.choice(self.n_set),
                random.choice(self.func_set)
            ]
        else:
            # Generates individual according to genes
            a_raw, b_raw, x_raw, n_raw, func_name = genes
            self.gene_list = [
                self.constraint(a_raw, 0, 1),
                self.constraint(b_raw, 0, 1),
                self.constraint(x_raw, -100, 100),
                self.closest(n_raw, self.n_set),
                func_name
            ]
        a, b, x, n ,func_name = self.gene_list

        # Compute the fitness of the individual
        self.fitness = black_box(a, b, x, n, func_name)
    
    # Function to enforce parameter constraints
    def constraint(self, g, lower, upper):
        return max(min(g, upper), lower)

    # Function for selecting discretely encoded genes
    def closest(self, value, value_list):
        return min(value_list, key = lambda x : abs(x - value))