from google.cloud import bigquery

def upload_to_bigquery(df, table_id, credentials):
    # Upload to BigQuery
    df.to_gbq(
        table_id,
        credentials=credentials,
        if_exists="append"
    )

    # Create client BigQuery
    client = bigquery.Client(credentials=credentials, project_id=table_id.split(".")[0])

    # Take table reference
    dataset_name = table_id.split(".")[1]
    table_name = table_id.split(".")[2]
    table_ref = client.dataset(dataset_name).table(table_name)

    # Get the metadata of the table
    table = client.get_table(table_ref)

    # Change the expiration table to None
    table.expires = None

    # Update the table with the changed metadata
    client.update_table(table, ["expires"])