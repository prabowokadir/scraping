# scraper_shoots.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def shooting_data(url, start_year):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    # Request the page with headers
    response = requests.get(url, headers=headers)
    if response.status_code == 403:
        print(f"Access forbidden to {url}. Consider changing headers or use a different approach.")
        return pd.DataFrame()  # Return an empty DataFrame to handle error gracefully
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select("table.stats_table")[0]

    links = [l.get("href") for l in table.find_all("a") if '/squads' in l.get("href")]
    team_urls = [f"https://fbref.com{l}" for l in links]

    shoot_frames = []

    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")

        # Request team page with headers
        response_team = requests.get(team_url, headers=headers)
        if response_team.status_code == 403:
            print(f"Access forbidden to {team_url}. Consider changing headers or use a different approach.")
            continue  # Skip this team if access is forbidden

        html_team = response_team.text
        soup_team = BeautifulSoup(html_team, "html.parser")

        shoots = soup_team.find_all("a")
        shoots = [s.get("href") for s in shoots]
        shoots = [s for s in shoots if s and '/all_comps/shooting/' in s]
        if not shoots:
            print(f"No shooting data found for {team_name}.")
            continue

        shoots_url = f"https://fbref.com{shoots[0]}"

        # Request shoots data page with headers
        response_shoots = requests.get(shoots_url, headers=headers)
        if response_shoots.status_code == 403:
            print(f"Access forbidden to {shoots_url}. Consider changing headers or use a different approach.")
            continue  # Skip this page if access is forbidden

        shoots_html = response_shoots.text
        shoots_data = pd.read_html(shoots_html, match="Shooting")[0]

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
