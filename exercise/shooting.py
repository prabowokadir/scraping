import time
import pandas as pd
import pandas_gbq
from bs4 import BeautifulSoup
from urllib.request import urlopen

start_year = 2023
url = f"https://fbref.com/en/comps/9/{str(start_year)}-{str(start_year+1)}/{str(start_year)}-{str(start_year+1)}-Premier-League-Stats"

# project name in BigQuery to store the data
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
        # get the name of the team
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        
        # open and read the HTML team
        page_team = urlopen(team_url)
        html_team = page_team.read().decode("utf-8")

        # create the BeautifulSoup object for HTML team
        soup_team = BeautifulSoup(html_team, "html.parser")

        # get the shooting stats data
        data = soup_team.find_all("a")
        data = [d.get("href") for d in data]
        data = [d for d in data if d and f"all_comps/shooting/" in d]
        print(data)
        data = f"https://fbref.com{data[0]}"
        data = urlopen(data)
        data = data.read().decode("utf-8")
        data = pd.read_html(data, match="Shooting")
        data = data[0]

        # clean the table and data on pandas dataframe
        data.columns = data.columns.droplevel(0)
        data.columns = [
            c.lower()
            .replace(" ", "_")
            .replace("%", "prctg")
            .replace("/", "per")
            .replace("-", "minus")
            .replace(":", "_")
            .replace("1/3", "pass_final_third")
            .replace("+", "plus")
            for c in data.columns
        ]
        data["season"] = start_year
        data["team_name"] = team_name

        # upload the data to BigQuery
        pandas_gbq.to_gbq(
            data,
            "raw.premier_league_shooting_stats",
            project_id = project_id,
            if_exists="append"
        )

    print(f"Premier League season {str(start_year)}-{str(start_year+1)} has been done.")

    start_year-=1

    time.sleep(5)