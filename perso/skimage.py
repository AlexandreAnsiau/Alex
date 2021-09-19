import copy

import matplotlib.pyplot as plt
import numpy as np
import skimage
import skimage.exposure
import skimage.io


def save_func(name_doc):
    """
    This function is input in other ones of this module. So it must not be use
    by user
    """

    from pathlib import Path

    path = "/Users/Alex/perso/files/skimage/"
    path = path + name_doc
    
    if Path(path).exists():
        print("This file name is already existing. Choose an other name.")
    else:
        plt.savefig(path)
        print(f"The absolut path of the saved file is {path}")


def frame(image, x1,x2,y1,y2, show=True, color="red", save=False, doc_title=None):
    """
    Display the image with the frame itself and the image inside the frame,
    return the image inside the frame.

    Parameters
    ----------
    image : np.array (skimage) or str (path of the image)
        Image must be a numpy matrix or str which is the absolut path of the
        picture in the computer
    x1, x2 : int
        Colums of the picture, x1 must be smaller than x2.
    y1, y2 : int
        Lines of the picture, y1 must be smaller than y2. 
    show : boolean, optional
        If the value of show is True, then the image will be show to the user,
        other way it will not be, default is True.
    color : str, optional
        The color of of the frame containing the area of the original picture.
    save : boolean, optional       
        if True, the image will be saved in /Users/Alex/perso/files directory,
        default is False
    doc_title : str, optional
        The name of the picture only if save parameter is True which is not the
        default option.

    Returns
    -------
    out : nd.array
        The nd.array containing between x1, x2, x3, x4 specify by user
    """
    try:
        
        if isinstance(image, str):
            image = skimage.io.imread(image)
            
            
        if show:
        
            plt.figure( figsize = (15,15))

            plt.subplot(1,2,1)
            plt.title("Image with frame")
            plt.imshow (image)
            plt.plot([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1], color=color)


            plt.subplot(1,2,2)
            plt.title("Result")
            plt.imshow(image[y1:y2,x1:x2])

            
            if save and doc_title :
                saveFunc(doc_title)
            elif save and doc_title == None:
                print("No name (docTitle) have been input.")

            plt.show()
    
        return image[y1:y2,x1:x2]
    
    
    except ValueError: 
        print(f"Erreur de valeurs:")
        print(f"Soit les x ou bien les y sont dans le mauvais ordre soit dépasse la taille de l'image")
        print(f"Axe0 : max = {image.shape[0]}  ; Axe1 : max = {image.shape[1]}")


def gray(image):
    """
    Returns the gray image.

    Parameters
    ----------
    image : nd.array or str
        The image must be a matrice or a string indicating the path of the
        image in the computer.

    Returns
    -------
    out : nd.array
        The gray version of the image
    """
    if isinstance(image, str):
        image = skimage.io.imread(image)
    gray = 0.2126 * image[:,:,0] + 0.7152 * image[:,:,1]  + 0.0722 * image[:,:,2]
    gray = gray.astype('uint8')
    return gray


def equalize(image, show=False):

    """
    permit to get more levels of intensity in the picture

    """   
    if isinstance(image, str):
        image = skimage.io.imread(image)
        
    image_original = copy.deepcopy(image)
    canal_image_original = image_original
    
    if len(image.shape) == 3:
        canal_image = np.zeros([image.shape[0], image.shape[1], image.shape[2]])
        number_canals = 3
        color = ["red", "green", "blue"]

        for i in range(number_canals):

            if (np.min(image_original[:,:,i]) != 0 or 
                np.max(image_original[:,:,i]) != 255):
                image[:,:,i] = image[:,:,i] - np.min(image[:,:,i])
                multi = 255 / np.max(image[:,:,i])
                canal_image[:,:,i] = image[:,:,i] * multi
                canal_image[:,:,i] = canal_image[:,:,i].astype('uint8')
                               
            elif (np.min(image_original[:,:,i]) == 0 and 
                np.max(image_original[:,:,i]) == 255):
                canal_image[:,:,i] = skimage.exposure.equalize_hist(image[:,:,i])
                canal_image[:,:,i] = canal_image[:,:,i] * 255
                canal_image[:,:,i] = canal_image[:,:,i].astype('uint8')
        
    elif len(image.shape) == 2:
        canal_image = np.zeros([image.shape[0], image.shape[1]])
        number_canals = 1
        color = ["gray"]
                    
        if np.min(image_original) != 0 or np.max(image_original) != 255:
            canal_image = image - np.min(image)
            multi = 255 / np.max(canal_image)
            canal_image = canal_image * multi
            canal_image = canal_image.astype('uint8')
                
                
        elif np.min(image_original) == 0 and np.max(image_original) == 255:
            canal_image = skimage.exposure.equalize_hist(image)
            canal_image = canal_image * 255
            canal_image = canal_image.astype('uint8')
            
    
    if show:
                
        for i in range(number_canals):
                
            plt.figure(figsize=(20,4))
       
            unique_original, count_original = np.unique(canal_image_original, return_counts=True)
            unique, count = np.unique(canal_image, return_counts=True)

            plt.subplot(1,2,1)
            plt.plot(unique_original, (count_original / sum(count_original)) * 100, color=color[i])                    
            plt.title(f"original {color[i]} canal")         
            plt.xlabel("population")
            plt.ylabel("density (%)")

            plt.subplot(1,2,2)

            plt.plot(unique, (count / sum(count)) * 100, color=color[i])
            plt.title(f"modify {color[i]} canal")
            plt.xlabel("population")
            plt.ylabel("density (%)")

            plt.show()

        
        plt.figure()
        
        if len(image.shape) == 2:
            plt.imshow(canal_image, "gray")
        else : 
            plt.imshow(canal_image)
        
        plt.show()
        
        return image


def orthogonal_symmetry(image, show=False):

    if isinstance(image, str):
        image = skimage.io.imread(image)

    image_orig = image

    if len(image_orig.shape) == 3:
        image = np.zeros([image_orig.shape[0], image_orig.shape[1], image_orig.shape[2]])
    else:
        image = np.zeros([image_orig.shape[0], image_orig.shape[1]])

    for i in range(image_orig.shape[1]):
        image[:,i] = image_orig[:,-i]

    image = image.astype('uint8')

    if show:

        plt.figure(figsize=(10,10))

        if len(image_orig.shape) == 3:

            plt.imshow(image)
        else :
            plt.imshow(image,"gray")

        plt.show()


    return image

    
