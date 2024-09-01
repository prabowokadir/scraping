from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import time

def shooting_data(url, start_year):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select("table.stats_table")[0]

    links = [l.get("href") for l in table.find_all("a") if '/squads' in l.get("href")]
    team_urls = [f"https://fbref.com{l}" for l in links]

    shoot_frames = []

    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        page_team = urlopen(team_url)
        html_team = page_team.read().decode("utf-8")
        soup_team = BeautifulSoup(html_team, "html.parser")

        shoots = soup_team.find_all("a")
        shoots = [s.get("href") for s in shoots]
        shoots = [s for s in shoots if s and '/all_comps/shooting/' in s]
        shoots = f"https://fbref.com{shoots[0]}"
        shoots = urlopen(shoots)
        shoots = shoots.read().decode("utf-8")
        shoots = pd.read_html(shoots, match="Shooting")[0]

        # Clean the data
        shoots.columns = shoots.columns.droplevel(0)
        shoots.columns = [
            s.lower()
            .replace(" ", "_")
            .replace("%", "prctg")
            .replace("/", "per")
            .replace("-", "minus")
            .replace(":", "_")
            .replace("1/3", "pass_final_third")
            .replace("+", "plus")
            for s in shoots.columns
        ]
        shoots["season"] = start_year
        shoots["team_name"] = team_name
        shoot_frames.append(shoots)

        time.sleep(5)

    return pd.concat(shoot_frames, ignore_index=True)