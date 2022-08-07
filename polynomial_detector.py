import random

import matplotlib.pyplot as plt
import numpy as np


class RandomPolynomialCreator():
    """This class aims to create lists of points x and y according to a 
    random polynomial.
    """
    
    def __init__(self, difficulty="normal"):
        self.difficulty = difficulty
        self.error_multiplicator = self.get_error_multiplicator()
        self.x = np.array([i for i in range(-10, 11)])
        self.random_polynomial = self.create_random_polynomial()
        self.y = self.generate_errors()
        
    def get_error_multiplicator(self):
        difficulty_dico = {"normal": 1, "hard": 2, "very hard": 3}
        return difficulty_dico[self.difficulty]
    
    def create_random_polynomial(self):
        return np.poly1d([random.randint(1, 4) for _ in range(random.randint(1, 5))])      
        
    def generate_errors(self):
        y = self.random_polynomial(self.x)
        error_max = self.error_multiplicator*10**(len(self.random_polynomial)-1) if len(self.random_polynomial) > 0 else 0 
        errors_matrice = np.random.randint(-error_max, error_max+1, size=len(self.x)) 
        return y - errors_matrice
    

class PolynomialFinder:
    """This class aims to get the original polynomial of a curve which y 
    points values suffer error.
    """
    
    def __init__(self, sample):
        self.x, self.y = sample.x, sample.y
        self.polynomial_found = self.find_polynomial()
    
    def find_polynomial(self):
        dico = {}
        for poly_degree in range(0, 5):
            a = np.polyfit(self.x, self.y, poly_degree)
            poly = np.poly1d(a)
            if (len(a) > 2 and (a[0] > 1 or a[0] < -1)) or len(a) <= 2:
                poly_valid = poly           
        return poly_valid
    
    def show_graph(self, figsize=None):
        plt.figure(figsize=figsize)
        plt.plot(self.x, self.y, label="curve with errors")
        plt.plot(self.x, self.polynomial_found(self.x), label=f"polynomial found: {len(self.polynomial_found)}")
        plt.legend()
        plt.show()
        
    def __str__(self):
        return str(self.polynomial_found)

polynomial = PolynomialFinder(RandomPolynomialCreator("very hard"))

print(polynomial.polynomial_found)
polynomial.show_graph(figsize=(10, 8))
