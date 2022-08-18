import random
from itertools import compress
from item import *

# Class for the Individuals
class Individual():

    # Paramters for the class
    counter = 0
    weight_limit = None
    items = None

    # Class method to set the weight
    @classmethod
    def set_weight(cls, weight):
        cls.weight_limit = weight

    # Class method to set the items that will be considered
    @classmethod
    def set_items(cls, items):
        cls.items = items

    # Class method for generating a random population
    # parameters zeros and ones are used to control the distribution of 0's and 1's in the generated genomes
    # Ideally we want more 0's than 1's to prevent the individuals beign over the weight limit
    @classmethod
    def generate_individual(cls, zeros = 1, ones = 1):
        s = ([0] * zeros) + ([1] * ones)
        return Individual([random.choice(s) for _ in cls.items])
    
    # Constructor for an individual
    def __init__(self, gene_list):
        self.gene_list = gene_list
        self.fitness = self.fitness(gene_list)
        self.__class__.counter += 1

    # Returns the fitness of an individual
    def fitness(self, gene_list):
        weight = self.weight()
        if weight > self.__class__.weight_limit:
            return 0
        else:
            return sum([i.value for i in compress(self.__class__.items, gene_list)])
    
    # Returns the total wieght of an individual
    def weight(self):
        return sum([i.weight for i in compress(self.__class__.items, self.gene_list)])

    
