import random
from path import *

class Individual:

    count = 0
    points = []
    gene_length = 0

    def __init__(self, gene_list):
        if self.__class__.points == []:
            raise Exception("Set points using set_points function.")
        self.gene_list = gene_list
        self.fitness = -distance(self.points, self.gene_list)
        self.__class__.count += 1

    @classmethod
    def generate_individual(cls):
        path = list(range(len(cls.points)))
        random.shuffle(path)
        return Individual(path)
    
    @classmethod
    def set_points(cls, points):
        cls.points = points
        cls.gene_length = len(points)