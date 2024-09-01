from google.cloud import bigquery

def upload_to_bigquery(df, table_id, project_id, credentials):

    # Upload to BigQuery
    df.to_gbq(
        table_id,
        project_id=project_id,
        credentials=credentials,
        if_exists="append"
    )