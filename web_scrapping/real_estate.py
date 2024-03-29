import re

from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import pandas as pd
from string import ascii_letters, digits, punctuation
import requests

towns = pd.read_excel("paca.xlsx")
len_file = len(towns)

nums = [towns['num'].values[i] - 6000 + 2035 for i in range(len_file)]
print(type(nums[0]))

names_towns = [towns["town"].values[i] for i in range(len_file)]

punctuation = re.sub(r"\\|\"|\'|\`", "",punctuation)
caracter = ascii_letters + punctuation + digits
sentence = "ivwtx@@[FGH_zoxIFFLyOwMNzRUGPISZZhO#l*VS.+r8XU/Y&x;*=I;&?/L:}Cs80?d1244^|!GqASk8cd7m.77jhsf)selk_"
url_pattern = "".join([caracter[(caracter.index(letter)-num-1)%len(caracter)] for num, letter in enumerate(sentence)])

urls = [re.sub("balise", str(num), url_pattern) for num in nums]

plt.figure(figsize=(10, 10))

for name_town, url in zip(names_towns, urls):
    
    prices = []
    sizes = []

    page = 1
    webpage = requests.get(f"{url}{page}")
    soup = bs(webpage.content)
    pages = [int(page.get_text()) for page in soup.find_all(attrs={"class": ["pagi_actif", "pagi_passif"]})]

    for page in range(min(pages), max(pages)):
        webpage = requests.get(f"{url}{page}")
        soup = bs(webpage.content)
        body = soup.body
        divisions = body.find_all(attrs={"class": "newBlock"})
        informations = [(division.find(attrs={"itemprop": "floorSize"}).get_text(),
                         division.find(attrs={"class": "RR_prix"}).get_text()) \
                        for division in divisions \
                        if (division.find(attrs={"itemprop": "floorSize"}) is not None and
                            division.find(attrs={"class": "RR_prix"}) is not None)]


        for size, price in informations:
            if len(price) <= 11:
                sizes.append(size)
                prices.append(price)
            else:
                pass

    list_prices = [int(re.compile(r"[^0-9]").sub("", price)) for price in prices]
    list_sizes = [int(re.compile(r"[^0-9]").sub("", size)) for size in sizes]

    if len(list_prices) == len(list_sizes):
        flat = pd.DataFrame({"prices": list_prices, "sizes": list_sizes})
    else:
        print("They do not have the same size")

    plt.scatter(flat["prices"], flat["sizes"], label=name_town)
    
plt.xlabel("price [euro]")
plt.ylabel("surface [m^2]")
plt.legend()
plt.show()
