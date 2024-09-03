# scraper_shoots.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def get_response_with_backoff(url, headers, retries=5):
    """Make a request with exponential backoff on receiving a 429 Too Many Requests error."""
    delay = 1  # Start with a delay of 1 second
    for i in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:  # Successful request
            return response
        elif response.status_code == 429:  # Too Many Requests
            print(f"Rate limit exceeded. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        else:
            response.raise_for_status()  # Raise other HTTP errors
    raise Exception(f"Failed to retrieve {url} after {retries} retries.")

def shooting_data(url, start_year):
    # List of User-Agent strings to rotate
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
        # Add more User-Agents if needed
    ]

    # Rotate headers with random User-Agent
    headers = {"User-Agent": random.choice(user_agents)}
    
    # Request the main page with headers and exponential backoff
    response = get_response_with_backoff(url, headers)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select("table.stats_table")[0]

    links = [l.get("href") for l in table.find_all("a") if '/squads' in l.get("href")]
    team_urls = [f"https://fbref.com{l}" for l in links]

    shoot_frames = []

    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")

        # Rotate headers for each team request
        headers = {"User-Agent": random.choice(user_agents)}
        
        # Request team page with headers and exponential backoff
        response_team = get_response_with_backoff(team_url, headers)
        html_team = response_team.text
        soup_team = BeautifulSoup(html_team, "html.parser")

        shoots = soup_team.find_all("a")
        shoots = [s.get("href") for s in shoots]
        shoots = [s for s in shoots if s and '/all_comps/shooting/' in s]
        if not shoots:
            print(f"No shooting data found for {team_name}.")
            continue

        shoots_url = f"https://fbref.com{shoots[0]}"

        # Rotate headers for each shoot data request
        headers = {"User-Agent": random.choice(user_agents)}
        
        # Request shoots data page with headers and exponential backoff
        response_shoots = get_response_with_backoff(shoots_url, headers)
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

        # Introduce random delay between requests (e.g., between 30 to 60 seconds)
        time.sleep(random.uniform(30, 60))

    return pd.concat(shoot_frames, ignore_index=True) if shoot_frames else pd.DataFrame()
