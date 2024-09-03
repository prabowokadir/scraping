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
        shoots_url = f"https://fbref.com{shoots[0]}"

        # Request shoots data page with headers
        page_shoots = urlopen(shoots_url)
        html_shoots = page_shoots.read().decode("utf-8")
        shoots_data = pd.read_html(html_shoots, match="Shooting")[0]

        # Clean the data
        shoots_data.columns = shoots_data.columns.droplevel(0)
        shoots_data.columns = [
            s.lower()
            .replace(" ", "_")
            .replace("%", "prctg")
            .replace("/", "per")
            .replace("-", "minus")
            .replace(":", "_")
            .replace("1/3", "pass_final_third")
            .replace("+", "plus")
            for s in shoots_data.columns
        ]
        shoots_data["season"] = start_year
        shoots_data["team_name"] = team_name
        shoots_data["gf"] = shoots_data["gf"].astype("str")
        shoots_data["ga"] = shoots_data["ga"].astype("str")
        shoot_frames.append(shoots_data)

        time.sleep(5)  # Delay to avoid hitting server too frequently

    return pd.concat(shoot_frames, ignore_index=True) if shoot_frames else pd.DataFrame()
