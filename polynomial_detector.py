class RandomPolyCreator():
    """This class aims to create lists of points x and y according to a 
    random polynomial.
    """
    
    def __init__(self, mode="normal"):
        import numpy as np
        self.mode_dico = {"normal": 1, "difficile": 2, "très difficile": 3}
        self.mode = self.mode_dico[mode] 
        self.x = np.array([i for i in range(-10, 11)])
        self.poly = self.poly()
        self.y = self.y_creator()
    
    def poly(self,):
        import random
        import numpy as np
        return np.poly1d([random.randint(1, 4) for _ in range(random.randint(1, 5))])      
        
    def y_creator(self,):
        import random
        import numpy as np
        y = self.poly(self.x)
        error_max = self.mode*10**(len(self.poly)-1) if len(self.poly) > 0 else 0 
        print(f"Error max:{error_max}")
        errors_matrice = np.random.randint(-error_max, error_max+1, size=len(self.x)) 
        return y - errors_matrice
    

class PolyDetector:
    """This class aims to get the original polynomial of a curve which y 
    points values suffer error.
    """
    
    def __init__(self, sample):
        self.x, self.y = sample.x, sample.y
        self.poly = self.poly()
        self.graph()
    
    def poly(self,):
        import numpy as np
        dico = {}
        for poly_degree in range(0, 5):
            a = np.polyfit(self.x, self.y, poly_degree)
            poly = np.poly1d(a)
            if (len(a) > 2 and (a[0] > 1 or a[0] < -1)) or len(a) <= 2:
                print(a)
                poly_valid = poly           
        return poly_valid
    
    def graph(self,):
        import matplotlib.pyplot as plt
        print(self.poly)
        plt.figure()
        plt.plot(self.x, self.y)
        plt.plot(self.x, self.poly(self.x), label=len(self.poly))
        plt.legend()
        plt.show()

PolyDetector(RandomPolyCreator("très difficile"))    
