import matplotlib.pyplot as plt
import numpy as np


def log_normal(mean, sigma, show=False):
    """
    return x and y values (numpy.ndarray) according log normal equation
    Attntion float not accept due to x and y calculation. But this defaulr can
    be change.

    """

    try:
        
        if not isinstance(mean, int) and not isinstance(sigma, int):
            raise TypeError("mean and sigma must be int or float")

        minimum = mean - 3 * sigma
        maximum = mean + 3 * sigma
        
        x = np.linspace(minimum, maximum, (maximum-minimum) * 5)
        y = (1 / sigma * (2 * np.pi) ** (1 / 2)) * np.exp((-1 / 2) * ((x - mean) / sigma) ** 2) 

        if show:
            plt.figure()
            plt.plot(x, y)
            plt.show()
        return x, y

    except TypeError as e:
        print(e)


def log_normal_vs_hist(sample):

    """
    drawing of the log normal graph of the sample
    vs the histogram of the sample
    """

    sigma = np.std(sample)
    mean = np.mean(sample)

    plt.figure(figsize=(15, 5))
    
    # for logNormal curve
    x = np.linspace(np.min(sample), np.max(sample), (np.max(sample) - np.min(sample)) *4)
    y = (1 / sigma * (2 * np.pi) ** (1/2)) * np.exp((-1/2) * ((x-mean)/sigma) ** 2) 

    plt.title(f"moyenne : {mean} ; sigma : {sigma}")
    plt.xlabel("population")
    plt.ylabel("propability density").set_rotation(90)

    # for sample curve
    if isinstance(sample, np.ndarray):
        population, density = np.unique(sample, return_counts=True)
        density = density / sum(density)
        plt.plot(population, density, label="sample")
    else:
        plt.hist(sample, density=True, label="sample")
    
    plt.plot(x,y, label="log normal")

    plt.legend()

    plt.show()


def sample(characteristics, population):
    
    """create table of values including characteristics, population, 
    frequence_effectif, effectif_cumule, frequence_effectif_cumule

    Parameters
    ----------
    characteristics : list
        list of characteristics which are used to studied the population
    population : list
        list of the effectif of the population

    Returns
    -------
    pandas.core.frame.DataFrame
        table of values with 4 columns: characteristics, population, 
        frequence_effectif, effectif_cumule, frequence_effectif_cumule
    """
    
    import pandas as pd
    
    frequence_effectif = [(effectif / sum(population)) for effectif in population]
    effectif_cumule = [sum(population[:i+1]) for i in range(len(population))]
    frequence_effectif_cumule = [(effectif_cumule_part / max(effectif_cumule)) \
                                 for effectif_cumule_part in effectif_cumule]
    parameters_list = [characteristics, population, frequence_effectif, effectif_cumule, \
                       frequence_effectif_cumule]
    parameters_name_list = ["characteristics", "population", "frequence effectif", \
                            "effectif cumule", "frequence effectif cumule"]
    index_artificiel = [i for i in range(len(population))]
    study = pd.DataFrame({"index": index_artificiel})
    
    for column_name, values_list in zip(parameters_name_list, parameters_list):
        study[column_name] = values_list
        
    study = study.drop(columns="index")
    
    return study



    
