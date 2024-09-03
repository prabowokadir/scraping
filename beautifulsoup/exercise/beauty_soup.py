from bs4 import BeautifulSoup
from urllib.request import urlopen

url = 'http://olympus.realpython.org/profiles/dionysus'
page = urlopen(url) # open the URL
html = page.read().decode("utf-8") # read the HTML as a string

# create BeautifulSoup object, html.parser represents Python's built-in HTML parser
soup = BeautifulSoup(html, "html.parser")
image_1, image_2 = soup.find_all("img")

# get the source of the image by call the attribute name i.e src
image_1_src = image_1["src"]
image_2_src = image_2["src"]

# get the title and name from the web
title = soup.title.string
name = soup.h2.string

# print(f'{title}\n{name}')

url = "http://olympus.realpython.org/profiles"
page = urlopen(url)
html = page.read().decode("utf-8")

soup = BeautifulSoup(html, "html.parser")
links = soup.h2.find_all("a")

for i in range(len(links)):
    detail_links = links[i]["href"]
    print(f"http://olympus.realpython.org{detail_links}")