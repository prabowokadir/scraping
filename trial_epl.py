import time
import requests
import pandas as pd
import pandas_gbq
from bs4 import BeautifulSoup
from urllib.request import urlopen

# open and read the HTML
url = "https://fbref.com/en/comps/9/Premier-League-Stats"

# season
years = list(range(2024, 2010, -1))

for year in years:
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select("table.stats_table")[0]

    links = [l.get("href") for l in table.find_all("a")]
    links = [l for l in links if '/squads/' in l]
    team_urls = [f"https://fbref.com{l}" for l in links]

    previous_season = soup.select("a.prev")[0].get("href")
    url = f"https://fbref.com{previous_season}"

    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        
        # open and read the HTML team
        page_team = urlopen(team_url)
        html_team = page_team.read().decode("utf-8")

        # create BeautifulSoup object for HTML team
        soup_team = BeautifulSoup(html_team, "html.parser")

        # store the scores and fixtures data on pandas
        matches = pd.read_html(html_team, match="Scores & Fixtures")
        matches = matches[0]

        matches.columns = [c.lower() for c in matches.columns]
        matches.columns = [c.replace(" ", "_") for c in matches.columns]

        pandas_gbq.to_gbq(
            matches, "raw."
        )