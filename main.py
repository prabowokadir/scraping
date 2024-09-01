from credentials import get_credentials
from scraper_matches import matches_data
from scraper_shoots import shooting_data
from bigquery_utils import upload_to_bigquery
import time
import argparse

def main(start_year, project_id, dataset_id, iterations):
    table_matches_id = f"{project_id}.{dataset_id}.premier_league_matches_stats"
    table_shoots_id = f"{project_id}.{dataset_id}.premier_league_shoots_stats"

    # Get credentials
    credentials = get_credentials()

    for _ in range(iterations):
        # Scrape data
        url = f"https://fbref.com/en/comps/9/{start_year}-{start_year+1}/{start_year}-{start_year+1}-Premier-League-Stats"
        matches = matches_data(url, start_year)
        shoots = shooting_data(url, start_year)

        # Store data to BigQuery
        upload_to_bigquery(matches, table_matches_id, project_id, credentials)
        
        time.sleep(5)

        upload_to_bigquery(shoots, table_shoots_id, project_id, credentials)
        print(f"Premier League season {start_year}-{start_year+1} data uploaded.")

        # Move to previous season
        start_year -= 1
        time.sleep(5) # Optional delay between each request

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Scrape and upload Premier League data to BigQuery.")
    parser.add_argument(
        "start_year",
        type=int,
        help="The starting year of the Premier League season to scrape."
    )
    parser.add_argument(
        "project_id", 
        type=str, 
        help="The Google Cloud project ID where BigQuery data will be uploaded."
    )
    parser.add_argument(
        "dataset_id", 
        type=str, 
        help="The BigQuery dataset ID where the data will be stored."
    )
    parser.add_argument(
        "iterations", 
        type=int, 
        help="The number of seasons to scrape and upload."
    )

    # Parse arguments
    args = parser.parse_args()

    # Call main function with parsed arguments
    main(
        args.start_year, 
        args.project_id, 
        args.dataset_id, 
        args.iterations
    )