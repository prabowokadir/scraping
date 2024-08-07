import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

# open and read the HTML
url = "https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats"
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
team_urls = team_urls[0]

# open and read the HTML team
page_team = urlopen(team_urls)
html_team = page_team.read().decode("utf-8")

# create BeautifulSoup object for HTML team
soup_team = BeautifulSoup(html_team, "html.parser")

# store the scores and fixtures data on pandas
matches = pd.read_html(html_team, match="Scores & Fixtures")
matches = matches[0]

# get and store the shooting data on pandas
shoot = soup_team.find_all("a")
shoot = [s.get("href") for s in shoot]
shoot = [s for s in shoot if s and "all_comps/shooting/" in s]
shoot = shoot[0]

# get and store the goalkeeping data on pandas
keeper = soup_team.find_all("a")
keeper = [k.get("href") for k in keeper]
keeper = [k for k in keeper if k and "all_comps/keeper" in k]
keeper = keeper[0]

# get and store the passing data on pandas
pass_ = soup_team.find_all("a")
pass_ = [p.get("href") for p in pass_]
pass_ = [p for p in pass_ if p and "all_comps/passing" in p]
pass_ = pass_[0]

# get and store the passing types data on pandas
pass_types = soup_team.find_all("a")
pass_types = [p.get("href") for p in pass_types]
pass_types = [p for p in pass_types if p and "all_comps/passing_types" in p]
pass_types = pass_types[0]

print(pass_types)