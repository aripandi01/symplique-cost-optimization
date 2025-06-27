
# functions/archive_old_records/timer_trigger.py

import json
from datetime import datetime, timedelta
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

COSMOS_URL = "https://<your-account>.documents.azure.com:443/"
COSMOS_KEY = "<your-cosmos-key>"
BLOB_CONN_STRING = "<your-blob-conn-string>"

def main(mytimer: func.TimerRequest) -> None:
    cutoff = datetime.utcnow() - timedelta(days=90)

    cosmos = CosmosClient(COSMOS_URL, COSMOS_KEY)
    db = cosmos.get_database_client("billing-db")
    container = db.get_container_client("records")

    blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STRING)
    archive_container = blob_service.get_container_client("billing-archive")

    query = f"SELECT * FROM c WHERE c.timestamp < '{cutoff.isoformat()}'"
    results = list(container.query_items(query, enable_cross_partition_query=True))

    for record in results:
        record_id = record["id"]
        partition_key = record["customerId"]
        blob_name = f"{partition_key}/{record_id}.json"

        archive_container.upload_blob(blob_name, json.dumps(record), overwrite=True)
        container.delete_item(record=record_id, partition_key=partition_key)

