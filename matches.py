import time
import pandas as pd
import pandas_gbq
from bs4 import BeautifulSoup
from urllib.request import urlopen


start_year = 2023
url = f"https://fbref.com/en/comps/9/{str(start_year)}-{str(start_year+1)}/{str(start_year)}-{str(start_year+1)}-Premier-League-Stats"

project_id = "sacred-bonbon-399703"

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

        pandas_gbq.to_gbq(
            matches,
            "raw.premier_league_matches_stats",
            project_id=project_id,
            if_exists="append"
        )

    print(f"Premier League season {str(start_year)}-{str(start_year+1)} has been done.")

    start_year-=1

    time.sleep(5)