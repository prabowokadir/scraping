from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import time

def scraper_premier_league_data(url, start_year):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select("table.stats_table")[0]

    links = [l.get("href") for l in table.find_all("a") if '/squads' in l.get("href")]
    team_urls = [f"https://fbref.com{l}" for l in links]

    data_frames = []

    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        page_team = urlopen(team_url)
        html_team = page_team.read().decode("utf-8")

        matches = pd.read_html(html_team, match="Scores & Fixtures")[0]
        matches.columns = [c.lower().replace(" ", "_") for c in matches.columns]
        matches["season"] = start_year
        matches["team_name"] = team_name
        data_frames.append(matches)

        time.sleep(5)
    
    return pd.concat(data_frames, ignore_index=True)