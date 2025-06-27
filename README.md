# symplique-cost-optimization
symplique-cost-optimization-task

🧩 1. Problem Overview:

Storing all billing records in Cosmos DB became too expensive. Old records aren't accessed often but still need to be available. We needed a cost-effective way to store them long-term without affecting users.

🚀 2. Solution Summary:

We move old records (older than 3 months) to Blob Storage to save costs. Recent records stay in Cosmos DB. When someone asks for a record, the system checks Cosmos DB first, then Blob if needed — without changing the API.

🧱 3. Infrastructure with Terraform: 

We use Terraform to create everything

Resource Group
Cosmos DB + SQL DB + Container
Blob Storage + Container
Function App Plan (serverless)
Azure Function App with settings

It’s all repeatable and version-controlled.

🧠 4. Python Functions:

What the code does

archive_old_records (Timer):

Runs automatically (e.g., daily)

Moves records older than 90 days to Blob

Deletes them from Cosmos DB

archive_reader (HTTP):

Tries to get the record from Cosmos DB

If not found, it loads it from Blob

Keeps the API response the same
