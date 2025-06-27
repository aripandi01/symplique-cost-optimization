# functions/archive_reader/http_trigger.py

import json
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
from azure.storage.blob import BlobServiceClient

COSMOS_URL = "https://<your-account>.documents.azure.com:443/"
COSMOS_KEY = "<your-cosmos-key>"
BLOB_CONN_STRING = "<your-blob-conn-string>"

def main(req: func.HttpRequest) -> func.HttpResponse:
    record_id = req.params.get("id")
    customer_id = req.params.get("customerId")

    cosmos = CosmosClient(COSMOS_URL, COSMOS_KEY)
    container = cosmos.get_database_client("billing-db").get_container_client("records")

    try:
        item = container.read_item(item=record_id, partition_key=customer_id)
        return func.HttpResponse(json.dumps(item), mimetype="application/json")
    except exceptions.CosmosResourceNotFoundError:
        blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STRING)
        blob_name = f"{customer_id}/{record_id}.json"
        blob_client = blob_service.get_blob_client(container="billing-archive", blob=blob_name)

        try:
            data = blob_client.download_blob().readall()
            return func.HttpResponse(data, mimetype="application/json")
        except Exception:
            return func.HttpResponse("Record not found", status_code=404)

