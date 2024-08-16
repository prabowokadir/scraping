import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

# open and read the HTML
url = "https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats"

response = requests.get(url)
if response.status_code == 429:
    retry_after = int(response.headers.get("Retry-After", 60)) # default wait for 60s if there're no header
    time.sleep(retry_after)

page = urlopen(url)
html = page.read().decode("utf-8")

# create BeautifulSoup object
soup = BeautifulSoup(html, "html.parser")

# get all data on table
standings = soup.select("table.stats_table")[0]

# urls from each team
links = standings.find_all("a") # .find_all() function only call tag e.g a
links = [l.get("href") for l in links]
links = [l for l in links if '/squads/' in l]

team_urls = [f"https://fbref.com{l}" for l in links]

for i in range(len(team_urls)):
    team_name = team_urls[i].split("/")[-1].replace("-Stats", '').replace("-", " ")

    # open and read the HTML team
    page_team = urlopen(team_urls[i])
    html_team = page_team.read().decode("utf-8")

    # create BeautifulSoup object for HTML team
    soup_team = BeautifulSoup(html_team, "html.parser")

    # store the scores and fixtures data on pandas
    matches = pd.read_html(html_team, match="Scores & Fixtures")
    matches = matches[0]

    attr = ["shooting", "keeper", "passing", "passing_types", "gca", "defense", "possession", "misc"]
    table = ["Shooting", "Goalkeeping", "Passing", "Pass Types", "Goal and Shot Creation",
             "Defensive Actions", "Possession", "Miscellaneous Stats"]

    print(f"{team_name}:")

    for j in range(len(attr)):
        data = soup_team.find_all("a")
        data = [d.get("href") for d in data]
        data = [d for d in data if d and f"all_comps/{attr[j]}/" in d]
        data = f"https://fbref.com{data[0]}"
        data = urlopen(data)
        data = data.read().decode("utf-8")
        data = pd.read_html(data, match=table[j])
        data = data[0]
        
        print(f"Statistics of {table[j]} successfully retrieved")
    
    print("\n")

    time.sleep(60)