def number_words(path, name):
    """
    count number of words in a 'txt' file

    Parameters
    ----------
    path : str
        location of the file on the computer
    name : str
        name of the file

    Returns
    -------
    int
        number of words content in the file
    """
    
    from pathlib import Path
    
    name = path + "/" + name
    name = Path(name)
    
    try :
        with open(name, "r", encoding="utf8") as file:
            line_split_list = [line.split() for line in file] 
            number_words_in_line = [len(i) for i in line_split_list]
            sum_words = sum(number_words_in_line)
            
        return sum_words

    except FileNotFoundError:
        print("The file can not be found.")