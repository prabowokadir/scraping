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

print(soup_team)