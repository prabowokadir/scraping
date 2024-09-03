# import os
import time
# import pickle
import pandas as pd
# import pandas_gbq
from bs4 import BeautifulSoup
from urllib.request import urlopen
# from google.oauth2 import service_account
# from google.auth.transport.requests import Request
# from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.cloud import bigquery

# Start year and url to scrape
start_year = 2023
url = f"https://fbref.com/en/comps/9/{str(start_year)}-{str(start_year+1)}/{str(start_year)}-{str(start_year+1)}-Premier-League-Stats"

# Project, dataset, and table name in BigQuery
project_id = "sacred-bonbon-399703"
dataset_id = "raw"
table_id = f"{project_id}.{dataset_id}.premier_league_matches_stats"

# Path to client_secrets.json (OAuth 2.0 Client ID)
client_secrets_file = "/Users/prabowo.kadir/Desktop/client_secret_522378535070-7n86ogodaj9jgitmrcd9rkqeomogqfff.apps.googleusercontent.com.json"
# token_file = "/Users/prabowo.kadir/Desktop/token.pickle"

# Requirement scopes to BigQuery
SCOPES = [
    "https://www.googleapis.com/auth/bigquery",
    "https://www.googleapis.com/auth/cloud-platform"
]

# Authentication and get credentials
flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
credentials = flow.run_local_server(port=0)
client = bigquery.Client(credentials=credentials, project=project_id)

for i in range(3):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select("table.stats_table")[0]

    links = [l.get("href") for l in table.find_all("a")] # find all the link to team
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
        matches["season"] = start_year
        matches["team_name"] = team_name
        matches["gf"] = matches["gf"].astype("str")
        matches["ga"] = matches["ga"].astype("str")

        matches.to_gbq(
            table_id,
            project_id=project_id,
            if_exists="append",
            credentials=credentials
        )

    print(f"Premier League season {str(start_year)}-{str(start_year+1)} has been done.")

    start_year-=1

    time.sleep(5)