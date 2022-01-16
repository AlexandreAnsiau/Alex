from random import randint
import re
from string import ascii_letters, punctuation, digits
from time import sleep

import pandas as pd


LOW_SPEED = True
DEBUG = True


class Towns:
    
    def __init__(self, towns, modification_num=0):
        self.towns_dict = self.towns_dict(towns)
        
    def towns_dict(self, towns):
        import pandas as pd
        if isinstance(towns, pd.core.frame.DataFrame):
            towns = {k: v for k, v in zip(towns["town"], towns["num"])}
        elif isinstance(towns, dict):
            pass
        else:
            raise ValueError("Erreur: votre valeur pour l'instance Towns n'est pas valide")
        return towns

        
class Paginator:
    page_tag = ["pagi_actif", "pagi_passif"]
    urls = []
    
    def __init__(self, url):
        self.pages = self.pages(url)
        self.url = url
    
    def __iter__(self,):
        from bs4 import BeautifulSoup as bs
        import requests
        urls = set(Paginator.urls)
        for page in self.pages:
            url = f"{self.url}{page}"
            if url in urls:
                pass
            else:
                webpage = requests.get(f"{self.url}{page}")
                soup = bs(webpage.content)
                yield soup, f"{self.url}{page}"
        
    def pages(self, url):
        import re
        from bs4 import BeautifulSoup as bs
        import requests
        webpage = requests.get(url)
        soup = bs(webpage.content)
        pages = soup.find_all(attrs={"class": ["pagi_actif", "pagi_passif"]})
        pages = [int(page.get_text()) for page in pages
                if re.match(r"\d+", page.get_text())]
        return pages if len(pages) > 0 else [1] 

        
class Divisions:
    division_tag = "newBlock"
    
    def __init__(self, html):
        self.divisions = html.body.find_all(attrs={"class": "newBlock"}) 
                          
    def __iter__(self,):
        for division in self.divisions:
            yield division

    
class Division:
    import re
    
    price_tag = "RR_prix columns text-left small-12 left"
    size_tag = "floorSize"
    type_tag = "RR_detail1"
    houses = []
    flats = []
    lands = []
    total = []
    
    def __init__(self, division, url, town=None):
        self.division = division 
        self.url = url
        self.town = town
        self.price = self.price()
        self.size = self.size()
        self.new = self.new()
        self.type_location = self.type_location()
        
    def price(self):
        import re
        price_str = self.division.find(attrs={"class": Division.price_tag})
        if price_str:
            price_str = price_str.get_text()
            if re.search("€", price_str):
                return int(re.sub("€| ", "", price_str))
        return None
    
    def size(self):
        size_str = self.division.find(attrs={"itemprop": Division.size_tag})
        if size_str:
            return int(size_str.get_text())
        else:
            return None
    
    def new(self):
        new_str = self.division.find(attrs={"class": Division.type_tag}).get_text()
        if {"nouveau", "neuf", "récent"} & set(new_str.split(" ")):
            return True
        else:
            return False
    
    def type_location(self):
        type_location_str = self.division.find(attrs={"class": Division.type_tag}).get_text()
        Division.total.append(self)
        for type_location, list_type in zip(["maison", "appartement", "terrain"],
                                       [Division.houses, Division.flats, Division.lands]):
            if type_location in type_location_str.lower():
                list_type.append(self)
                return type_location
        return None

    
class Graph:
    def __init__(self, table, regression_curve=True):
        self.graph = self.graph(table, regression_curve)
    
    def graph(self, table, regression_curve):
        import matplotlib.pyplot as plt
        import numpy as np
        towns = table["town"].unique()
        plt.figure(figsize=(20, 10))
        for town in towns:
            table_town = table.loc[table["town"]==town]
            plt.scatter(table_town["price"], table_town["size"], label=town)
            if regression_curve:
                a, b = np.polyfit(table_town["price"], table_town["size"], 1)
                plt.plot(table_town["price"], a*table_town["price"] + b, label=f"{town} regression", linestyle="--")
        plt.xlabel("price [euro]")
        plt.ylabel("surface [m^2]")
        plt.legend()
        plt.show()

towns = pd.read_excel("/Users/Alex/Desktop/paca.xlsx")
towns = Towns(towns[(towns["town"]=="Antibes") | (towns["town"]=="Monaco")]).towns_dict

punctuation = re.sub(r"\\|\"|\'|\`", "",punctuation)
caracter = ascii_letters + punctuation + digits

for town in towns:
    sentence = "ivwtx@@[FGH_zoxIFFLyOwMNzRUGPISZZhO#l*VS.+r8XU/Y&x;*=I;&?/L:}Cs80?d1244^|!GqASk8cd7m.77jhsf)selk_"
    url = "".join([caracter[(caracter.index(letter)-num-1)%len(caracter)] for num, letter in enumerate(sentence)])
    url = re.sub("balise", f"{towns[town]-6000+2035}", url)
    for page, url_page in Paginator(url):
        try:
            for division in Divisions(page):
                if DEBUG:
                    print(Division(division, url_page, town).type_location)
        except ValueError:
            pass
        if LOW_SPEED:
            sleep(randint(20, 30))

columns = ["price", "size", "town", "type_location", "new", "url"]
data = {k: [] for k in columns}
table = pd.DataFrame(data)
for location in Division.total:
    if location.price and location.size:
        location_data = {k: [location.__dict__[k]] for k in columns}
        table = pd.concat([table, pd.DataFrame(location_data)], ignore_index=True)
Graph(table, regression_curve=True)
